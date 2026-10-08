#!/usr/bin/env python3
"""chamcong.py - Xu ly file cham cong xuat tu nhieu thiet bi.

Bai toan: nhieu may cham cong lam 1 ngay bi tach thanh 2 dong (1 dong chi co Vao,
1 dong chi co Ra). Can gom ve 1 dong duy nhat, tinh lai tong gio + tong phut,
danh dau loi:
  - Quen cham cong (thieu Vao hoac Ra) -> to VANG.
  - Khong cham cong (ngay lam viec khong co dong nao) -> to DO.

Dung:
  python chamcong.py <file.xlsx> [--ma 741046] [--tu DD/MM/YYYY] [--den DD/MM/YYYY]
      [--nghi DD/MM/YYYY,DD/MM/YYYY] [--out out.xlsx]

  --ma      : ma nhan vien can xu ly (vd 741046). Bo qua -> xu ly TAT CA moi nguoi 1 sheet.
  --tu/--den: khoang ngay lam viec. Mac dinh = min/max ngay co trong du lieu.
  --nghi    : ngay nghi le (loai khoi "khong cham cong"). VD: 01/09/2026,02/09/2026
  --out     : file xuat. Mac dinh: <ten>_da_xu_ly.xlsx

Toi uu: lazy-import openpyxl (--help nhanh), doc read_only=True.
"""
import argparse
import os
import sys
from datetime import date, datetime, time, timedelta

THU = ["T.2", "T.3", "T.4", "T.5", "T.6", "T.7", "CN"]
HEADERS = ["Mã N.Viên", "Tên N.Viên", "Phòng ban", "Chức vụ",
           "Ngày", "Thứ", "Vào", "Ra", "Tổng giờ", "Tổng phút", "Ghi chú"]


# ---------- Parse helper ----------
def parse_date(v):
    """Tra ve datetime.date tu datetime/date/string."""
    if v is None:
        return None
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    s = str(v).strip().split()[0]
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def parse_date_arg(s):
    """Parse 'DD/MM/YYYY' tu tham so CLI."""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            pass
    sys.exit(f"[!] Ngay khong hop le: {s} (dung DD/MM/YYYY)")


def to_minutes(v):
    """Gio (datetime.time / 'HH:MM' / 'HH:MM:SS') -> so phut. None neu rong."""
    if v is None:
        return None
    if isinstance(v, time):
        return v.hour * 60 + v.minute
    if isinstance(v, datetime):
        return v.hour * 60 + v.minute
    s = str(v).strip()
    if not s or s.lower() in ("none", "null", "-"):
        return None
    parts = s.split(":")
    try:
        h = int(float(parts[0]))
        m = int(float(parts[1])) if len(parts) > 1 else 0
        return h * 60 + m
    except (ValueError, IndexError):
        return None


def fmt_hm(mins):
    return "" if mins is None else f"{mins // 60:02d}:{mins % 60:02d}"


# ---------- Doc file ----------
def find_header_row(ws):
    """Tim dong header chua cot Vao/Ra/Ngay."""
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        vals = [str(v) if v is not None else "" for v in row]
        if any("Vào" in v or "Vao" in v for v in vals) and \
           any("Ra" in v for v in vals) and \
           any("Ngày" in v or "Ngay" in v for v in vals):
            return i, row
    return None, None


