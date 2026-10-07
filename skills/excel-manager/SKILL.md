---
name: excel-manager
description: Quản lý file Excel (.xlsx) — đọc/tạo bảng, điền dữ liệu vào form mẫu (giữ nguyên merge/màu/công thức), format hàng loạt, chuyển CSV <-> XLSX, tối ưu giảm dung lượng. Dùng khi cần đọc, tạo, sửa, điền form, format hoặc tối ưu file Excel / bảng tính.
license: MIT
allowed-tools: bash, read, write
metadata:
  version: 0.1.0
  purpose: "AI agent quản lý Excel: đọc/tạo/điền form/format/tối ưu .xlsx"
  dependencies: "python + openpyxl; scripts/excel_assistant.py"
  tests: "bash:python scripts/excel_assistant.py demo"
  triggers: "excel, xlsx, bảng tính, điền form, spreadsheet, tối ưu excel"
---

# Excel Manager

Trợ lý quản lý bảng tính `.xlsx` bằng `openpyxl` — không cần cài Microsoft Excel.

## Công cụ

Script đóng gói sẵn (chạy từ thư mục skill này):

```bash
python scripts/excel_assistant.py <lệnh> ...
```

| Lệnh | Việc |
|---|---|
| `info <file>` | liệt kê sheet + số hàng/cột |
| `read <file> [--sheet S] [--head N]` | in nội dung |
| `csv2xlsx <in.csv> <out.xlsx>` / `xlsx2csv <in.xlsx> <out.csv>` | chuyển đổi |
| `beautify <file>` | header đậm, viền, auto-width, freeze, filter |
| `fill <template> <data.json> [out.xlsx]` | điền giá trị theo địa chỉ ô |
| `optimize <in> <out>` | ghi lại, giảm dung lượng |
| `demo` | tự kiểm (`SELFTEST PASS`) |

Cài trước: `pip install openpyxl`.

## Quy trình

### 1. Điền form từ dữ liệu có sẵn
1. `info` + `read` template → xác định địa chỉ ô cần điền và các cột.
2. Dựng `data.json` dạng `{"TênSheet": {"B2": "giá trị", "C3": 4}}`.
3. `fill template.xlsx data.json ketqua.xlsx`.
4. **Verify**: `read ketqua.xlsx --head 5` → đối chiếu đúng ô.

### 2. Điền form từ ẢNH (ảnh chụp bảng/form)
1. Đọc ảnh bằng skill `image-reader` (RapidOCR) để lấy **text + toạ độ**.
2. Suy bố cục: hàng/cột, ô nào là nhãn, ô nào cần điền.
3. Nếu **có file `.xlsx` gốc** → `fill` vào chính file đó (giữ form 100%). Nếu **chỉ có ảnh** → dựng lại bảng bằng `openpyxl` (bố cục tương đương, không khớp pixel).
4. Verify lại bằng `read` + (nếu cần) chụp màn hình file đã mở.

### 3. Tối ưu / format
- `beautify` cho bảng thô cần trình bày.
- `optimize` khi file phình to; lưu ý có thể mất vài định dạng hiếm.

## Giới hạn (nói thẳng khi gặp)
- Không tính lại công thức (openpyxl chỉ đọc giá trị đã lưu).
- Không hỗ trợ macro VBA; file `.xls` cũ phải đổi sang `.xlsx` trước.
- `optimize` có thể làm mất vài style hiếm → giữ bản gốc nếu quan trọng.
