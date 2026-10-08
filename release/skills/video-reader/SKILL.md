---
name: video-reader
description: Đọc và phân tích nội dung video (mp4, avi, mov, webm). Trích xuất text (OCR từng frame), transcript, mô tả nội dung. Dùng khi cần xem video demo, tutorial, recording, hoặc extract thông tin từ video.
metadata:
  version: 1.0.0
  purpose: "Đọc và phân tích nội dung video (mp4, avi, mov, webm). Trích xuất text (OCR từng frame), transcript, mô tả nội dung."
  allowed-tools: bash
  dependencies: none
  tests: 'grep:skills\video-reader\SKILL.md:^## '
  triggers: "đọc, phân, tích, nội, dung, video"
---

# Video Reader

Skill đọc và phân tích video: extract frames, OCR text, tổng hợp nội dung.

## Cách dùng

### Bước 1: Cài đặt (chạy 1 lần)

```bash
pip install opencv-python pillow easyocr
```

### Bước 2: Phân tích video

```bash
python scripts/read_video.py "đường_dẫn_video.mp4" --interval 2
```

- `--interval 2`: chụp 1 frame mỗi 2 giây
- `--max-frames 20`: tối đa số frame
- `--output results/`: thư mục output

### Bước 3: Đọc kết quả

Script tạo ra:
- `results/frames/` — các frame đã chụp
- `results/ocr_text.txt` — text OCR từ tất cả frame
- `results/summary.json` — metadata + text

## Luồng xử lý

```
Video → Extract frames (mỗi N giây) → OCR từng frame → Tổng hợp text → Trả lời
```

## Scripts

| Script | Mô tả |
|--------|-------|
| `scripts/read_video.py` | Extract frames + OCR + tổng hợp |

## Changelog
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