def col_index(header_row, *names):
    """Tim chi so cot (0-based) theo ten cot, so sanh khong dau/khoang trang."""
    def norm(s):
        s = str(s).lower()
        for a, b in (("á", "a"), ("à", "a"), ("ả", "a"), ("ã", "a"), ("ạ", "a"),
                     ("ă", "a"), ("ắ", "a"), ("ằ", "a"), ("ẳ", "a"), ("ẵ", "a"),
                     ("ặ", "a"), ("â", "a"), ("ấ", "a"), ("ầ", "a"), ("ẩ", "a"),
                     ("ẫ", "a"), ("ậ", "a"), ("é", "e"), ("è", "e"), ("ẻ", "e"),
                     ("ẽ", "e"), ("ẹ", "e"), ("ê", "e"), ("ế", "e"), ("ề", "e"),
                     ("ể", "e"), ("ễ", "e"), ("ệ", "e"), ("í", "i"), ("ì", "i"),
                     ("ỉ", "i"), ("ĩ", "i"), ("ị", "i"), ("ó", "o"), ("ò", "o"),
                     ("ỏ", "o"), ("õ", "o"), ("ọ", "o"), ("ô", "o"), ("ố", "o"),
                     ("ồ", "o"), ("ổ", "o"), ("ỗ", "o"), ("ộ", "o"), ("ơ", "o"),
                     ("ớ", "o"), ("ờ", "o"), ("ở", "o"), ("ỡ", "o"), ("ợ", "o"),
                     ("ú", "u"), ("ù", "u"), ("ủ", "u"), ("ũ", "u"), ("ụ", "u"),
                     ("ư", "u"), ("ứ", "u"), ("ừ", "u"), ("ử", "u"), ("ữ", "u"),
                     ("ự", "u"), ("ý", "y"), ("ỳ", "y"), ("ỷ", "y"), ("ỹ", "y"),
                     ("ỵ", "y"), ("đ", "d")):
            s = s.replace(a, b)
        return s.replace(" ", "").replace(".", "")

    wanted = [norm(n) for n in names]
    for j, h in enumerate(header_row):
        if norm(h) in wanted:
            return j
    return None


def read_rows(path):
    """Doc file cham cong -> dict {ma: [(ngay, vao_min, ra_min, ten, phong, chucvu, thu)]}"""
    from openpyxl import load_workbook  # lazy import

    wb = load_workbook(path, read_only=True)
    ws = wb.active
    hrow, header = find_header_row(ws)
    if hrow is None:
        wb.close()
        sys.exit("[!] Khong tim thay dong header (Vao/Ra/Ngay) trong file.")

    j_ma = col_index(header, "Mã N.Viên", "Mã NV", "Ma NV", "Mã NViên", "Ma")
    j_ten = col_index(header, "Tên N.Viên", "Tên NV", "Họ tên", "Ten")
    j_phong = col_index(header, "Phòng ban", "Phong ban", "Bộ phận")
    j_cv = col_index(header, "Chức vụ", "Chuc vu")
    j_ngay = col_index(header, "Ngày", "Ngay")
    j_thu = col_index(header, "Thứ", "Thu")
    j_vao = col_index(header, "Vào", "Vao", "Giờ vào", "Gio vao")
    j_ra = col_index(header, "Ra", "Giờ ra", "Gio ra")

    data = {}
    order = []
    for row in ws.iter_rows(min_row=hrow + 1, values_only=True):
        if all(v is None or str(v).strip() == "" for v in row):
            continue
        ma = str(row[j_ma]).strip() if j_ma is not None and row[j_ma] is not None else "?"
        ngay = parse_date(row[j_ngay]) if j_ngay is not None else None
        if ngay is None:
            continue
        vao = to_minutes(row[j_vao]) if j_vao is not None else None
        ra = to_minutes(row[j_ra]) if j_ra is not None else None
        ten = row[j_ten] if j_ten is not None else ""
        phong = row[j_phong] if j_phong is not None else ""
        cv = row[j_cv] if j_cv is not None else ""
        thu = str(row[j_thu]).strip() if j_thu is not None and row[j_thu] is not None else THU[ngay.weekday()]
        rec = {"ngay": ngay, "vao": vao, "ra": ra, "ten": ten,
               "phong": phong, "cv": cv, "thu": thu}
        data.setdefault(ma, []).append(rec)
        if ma not in order:
            order.append(ma)
    wb.close()
    return data, order


