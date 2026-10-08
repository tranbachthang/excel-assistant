# 🧠 Hướng dẫn cài "Trợ lý AI quản lý Excel" (AI Agent) — CHI TIẾT

Trợ lý AI này chạy **ngay trên máy bạn**. Bạn **nói chuyện tiếng Việt**, nó tự đọc file Excel,
xử lý chấm công, tạo sổ kho, tính toán...

> Chỉ cần cài **1 lần duy nhất**. Sau đó mỗi ngày chỉ double-click 1 file là dùng.

---

## 0. Chuẩn bị (hỏi Thăng trước)

| Cần gì | Lấy ở đâu |
|---|---|
| **API key** (chìa khóa AI) | Nhờ **Thăng** cấp |
| Mạng internet | có sẵn |
| Trình duyệt (Chrome / Edge / Cốc Cốc) | có sẵn |

---

## Gói này có gì (8 kỹ năng)

| Skill | Chức năng |
|---|---|
| **excel-manager** | Đọc/tạo/sửa/điền form Excel (chính) |
| **image-reader** | Đọc ảnh, OCR trích xuất text |
| **video-reader** | Phân tích video, OCR từng frame |
| **google-docs** | Đọc Google Docs/Sheets/Drive |
| **chat-history** | Lưu & tìm lại lịch sử chat |
| **screen-watch** | Chụp màn hình + OCR |
| **self-check** | Tự kiểm tra kết quả sau mỗi thao tác |
| **session-context** | Nạp ngữ cảnh từ phiên trước |

