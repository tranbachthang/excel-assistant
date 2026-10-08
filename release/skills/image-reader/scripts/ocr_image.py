"""
ocr_image.py - Trich xuat text tu anh (Tesseract hoac EasyOCR, tu dong chon)

Da toi uu:
  - Skip Tesseract neu binary KHONG ton tai (khong con loop loi vo ich)
  - Cache EasyOCR Reader (chi init 1 lan / process)
  - download_enabled=False (khong check mang, model da cache san)

Usage:
  python ocr_image.py <path> [--lang vie+eng] [--info] [--json] [--reader auto|tesseract|easyocr]
"""
import sys
import os
import shutil
import json
import warnings

# Tat warning (vd torch 'pin_memory' khi chay EasyOCR tren CPU) de tranh nhieu output
os.environ.setdefault('PYTHONWARNINGS', 'ignore')
warnings.filterwarnings('ignore')

# Unicode tieng Viet tren Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Cache EasyOCR Reader (chi init 1 lan)
_EASYOCR_READER = None
_RAPIDOCR_ENGINE = None


def find_tesseract_binary():
    """Tim tesseract.exe. Tra ve path hoac None."""
    # 1. Thu trong PATH
    which = shutil.which('tesseract')
    if which:
        return which
    # 2. Thu cac vi tri cai dat pho bien tren Windows
    candidates = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def has_tesseract():
    return find_tesseract_binary() is not None


def ocr_with_tesseract(image_path, lang='eng'):
    """Dung Tesseract. Tra ve text hoac None neu khong kha dung."""
    binary = find_tesseract_binary()
    if not binary:
        return None
    try:
        import pytesseract
        from PIL import Image
        pytesseract.pytesseract.tesseract_cmd = binary
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang=lang)
        return text.strip()
    except Exception as e:
        return f"[Tesseract Error] {e}"


def ocr_with_easyocr(image_path):
    """Dung EasyOCR (cache reader). Tra ve text hoac None."""
    global _EASYOCR_READER
    try:
        import easyocr
        from PIL import Image
        import numpy as np
        if _EASYOCR_READER is None:
            # download_enabled=False: khong check mang, model da co san trong ~/.EasyOCR
            _EASYOCR_READER = easyocr.Reader(['vi', 'en'], gpu=False,
                                             download_enabled=False, verbose=False)
        img = Image.open(image_path).convert('RGB')
        # ponytail: downscale anh to de CRAFT detection nhanh hon nhieu
        w, h = img.size
        max_side = 1600
        if max(w, h) > max_side:
            s = max_side / max(w, h)
            img = img.resize((int(w * s), int(h * s)), Image.LANCZOS)
        arr = np.array(img)
        # canvas_size + mag_ratio giam -> detect nhanh (van du doc text ro)
        results = _EASYOCR_READER.readtext(arr, detail=0,
                                           canvas_size=1280, mag_ratio=1.0)
        return '\n'.join(results)
    except ImportError:
        return None
    except Exception as e:
        return f"[EasyOCR Error] {e}"


def ocr_with_rapidocr(image_path):
    """Dung RapidOCR (onnxruntime, ~1s, nhanh hon EasyOCR). Tra ve text hoac None."""
    global _RAPIDOCR_ENGINE
    try:
        from rapidocr_onnxruntime import RapidOCR
        if _RAPIDOCR_ENGINE is None:
            _RAPIDOCR_ENGINE = RapidOCR()
        result, _ = _RAPIDOCR_ENGINE(image_path)
        if not result:
            return None
        return '\n'.join(r[1] for r in result)
    except ImportError:
        return None
    except Exception as e:
        return f"[RapidOCR Error] {e}"


def get_image_info(image_path):
    try:
        from PIL import Image
        img = Image.open(image_path)
        return {
            "size": f"{img.width}x{img.height}",
            "format": img.format,
            "mode": img.mode,
            "filesize_kb": round(os.path.getsize(image_path) / 1024, 1)
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python ocr_image.py <path> [--lang vie+eng] [--info] [--json] [--reader auto|rapidocr|easyocr|tesseract]")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"[!] File khong ton tai: {image_path}")
        sys.exit(1)

    lang = 'eng'
    show_info = False
    json_output = False
    reader_choice = 'auto'

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        a = args[i]
        if a == '--lang' and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
            continue
        if a == '--reader' and i + 1 < len(args):
            reader_choice = args[i + 1].lower()
            i += 2
            continue
        if a == '--info':
            show_info = True
        if a == '--json':
            json_output = True
        i += 1

    info = get_image_info(image_path)

    # Chon reader
    text = None
    method = "?"

    if reader_choice == 'tesseract':
        if has_tesseract():
            text = ocr_with_tesseract(image_path, lang)
            method = "Tesseract"
        else:
            text = "[!] Tesseract chua cai. Dung --reader rapidocr."
            method = "Tesseract (missing)"
    elif reader_choice == 'easyocr':
        text = ocr_with_easyocr(image_path)
        method = "EasyOCR"
    elif reader_choice == 'rapidocr':
        text = ocr_with_rapidocr(image_path)
        method = "RapidOCR"
    else:  # auto: RapidOCR -> EasyOCR -> Tesseract
        text = ocr_with_rapidocr(image_path)
        method = "RapidOCR"
        if text is None or (isinstance(text, str) and text.startswith('[')):
            text = ocr_with_easyocr(image_path)
            method = "EasyOCR"
        if text is None or (isinstance(text, str) and text.startswith('[')):
            if has_tesseract():
                text = ocr_with_tesseract(image_path, lang)
                method = "Tesseract"

    if json_output:
        print(json.dumps({"info": info, "ocr_method": method, "text": text or ""},
                         ensure_ascii=False, indent=2))
        return

    if show_info or not text:
        print(f"[*] File: {image_path}")
        print(f"[*] Size: {info.get('size', '?')} | Format: {info.get('format', '?')} | {info.get('filesize_kb', '?')} KB")
        print(f"[*] OCR: {method}")
        print("=" * 60)

    if text and not (isinstance(text, str) and text.startswith('[!')):
        print(text)
    else:
        print(text or "[!] Khong trich xuat duoc text.")


if __name__ == "__main__":
    main()
