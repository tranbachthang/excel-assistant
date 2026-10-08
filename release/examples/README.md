# examples — file mock để test agent Excel

| File | Là gì |
|---|---|
| `cong_viec_template.xlsx` | **Form mẫu** "Bảng theo dõi công việc tuần" (10 dòng trống để điền) |
| `cong_viec_data.json` | **Dữ liệu mock** (3 dòng) để test điền form |
| `cong_viec_filled.xlsx` | Kết quả điền thử (sinh từ 2 file trên) |

## Test

```bash
cd skills/excel-manager

# 1. Xem cấu trúc
python scripts/excel_assistant.py info ../../examples/cong_viec_template.xlsx

# 2. Điền dữ liệu mock vào form
python scripts/excel_assistant.py fill ../../examples/cong_viec_template.xlsx ../../examples/cong_viec_data.json /tmp/out.xlsx

# 3. Đọc lại kiểm
python scripts/excel_assistant.py read /tmp/out.xlsx --head 6
```

Hoặc nhờ agent (sau khi `pi install`): *"điền dữ liệu trong cong_viec_data.json vào cong_viec_template.xlsx"*.
