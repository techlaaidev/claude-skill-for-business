#!/usr/bin/env node
/**
 * Techla Pancake MCP Server
 * Theo dõi tin nhắn Zalo qua Pancake Public API.
 *
 * Author: Techla — v1.0.0 — License: xem LICENSE.md
 *
 * Tools:
 *   - list_conversations    : liệt kê các cuộc trò chuyện
 *   - get_messages          : lấy tin nhắn trong 1 cuộc trò chuyện
 *   - search_messages       : tìm tin nhắn theo keyword
 *   - summarize_conversation: tóm tắt nhanh N ngày gần nhất
 *
 * Env (Claude Desktop truyền qua manifest):
 *   - PANCAKE_API_KEY  (required, sensitive)
 *   - PANCAKE_PAGE_ID  (optional — auto-detect từ JWT payload)
 *
 * Endpoints (theo docs https://developer.pancake.biz):
 *   - list_conversations → v2 (trả cả INBOX + GROUP, cursor `last_conversation_id`)
 *   - get_messages       → v1 (v2 không có endpoint này; offset `current_count`)
 * Rate limit: 5 req/page/s → throttle ≥ 220ms/req.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { Buffer } from "node:buffer";
import { appendFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Diagnostic log file: %TEMP%/techla-pancake-debug.log
const DEBUG_LOG = join(tmpdir(), "techla-pancake-debug.log");
function dlog(msg) {
  try {
    appendFileSync(DEBUG_LOG, `${new Date().toISOString()} ${msg}\n`);
  } catch {}
  console.error(msg);
}

// ───────────────────────────────────────────────────────────────
// Config
// ───────────────────────────────────────────────────────────────

// Claude Desktop quirk: khi optional user_config để trống, Claude Desktop truyền
// literal placeholder "${user_config.xxx}" thay vì empty string.
// → sanitize: bỏ qua nếu giá trị chứa "${" để fallback về JWT decode / error.
function sanitizeEnv(v) {
  if (!v || typeof v !== "string") return "";
  if (v.includes("${")) return "";
  return v.trim();
}

const API_KEY = sanitizeEnv(process.env.PANCAKE_API_KEY);
const V1_BASE = "https://pages.fm/api/public_api/v1";
const V2_BASE = "https://pages.fm/api/public_api/v2";

// Page ID: ưu tiên user config; nếu trống thì decode từ JWT payload của API key
// (Pancake gắn token theo từng page, id nhúng thẳng vào JWT).
function decodePageIdFromToken(token) {
  if (!token || typeof token !== "string") return null;
  const parts = token.split(".");
  if (parts.length !== 3) return null;
  try {
    const payloadB64 = parts[1].replace(/-/g, "+").replace(/_/g, "/");
    const json = Buffer.from(payloadB64, "base64").toString("utf8");
    const payload = JSON.parse(json);
    return payload.id || null;
  } catch {
    return null;
  }
}

const PAGE_ID = sanitizeEnv(process.env.PANCAKE_PAGE_ID) || decodePageIdFromToken(API_KEY);

function requireConfig() {
  if (!API_KEY) {
    throw new Error(
      "Thiếu PANCAKE_API_KEY. Mở Claude Desktop → Settings → Extensions → Techla Pancake để điền."
    );
  }
  if (!PAGE_ID) {
    throw new Error(
      "Không xác định được Page ID. Token không hợp lệ hoặc không chứa 'id'. " +
        "Kiểm tra lại API key trong Settings → Extensions → Techla Pancake, " +
        "hoặc điền thủ công vào ô Page ID (format: pzl_...)."
    );
  }
}

// ───────────────────────────────────────────────────────────────
// HTTP helper + rate-limit throttle
// ───────────────────────────────────────────────────────────────

// Pancake giới hạn 5 req/page/s. Đệm thêm buffer → cách nhau ≥ 220ms.
const MIN_REQ_INTERVAL_MS = 220;
let _lastRequestAt = 0;

async function throttle() {
  const elapsed = Date.now() - _lastRequestAt;
  if (elapsed < MIN_REQ_INTERVAL_MS) {
    await new Promise((r) => setTimeout(r, MIN_REQ_INTERVAL_MS - elapsed));
  }
  _lastRequestAt = Date.now();
}

function buildUrl(base, path, query = {}) {
  const q = new URLSearchParams({ ...query, access_token: API_KEY });
  return `${base}${path}?${q.toString()}`;
}

async function pancakeGet(base, path, query = {}) {
  requireConfig();
  await throttle();
  const url = buildUrl(base, path, query);

  // Diagnostic: log request URL đã redact access_token (giữ fingerprint đầu/cuối)
  const safeUrl = url.replace(
    /access_token=([^&]+)/,
    (_, t) => `access_token=${t.slice(0, 10)}...${t.slice(-10)}[len=${t.length}]`
  );
  dlog(`[techla-pancake] GET ${safeUrl}`);

  let res;
  try {
    res = await fetch(url, { method: "GET" });
  } catch (err) {
    dlog(`[techla-pancake] FETCH ERROR: ${err.message}`);
    throw new Error(
      `Không kết nối được Pancake (${err.message}). Kiểm tra internet hoặc BASE_URL.`
    );
  }
  dlog(`[techla-pancake] ← HTTP ${res.status} ${res.statusText}`);

  if (res.status === 401 || res.status === 403) {
    throw new Error(
      "Sai API key (HTTP " +
        res.status +
        "). Mở Claude Desktop → Settings → Extensions → Techla Pancake → cập nhật lại Pancake API Key."
    );
  }
  if (res.status === 404) {
    throw new Error(
      "Không tìm thấy page (HTTP 404). Kiểm tra lại Page ID trong Settings → Extensions → Techla Pancake."
    );
  }
  if (res.status === 429) {
    throw new Error(
      "Pancake rate limit (HTTP 429). Chờ 1 phút rồi thử lại, hoặc giảm limit của câu query."
    );
  }
  if (!res.ok) {
    const text = await safeText(res);
    throw new Error(`Pancake trả lỗi HTTP ${res.status}: ${text}`);
  }

  let data;
  try {
    data = await res.json();
  } catch (err) {
    throw new Error(`Pancake trả response không phải JSON: ${err.message}`);
  }

  // Pancake đôi khi trả HTTP 200 nhưng kèm {"success": false, "message": "..."}
  // → phải check field 'success' thay vì chỉ HTTP status.
  if (data && data.success === false) {
    dlog(`[techla-pancake] ← BODY(fail): ${JSON.stringify(data).slice(0, 300)}`);
    const code = data.error_code ? ` (error_code=${data.error_code})` : "";
    const msg = data.message || "Pancake trả về lỗi không rõ";
    if (/invalid.*access.*token|access_token|renewed/i.test(msg)) {
      throw new Error(
        `Sai Pancake API key${code}: "${msg}". Mở Claude Desktop → Settings → Extensions → Techla Pancake → cập nhật API key mới.`
      );
    }
    throw new Error(`Pancake lỗi${code}: ${msg}`);
  }

  const convCount = Array.isArray(data?.conversations) ? data.conversations.length
    : Array.isArray(data?.data) ? data.data.length : "?";
  dlog(`[techla-pancake] ← BODY(ok): conversations=${convCount}`);
  return data;
}

async function safeText(res) {
  try {
    return (await res.text()).slice(0, 300);
  } catch {
    return "(không đọc được body)";
  }
}

// ───────────────────────────────────────────────────────────────
// Utils
// ───────────────────────────────────────────────────────────────

function toIso(input) {
  if (!input) return null;
  if (input instanceof Date) return input.toISOString();
  if (typeof input === "number") {
    const ms = input < 1e12 ? input * 1000 : input;
    return new Date(ms).toISOString();
  }
  if (typeof input === "string") {
    const d = new Date(input);
    if (!isNaN(d.getTime())) return d.toISOString();
  }
  return String(input);
}

function summarizeConversation(c) {
  return {
    id: c.id || c.conversation_id || c._id,
    title:
      c.from?.name ||
      c.title ||
      c.name ||
      c.customer_name ||
      c.page_customer?.name ||
      "(không có tên)",
    type: c.type || null,
    message_count: c.message_count ?? null,
    last_message_at: toIso(c.updated_at || c.inserted_at || c.last_sent_at),
    seen: c.seen ?? null,
    last_message_snippet:
      (c.snippet || c.last_message || "").toString().slice(0, 140) || null,
  };
}

function stripHtml(s) {
  return (s || "")
    .toString()
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .trim();
}

function summarizeMessage(m) {
  return {
    id: m.id || m._id,
    from: m.from?.name || m.sender_name || m.customer_name || "(không rõ)",
    from_id: m.from?.id || null,
    type: m.type || null,
    content: stripHtml(m.message || m.content || m.text || ""),
    attachments: (m.attachments || []).map((a) => ({
      type: a.type || null,
      url: a.url || a.src || null,
    })),
    sent_at: toIso(m.inserted_at || m.created_at || m.sent_at),
  };
}

function textOf(msg) {
  return (msg?.message || msg?.content || msg?.text || "").toString();
}

// ───────────────────────────────────────────────────────────────
// MCP server
// ───────────────────────────────────────────────────────────────

const server = new Server(
  { name: "techla-pancake", version: "1.0.5" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_conversations",
      description:
        "Liệt kê các cuộc trò chuyện / nhóm Zalo của page Pancake. Trả về tối đa 60 conversation mới nhất / call (theo Pancake v2). Để lấy trang tiếp, truyền `last_conversation_id` = id của conversation cuối cùng từ call trước.",
      inputSchema: {
        type: "object",
        properties: {
          limit: {
            type: "number",
            description:
              "Số conversation tối đa trả về sau khi filter client-side. Pancake luôn trả 60/call nên đặt >60 không có tác dụng. Mặc định 60.",
            default: 60,
          },
          last_conversation_id: {
            type: "string",
            description:
              "(Optional) ID của conversation cuối từ call trước, dùng để phân trang. Để trống = 60 conversation mới nhất.",
          },
          days_back: {
            type: "number",
            description:
              "Lọc conversation có hoạt động trong N ngày qua. Mặc định 30.",
            default: 30,
          },
          since: {
            type: "string",
            description:
              "(Optional) ISO datetime hoặc Unix timestamp. Override days_back.",
          },
          until: {
            type: "string",
            description:
              "(Optional) ISO datetime hoặc Unix timestamp. Mặc định = now.",
          },
          type: {
            type: "string",
            description:
              "(Optional) Filter theo loại: 'INBOX' (chat 1-1) hoặc 'COMMENT'. Để trống = tất cả (bao gồm group Zalo).",
          },
        },
      },
    },
    {
      name: "get_messages",
      description:
        "Lấy tin nhắn trong 1 cuộc trò chuyện (Pancake v1 trả 30 tin / call, mới nhất trước). Có thể lấy nhiều trang qua `current_count`, filter client-side theo `since`.",
      inputSchema: {
        type: "object",
        properties: {
          conversation_id: {
            type: "string",
            description: "ID của cuộc trò chuyện (lấy từ list_conversations).",
          },
          since: {
            type: "string",
            description:
              "ISO datetime (ví dụ '2026-04-15T00:00:00Z'). Chỉ giữ lại tin sau thời điểm này (filter client-side).",
          },
          limit: {
            type: "number",
            description:
              "Số tin nhắn tối đa trả về. Server tự lật trang 30 tin / call đến khi đủ hoặc hết. Mặc định 30, tối đa 200.",
            default: 30,
          },
          current_count: {
            type: "number",
            description:
              "(Optional) Vị trí offset để bắt đầu lấy lùi về quá khứ (theo spec Pancake). Mặc định 0.",
            default: 0,
          },
        },
        required: ["conversation_id"],
      },
    },
    {
      name: "search_messages",
      description:
        "Tìm tin nhắn theo từ khóa (tiếng Việt có dấu hoặc không). Có thể giới hạn trong 1 cuộc trò chuyện hoặc toàn bộ page.",
      inputSchema: {
        type: "object",
        properties: {
          keyword: {
            type: "string",
            description: "Từ khóa cần tìm (ví dụ: 'phàn nàn', 'hủy đơn').",
          },
          conversation_id: {
            type: "string",
            description:
              "(Optional) ID cuộc trò chuyện. Nếu bỏ trống sẽ tìm trong tất cả.",
          },
          days_back: {
            type: "number",
            description: "Tìm tin trong N ngày gần nhất. Mặc định 7.",
            default: 7,
          },
          max_results: {
            type: "number",
            description: "Số kết quả tối đa. Mặc định 30.",
            default: 30,
          },
        },
        required: ["keyword"],
      },
    },
    {
      name: "summarize_conversation",
      description:
        "Shortcut tóm tắt 1 cuộc trò chuyện trong N ngày qua: trả về danh sách tin nhắn (đã rút gọn) để Claude phân tích tiếp.",
      inputSchema: {
        type: "object",
        properties: {
          conversation_id: {
            type: "string",
            description: "ID của cuộc trò chuyện.",
          },
          days_back: {
            type: "number",
            description: "Tóm tắt tin trong N ngày qua. Mặc định 3.",
            default: 3,
          },
          max_messages: {
            type: "number",
            description: "Giới hạn số tin trả về (chống đầy context). Mặc định 100.",
            default: 100,
          },
        },
        required: ["conversation_id"],
      },
    },
  ],
}));

// ───────────────────────────────────────────────────────────────
// Tool handlers
// ───────────────────────────────────────────────────────────────

function unixNow() {
  return Math.floor(Date.now() / 1000);
}

function toUnix(input) {
  if (!input) return null;
  if (typeof input === "number") {
    return input < 1e12 ? input : Math.floor(input / 1000);
  }
  const d = new Date(input);
  if (!isNaN(d.getTime())) return Math.floor(d.getTime() / 1000);
  return null;
}

async function handleListConversations(args) {
  // Pancake v2 trả tối đa 60/call, pagination qua last_conversation_id (cursor).
  const limit = Math.min(Math.max(Number(args.limit) || 60, 1), 60);
  const daysBack = Math.max(Number(args.days_back) || 30, 1);
  const until = toUnix(args.until) || unixNow();
  const since = toUnix(args.since) || until - daysBack * 86400;

  const query = { since, until };
  if (args.last_conversation_id) query.last_conversation_id = args.last_conversation_id;
  if (args.type) query.type = args.type;

  const data = await pancakeGet(V2_BASE, `/pages/${PAGE_ID}/conversations`, query);

  const rawList = data.conversations || data.data || data.items || [];
  const list = rawList.slice(0, limit).map(summarizeConversation);
  const lastRaw = rawList[rawList.length - 1];
  const nextCursor =
    rawList.length >= 60 ? lastRaw?.id || lastRaw?._id || null : null;

  return {
    count: list.length,
    range_since: new Date(since * 1000).toISOString(),
    range_until: new Date(until * 1000).toISOString(),
    next_last_conversation_id: nextCursor,
    conversations: list,
  };
}

async function handleGetMessages(args) {
  if (!args.conversation_id) {
    throw new Error("Thiếu 'conversation_id'.");
  }
  // Pancake v1: 30 msg/call, offset qua `current_count`. Lật trang cho đến khi đủ limit hoặc hết.
  const limit = Math.min(Math.max(Number(args.limit) || 30, 1), 200);
  const sinceMs = args.since
    ? new Date(toIso(args.since)).getTime()
    : null;
  const path = `/pages/${PAGE_ID}/conversations/${encodeURIComponent(
    args.conversation_id
  )}/messages`;

  let offset = Math.max(Number(args.current_count) || 0, 0);
  const collected = [];
  let stopBySince = false;

  while (collected.length < limit && !stopBySince) {
    const data = await pancakeGet(V1_BASE, path, { current_count: offset });
    const batch = (data.messages || data.data || data.items || []).map(
      summarizeMessage
    );
    if (batch.length === 0) break;

    // Pancake trả 30 tin chronological (oldest→newest); caller mong "N tin mới nhất"
    // → sắp ngược để newest-first trong batch này.
    batch.sort((a, b) => {
      const ta = a.sent_at ? new Date(a.sent_at).getTime() : 0;
      const tb = b.sent_at ? new Date(b.sent_at).getTime() : 0;
      return tb - ta;
    });

    for (const m of batch) {
      if (sinceMs && m.sent_at && new Date(m.sent_at).getTime() < sinceMs) {
        stopBySince = true;
        break;
      }
      collected.push(m);
      if (collected.length >= limit) break;
    }
    if (batch.length < 30) break; // hết tin
    offset += batch.length;
  }

  return {
    conversation_id: args.conversation_id,
    count: collected.length,
    next_current_count: stopBySince || collected.length < limit ? null : offset,
    messages: collected,
  };
}

async function handleSearchMessages(args) {
  if (!args.keyword) {
    throw new Error("Thiếu 'keyword'.");
  }
  const kw = String(args.keyword).toLowerCase();
  const daysBack = Math.max(Number(args.days_back) || 7, 1);
  const maxResults = Math.min(Math.max(Number(args.max_results) || 30, 1), 100);

  const since = new Date(Date.now() - daysBack * 24 * 3600 * 1000).toISOString();

  let convIds = [];
  if (args.conversation_id) {
    convIds = [args.conversation_id];
  } else {
    const convs = await handleListConversations({ limit: 60, days_back: daysBack });
    convIds = convs.conversations.map((c) => c.id).filter(Boolean);
  }

  const hits = [];
  for (const cid of convIds) {
    if (hits.length >= maxResults) break;
    try {
      const m = await handleGetMessages({
        conversation_id: cid,
        since,
        limit: 100,
      });
      for (const msg of m.messages) {
        if (hits.length >= maxResults) break;
        if (textOf(msg).toLowerCase().includes(kw)) {
          hits.push({
            conversation_id: cid,
            ...msg,
          });
        }
      }
    } catch (err) {
      // Skip conversation nếu lỗi, không fail cả search
      console.error(
        `[search_messages] conversation ${cid} skip: ${err.message}`
      );
    }
  }

  return {
    keyword: args.keyword,
    searched_conversations: convIds.length,
    hit_count: hits.length,
    hits,
  };
}

async function handleSummarizeConversation(args) {
  if (!args.conversation_id) {
    throw new Error("Thiếu 'conversation_id'.");
  }
  const daysBack = Math.max(Number(args.days_back) || 3, 1);
  const maxMessages = Math.min(
    Math.max(Number(args.max_messages) || 100, 1),
    300
  );

  const since = new Date(Date.now() - daysBack * 24 * 3600 * 1000).toISOString();
  const m = await handleGetMessages({
    conversation_id: args.conversation_id,
    since,
    limit: maxMessages,
  });

  return {
    conversation_id: args.conversation_id,
    range_from: since,
    range_to: new Date().toISOString(),
    message_count: m.count,
    messages: m.messages,
    hint:
      m.count === 0
        ? "Không có tin nhắn mới. Có thể tăng 'days_back' hoặc check lại conversation_id."
        : "Đã trả về tin nhắn rút gọn — có thể phân tích/ tóm tắt tiếp trong Claude chat.",
  };
}

const HANDLERS = {
  list_conversations: handleListConversations,
  get_messages: handleGetMessages,
  search_messages: handleSearchMessages,
  summarize_conversation: handleSummarizeConversation,
};

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const handler = HANDLERS[name];
  if (!handler) {
    return {
      isError: true,
      content: [{ type: "text", text: `Tool không tồn tại: ${name}` }],
    };
  }

  try {
    const result = await handler(args || {});
    return {
      content: [{ type: "text", text: JSON.stringify(result, null, 2) }],
    };
  } catch (err) {
    console.error(`[${name}] ERROR: ${err.stack || err.message}`);
    return {
      isError: true,
      content: [
        {
          type: "text",
          text: `Lỗi khi gọi ${name}: ${err.message}`,
        },
      ],
    };
  }
});

// ───────────────────────────────────────────────────────────────
// Startup
// ───────────────────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // Diagnostic: log token fingerprint (first 10 + last 10 chars) để verify config đúng
  const k = API_KEY || "";
  const fp = k.length > 30 ? `${k.slice(0, 10)}...${k.slice(-10)} (len=${k.length})` : "(empty/short)";
  dlog(
    `[techla-pancake] MCP server started. Page: ${PAGE_ID || "(chưa cấu hình)"} | TokenFP: ${fp}`
  );
}

// Electron UtilityProcess không set argv[1] chuẩn → chạy main() mặc định khi import.
// Test harness set PANCAKE_SKIP_MAIN=1 để gọi handlers trực tiếp không cần stdio.
if (process.env.PANCAKE_SKIP_MAIN !== "1") {
  main().catch((err) => {
    console.error("[techla-pancake] FATAL:", err);
    process.exit(1);
  });
}

// Export handlers để test độc lập
export { HANDLERS, decodePageIdFromToken };
export const getPageId = () => PAGE_ID;
