---
name: screen-watch
description: Cho AI text-only "nhìn" nội dung màn hình bằng cách chụp màn hình + OCR, trả về mô tả dạng text. Dùng khi cần xem/giám sát màn hình desktop Windows, theo dõi thao tác người dùng, hoặc trích xuất text trên màn hình.
metadata:
  version: 1.0.0
  purpose: "Cho AI text-only nhìn nội dung màn hình bằng cách chụp màn hình + OCR, trả về mô tả dạng text."
  allowed-tools: read
  dependencies: none
  tests: 'grep:skills\screen-watch\SKILL.md:^## '
  triggers: "text, only, nhìn, nội, dung, màn"
---
# screen-watch skill

Cho phep AI agent (text-only) "nhin" duoc noi dung tren man hinh cua nguoi dung
bang cach chup man hinh, chay OCR, va tra ve mo ta dang text.

## Cai dat (chay tren may Windows, 1 lan)

```powershell
pip install mss pytesseract pillow
```

Cai them Tesseract OCR engine (khong phai package Python):
https://github.com/UB-Mannheim/tesseract/wiki

Sau khi cai xong, neu `tesseract` khong nam trong PATH, sua bien
`pytesseract.pytesseract.tesseract_cmd` trong `screen_watch.py` tro toi
duong dan file `tesseract.exe`.

## Cach agent goi skill nay

Chup 1 lan (dung khi ban chu dong hoi "man hinh dang co gi"):

```
python screen_watch.py capture
```

Theo doi lien tuc, chi bao khi man hinh thay doi dang ke (dung cho che do
"dong hanh real-time", tranh spam token vao moi 1-3 giay):

```
python screen_watch.py watch --interval 3
```

## Khi nao agent nen goi tool nay

- Khi nguoi dung hoi ve noi dung dang hien tren man hinh ("dang co loi gi vay",
  "doc giup tao dong text nay").
- Khi nguoi dung bat che do "quan sat real-time" va muon agent tu dong comment
  theo tien do (dung lenh `watch`, doc output moi khi co dong "=== Man hinh
  thay doi ===" xuat hien).
- KHONG tu y goi tool nay de yeu cau nguoi dung chup/paste anh chua thong tin
  nhay cam (CCCD, passport, OTP, mat khau). Neu OCR phat hien noi dung co the
  la giay to tuy than hoac thong tin dang nhap, agent nen bao nguoi dung va
  KHONG tu dong xu ly tiep noi dung do.

## Gioi han hien tai

- Chi doc duoc text hien thi, khong "nhin" duoc hinh anh/icon/layout (can VLM
  neu muon hieu ca giao dien truc quan).
- OCR co the sai/thieu voi font nho hoac chu cach dieu.
- Nang cap sau: thay doan OCR bang goi 1 vision-language model local (vi du
  Qwen2-VL hoac MiniCPM-V qua Ollama) de agent hieu ca layout, khong chi text.

## Changelog
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
