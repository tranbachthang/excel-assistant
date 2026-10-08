# excel-assistant 🐍📊

**Một con Pi riêng, chỉ để quản lý Excel.** Đọc · tạo · **điền dữ liệu vào form mẫu** · format · tối ưu `.xlsx`.
Chỉ cần Python + `openpyxl`, **không cần Microsoft Excel**.

Repo này vừa là **pi package** (cài vào Pi có sẵn), vừa là **agent dir độc lập** (chạy như một Pi riêng).

---

## 1. Lấy về

```bash
git clone https://github.com/tranbachthang/excel-assistant.git
cd excel-assistant
pip install openpyxl
```

## 2. Cách sử dụng

### (A) Chạy như một con Pi riêng (khuyến nghị)

```bash
# Windows
run.cmd

# Git Bash / Linux / macOS
./run.sh
```

Launcher tự đặt `PI_CODING_AGENT_DIR` = thư mục repo → Pi nạp `AGENTS.md` (persona) + skill `excel-manager`, **tách khỏi cấu hình Pi cá nhân**.

Lần đầu cần key (xem mục 3). Sau đó vào Pi và ra lệnh bằng tiếng Việt:

> đọc `examples/cong_viec_template.xlsx`, điền công việc hôm nay rồi xuất `ketqua.xlsx`

Hoặc gọi thẳng skill: `/skill:excel-manager tối ưu file big.xlsx`

### (B) Cài vào Pi đang dùng (không tách)

```bash
pi install git:github.com/tranbachthang/excel-assistant
```

### (C) Dùng trực tiếp, không cần AI

```bash
cd skills/excel-manager
python scripts/excel_assistant.py info    ../../examples/cong_viec_template.xlsx
python scripts/excel_assistant.py read    ../../examples/cong_viec_1000.xlsx --head 5
python scripts/excel_assistant.py csv2xlsx data.csv out.xlsx
python scripts/excel_assistant.py beautify book.xlsx
python scripts/excel_assistant.py fill    template.xlsx data.json filled.xlsx
python scripts/excel_assistant.py optimize big.xlsx small.xlsx
python scripts/excel_assistant.py demo                       # SELFTEST PASS
```

## 3. Nhập API key (lần đầu)

Vào Pi rồi gõ `/login` → chọn provider (vd `deepseek`) → dán key. Key lưu ở `auth.json` **trong thư mục repo** (đã `.gitignore`, không bị push).

Hoặc dùng biến môi trường (không lưu file):
```bash
DEEPSEEK_API_KEY=sk-... ./run.sh      # DeepSeek
OPENAI_API_KEY=sk-...   ./run.sh      # OpenAI
```

## 4. Điền form

Giữ nguyên form mẫu (merge ô, màu, công thức) và chỉ điền giá trị vào ô cần thiết:

```json
{ "Sheet1": { "B2": "Tran Bach Thang", "B3": "07/10/2026", "C5": 4 } }
```

```bash
python scripts/excel_assistant.py fill template.xlsx data.json filled.xlsx
```

> Điền form từ **ảnh**: dùng skill `image-reader` (OCR) lấy text + toạ độ, suy bố cục, rồi `fill`.
> Có file `.xlsx` gốc thì khớp 100%; chỉ có ảnh thì form dựng lại tương đương (không khớp pixel).

## 4b. Pipeline chất lượng (5 agent)

Repo có 5 agent trong `.pi/agents/` để giữ chất lượng khi việc nhiều bước:

```
excel-planner → excel-critic (≥8/10) → excel-worker → excel-verifier (≥8/10)
```

- **Không bịa dữ liệu**: `excel-critic` chấm 0 điểm mục "đúng dữ liệu" nếu có giá trị đoán.
- **Giữ form**: kiểm merge/màu/công thức còn nguyên.
- **Bắt buộc verify**: `excel-verifier` đọc lại file thật trước khi báo xong.
- Phân tầng: việc nhỏ (đọc 1 file/sửa 1 ô) làm thẳng; việc vừa/lớn mới chạy pipeline.
- Gọi agent: tool `subagent` với `agentScope: "both"`. Lịch sử: `.pi/agents/MEMORY.md`.

## 5. Ví dụ có sẵn (`examples/`)

| File | Là gì |
|---|---|
| `cong_viec_template.xlsx` | Form mẫu "Bảng theo dõi công việc tuần" |
| `cong_viec_data.json` | Dữ liệu mock để test điền |
| `cong_viec_filled.xlsx` | Kết quả điền thử |
| `cong_viec_1000.xlsx` | Bảng **1000 dòng** để test hiệu năng |

## 6. Cấu trúc

```text
excel-assistant/
├── run.cmd / run.sh                 # chạy như Pi riêng (set PI_CODING_AGENT_DIR)
├── AGENTS.md                        # persona + pipeline agent
├── .pi/agents/                      # 5 agent Excel (planner/critic/worker/verifier/orchestrator)
├── extensions/subagent/             # tool `subagent` để gọi các agent trên
├── settings.json                    # config dir (skills)
├── package.json                     # manifest cho `pi install`
├── skills/excel-manager/
│   ├── SKILL.md                     # playbook
│   └── scripts/excel_assistant.py
├── examples/
├── requirements.txt
└── LICENSE (MIT)
```

## Phạm vi

| Làm được | Không làm |
|---|---|
| Đọc/ghi `.xlsx`, nhiều sheet | Tính lại công thức (openpyxl không tính) |
| Điền giá trị theo địa chỉ ô (giữ form) | Macro VBA |
| Điền từ ảnh qua OCR | File `.xls` cũ → đổi `.xlsx` trước |
| Format bảng, CSV ↔ XLSX, tối ưu dung lượng | |

MIT License.
