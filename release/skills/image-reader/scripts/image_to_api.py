"""
image_to_api.py - Doc anh qua API Vision (OpenAI GPT-4o, Claude, Gemini)
Khi model hien tai khong ho tro anh, dung API de phan tich.
Cai dat: pip install openai pillow base64

Set API key:
  $env:OPENAI_API_KEY = "sk-..."
  Hoac tao file .env cung thu muc

Usage: python image_to_api.py <path_to_image> [--prompt "cau hoi"]
"""
import sys
import os
import base64
import json

def encode_image(image_path):
    """Ma hoa anh thanh base64"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def load_api_key():
    """Load API key tu env hoac .env file"""
    key = os.getenv("OPENAI_API_KEY")
    if key:
        return key
    
    # Thu load tu file .env
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_files = [
        os.path.join(script_dir, '.env'),
        os.path.join(script_dir, '..', '.env'),
    ]
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('OPENAI_API_KEY='):
                        return line.split('=', 1)[1].strip('"').strip("'")
    return None


def analyze_with_openai(image_path, prompt=None, api_key=None):
    """Phan tich anh qua OpenAI GPT-4o Vision"""
    try:
        from openai import OpenAI
        
        if not api_key:
            api_key = load_api_key()
        if not api_key:
            return None, "Thieu OPENAI_API_KEY. Set: $env:OPENAI_API_KEY = 'sk-...'"
        
        client = OpenAI(api_key=api_key)
        b64 = encode_image(image_path)
        
        if not prompt:
            prompt = "Hay mo ta chi tiet noi dung cua anh nay. Trich xuat tat ca text, so lieu, va thong tin co trong anh. Tra loi bang tieng Viet."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{b64}",
                        "detail": "high"
                    }}
                ]
            }],
            max_tokens=2000
        )
        return response.choices[0].message.content, None
    except ImportError:
        return None, "Chua cai openai: pip install openai"
    except Exception as e:
        return None, f"[API Error] {e}"


def analyze_with_claude(image_path, prompt=None):
    """Phan tich anh qua Anthropic Claude"""
    try:
        import anthropic
        from PIL import Image
        import io
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return None, "Thieu ANTHROPIC_API_KEY"
        
        client = anthropic.Anthropic(api_key=api_key)
        
        # Detect media type
        img = Image.open(image_path)
        fmt = img.format.lower()
        media_type = f"image/{fmt}" if fmt in ['jpeg', 'png', 'gif', 'webp'] else "image/png"
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format=fmt or 'PNG')
        img_bytes = buffer.getvalue()
        
        if not prompt:
            prompt = "Hay mo ta chi tiet noi dung cua anh nay. Trich xuat tat ca text, so lieu, va thong tin co trong anh. Tra loi bang tieng Viet."
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64.b64encode(img_bytes).decode("utf-8")
                    }},
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        return response.content[0].text, None
    except ImportError:
        return None, "Chua cai anthropic: pip install anthropic"
    except Exception as e:
        return None, f"[Claude API Error] {e}"


def main():
    if len(sys.argv) < 2:
        print("Usage: python image_to_api.py <path_to_image> [--prompt '...'] [--provider openai|claude]")
        print("  Vi du: python image_to_api.py screenshot.png")
        print("         python image_to_api.py chart.png --prompt 'Phan tich bieu do nay'")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"[!] File khong ton tai: {image_path}")
        sys.exit(1)
    
    prompt = None
    provider = 'openai'
    
    for i, arg in enumerate(sys.argv):
        if arg == '--prompt' and i + 1 < len(sys.argv):
            prompt = sys.argv[i + 1]
        if arg == '--provider' and i + 1 < len(sys.argv):
            provider = sys.argv[i + 1]
    
    # Thu load API key
    api_key = load_api_key()
    
    if provider == 'openai':
        if not api_key:
            print("[!] Thieu OPENAI_API_KEY")
            print("[*] Set: `$env:OPENAI_API_KEY = 'sk-...'`")
            print("[*] Hoac tao file .env trong thu muc scripts/")
            print("[*] Hoac dung OCR offline: python ocr_image.py " + image_path)
            sys.exit(1)
        
        print(f"[*] Dang phan tich anh qua GPT-4o...")
        result, error = analyze_with_openai(image_path, prompt, api_key)
    
    elif provider == 'claude':
        print(f"[*] Dang phan tich anh qua Claude...")
        result, error = analyze_with_claude(image_path, prompt)
    
    else:
        print(f"[!] Provider khong ho tro: {provider}")
        sys.exit(1)
    
    if error:
        print(f"\n[!] {error}")
    else:
        print("\n" + "=" * 60)
        print(result)
        print("=" * 60)


if __name__ == "__main__":
    main()
