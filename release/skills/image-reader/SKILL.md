---
name: image-reader
description: Đọc và phân tích ảnh (jpg, png, gif, webp). Trích xuất text (OCR), mô tả nội dung ảnh, phân tích biểu đồ, screenshot, meme, code screenshot, bảng biểu. Dùng khi cần đọc chữ trong ảnh, mô tả ảnh, phân tích UI, đọc code từ screenshot, extract dữ liệu từ ảnh.
metadata:
  version: 1.0.0
  purpose: "Đọc và phân tích ảnh (jpg, png, gif, webp). Trích xuất text (OCR), mô tả nội dung ảnh, phân tích biểu đồ, screenshot, meme, code"
  allowed-tools: bash
  dependencies: '~/.EasyOCR/model, skills/image-reader/scripts/check_env.py, skills/image-reader/scripts/ocr_image.py, skills/image-reader/scripts/image_to_api.py'
  tests: 'file_exists:~/.EasyOCR/model; file_exists:skills/image-reader/scripts/check_env.py; file_exists:skills/image-reader/scripts/ocr_image.py; file_exists:skills/image-reader/scripts/image_to_api.py'
  triggers: "đọc, phân, tích, ảnh, jpg, png"
---

# Image Reader

Skill đọc và phân tích mọi loại ảnh: screenshot, ảnh chứa code, biểu đồ, bảng biểu, meme, UI.

## QUAN TRỌNG — Môi trường đã cố định (đọc trước khi làm)

Môi trường OCR trên máy Thăng ĐÃ được kiểm tra và cố định. **Không chạy lại vòng lặp `where python`/`where tesseract` mỗi lần** — đây là nguyên nhân gây nhiễu "chưa cài này cài kia".

| Thành phần | Trạng thái |
|-----------|-----------|
| Python | ✅ `python` (3.11) |
| Tesseract | ❌ **CHƯA cài** — đừng thử, bỏ qua thẳng |
| RapidOCR | ✅ 1.4.4 (onnxruntime) — **nhanh ~1s, dùng chính** |
| EasyOCR | ✅ 1.7.2 + model đã cache `~/.EasyOCR/model/` — fallback tiếng Việt |
| Pillow | ✅ 12.2.0 |
| pytesseract | ✅ 0.3.13 (vô dụng vì thiếu binary) |

→ **Luôn dùng RapidOCR** (nhanh ~1s). EasyOCR fallback tiếng Việt. Đặt biến một lần:

```bash
PY="python"
```

Nếu nghi ngờ môi trường đổi (sau cài đặt mới), chạy đúng 1 lệnh để kiểm tra lại:

```bash
"$PY" "skills/image-reader/scripts/check_env.py"
```

## Model Vision (mới — pi 0.85.1)

DeepSeek giờ có model vision: `deepseek-v4-flash-vision-exp` (provider `deepseek`, images: yes).

- `read` ảnh bằng model chính (`deepseek-v4-pro`) có thể fail nếu model không hỗ trợ ảnh.
- Ảnh phức tạp (biểu đồ, code screenshot, UI) → đổi model sang `deepseek-v4-flash-vision-exp` rồi `read` ảnh → chính xác hơn EasyOCR nhiều.
- RapidOCR (nhanh ~1s) / EasyOCR là fallback offline (không tốn token).

## Luồng xử lý ảnh (TỐI ƯU)

Khi nhận ảnh, **gọi `read` + chạy OCR song song trong cùng một lượt** — không gọi riêng lẻ, không bước trung gian:

```bash
PY="python"
"$PY" "skills/image-reader/scripts/ocr_image.py" "<ảnh>" --lang vie+eng --info
```

- `read` trả được nội dung → dùng `read` (model hỗ trợ ảnh).
- `read` trả `"model does not support images"` → dùng output OCR, **đã có sẵn ngay**, không gọi lại.
- Không đoán trước model hỗ trợ ảnh hay không — cứ chạy cả hai song song.

### Bước 2: Chạy OCR (RapidOCR, mặc định — ~1s)

```bash
PY="python"
"$PY" "skills/image-reader/scripts/ocr_image.py" "ĐƯỜNG_DẪN_ẢNH" --info
```

Script đã tối ưu: **RapidOCR mặc định (~1s)** → fallback EasyOCR → Tesseract. Cache model, không check mạng.

### Bước 3: Chọn reader tường minh

```bash
# RapidOCR — nhanh nhất (~1s), ảnh thường
"$PY" "skills/image-reader/scripts/ocr_image.py" "ẢNH" --reader rapidocr

# EasyOCR — tiếng Việt có dấu tốt hơn, chậm hơn (~8-15s)
"$PY" "skills/image-reader/scripts/ocr_image.py" "ẢNH" --reader easyocr
```

### Bước 4: Fallback API (chỉ khi OCR thất bại và có API key)

```bash
"$PY" "skills/image-reader/scripts/image_to_api.py" "ĐƯỜNG_DẪN_ẢNH"
```

Cần `OPENAI_API_KEY` trong env hoặc file `.env`.

## Tổng hợp kết quả

Sau khi có text:
1. Phân tích nội dung text.
2. Trả lời câu hỏi người dùng dựa trên text.
3. Nếu text nhiễu → nói rõ đoạn nào chưa rõ, đề nghị paste lại vào model hỗ trợ ảnh.

## Scripts

| Script | Mô tả | Cần API key? |
|--------|-------|:---:|
| `scripts/check_env.py` | Kiểm tra môi trường 1 lần, ghi cache `.env_cache.json` | ❌ |
| `scripts/ocr_image.py` | OCR offline (RapidOCR→EasyOCR→Tesseract tự fallback) | ❌ |
| `scripts/image_to_api.py` | Phân tích qua GPT-4o Vision / Claude | ✅ |

## Cài đặt khi thiếu (chỉ khi `check_env.py` báo thiếu)

```bash
winget install UB-Mannheim.TesseractOCR        # nếu muốn Tesseract
"python" -m pip install pytesseract pillow easyocr
```

> **Không cài đặt lặp lại** nếu `check_env.py` đã báo OK — đó chính là lỗi "chưa cài này cài kia" trước đây.

## Hỗ trợ tiếng Việt

Mọi phân tích trả về tiếng Việt trừ khi người dùng yêu cầu ngôn ngữ khác.

## Changelog
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
