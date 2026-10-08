#!/usr/bin/env python3
"""
screen_watch.py — Chup man hinh + OCR, tra ve text mo ta cho AI agent text-only.

Cai dat tren Windows (PowerShell):
    pip install mss pytesseract pillow
    # Tesseract OCR engine (khong phai package Python) can cai rieng:
    # https://github.com/UB-Mannheim/tesseract/wiki  (chon ban Windows installer)
    # Sau khi cai, sua bien TESSERACT_CMD ben duoi cho dung duong dan cai dat.

Cach dung:
    python screen_watch.py capture          # chup 1 lan, in text ra stdout
    python screen_watch.py watch --interval 3   # chup lien tuc, chi in khi man hinh doi khac dang ke
"""

import argparse
import hashlib
import sys
import time
from pathlib import Path

import mss
from PIL import Image

# Thu tu uu tien OCR: Tesseract -> EasyOCR
OCR_ENGINE = None  # 'tesseract' or 'easyocr'

# Try Tesseract first
try:
    import pytesseract
    # Tu dong tim tesseract tren Windows
    import os
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    for p in possible_paths:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break
    # Test if tesseract works
    pytesseract.get_tesseract_version()
    OCR_ENGINE = 'tesseract'
except Exception:
    pass

# Fallback to EasyOCR
if OCR_ENGINE is None:
    try:
        import easyocr
        _easyocr_reader = easyocr.Reader(['vi', 'en'], gpu=False, verbose=False)
        OCR_ENGINE = 'easyocr'
    except ImportError:
        pass

OUT_DIR = Path.home() / ".pi" / "screen_watch"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def capture_and_ocr(monitor_index: int = 1) -> str:
    """Chup 1 frame man hinh, chay OCR, tra ve text."""
    global _easyocr_reader
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.rgb)
        
        if OCR_ENGINE == 'tesseract':
            return pytesseract.image_to_string(img, lang="vie+eng").strip()
        elif OCR_ENGINE == 'easyocr':
            # Save temp image for EasyOCR
            temp_path = str(OUT_DIR / "_screen_temp.png")
            img.save(temp_path)
            results = _easyocr_reader.readtext(temp_path, detail=0)
            return '\n'.join(results)
        else:
            return "[!] Khong co OCR engine nao kha dung. Cai dat: pip install pytesseract hoac easyocr"


def frame_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def cmd_capture(args):
    text = capture_and_ocr(args.monitor)
    if not text:
        print("[man hinh khong co text nhan dien duoc]")
        return
    print(text)


def cmd_watch(args):
    """Chup lien tuc, chi in ra khi noi dung thay doi dang ke (tranh spam)."""
    last_hash = None
    print(f"[screen_watch] Bat dau theo doi man hinh, interval={args.interval}s. Ctrl+C de dung.", file=sys.stderr)
    try:
        while True:
            text = capture_and_ocr(args.monitor)
            h = frame_hash(text)
            if h != last_hash:
                last_hash = h
                ts = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"\n=== [{ts}] Man hinh thay doi ===")
                print(text if text else "[khong co text]")
                sys.stdout.flush()
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[screen_watch] Da dung.", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Chup va OCR man hinh cho AI agent text-only")
    sub = parser.add_subparsers(dest="command", required=True)

    p_capture = sub.add_parser("capture", help="Chup 1 lan va in text")
    p_capture.add_argument("--monitor", type=int, default=1, help="Chi so man hinh (1 = man hinh chinh)")
    p_capture.set_defaults(func=cmd_capture)

    p_watch = sub.add_parser("watch", help="Theo doi lien tuc, chi in khi co thay doi")
    p_watch.add_argument("--interval", type=float, default=3.0, help="So giay giua moi lan chup")
    p_watch.add_argument("--monitor", type=int, default=1)
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