Toàn bộ kỹ năng **đã nằm sẵn trong thư mục gói** (`skills\`) — không cần tải thêm gì.

---

## BƯỚC 1 — Tải & cài Node.js

**Node.js** là nền tảng để chạy trợ lý AI.

### 1.1 Tải
1. Mở trình duyệt (Chrome, Edge...).
2. Gõ địa chỉ vào thanh địa chỉ: **https://nodejs.org** rồi Enter.
3. Trang hiện ra **2 nút xanh**:
   - Nút **"LTS"** (khuyên dùng — ổn định)
   - Nút "Current" (mới nhất, không cần)
4. **Bấm nút "LTS"** (thường ghi "v22.x.x LTS").
5. Trình duyệt tải file về (file tên kiểu `node-v22.x.x-x64.msi`, thường nằm trong thư mục **Downloads**).

### 1.2 Cài
1. Mở thư mục **Downloads**, **double-click** file `node-v...msi` vừa tải.
2. Cửa sổ cài đặt hiện ra, bấm lần lượt:
   - `Next`
   - Tick vào ô **"I accept the terms..."** → `Next`
   - `Next` (để nguyên thư mục mặc định)
   - `Next` (để nguyên các mục)
   - `Install`
   - Chờ chạy xong → `Finish`
3. Xong. (Không cần làm gì thêm với Node.js.)

---

## BƯỚC 2 — Tải & cài Git for Windows

**Git** giúp trợ lý AI chạy lệnh trên Windows.

1. Mở trình duyệt, vào: **https://git-scm.com/download/win**
2. Trang **tự động tải** file về (nếu không, bấm dòng **"64-bit Git for Windows Setup"**).
3. Mở file vừa tải (trong Downloads), double-click.
4. Bấm **Next → Next → ... → Install → Finish** (để mặc định hết, đừng đổi gì).

---

## BƯỚC 3 — Tải & cài Python

**Python** để chạy các lệnh xử lý Excel.

### 3.1 Tải
1. Mở trình duyệt, vào: **https://www.python.org/downloads/**
2. Bấm nút **vàng "Download Python 3.x.x"**.
3. File tải về thư mục **Downloads**.

### 3.2 Cài (BƯỚC QUAN TRỌNG NHẤT)
1. Double-click file `python-3.x.x-amd64.exe` vừa tải.
2. Ở **màn hình đầu tiên**, nhìn xuống dưới cùng:
   - ☑️ **TICK vào ô "Add Python to PATH"**  ← bắt buộc!
3. Bấm **"Install Now"**.
4. Chờ chạy xong → bấm **"Close"**.

> ⚠️ Nếu quên tick "Add Python to PATH", phải gỡ ra cài lại. Bước này rất quan trọng.

---

## BƯỚC 4 — Mở PowerShell

1. Bấm nút **Start** (góc trái dưới màn hình).
2. Gõ chữ: **PowerShell**
3. Bấm **Enter** (hoặc bấm vào kết quả "Windows PowerShell").
4. Hiện ra 1 cửa sổ **màu xanh dương/đen** có con trỏ nhấp nháy → sẵn sàng gõ lệnh.

---

## BƯỚC 5 — Cài thư viện Excel + OCR (gõ 1 lệnh)

Trong cửa sổ PowerShell, **gõ đúng dòng này** rồi bấm Enter:

```
pip install openpyxl rapidocr-onnxruntime pillow
```

Chờ đến khi thấy chữ **"Successfully installed ..."** là xong.

> 📸 `rapidocr-onnxruntime` là thư viện **đọc chữ trong ảnh (OCR)** — bắt buộc để tính năng "ảnh → Excel" chạy được.
> Nếu muốn đọc tiếng Việt chính xác hơn, gõ thêm (tùy chọn, tải model ~1GB): `pip install easyocr`

---

## BƯỚC 6 — Cài Pi (trợ lý AI) — gõ 1 lệnh

Trong PowerShell, gõ:

```
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

Chờ 1–2 phút. Sau đó kiểm tra:

```
pi --version
```

Nếu hiện ra **số phiên bản** (ví dụ `0.8x.x`) là thành công.

---

## BƯỚC 7 — Mở trợ lý AI (không cần tải kỹ năng)

Trong thư mục gói này có file **`ChayAI.bat`**. **Double-click** nó → trợ lý AI mở ra ngay,
đã tự nạp sẵn **8 kỹ năng** ở bảng trên.

> Nếu muốn để file Excel ở thư mục riêng: **copy cả thư mục gói** vào thư mục đó rồi double-click `ChayAI.bat`.

---

## BƯỚC 8 — Nhập API key (chìa khóa AI)

1. Trong PowerShell, gõ `pi` rồi Enter → màn hình Pi hiện ra.
2. Gõ `/login` rồi Enter.
3. Dùng **mũi tên lên/xuống** chọn **DeepSeek** → Enter.
4. **Dán API key** (chìa khóa Thăng đưa) → Enter.
5. Nếu muốn chọn model, gõ `/model` rồi chọn `deepseek-v4-pro` (hoặc để mặc định).

---

## BƯỚC 9 — Bắt đầu dùng 🎉

1. Bỏ các file Excel vào thư mục gói (hoặc thư mục bạn đã copy gói vào).
2. **Double-click `ChayAI.bat`**.
3. Nói chuyện tiếng Việt, ví dụ:

```
đọc file chamcong_raw.xlsx rồi gom dòng trùng, tính tổng giờ, tô vàng chỗ quên chấm công, tô đỏ chỗ không đi làm
```

```
tạo sổ theo dõi kho từ 03/09 đến 30/09
```

```
tháng này ai nghỉ nhiều nhất?
```

---

## 🔁 Dùng hàng ngày (đơn giản)

**Cách duy nhất (đã đơn giản hóa):** **double-click file `ChayAI.bat`** trong thư mục gói.

Nếu muốn gõ tay trong PowerShell (phải đứng trong thư mục gói):

```
cd <thư mục gói>
set PI_CODING_AGENT_DIR=%CD%\
pi
```

Muốn tiếp tục việc hôm qua:

```
pi --continue
```

---

## ❓ Lỗi thường gặp & cách xử lý

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `pi` báo "không tìm thấy lệnh" | Chưa cài xong bước 6 | Gõ lại lệnh bước 6, chờ xong |
| Trợ lý không biết gì về Excel / thiếu kỹ năng | Chạy `pi` ở thư mục khác (không phải thư mục gói) | Double-click `ChayAI.bat` trong thư mục gói |
| Báo "python không tìm thấy" | Quên tick "Add to PATH" | Gỡ Python, cài lại (bước 3) |
| Báo "không có openpyxl" | Chưa chạy bước 5 | Gõ `pip install openpyxl` |
| Đọc ảnh báo lỗi `rapidocr_onnxruntime` / không OCR | Chưa cài OCR (máy khác) | Gõ `pip install rapidocr-onnxruntime pillow` |
| Không nhớ API key | — | Nhờ Thăng cấp lại |
| Hỏi model không trả lời | Hết tiền/key sai | Kiểm tra lại key ở `/login` |

---

*Cần hỗ trợ: liên hệ Thăng.*
