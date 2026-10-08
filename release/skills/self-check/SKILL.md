---
name: self-check
description: Tự kiểm tra kết quả sau mỗi thao tác. Xác nhận file đã tạo, VM đã thêm, build thành công, service đang chạy. Dùng sau mỗi lần AI thực hiện 1 hành động.
metadata:
  version: 1.0.0
  purpose: "Tự kiểm tra kết quả sau mỗi thao tác. Xác nhận file đã tạo, VM đã thêm, build thành công, service đang chạy. Dùng sau mỗi lần AI thực hiện"
  allowed-tools: bash, http_request
  dependencies: "~/AppData/Roaming/VMware/inventory.vmls"
  tests: "file_exists:~/AppData/Roaming/VMware/inventory.vmls"
  triggers: "kiểm, tra, kết, quả, sau, mỗi"
---

# Self-Check — Tự xác minh kết quả

## Nguyên tắc

SAU MỖI THAO TÁC (tạo file, chạy lệnh, cài đặt, build), AI PHẢI:
1. Chạy 1 lệnh xác minh kết quả
2. Báo cáo: ✅ thành công hay ❌ thất bại
3. Nếu thất bại → thử cách khác, không dừng

## Các mẫu xác minh

### File đã tạo chưa?
```bash
ls -la "đường_dẫn_file" && echo "✅ FILE EXISTS" || echo "❌ FILE MISSING"
```

### File đã có nội dung?
```bash
wc -l "đường_dẫn_file" && head -3 "đường_dẫn_file"
```

### VM đã có trong VMware?
```bash
cat "~/AppData/Roaming/VMware/inventory.vmls" | grep -c "DisplayName"
```

### Service/process đang chạy?
```bash
curl -s http://localhost:PORT/health && echo "✅ RUNNING" || echo "❌ NOT RUNNING"
```

### Build C code thành công?
```bash
ls -la "output.exe" && file "output.exe" && echo "✅ BUILD OK" || echo "❌ BUILD FAIL"
```

### Python script chạy được?
```bash
python -c "import tên_thư_viện; print('✅ IMPORT OK')" 2>&1
```

### Network ping được?
```bash
ping -n 1 IP && echo "✅ PING OK" || echo "❌ NO PING"
```

## Quy trình bắt buộc

```
AI làm gì đó (tạo file, cài đặt, build...)
    │
    ▼
AI TỰ ĐỘNG chạy lệnh verify
    │
    ├── OK → chấm điểm chất lượng (thang 10) → chỉ đưa user khi ≥ 9.5/10
    │
    └── FAIL → báo "❌ Thất bại ở bước X. Đang thử cách khác..."
               → Tự sửa, không hỏi user
```

## 🎯 Quality Gate — thang điểm 10 (chỉ ≥9.5/10 mới duyệt)

Mọi output đưa cho Thăng (design, code, báo cáo, dashboard) PHẢI tự chấm trước:

| Điểm | Nghĩa |
|------|-------|
| 9.5–10 | ✅ Xuất sắc — đưa cho Thăng xem |
| 8–9.4 | ⚠️ Khá nhưng còn thiếu → tự sửa tiếp, KHÔNG đưa vội |
| <8 | ❌ Chưa đạt → làm lại |

### Tiêu chí chấm (mỗi mục 0–2 điểm, tổng 10)
1. **Đúng yêu cầu** — làm đúng thứ Thăng nhờ (2đ)
2. **Hoạt động thật** — đã verify chạy được, không lỗi (2đ)
3. **Đẹp/sạch** — thẩm mỹ, bố cục, không rác (2đ)
4. **Đầy đủ** — không thiếu tính năng đã hứa (2đ)
5. **Tối giản** — không thừa, không over-engineer (2đ)

### Cách chấm
- Tự chấm trung thực, không tự nâng điểm.
- Chưa chắc đẹp → nhờ AI khác chấm (skill `design-review`) rồi lấy điểm đó.
- **<9.5 → tự sửa, không hỏi Thăng.** Chỉ hỏi khi hết hướng hoặc tốn token gần ngân sách.

## Changelog
- 1.0.0 (2026-09-29): chuẩn hoá metadata module (auto-stamp: version/purpose/allowed-tools/dependencies/tests/triggers).
