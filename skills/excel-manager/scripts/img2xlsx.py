#!/usr/bin/env python3
"""img2xlsx.py - 1 lenh: anh (screenshot bang) -> file Excel co format san.

Toi uu quy trinh "quet + tao" xuong con 1 cau lenh:
  python img2xlsx.py <anh.png> [out.xlsx]

Cach hoat dong:
  1. OCR bang RapidOCR (~1s, co toa do).
  2. Gom text thanh hang (theo y) -> cot (theo x cua header).
  3. Dung bang .xlsx: title merge, header dam + nen + vien, auto-width, freeze.

Khuyen dung: python scripts/img2xlsx.py --help
"""
import os
import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

THIN = Side(style="thin", color="000000")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor="D9E1F2")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def ocr_boxes(image_path):
    """Tra ve list (x_center, y_center, width, height, text)."""
    try:
        from rapidocr_onnxruntime import RapidOCR
        engine = RapidOCR()
        result, _ = engine(image_path)
    except Exception as e:
        sys.exit(f"[!] OCR loi: {e}")
    if not result:
        sys.exit("[!] Khong doc duoc text tu anh.")

    boxes = []
    for box, text, _ in result:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if not text.strip():
            continue
        boxes.append(((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0, text.strip()))
    return boxes


def cluster_rows(boxes, tol_ratio=0.55):
    """Gom box thanh cac hang theo toa do y."""
    boxes = sorted(boxes, key=lambda b: b[1])  # theo y_center
    heights = [b[3] for b in boxes if b[3] > 0]
    med_h = sorted(heights)[len(heights) // 2] if heights else 20
    tol = med_h * tol_ratio

    rows = []
    for b in boxes:
        if rows and abs(b[1] - rows[-1][0][1]) <= tol:
            rows[-1].append(b)
        else:
            rows.append([b])
    # sap xep moi hang theo x
    return [sorted(r, key=lambda b: b[0]) for r in rows]


def build(path, out):
    boxes = ocr_boxes(path)
    rows = cluster_rows(boxes)

    # Bo cac box "nhiem" nho (chu cai cot A/B/E/G...): cao < 18 va nam le loi
    rows = [r for r in rows if r]

    # Row nhieu o nhat -> header; tim chi so cua no
    def ncell(r):
        return len(r)

    # Loai cac hang chi chua box rat nho (chieu rong < 20) - nhieu
    clean = []
    for r in rows:
        r = [b for b in r if b[2] >= 20]
        if r:
            clean.append(r)
    rows = clean

    # Tim header = hang co nhieu o nhat (sau hang title)
    header_idx = max(range(len(rows)), key=lambda i: ncell(rows[i]))
    header = rows[header_idx]
    ncol = len(header)

    wb = Workbook()
    ws = wb.active
    ws.title = "Bang"

    r_out = 1
    # Cac hang truoc header: title + nhan -> merge het chieu rong, dam
    for i in range(header_idx):
        r = rows[i]
        txt = " ".join(b[4] for b in r)
        ws.merge_cells(start_row=r_out, start_column=1, end_row=r_out, end_column=ncol)
        c = ws.cell(row=r_out, column=1, value=txt)
        c.font = Font(bold=True, size=16 if i == 0 else 11)
        c.alignment = CENTER if i == 0 else LEFT
        r_out += 1

    # Header
    for j, b in enumerate(header, 1):
        c = ws.cell(row=r_out, column=j, value=b[4])
        c.font = Font(bold=True)
        c.alignment = CENTER
        c.fill = HEADER_FILL
        c.border = BORDER
    header_row = r_out
    r_out += 1

    # Du lieu: gan moi box vao cot gan nhat (theo x_center cua header)
    anchors = [b[0] for b in header]
    for i in range(header_idx + 1, len(rows)):
        for b in rows[i]:
            j = min(range(ncol), key=lambda k: abs(b[0] - anchors[k]))
            c = ws.cell(row=r_out, column=j + 1, value=b[4])
            c.border = BORDER
            c.alignment = CENTER if j in (0, 1, 4, 5) else LEFT
        r_out += 1

    # Do rong cot tuong doi theo header
    for j in range(1, ncol + 1):
        w = max(len(str(header[j - 1][4])) + 4, 12)
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(row=header_row + 1, column=1).coordinate

    wb.save(out)
    print("OK ->", os.path.abspath(out))
    print(f"[*] {ncol} cot, {r_out - header_row - 1} dong du lieu.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python img2xlsx.py <anh.png> [out.xlsx]")
        sys.exit(1)
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + ".xlsx"
    if not os.path.exists(src):
        sys.exit(f"[!] Khong thay anh: {src}")
    build(src, out)
