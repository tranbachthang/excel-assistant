"""
quick_gdoc.py - Doc Google Docs public (khong can auth)
Dung khi file duoc share "Anyone with link can view"
Usage: python quick_gdoc.py "https://docs.google.com/document/d/FILE_ID/edit"
Output: Markdown
"""
import sys
import re
import json
import urllib.request
import urllib.error

def extract_file_id(url):
    """Trich xuat file ID tu Google Docs URL"""
    patterns = [
        r'/document/d/([a-zA-Z0-9_-]+)',
        r'/spreadsheets/d/([a-zA-Z0-9_-]+)',
        r'/presentation/d/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1), 'doc' if 'document' in p else 'sheet' if 'spreadsheets' in p else 'slide'
    return url, 'doc'


def export_doc(file_id, mime_type):
    """Export Google Docs sang text/plain hoac text/html"""
    url = f"https://docs.google.com/document/d/{file_id}/export?format=txt"
    if mime_type == 'html':
        url = url.replace('format=txt', 'format=html')
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8')
            return content
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[!] File khong ton tai hoac khong public (HTTP {e.code})")
            print("[*] Dam bao file duoc share: File > Share > General access > Anyone with the link")
        elif e.code == 403:
            print(f"[!] Khong co quyen truy cap (HTTP {e.code})")
            print("[*] Can share file public hoac dung Service Account")
        else:
            print(f"[!] Loi HTTP {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"[!] Loi ket noi: {e}")
        return None


def export_sheet_csv(file_id):
    """Export Google Sheets sang CSV"""
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode('utf-8')
    except Exception as e:
        print(f"[!] Loi: {e}")
        return None


def html_to_markdown(html):
    """Convert HTML co ban sang Markdown"""
    # Bo script/style
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Headings
    for i in range(6, 0, -1):
        html = re.sub(rf'<h{i}[^>]*>(.*?)</h{i}>', rf'{"#"*i} \1\n\n', html, flags=re.DOTALL)

    # Bold, italic
    html = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', html, flags=re.DOTALL)
    html = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', html, flags=re.DOTALL)
    html = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', html, flags=re.DOTALL)

    # Links
    html = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html)

    # Lists
    html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html, flags=re.DOTALL)
    html = re.sub(r'</?[ou]l[^>]*>', '\n', html)

    # Paragraphs
    html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.DOTALL)
    html = re.sub(r'<br\s*/?>', '\n', html)

    # Remove remaining tags
    html = re.sub(r'<[^>]+>', '', html)

    # Clean up whitespace
    html = re.sub(r'\n\s*\n\s*\n+', '\n\n', html)
    html = html.strip()

    return html


def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_gdoc.py <google_docs_url> [--html]")
        print("  Vi du: python quick_gdoc.py https://docs.google.com/document/d/ABC123/edit")
        sys.exit(1)

    url = sys.argv[1]
    use_html = '--html' in sys.argv

    file_id, file_type = extract_file_id(url)
    print(f"[*] File ID: {file_id}")
    print(f"[*] Type: {file_type}")

    if file_type == 'sheet':
        content = export_sheet_csv(file_id)
        if content:
            print("\n" + "=" * 60)
            print(content)
    elif file_type == 'doc':
        if use_html:
            content = export_doc(file_id, 'html')
            if content:
                md = html_to_markdown(content)
                print("\n" + "=" * 60)
                print(md)
        else:
            content = export_doc(file_id, 'txt')
            if content:
                print("\n" + "=" * 60)
                print(content)
    else:
        print(f"[!] Loai file '{file_type}' chua ho tro (dung Google Drive API de download)")


if __name__ == "__main__":
    main()
