#!/usr/bin/env python3
"""menu.py - Giao dien don gian cho nguoi dung (khong can nho lenh).

Chay:  python menu.py
Chon chuc nang roi nhap theo huong dan.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(script, *args):
    cmd = [PY, os.path.join(HERE, script)] + list(args)
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(cmd, env=env)
    print()
    return r.returncode


def hoi(msg, mac_dinh=""):
    s = input(msg + (f" [{mac_dinh}]" if mac_dinh else "") + ": ").strip()
    return s if s else mac_dinh


def menu_chamcong():
    print("\n===== 1. XU LY CHAM CONG =====")
    file = hoi("Duong dan file cham cong (raw)", "data/chamcong_raw.xlsx")
    if not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    ma = hoi("Ma nhan vien (de trong = xu ly tat ca)", "")
    tu = hoi("Tu ngay DD/MM/YYYY (de trong = tu dong)", "")
    den = hoi("Den ngay DD/MM/YYYY (de trong = tu dong)", "")
    nghi = hoi("Ngay nghi le (VD: 01/09/2026,02/09/2026)", "")
    out = hoi("File xuat", os.path.splitext(file)[0] + "_da_xu_ly.xlsx")

    args = [file]
    if ma:
        args += ["--ma", ma]
    if tu:
        args += ["--tu", tu]
    if den:
        args += ["--den", den]
    if nghi:
        args += ["--nghi", nghi]
    args += ["--out", out]
    run("chamcong.py", *args)


def menu_kho():
    print("\n===== 2. THEO DOI KHO =====")
    file = hoi("Duong dan file theo doi kho", "data/theodoikho.xlsx")
    if not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    den = hoi("Tao den ngay DD/MM/YYYY (de trong = them 1 ngay)", "")
    out = hoi("File xuat (de trong = ghi de file goc)", "")

    args = [file]
    if den:
        args += ["--den", den]
    if out:
        args += ["--out", out]
    run("theodoikho.py", *args)


def menu_doc():
    print("\n===== 3. XEM NOI DUNG FILE =====")
    file = hoi("Duong dan file .xlsx", "")
    if not os.path.isfile(file):
        print(f"[!] Khong thay file: {file}")
        return
    sheet = hoi("Ten sheet (de trong = sheet dau)", "")
    args = [file]
    if sheet:
        args += ["--sheet", sheet]
    run("excel_assistant.py", "read", *args)


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
        chon = input("  Chon [0-3]: ").strip()
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
