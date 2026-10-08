#!/usr/bin/env node
/**
 * chat-history.mjs — CLI quản lý lịch sử chat (Pi)
 *
 * Dùng:  node chat-history.mjs <command> [args]
 *
 * Commands:
 *   list              Liệt kê tất cả chat (sort theo ngày, mới nhất trước)
 *   recent [n]        N chat gần nhất (mặc định 5)
 *   search <kw>       Tìm kiếm (không phân biệt hoa thường, hỗ trợ tiếng Việt không dấu)
 *   summary           Tạo data/_SUMMARY.md (bảng + thống kê tag)
 *   tags              Thống kê các tag đã dùng
 *   save <title>      Lưu chat mới (đọc nội dung từ stdin)
 *   help              In trợ giúp này
 */
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath } from "node:url";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(os.homedir(), ".agents", "skills", "chat-history", "data");

const C = {
  reset: "\x1b[0m",
  bold: "\x1b[1m",
  dim: "\x1b[2m",
  yellow: "\x1b[33m",
  green: "\x1b[32m",
  cyan: "\x1b[36m",
  red: "\x1b[31m",
};

// ---------- utils ----------
function normalize(s) {
  return String(s ?? "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // bỏ dấu
    .replace(/đ/g, "d");
}

function slugify(s) {
  return normalize(s)
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80);
}

function today() {
  return new Date().toISOString().slice(0, 10);
}

// ---------- frontmatter ----------
function parseFrontmatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") return { meta: {}, body: text };
  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") { end = i; break; }
  }
  if (end === -1) return { meta: {}, body: text };
  const fm = lines.slice(1, end);
  const body = lines.slice(end + 1).join("\n");

  const meta = {};
  let cur = null;
  for (const raw of fm) {
    const m = raw.match(/^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$/);
    if (m) {
      cur = m[1];
      meta[cur] = m[2];
    } else if (cur && /^\s+-\s+/.test(raw)) {
      if (!Array.isArray(meta[cur])) meta[cur] = [meta[cur]].filter((x) => x !== "");
      meta[cur].push(raw.trim().replace(/^-\s*/, ""));
    }
  }
  return { meta, body };
}

function extractDate(v) {
  const m = String(v ?? "").match(/\d{4}-\d{2}-\d{2}/);
  return m ? m[0] : "";
}

