"""
check_env.py - Kiem tra moi truong OCR 1 lan, in ket qua gon + ghi cache JSON.

Chay 1 lan de biet chinh xac: Python, Tesseract, EasyOCR, model cache.
Ket qua duoc ghi vao .env_cache.json (canh script) de cac lan sau doc nhanh.

Usage: python check_env.py [--json]
"""
import sys
import os
import json
import shutil

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env_cache.json')


def detect():
    env = {}

    # Python
    env['python'] = sys.executable
    env['python_version'] = sys.version.split()[0]

    # Tesseract
    tesseract = shutil.which('tesseract')
    if not tesseract:
        for p in [r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                  r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                  r'~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe']:
            if os.path.exists(p):
                tesseract = p
                break
    env['tesseract'] = tesseract
    env['tesseract_ok'] = bool(tesseract)

    # Pillow
    try:
        import PIL
        env['pillow'] = PIL.__version__
    except ImportError:
        env['pillow'] = None

    # pytesseract
    try:
        import pytesseract
        env['pytesseract'] = getattr(pytesseract, '__version__', 'installed')
    except ImportError:
        env['pytesseract'] = None

    # EasyOCR + model cache
    try:
        import easyocr
        env['easyocr'] = getattr(easyocr, '__version__', 'installed')
    except ImportError:
        env['easyocr'] = None
    model_dir = os.path.expanduser('~/.EasyOCR/model')
    env['easyocr_model_cache'] = model_dir if os.path.isdir(model_dir) else None

    # Ket luan reader nao dung duoc
    if env['tesseract_ok']:
        env['recommended_reader'] = 'tesseract'
    elif env['easyocr'] and env['easyocr_model_cache']:
        env['recommended_reader'] = 'easyocr'
    else:
        env['recommended_reader'] = None

    return env


def main():
    env = detect()
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(env, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    if '--json' in sys.argv:
        print(json.dumps(env, ensure_ascii=False, indent=2))
        return

    print("=== OCR Environment ===")
    print(f"Python      : {env['python_version']} ({env['python']})")
    print(f"Tesseract   : {'OK (' + env['tesseract'] + ')' if env['tesseract_ok'] else 'KHONG cai'}")
    print(f"pytesseract : {env['pytesseract'] or 'KHONG cai'}")
    print(f"Pillow      : {env['pillow'] or 'KHONG cai'}")
    print(f"EasyOCR     : {env['easyocr'] or 'KHONG cai'}")
    print(f"Model cache : {env['easyocr_model_cache'] or 'KHONG co'}")
    print(f"=> Dung reader: {env['recommended_reader'] or 'CHUA SAN SANG'}")

    if env['recommended_reader'] is None:
        print("\n[!] Chua san sang. Cai nhanh:")
        print("   winget install UB-Mannheim.TesseractOCR")
        print("   pip install pytesseract pillow easyocr")


if __name__ == "__main__":
    main()