def gom_ngay(records):
    """Gop cac dong cung ngay -> 1 dong (lay Vao som nhat, Ra tre nhat)."""
    by_day = {}
    for r in records:
        d = r["ngay"]
        cur = by_day.get(d)
        if cur is None:
            by_day[d] = {"ngay": d, "vao": r["vao"], "ra": r["ra"], "ten": r["ten"],
                         "phong": r["phong"], "cv": r["cv"], "thu": r["thu"]}
        else:
            if cur["ten"] in (None, ""):
                cur["ten"] = r["ten"]
            if cur["phong"] in (None, ""):
                cur["phong"] = r["phong"]
            if cur["cv"] in (None, ""):
                cur["cv"] = r["cv"]
            if r["vao"] is not None and (cur["vao"] is None or r["vao"] < cur["vao"]):
                cur["vao"] = r["vao"]
            if r["ra"] is not None and (cur["ra"] is None or r["ra"] > cur["ra"]):
                cur["ra"] = r["ra"]
    return sorted(by_day.values(), key=lambda x: x["ngay"])


def working_days(from_date, to_date, holidays):
    """Danh sach ngay lam viec (T2-T6, tru ngay nghi)."""
    days = []
    d = from_date
    while d <= to_date:
        if d.weekday() < 5 and d not in holidays:  # T2..T6
            days.append(d)
        d += timedelta(days=1)
    return days


def xay_dong(ma, rec, holidays):
    """Tra ve list cac dong xuat cho 1 nhan vien, danh dau vang/do."""
    rows = []
    gop = {r["ngay"]: r for r in gom_ngay(rec)}
    if not gop:
        return rows
    from_date = min(gop)
    to_date = max(gop)
    for d in working_days(from_date, to_date, holidays):
        r = gop.get(d)
        if r is None:
            rows.append({"ma": ma, "ten": "", "phong": "", "cv": "", "ngay": d,
                         "thu": THU[d.weekday()], "vao": None, "ra": None,
                         "gio": None, "phut": None, "ghichu": "Không chấm công",
                         "mau": "red"})
            continue
        vao, ra = r["vao"], r["ra"]
        ghichu, mau = "", "normal"
        gio, phut = None, None
        if vao is not None and ra is not None:
            phut = ra - vao
            gio = fmt_hm(phut)
        elif vao is None and ra is not None:
            ghichu, mau = "Quên chấm công vào", "yellow"
        elif vao is not None and ra is None:
            ghichu, mau = "Quên chấm công ra", "yellow"
        else:
            ghichu, mau = "Không chấm công", "red"
        rows.append({"ma": ma, "ten": r["ten"], "phong": r["phong"], "cv": r["cv"],
                     "ngay": d, "thu": THU[d.weekday()], "vao": vao, "ra": ra,
                     "gio": gio, "phut": phut, "ghichu": ghichu, "mau": mau})
    return rows


# ---------- Xuat file ----------
def write_sheet(ws, ma, rows):
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # lazy import

    THIN = Side(style="thin", color="999999")
    BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
    HEADER_FILL = PatternFill("solid", fgColor="D9E1F2")
    YELLOW = PatternFill("solid", fgColor="FFF200")
    RED = PatternFill("solid", fgColor="FF0000")
    RED_FONT = Font(color="FFFFFF", bold=True)
    CENTER = Alignment(horizontal="center", vertical="center")
    LEFT = Alignment(horizontal="left", vertical="center")

    ws.append(HEADERS)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = HEADER_FILL
        c.border = BORDER
        c.alignment = CENTER
    ws.freeze_panes = "A2"

    for r in rows:
        ws.append([r["ma"], r["ten"], r["phong"], r["cv"],
                   r["ngay"].strftime("%d/%m/%Y"), r["thu"],
                   fmt_hm(r["vao"]), fmt_hm(r["ra"]),
                   r["gio"] or "", r["phut"] if r["phut"] is not None else "",
                   r["ghichu"]])
        rr = ws.max_row
        for j in range(1, len(HEADERS) + 1):
            c = ws.cell(row=rr, column=j)
            c.border = BORDER
            c.alignment = CENTER if j in (1, 5, 6, 7, 8, 9, 10) else LEFT
        if r["mau"] == "yellow":
            for j in range(1, len(HEADERS) + 1):
                ws.cell(row=rr, column=j).fill = YELLOW
        elif r["mau"] == "red":
            for j in range(1, len(HEADERS) + 1):
                ws.cell(row=rr, column=j).fill = RED
                ws.cell(row=rr, column=j).font = RED_FONT

    # Tong cong gio/phut (chi tinh dong du lieu day du)
    tong_phut = sum(r["phut"] for r in rows if r["phut"] is not None)
    ws.append(["", "", "", "", "", "", "", "TỔNG", fmt_hm(tong_phut), tong_phut, ""])
    tr = ws.max_row
    for j in range(1, len(HEADERS) + 1):
        ws.cell(row=tr, column=j).font = Font(bold=True)
        ws.cell(row=tr, column=j).border = BORDER

    # Legend
    ws.append([])
    ws.append(["", "Chú thích:", "Vàng = quên chấm công (thiếu vào/ra)", "", "", "", "", "", "", ""])
    ws.append(["", "", "Đỏ = không chấm công (không đi làm)", "", "", "", "", "", "", ""])
    ws.cell(row=ws.max_row - 1, column=3).fill = YELLOW
    ws.cell(row=ws.max_row, column=3).fill = RED
    ws.cell(row=ws.max_row, column=3).font = RED_FONT

    from openpyxl.utils import get_column_letter  # lazy import
    widths = [11, 18, 14, 12, 12, 6, 8, 8, 10, 10, 22]
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w


