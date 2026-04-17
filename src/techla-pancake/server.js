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
 *   - PANCAKE_PAGE_ID  (required)
 *   - PANCAKE_BASE_URL (optional, default https://pages.fm/api/public_api/v1)
 */

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require("@modelcontextprotocol/sdk/types.js");

// ───────────────────────────────────────────────────────────────
// Config
// ───────────────────────────────────────────────────────────────

const API_KEY = process.env.PANCAKE_API_KEY;
const BASE_URL =
  process.env.PANCAKE_BASE_URL || "https://pages.fm/api/public_api/v1";

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

const PAGE_ID = process.env.PANCAKE_PAGE_ID || decodePageIdFromToken(API_KEY);

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
// HTTP helper
// ───────────────────────────────────────────────────────────────

function buildUrl(path, query = {}) {
  const q = new URLSearchParams({ ...query, access_token: API_KEY });
  return `${BASE_URL}${path}?${q.toString()}`;
}

async function pancakeGet(path, query = {}) {
  requireConfig();
  const url = buildUrl(path, query);

  let res;
  try {
    res = await fetch(url, { method: "GET" });
  } catch (err) {
    throw new Error(
      `Không kết nối được Pancake (${err.message}). Kiểm tra internet hoặc BASE_URL.`
    );
  }

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

  try {
    return await res.json();
  } catch (err) {
    throw new Error(`Pancake trả response không phải JSON: ${err.message}`);
  }
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
  { name: "techla-pancake", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "list_conversations",
      description:
        "Liệt kê các cuộc trò chuyện / nhóm Zalo của page Pancake trong 1 khoảng thời gian. Trả về id, tên, loại, thời gian tin nhắn cuối, snippet.",
      inputSchema: {
        type: "object",
        properties: {
          limit: {
            type: "number",
            description: "Số cuộc trò chuyện tối đa trả về (1-200). Mặc định 50.",
            default: 50,
          },
          page: {
            type: "number",
            description: "Số trang (1-indexed). Mặc định 1.",
            default: 1,
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
        },
      },
    },
    {
      name: "get_messages",
      description:
        "Lấy tin nhắn trong 1 cuộc trò chuyện. Có thể filter theo thời gian (since) hoặc giới hạn số tin (limit).",
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
              "ISO datetime (ví dụ '2026-04-15T00:00:00Z'). Chỉ trả về tin sau thời điểm này.",
          },
          limit: {
            type: "number",
            description: "Số tin nhắn tối đa. Mặc định 50.",
            default: 50,
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
  const limit = Math.min(Math.max(Number(args.limit) || 50, 1), 200);
  const page = Math.max(Number(args.page) || 1, 1);
  const daysBack = Math.max(Number(args.days_back) || 30, 1);

  const until = toUnix(args.until) || unixNow();
  const since = toUnix(args.since) || until - daysBack * 86400;

  const data = await pancakeGet(`/pages/${PAGE_ID}/conversations`, {
    since,
    until,
    page_number: page,
    page_size: limit,
  });

  const rawList = data.conversations || data.data || data.items || [];
  const list = rawList.map(summarizeConversation);

  return {
    total: data.total ?? null,
    count: list.length,
    page,
    range_since: new Date(since * 1000).toISOString(),
    range_until: new Date(until * 1000).toISOString(),
    conversations: list,
  };
}

async function handleGetMessages(args) {
  if (!args.conversation_id) {
    throw new Error("Thiếu 'conversation_id'.");
  }
  const limit = Math.min(Math.max(Number(args.limit) || 50, 1), 200);
  const page = Math.max(Number(args.page) || 1, 1);

  const data = await pancakeGet(
    `/pages/${PAGE_ID}/conversations/${encodeURIComponent(
      args.conversation_id
    )}/messages`,
    { page_number: page, page_size: limit }
  );

  const rawList = data.messages || data.data || data.items || [];
  let list = rawList.map(summarizeMessage);

  // Client-side filter vì API không hỗ trợ since
  if (args.since) {
    const sinceMs = new Date(toIso(args.since)).getTime();
    if (!isNaN(sinceMs)) {
      list = list.filter((m) => {
        if (!m.sent_at) return true;
        return new Date(m.sent_at).getTime() >= sinceMs;
      });
    }
  }

  return {
    conversation_id: args.conversation_id,
    count: list.length,
    page,
    messages: list,
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
    const convs = await handleListConversations({ limit: 50 });
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
  console.error(
    `[techla-pancake] MCP server started. Page: ${PAGE_ID || "(chưa cấu hình)"}`
  );
}

// Chỉ chạy stdio server khi được invoke trực tiếp (không chạy khi require từ test)
if (require.main === module) {
  main().catch((err) => {
    console.error("[techla-pancake] FATAL:", err);
    process.exit(1);
  });
}

// Export handlers để test độc lập
module.exports = {
  HANDLERS,
  decodePageIdFromToken,
  getPageId: () => PAGE_ID,
};
