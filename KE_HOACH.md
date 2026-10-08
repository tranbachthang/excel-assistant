# KẾ HOẠCH — excel-assistant (từ ghi chú tay của Thăng, 08/10/2026)

> Nguồn: ảnh chụp ghi chú viết tay. Chỗ nào đọc không chắc có ghi `(?)` — Thăng xác nhận lại.

## 1. CV1 — Chấm công

| Yêu cầu | Trạng thái |
|---|---|
| Lịch theo khoảng: từ ngày … → ngày … | `chamcong.py --tu/--den` ✅ có |
| 2 thiết bị chấm công **trùng giờ** → dữ liệu bị **chia 2 cột** → **gom về 1** | `chamcong.py` gom 2 dòng cùng ngày ✅ có |
| Tổng giờ / Tổng phút (tính lại từ Vào→Ra) | ✅ có |
| **Quên chấm công** → tô **VÀNG** + ghi chú | ✅ có ("Quên chấm công vào/ra") |
| **Không chấm công** → tô **ĐỎ** | ✅ có ("Không chấm công", T2–T6) |
| Ngày nghỉ lễ loại khỏi diện "không chấm công" | `--nghi DD/MM/YYYY,...` ✅ có |
| **Thông báo cho nhân viên quên chấm công** (Thăng bổ sung 08/10) | ❌ **chưa làm** |
| Lịch "từ ngày … → ngày …" — người dùng **điền rồi xoá** | ⚠️ có `--tu/--den` nhưng **chưa có chỗ điền/xoá trong file** |

> **Chốt 08/10:** Thăng nói **KHÔNG cần cột Thiết bị** → bỏ yêu cầu này.

### Đã test trên file thật (08/10/2026)

Nguồn: `C:\Users\thang\Downloads\` — 3 file Excel là dữ liệu thật. (`ceh.pdf` là **chứng chỉ CEH của Thăng** — không liên quan app, **không đụng tới**.)

| File | Kết quả test |
|---|---|
| `741046_NguyenThienNhan_export TimeSheet-Sep2026.xlsx` | `chamcong.py` → 20 dòng; **2 VÀNG** (16/09 thiếu Vào, 21/09 thiếu Ra) |
| `IToutsource_export_TimeSheet-Sep2026.xlsx` | `chamcong.py` → 4 nhân viên (741046–741049), mỗi người 20 dòng |
| `TheoDoiKho-Sep2026.xlsx` | `theodoikho.py --den 05/09/2026` → tạo `03-09`/`04-09`/`05-09`, nối tồn kho OK |
| timesheet + `--tu 01/09/2026 --den 30/09/2026` | 22 dòng; **2 ĐỎ** (01/09, 02/09 "Không chấm công") → **đỏ hoạt động** |

**Phát hiện cần chốt:** mặc định khoảng ngày = **min/max ngày CÓ dữ liệu**. File ghi "Từ 01/09 đến 01/10" nhưng dữ liệu bắt đầu 03/09 → **không tự sinh** dòng đỏ cho 01–02/09. Muốn đủ phải truyền `--tu`/`--den`.

## 2. CV2 — Theo dõi kho

| Yêu cầu | Trạng thái |
|---|---|
| Có mẫu cũ (`01-09`) → **tự động tạo các ngày sau** | `theodoikho.py` ✅ có |
| Tạo thêm 1 sheet cập nhật ngày (copy từ sheet trước) | ✅ có (nối "Tồn đầu ngày" ← "Tồn cuối ngày" sheet trước) |

## 3. Giao diện cho người dùng — **muốn giống Claude / Gemini** (việc số 3)

Yêu cầu: giao diện **chat** giống Claude/Gemini (khung chat + ô nhập dưới + lịch sử bên trái),
**highlight rõ** chỗ cần người dùng biết (ví dụ ô thiết bị lệch máy).

Hiện có: `menu.py` — **menu chữ** (1 chấm công · 2 theo dõi kho · 3 xem file · 0 thoát), chưa phải GUI.

**Phương án đề xuất (nhẹ nhất, không cần build .exe):**
- Web app **chạy local**: Python server nhỏ + 1 trang HTML/CSS/JS.
- Backend gọi `pi --mode rpc` (giữ hội thoại, có sẵn) — giống cách `pi_daemon.js` đang dùng.
- Mở bằng browser: `http://127.0.0.1:<port>` → giao diện chat như Claude.
- Highlight: ô/bảng có màu (vàng = quên chấm công, đỏ = không chấm công, cam = thiết bị lệch).

## 4. Bản phân phối cho người dùng thường (không phải lập trình viên)

| Việc | Trạng thái |
|---|---|
| Từ PC người dùng bình thường, công cụ/lệnh để chạy tải | ✅ **XONG** (Thăng chốt 08/10) |
| `CaiDat.bat` — cài Node/Git/Python + openpyxl + OCR + pi, 1 lần | ✅ có |
| `ChayAI.bat` — mở trợ lý | ✅ có (chưa "gọn gàng" — chờ làm rõ) |
| Bản phải có **giao diện** | ❌ chưa → xem mục 3 |
| Xuất KQ (mở file, phần làm việc để làm xong) | ⚠️ một phần (mở bằng Excel có) |
| **`GoCaiDat.bat` — gỡ cài đặt** (1 file .bat, xoá hết phần mềm đã cài) | ❌ **chưa làm** |

**"Làm từ đây" (Thăng chốt 08/10):** Chạy AI → giao diện → xuất KQ → gỡ cài đặt.

Ghi chú từ ảnh: *"từ PC (người dùng bình thường, không phải lập trình viên, thiếu công cụ) →
đưa ra các công cụ/lệnh để chạy; sau khi cài xong thì chạy AI; bản phải có giao diện →
xuất ra kết quả (mở file, phần làm việc để làm xong); tạo thêm 1 phần gỡ cài đặt
(1 file .bat để xoá hết các phần mềm đã cài)."*

## Chỗ cần Thăng xác nhận

1. "Ghi chú chấm công" → ghi vào **cột `Ghi chú`** (đang có) hay **comment ô**?
2. Giao diện **web local** (mở bằng browser) — **OK không**, hay cần app desktop (.exe)?
3. Khoảng ngày chấm công mặc định: lấy **min/max dữ liệu** (hiện tại) hay lấy theo **dòng "Từ ngày … đến ngày …"** trong header file?

## Việc làm tiếp (đề xuất thứ tự)

1. **`GoCaiDat.bat`** — gỡ sạch những gì `CaiDat.bat` đã cài (có xác nhận, không phá máy đã có sẵn).
2. `chamcong.py`: thêm **dòng "Từ ngày … đến ngày …" điền được + xoá được** trong file xuất.
3. `chamcong.py`: **thông báo nhân viên quên chấm công**.
4. **Giao diện chat giống Claude/Gemini** (web local + `pi --mode rpc`) — thay/thêm cho `menu.py`.
