# Quy trình nhanh: Ảnh → Excel (đã tối ưu, đừng làm lại bước thừa)

## Biến môi trường cố định (dùng 1 lần, khỏi dò lại)
```bash
PY="C:/Users/thang/AppData/Local/Microsoft/WindowsApps/python.exe"
```
- Luôn thêm `PYTHONIOENCODING=utf-8` khi `read`/in tiếng Việt (nếu không sẽ `UnicodeEncodeError`).
- OCR dùng **RapidOCR** (~1s) — KHÔNG cần check env lại mỗi lần.

## Case A — Bảng mới / ảnh lạ: 1 lệnh dựng tự động
```bash
"$PY" skills/excel-manager/scripts/img2xlsx.py "<anh.png>" "<out.xlsx>"
```
→ Tự OCR + dựng bảng (title merge, header đậm+nền+viền, freeze). ~1-2s.

## Case B — Bảng lặp lại (BẢNG THEO DÕI CÔNG VIỆC TUẦN): dùng template + fill
1. OCR lấy text thô:
```bash
"$PY" "C:/Users/thang/.agents/skills/image-reader/scripts/ocr_image.py" "<anh.png>"
```
2. Tôi map text → `data.json` (đúng cột, tách ô bị gộp như `4Hoàn thành` → Số giờ=4, Trạng thái=Hoàn thành).
3. Fill vào template:
```bash
"$PY" skills/excel-manager/scripts/excel_assistant.py fill "template.xlsx" "data.json" "ketqua.xlsx"
```

## Case C — Chấm công (gom dòng trùng do nhiều máy + tô vang/đỏ)
```bash
"$PY" skills/excel-manager/scripts/chamcong.py "data/chamcong_raw.xlsx" --ma 741046 --out "data/chamcong_741046.xlsx"
# tuỳ chọn: --tu/--den (khoảng ngày), --nghi "01/09/2026,02/09/2026" (ngày nghỉ lễ), bỏ --ma = xử lý tất cả
```
→ Gom 2 dòng cùng ngày (chỉ Vào / chỉ Ra) thành 1, tính lại Tổng giờ + Tổng phút.
→ Thiếu Vào/Ra → **VÀNG** "Quên chấm công vào/ra". Ngày làm việc không có dòng → **ĐỎ** "Không chấm công".

## Case D — Theo dõi kho (tự tạo sheet ngày từ mẫu 01-09)
```bash
"$PY" skills/excel-manager/scripts/theodoikho.py "data/theodoikho.xlsx" --den 30/09/2026
# bỏ --den = chỉ thêm 1 ngày kế tiếp
```
→ Copy mẫu 01-09, cập nhật Ngày + Thứ, cột "Tồn đầu ngày" nối "Tồn cuối ngày" sheet trước (công thức).

## Giao diện cho người dùng cuối
```bash
"$PY" skills/excel-manager/scripts/menu.py
```

## Verify (bắt buộc, 1 lệnh)
```bash
PYTHONIOENCODING=utf-8 "$PY" skills/excel-manager/scripts/excel_assistant.py read "<file.xlsx>"
```

## Mở file (lệnh NÀY mới chạy — `start ""` không đáng tin)
```bash
powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE' -ArgumentList '<duong_dan_tuyet_doi.xlsx>'"
```

## Ghi nhớ (kinh nghiệm đã tốn thời gian)
- `img2xlsx.py` dùng index cột 0-based → đã sửa `column=j+1`. Đừng quay lại bug cũ.
- Excel path: `C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE`.
- OCR hay **gộp ô liền kề** (STT+Ngày, Số giờ+Trạng thái) → với bảng quen thì tự tách theo ngữ nghĩa.
