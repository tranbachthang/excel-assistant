---
name: chat-history
description: Lưu, tìm kiếm và tái sử dụng lịch sử chat. Dùng khi cần lưu hội thoại hiện tại, xem lại các chat cũ, hoặc nạp lại ngữ cảnh từ phiên trước. Hỗ trợ lưu tự động, tìm kiếm theo từ khóa (kể cả tiếng Việt không dấu), và tổng hợp nội dung từ nhiều phiên chat.
metadata:
  version: 1.0.0
  purpose: "Lưu, tìm kiếm và tái sử dụng lịch sử chat."
  allowed-tools: bash, edit
  dependencies: none
  tests: 'grep:skills\chat-history\SKILL.md:^## '
  triggers: "lưu, tìm, kiếm, tái, dụng, lịch"
---

# Chat History

Skill này giúp lưu trữ và tái sử dụng lịch sử hội thoại giữa các phiên làm việc.

## Thư mục

- `data/` — nơi lưu các file lịch sử chat (định dạng `.chat.md`)
- `scripts/chat-history.mjs` — CLI chính (Node.js)

## Cách dùng

Tất cả thao tác qua 1 CLI duy nhất:

```bash
CH=~/.agents/skills/chat-history/scripts/chat-history.mjs

node "$CH" list              # Liệt kê tất cả chat (mới nhất trước)
node "$CH" recent 5          # 5 chat gần nhất
node "$CH" search <từ khóa>  # Tìm kiếm (không dấu, không phân biệt hoa thường)
node "$CH" summary           # Tạo data/_SUMMARY.md + thống kê tag
node "$CH" tags              # Thống kê các tag đã dùng
node "$CH" help              # Trợ giúp
```

### 1. Lưu lịch sử chat hiện tại

Dùng `save` — nội dung chat đưa qua stdin:

```bash
echo '<nội dung chat>' | node "$CH" save "Tiêu đề chat"
```

Hoặc AI tự ghi file trực tiếp vào `data/<tên-ngắn-gọn>-<YYYY-MM-DD>.chat.md`.

File nên có format:
```markdown
---
title: <tiêu đề ngắn>
date: <YYYY-MM-DD HH:MM>
tags: [tag1, tag2]
---

# <Tiêu đề>

<Nội dung chat được format rõ ràng, phân biệt User và Assistant>

## Tóm tắt
<Tóm tắt 2-3 câu về nội dung chính và kết quả>
```

### 2. Tìm kiếm trong lịch sử chat

```bash
node "$CH" search "sql injection"   # tìm theo từ khóa
node "$CH" search "chot scope"      # tìm không dấu vẫn ra "Chốt scope"
```

### 3. Nạp lại ngữ cảnh từ chat cũ

`search` để tìm đúng file, rồi `read` file `.chat.md` để tiếp tục làm việc với ngữ cảnh đã lưu.

### 4. Tạo bản tóm tắt tổng hợp

```bash
node "$CH" summary
```
Kết quả lưu tại `data/_SUMMARY.md` (bảng + top tags).

## Quy tắc lưu chat

- **Ưu tiên `/name`**: nếu session có tên do Thăng đặt (`session_info.name` trong file `.jsonl`) → dùng **đúng tên đó** làm tiêu đề + tên file. Chưa đặt tên mới lấy tin đầu (do `extensions/chat-autosave.ts` xử lý từ 03/10/2026).
- Tên file: `<chủ-đề>-<YYYY-MM-DD>.chat.md`, chữ thường, không dấu, dùng dấu gạch ngang
- Luôn thêm frontmatter với `title`, `date`, `tags`
- Luôn có phần `## Tóm tắt` ở cuối
- Nội dung giữa User và Assistant cần được phân biệt rõ ràng
- Nếu chat dài, ưu tiên giữ các phần quan trọng: quyết định, code đã viết, kết quả cuối cùng

## Changelog
- 1.1.0 (2026-10-03): autosave lưu theo `/name` của session (trước đây lấy tin đầu tiên); thêm `session: <id>` vào frontmatter để đổi tên/truy vết về sau.
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