function parseTags(v) {
  if (Array.isArray(v)) return v.map(String);
  return String(v ?? "")
    .replace(/[\[\]]/g, "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

// ---------- load ----------
function listFiles() {
  if (!fs.existsSync(DATA_DIR)) return [];
  return fs.readdirSync(DATA_DIR)
    .filter((f) => f.endsWith(".chat.md") && f !== "_SUMMARY.md")
    .map((f) => path.join(DATA_DIR, f));
}

function loadChats() {
  return listFiles()
    .map((file) => {
      const { meta, body } = parseFrontmatter(fs.readFileSync(file, "utf8"));
      return {
        file,
        name: path.basename(file),
        title: meta.title ?? "",
        date: extractDate(meta.date),
        tags: parseTags(meta.tags),
        meta,
        body,
      };
    })
    .sort((a, b) => (b.date || "").localeCompare(a.date || ""));
}

function readStdin() {
  return fs.readFileSync(0, "utf8");
}

// ---------- commands ----------
function cmdList(chats) {
  console.log(`${C.bold}${C.cyan}📁 Saved Chats${C.reset} (${chats.length})\n`);
  for (const c of chats) {
    console.log(`${C.bold}${c.name}${C.reset}`);
    console.log(`   ${C.green}Title:${C.reset} ${c.title || "N/A"}`);
    console.log(`   ${C.yellow}Date: ${C.reset}${c.date || "?"}    ${C.dim}Tags:${C.reset} ${c.tags.join(", ") || "—"}`);
    console.log("");
  }
}

function cmdRecent(chats, n) {
  const k = Math.max(1, parseInt(n, 10) || 5);
  cmdList(chats.slice(0, k));
}

function cmdSearch(chats, kw) {
  if (!kw) { console.log("Usage: search <keyword>"); return; }
  const nk = normalize(kw);
  console.log(`${C.bold}🔍 Searching: ${kw}${C.reset}\n`);
  let found = 0;
  for (const c of chats) {
    const hay = normalize(c.title + "\n" + c.body);
    if (!hay.includes(nk)) continue;
    found++;
    console.log(`${C.bold}${C.cyan}📄 ${c.name}${C.reset} — ${c.title || "No title"}`);
    const lines = c.body.split(/\r?\n/);
    lines.forEach((line, i) => {
      if (normalize(line).includes(nk)) {
        const shown = line.trim().slice(0, 120);
        const idx = normalize(shown).indexOf(nk);
        let out = shown;
        if (idx >= 0) {
          const orig = shown.slice(idx, idx + kw.length);
          out = shown.slice(0, idx) + C.yellow + orig + C.reset + shown.slice(idx + kw.length);
        }
        console.log(`   ${C.dim}L${i + 1}${C.reset}  ${out}`);
      }
    });
    console.log("");
  }
  console.log(found ? `${found} chat khớp.` : "Không có kết quả.");
}

function cmdSummary(chats) {
  const summary = path.join(DATA_DIR, "_SUMMARY.md");
  const lines = [];
  lines.push("# Chat History Summary", "");
  lines.push(`Generated: ${new Date().toISOString().replace("T", " ").slice(0, 16)}`, "");
  lines.push("| Date | Title | Tags | File |");
  lines.push("|------|-------|------|------|");
  for (const c of chats) {
    lines.push(`| ${c.date || "?"} | ${(c.title || "?").replace(/\|/g, "\\|")} | ${c.tags.join(", ") || "—"} | ${c.name} |`);
  }
  lines.push("", `Total chats: ${chats.length}`, "");

  // thống kê tag
  const count = {};
  for (const c of chats) for (const t of c.tags) count[t] = (count[t] || 0) + 1;
  const top = Object.entries(count).sort((a, b) => b[1] - a[1]);
  if (top.length) {
    lines.push("## Top tags", "");
    for (const [t, n] of top) lines.push(`- \`${t}\` ×${n}`);
    lines.push("");
  }
  fs.writeFileSync(summary, lines.join("\n"));
  console.log(`✅ Summary → ${summary}`);
  console.log(`   ${chats.length} chat, ${top.length} tag khác nhau.`);
}

function cmdTags(chats) {
  const count = {};
  for (const c of chats) for (const t of c.tags) count[t] = (count[t] || 0) + 1;
  const top = Object.entries(count).sort((a, b) => b[1] - a[1]);
  console.log(`${C.bold}🏷️  Tags${C.reset} (${top.length})\n`);
  for (const [t, n] of top) console.log(`   ${C.cyan}${t}${C.reset} ×${n}`);
}

function cmdSave(chats, title) {
  if (!title) { console.log("Usage: save <title>  (nội dung đọc từ stdin)"); return; }
  const body = readStdin();
  const date = today();
  const fname = `${slugify(title)}-${date}.chat.md`;
  const file = path.join(DATA_DIR, fname);
  const content = `---
title: ${title}
date: ${date}
tags: []
---

# ${title}

${body.trim()}

## Tóm tắt
(Tự tóm tắt sau khi lưu)
`;
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(file, content);
  console.log(`✅ Đã lưu → ${file}`);
}

function cmdHelp() {
  console.log(`${C.bold}chat-history.mjs${C.reset} — quản lý lịch sử chat\n`);
  console.log(`  ${C.cyan}list${C.reset}              Liệt kê tất cả (mới nhất trước)`);
  console.log(`  ${C.cyan}recent [n]${C.reset}        N chat gần nhất (mặc định 5)`);
  console.log(`  ${C.cyan}search <kw>${C.reset}       Tìm kiếm (không dấu, không phân biệt hoa thường)`);
  console.log(`  ${C.cyan}summary${C.reset}           Tạo data/_SUMMARY.md + thống kê tag`);
  console.log(`  ${C.cyan}tags${C.reset}              Thống kê tag đã dùng`);
  console.log(`  ${C.cyan}save <title>${C.reset}      Lưu chat mới (nội dung qua stdin)`);
  console.log(`  ${C.cyan}help${C.reset}              Trợ giúp`);
}

// ---------- main ----------
const [cmd, ...args] = process.argv.slice(2);
const chats = loadChats();

switch (cmd) {
  case "list": cmdList(chats); break;
  case "recent": cmdRecent(chats, args[0]); break;
  case "search": cmdSearch(chats, args.join(" ")); break;
  case "summary": cmdSummary(chats); break;
  case "tags": cmdTags(chats); break;
  case "save": cmdSave(chats, args.join(" ")); break;
  case "help":
  case undefined: cmdHelp(); break;
  default:
    console.error(`Lệnh không rõ: ${cmd}\n`);
    cmdHelp();
    process.exit(1);
}