def main():
    p = argparse.ArgumentParser(description="Gom va xu ly file cham cong nhieu thiet bi")
    p.add_argument("file", help="File .xlsx cham cong (raw)")
    p.add_argument("--ma", help="Ma nhan vien (vd 741046). Bo qua -> xu ly tat ca")
    p.add_argument("--tu", help="Tu ngay DD/MM/YYYY")
    p.add_argument("--den", help="Den ngay DD/MM/YYYY")
    p.add_argument("--nghi", help="Ngay nghi le, phan cach boi phay: 01/09/2026,02/09/2026")
    p.add_argument("--out", help="File xuat (mac dinh <ten>_da_xu_ly.xlsx)")
    a = p.parse_args()

    if not os.path.isfile(a.file):
        sys.exit(f"[!] Khong thay file: {a.file}")

    data, order = read_rows(a.file)
    if not data:
        sys.exit("[!] Khong doc duoc du lieu cham cong.")

    holidays = set()
    if a.nghi:
        for s in a.nghi.split(","):
            s = s.strip()
            if s:
                holidays.add(parse_date_arg(s))

    from_override = parse_date_arg(a.tu) if a.tu else None
    to_override = parse_date_arg(a.den) if a.den else None

    from openpyxl import Workbook  # lazy import
    wb = Workbook()
    wb.remove(wb.active)
    masks = [a.ma] if a.ma else order
    total_sheets = 0

    for ma in masks:
        if ma not in data:
            print(f"[!] Bo qua ma khong co trong du lieu: {ma}")
            continue
        rec = data[ma]
        if from_override and to_override:
            rec = [r for r in rec if from_override <= r["ngay"] <= to_override]
            if not rec:
                print(f"[!] Ma {ma} khong co du lieu trong khoang {a.tu} -> {a.den}")
                continue
        rows = xay_dong(ma, rec, holidays)
        if from_override and to_override:
            gop = {r["ngay"] for r in rows}
            extra = []
            for d in working_days(from_override, to_override, holidays):
                if d not in gop:
                    extra.append({"ma": ma, "ten": "", "phong": "", "cv": "", "ngay": d,
                                  "thu": THU[d.weekday()], "vao": None, "ra": None,
                                  "gio": None, "phut": None, "ghichu": "Không chấm công",
                                  "mau": "red"})
            rows = sorted(rows + extra, key=lambda x: x["ngay"])

        ws = wb.create_sheet(title=str(ma)[:31])
        write_sheet(ws, ma, rows)
        total_sheets += 1
        print(f"[*] Ma {ma}: {len(rows)} dong (gom xong)")

    if total_sheets == 0:
        sys.exit("[!] Khong co sheet nao duoc tao.")

    out = a.out or os.path.splitext(a.file)[0] + "_da_xu_ly.xlsx"
    wb.save(out)
    print(f"OK -> {os.path.abspath(out)}")


if __name__ == "__main__":
    main()
