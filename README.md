# excel-assistant

**AI agent quản lý Excel** — đọc / tạo / **điền dữ liệu vào form mẫu** / format hàng loạt / tối ưu `.xlsx`.
Đóng gói dưới dạng **pi package**: cài một lệnh là Pi trở thành trợ lý Excel.

Chỉ cần Python + `openpyxl`, **không cần Microsoft Excel**.

## Cài như một AI agent (pi package)

```bash
pip install openpyxl
pi install git:github.com/tranbachthang/excel-assistant
```

Sau đó trong Pi, agent tự biết skill `excel-manager` và nhận việc Excel bằng tiếng Việt:

> "đọc form.xlsx, điền tên và ngày vào rồi xuất ketqua.xlsx"

Hoặc gọi thẳng skill:

```text
/skill:excel-manager tối ưu file big.xlsx
```

### Chạy như agent riêng (nhẹ, tách khỏi cấu hình Pi cá nhân)

```bash
PI_CODING_AGENT_DIR=$(pwd) pi
```

Pi nạp `AGENTS.md` (persona) + skill trong repo → một agent chỉ chuyên Excel.

## Dùng trực tiếp (không cần AI)

```bash
cd skills/excel-manager
python scripts/excel_assistant.py info    book.xlsx
python scripts/excel_assistant.py read    book.xlsx --head 10
python scripts/excel_assistant.py csv2xlsx data.csv out.xlsx
python scripts/excel_assistant.py xlsx2csv book.xlsx out.csv
python scripts/excel_assistant.py beautify book.xlsx
python scripts/excel_assistant.py fill    template.xlsx data.json filled.xlsx
python scripts/excel_assistant.py optimize big.xlsx small.xlsx
python scripts/excel_assistant.py demo                      # SELFTEST PASS
```

### Điền form

Giữ nguyên form mẫu (merge, màu, công thức) và chỉ điền giá trị vào ô:

```json
{ "Sheet1": { "B2": "Tran Bach Thang", "B3": "07/10/2026", "C5": 4 } }
```

## Cấu trúc

```text
excel-assistant/
├── package.json            # pi package manifest
├── AGENTS.md               # persona của agent
├── skills/excel-manager/
│   ├── SKILL.md            # playbook: điền form, điền từ ảnh, tối ưu
│   └── scripts/excel_assistant.py
├── requirements.txt
└── LICENSE
```

## Phạm vi

| Làm được | Không làm |
|---|---|
| Đọc/ghi `.xlsx`, nhiều sheet | Tính lại công thức (openpyxl không tính) |
| Điền giá trị theo địa chỉ ô (giữ form) | Macro VBA |
| Điền từ ảnh qua OCR (dùng skill `image-reader`) | File `.xls` cũ → đổi `.xlsx` trước |
| Format bảng, CSV ↔ XLSX, tối ưu dung lượng | |

MIT License.
