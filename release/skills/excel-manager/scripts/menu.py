#!/usr/bin/env python3
"""menu.py - Giao dien don gian cho nguoi dung cuoi (dong goi thanh .exe).

Chay:  python menu.py   (hoac double-click file CongCuExcel.exe sau khi dong goi)
Chon chuc nang roi nhap theo huong dan. Co hop thoai chon file neu de trong.
"""
import os
import sys

# Hien thi tieng Viet an toan tren console Windows
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _chay(module_name, args):
    """Goi truc tiep module (khong can Python ngoai, chay duoc trong .exe)."""
    sys.argv = [module_name] + args
    try:
        if module_name == "chamcong":
            import chamcong
            chamcong.main()
        elif module_name == "theodoikho":
            import theodoikho
            theodoikho.main()
        elif module_name == "excel_assistant":
            import excel_assistant
            excel_assistant.main()
    except SystemExit:
        pass  # cac script dung sys.exit() -> khong lam menu thoat
    print()


def chon_file():
    """Mo hop thoai chon file Excel (tkinter). Tra ve '' neu nguoi dung huy."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        f = filedialog.askopenfilename(
            title="Chon file Excel",
            filetypes=[("File Excel", "*.xlsx"), ("Tat ca", "*.*")],
        )
        root.destroy()
        return f or ""
    except Exception:
        return ""


def hoi(msg, mac_dinh=""):
    s = input(msg + (f" [{mac_dinh}]" if mac_dinh else "") + ": ").strip()
    return s if s else mac_dinh


def hoi_file(msg):
    """Hoi duong dan file; neu de trong -> mo hop thoai chon file."""
    s = input(msg + " (Enter = chon bang hop thoai): ").strip()
    if not s:
        s = chon_file()
    return s


def menu_chamcong():
    print("\n===== 1. XU LY CHAM CONG =====")
    file = hoi_file("File cham cong (raw)")
    if not file or not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    ma = hoi("Ma nhan vien (de trong = xu ly tat ca)", "")
    tu = hoi("Tu ngay DD/MM/YYYY (de trong = tu dong)", "")
    den = hoi("Den ngay DD/MM/YYYY (de trong = tu dong)", "")
    nghi = hoi("Ngay nghi le (VD: 01/09/2026,02/09/2026)", "")
    out = hoi("File xuat (de trong = <ten>_da_xu_ly.xlsx)", "")

    args = [file]
    if ma:
        args += ["--ma", ma]
    if tu:
        args += ["--tu", tu]
    if den:
        args += ["--den", den]
    if nghi:
        args += ["--nghi", nghi]
    if out:
        args += ["--out", out]
    _chay("chamcong", args)


def menu_kho():
    print("\n===== 2. THEO DOI KHO =====")
    file = hoi_file("File theo doi kho")
    if not file or not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    den = hoi("Tao den ngay DD/MM/YYYY (de trong = them 1 ngay)", "")
    out = hoi("File xuat (de trong = ghi de file goc)", "")

    args = [file]
    if den:
        args += ["--den", den]
    if out:
        args += ["--out", out]
    _chay("theodoikho", args)


def menu_doc():
    print("\n===== 3. XEM NOI DUNG FILE =====")
    file = hoi_file("File .xlsx can xem")
    if not file or not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    sheet = hoi("Ten sheet (de trong = sheet dau)", "")
    args = ["read", file]
    if sheet:
        args += ["--sheet", sheet]
    _chay("excel_assistant", args)


def main():
    while True:
        print("\n" + "=" * 46)
        print("  CONG CU QUAN LY EXCEL - MENU CHINH")
        print("=" * 46)
        print("  1. Xu ly cham cong (gom + tinh gio + vang/do)")
        print("  2. Theo doi kho (tu tao sheet ngay)")
        print("  3. Xem noi dung file Excel")
        print("  0. Thoat")
        print("-" * 46)
        try:
            chon = input("  Chon [0-3]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTam biet!")
            break
        if chon == "1":
            menu_chamcong()
        elif chon == "2":
            menu_kho()
        elif chon == "3":
            menu_doc()
        elif chon == "0":
            print("Tam biet!")
            break
        else:
            print("[!] Chon khong hop le.")


if __name__ == "__main__":
    main()
