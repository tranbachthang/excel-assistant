---
name: google-docs
description: Đọc, phân tích và trích xuất nội dung từ Google Docs, Google Sheets, Google Slides, Google Drive. Hỗ trợ đọc tài liệu online, export ra markdown/text/JSON, tìm kiếm trong Drive, xử lý Google Sheets như database. Dùng khi cần đọc tài liệu Google, lấy dữ liệu từ Sheets, tìm file trên Drive, trích xuất nội dung Docs/Slides.
metadata:
  version: 1.0.0
  purpose: "Đọc, phân tích và trích xuất nội dung từ Google Docs, Google Sheets, Google Slides, Google Drive. Hỗ trợ đọc tài liệu online, export ra"
  allowed-tools: browser, bash, edit
  dependencies: none
  tests: 'grep:skills\google-docs\SKILL.md:^## '
  triggers: "đọc, phân, tích, trích, xuất, nội"
---

# Google Docs Reader

Skill đọc và xử lý tài liệu từ Google Workspace: Docs, Sheets, Slides, Drive.

## Yêu cầu

Cần cài đặt thư viện Python:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## Các tác vụ

### 1. Đọc Google Docs
- Nhập link Google Docs → trích xuất toàn bộ nội dung văn bản
- Giữ định dạng: heading, bold, italic, list, table
- Output: Markdown hoặc plain text

### 2. Đọc Google Sheets
- Nhập link Sheets → lấy dữ liệu dạng bảng
- Hỗ trợ query range (A1:D10), lọc dữ liệu
- Output: JSON, CSV, Markdown table

### 3. Đọc Google Slides
- Nhập link Slides → trích xuất text từ tất cả slide
- Output: text theo từng slide

### 4. Tìm kiếm Google Drive
- Tìm file theo tên, loại, ngày tạo
- Liệt kê file trong thư mục

### 5. Export & Convert
- Docs → Markdown, PDF
- Sheets → CSV, JSON
- Slides → text

## Script hỗ trợ

Scripts nằm trong `scripts/`:
- `read_doc.py` — đọc Google Docs
- `read_sheet.py` — đọc Google Sheets  
- `read_slides.py` — đọc Google Slides
- `drive_search.py` — tìm kiếm Google Drive
- `quick_gdoc.py` — đọc nhanh không cần auth (nếu file public)

## Xác thực Google API

### Cách 1: Service Account (khuyên dùng)
1. Tạo Service Account trên Google Cloud Console
2. Tải JSON key, lưu vào `scripts/credentials.json`
3. Share Docs/Sheets với email service account

### Cách 2: OAuth (cho tài khoản cá nhân)
1. Chạy script, mở browser đăng nhập Google
2. Token tự lưu vào `scripts/token.pickle`

### Cách 3: Public file (không cần auth)
Nếu file được share "Anyone with link can view", dùng script `quick_gdoc.py`:
```bash
python scripts/quick_gdoc.py "https://docs.google.com/document/d/FILE_ID/edit"
```

## Cách dùng

Khi người dùng gửi link Google:
1. Xác định loại (Docs / Sheets / Slides / Drive folder)
2. Chọn script phù hợp
3. Chạy script, lấy kết quả
4. Trình bày nội dung rõ ràng cho người dùng

## Ví dụ

```bash
# Đọc Google Docs có auth
python scripts/read_doc.py "https://docs.google.com/document/d/ABC123/edit"

# Đọc Google Sheets, lấy range cụ thể
python scripts/read_sheet.py "https://docs.google.com/spreadsheets/d/ABC123/edit" --range "Sheet1!A1:E20"

# Tìm file trên Drive
python scripts/drive_search.py "báo cáo tháng 6" --type spreadsheet

# Đọc Docs public không cần auth
python scripts/quick_gdoc.py "https://docs.google.com/document/d/ABC123/edit"
```

## Changelog
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
