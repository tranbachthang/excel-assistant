---
name: excel-manager
description: Quản lý file Excel (.xlsx) — đọc/tạo bảng, điền dữ liệu vào form mẫu (giữ nguyên merge/màu/công thức), format hàng loạt, chuyển CSV <-> XLSX, tối ưu giảm dung lượng. Xử lý CHẤM CÔNG (gom dòng trùng do nhiều máy, tính tổng giờ/phút, tô VÀNG quên chấm công / ĐỎ không chấm công) và THEO DÕI KHO (tự tạo sheet ngày từ mẫu, nối tồn kho qua công thức). Dùng khi cần đọc, tạo, sửa, điền form, format, tối ưu file Excel; xử lý timesheet/chấm công; tạo sheet theo dõi kho theo ngày.
license: MIT
allowed-tools: bash, read, write
metadata:
  version: 1.0.0
  purpose: "AI agent quản lý Excel: đọc/tạo/điền form/format/tối ưu .xlsx + xử lý chấm công + theo dõi kho"
  dependencies: "python + openpyxl; scripts/excel_assistant.py, chamcong.py, theodoikho.py, menu.py, img2xlsx.py, txt2xlsx.py"
  tests: "bash:python scripts/excel_assistant.py demo; bash:python scripts/chamcong.py --help; bash:python scripts/theodoikho.py --help"
  triggers: "excel, xlsx, bảng tính, điền form, spreadsheet, chấm công, timesheet, time sheet, theo dõi kho, tồn kho, nhập xuất"
---

# Excel Manager

Trợ lý quản lý bảng tính `.xlsx` bằng `openpyxl` — không cần cài Microsoft Excel.

Cài trước: `pip install openpyxl`.

## Công cụ (chạy từ thư mục skill này)

```bash
python scripts/<script>.py <lệnh> ...
```

| Script / Lệnh | Việc |
|---|---|
| `excel_assistant.py info <file>` | liệt kê sheet + số hàng/cột |
| `excel_assistant.py read <file> [--sheet S] [--head N]` | in nội dung |
| `excel_assistant.py csv2xlsx <in.csv> <out.xlsx>` / `xlsx2csv` | chuyển đổi CSV ↔ XLSX |
| `excel_assistant.py beautify <file>` | header đậm, viền, auto-width, freeze, filter |
| `excel_assistant.py fill <template> <data.json> [out.xlsx]` | điền giá trị theo địa chỉ ô |
| `excel_assistant.py optimize <in> <out>` | ghi lại, giảm dung lượng |
| `chamcong.py <file> [--ma M] [--tu ..] [--den ..] [--nghi ..]` | **1 lệnh**: gom dòng trùng + tính tổng giờ/phút + tô VÀNG/ĐỎ |
| `theodoikho.py <file> [--den DD/MM/YYYY]` | **1 lệnh**: tự tạo sheet ngày theo dõi kho, nối tồn kho |
| `menu.py` | giao diện menu cho người dùng cuối (không cần nhớ lệnh) |
| `img2xlsx.py <anh.png> [out.xlsx]` | ảnh → Excel (OCR + dựng bảng) |
| `excel_assistant.py demo` | tự kiểm (`SELFTEST PASS`) |

## 1) Chấm công (1 lệnh)

Bài toán: nhiều máy chấm công làm 1 ngày bị tách 2 dòng (1 dòng chỉ Vào, 1 dòng chỉ Ra). Cần gom về 1 dòng, tính lại tổng giờ + phút, đánh dấu lỗi.

```bash
# 1 nhân viên
python scripts/chamcong.py data/chamcong_raw.xlsx --ma 741046 --out ketqua.xlsx

# TẤT CẢ nhân viên (mỗi người 1 sheet)
python scripts/chamcong.py data/chamcong_raw.xlsx --out ketqua.xlsx
```

Tham số:
- `--ma M` — mã nhân viên (bỏ qua = xử lý tất cả).
- `--tu/--den DD/MM/YYYY` — khoảng ngày (mặc định = min/max ngày có trong dữ liệu).
- `--nghi DD/MM/YYYY,...` — ngày nghỉ lễ, loại khỏi diện "không chấm công".
- `--out` — file xuất (mặc định `<ten>_da_xu_ly.xlsx`).

Kết quả: cột `Tổng giờ`/`Tổng phút` tính lại từ Vào→Ra; dòng `TỔNG` cuối bảng.
- Thiếu Vào hoặc Ra → **VÀNG** + ghi "Quên chấm công vào/ra".
- Ngày làm việc (T2–T6) không có dòng nào → **ĐỎ** + ghi "Không chấm công".

## 2) Theo dõi kho (1 lệnh)

Từ mẫu sheet `01-09`, tự tạo các sheet ngày tiếp theo, nối "Tồn đầu ngày" ← "Tồn cuối ngày" sheet trước.

```bash
# Tao den cuoi thang
python scripts/theodoikho.py data/theodoikho.xlsx --den 30/09/2026

# Chi them 1 ngay ke tiep
python scripts/theodoikho.py data/theodoikho.xlsx
```

- Copy mẫu `01-09`, cập nhật ô `Ngày` (B2) + `Thứ` (C2).
- Cột `Tồn đầu ngày` (E5:E19) tham chiếu `'<sheet trước>'!H` (công thức).
- Cột Nhập/Xuất/Ghi chú để trống cho người dùng nhập.

## 3) Giao diện menu

```bash
python scripts/menu.py
```
Menu: 1) chấm công · 2) theo dõi kho · 3) xem nội dung file · 0) thoát. Nhập theo hướng dẫn, không cần nhớ lệnh.

## 4) Ảnh → Excel 1 lệnh

```bash
python scripts/img2xlsx.py <anh.png> [out.xlsx]
```
Tự OCR (RapidOCR ~1s) + dựng bảng: title merge, header đậm+nền+viền, freeze.
**Lưu ý:** OCR hay gộp ô liền kề (STT+Ngày, Số giờ+Trạng thái) → kiểm tra lại bằng `read`.

## 5) Điền form

1. `info` + `read` template → xác định địa chỉ ô cần điền.
2. Dựng `data.json` dạng `{"TênSheet": {"B2": "giá trị", "C3": 4}}`.
3. `fill template.xlsx data.json ketqua.xlsx`.
4. **Verify**: `read ketqua.xlsx --head 5` → đối chiếu đúng ô.

Điền form từ **ảnh**: dùng skill `image-reader` (OCR) lấy text + toạ độ → suy bố cục → `fill` vào file gốc (giữ form 100%) hoặc dựng lại nếu chỉ có ảnh.

## Giới hạn (nói thẳng khi gặp)
- Không tính lại công thức (openpyxl chỉ đọc giá trị đã lưu).
- Không hỗ trợ macro VBA; file `.xls` cũ phải đổi sang `.xlsx` trước.
- `optimize` có thể làm mất vài style hiếm → giữ bản gốc nếu quan trọng.
- Chấm công "không đi làm" chỉ đánh đỏ ngày làm việc trong khoảng dữ liệu; ngày nghỉ lễ khai báo qua `--nghi`.
