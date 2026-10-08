---
name: session-context
description: Tự động nạp ngữ cảnh khi bắt đầu phiên mới. Biết đang làm dự án gì, đã làm đến đâu, việc tiếp theo là gì. Dùng mỗi khi bắt đầu chat ở một phiên mới.
metadata:
  version: 1.0.1
  purpose: "Nạp ngữ cảnh đầu phiên: đọc persona + quy trình + lịch sử chat gần nhất trong gói."
  allowed-tools: bash, read
  dependencies: "AGENTS.md, QUY_TRINH_NHANH.md, skills/chat-history/data/"
  tests: "file_exists:AGENTS.md; file_exists:QUY_TRINH_NHANH.md"
  triggers: "ngữ cảnh, phiên mới, session, đang làm gì, đã làm đến đâu"
---

# Session Context — Nạp ngữ cảnh đầu phiên

## Mục đích

Mỗi khi mở phiên mới, đọc trước để biết: **đang làm gì** · **đã làm đến đâu** · **việc tiếp theo**.

## Cách dùng (bắt buộc khi mở phiên mới)

```
Bước 1: Đọc persona + quy tắc
  → AGENTS.md

Bước 2: Đọc quy trình nhanh
  → QUY_TRINH_NHANH.md

Bước 3: Đọc chat gần nhất (nếu có)
  → ls -t skills/chat-history/data/*.chat.md | head -1
  → Đọc file mới nhất
```

Sau khi đọc xong, tóm tắt ngắn cho người dùng:

```
📋 Bối cảnh:
- Đang làm: [việc chính]
- Đã xong: [kết quả gần nhất]
- Tiếp theo: [việc kế tiếp]
```

## Lưu trữ lịch sử chat

```bash
CH=skills/chat-history/scripts/chat-history.mjs
node "$CH" list              # liệt kê chat
node "$CH" recent 5          # 5 chat gần nhất
node "$CH" search <từ khóa>  # tìm kiếm
```

Lưu chat hiện tại: ghi file vào `skills/chat-history/data/<tên-ngắn>-<YYYY-MM-DD>.chat.md`.

## Lưu ý

- File nào không tồn tại → bỏ qua, không dừng.
- Nếu người dùng đã nói rõ bối cảnh trong tin nhắn → dùng luôn, không đọc lại hết.
- Luôn trả lời bằng tiếng Việt.

## Changelog
- 1.0.1 (2026-10-08): bản cho gói release — bỏ phần Telegram riêng, dùng file trong gói.
- 1.0.0 (2026-09-29): chuẩn hoá metadata module.
