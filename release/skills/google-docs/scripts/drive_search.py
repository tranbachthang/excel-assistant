"""
drive_search.py - Tim kiem file trong Google Drive (can Service Account)
Usage: 
  python drive_search.py "tu khoa" 
  python drive_search.py "tu khoa" --type spreadsheet
  python drive_search.py "tu khoa" --folder

Cai dat:
  pip install google-api-python-client google-auth
  Dat credentials.json (Service Account) cung thu muc
"""
import sys
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def get_drive_service():
    creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    if not os.path.exists(creds_path):
        # Th? tim trong thu muc cha
        creds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
    
    if not os.path.exists(creds_path):
        print("[!] Khong tim thay credentials.json")
        print("[*] Tao Service Account: https://console.cloud.google.com/apis/credentials")
        print("[*] Tai JSON key va dat vao: " + os.path.dirname(__file__))
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def search_files(service, query, file_type=None, folder_only=False):
    """Tim kiem file tren Drive"""
    q_parts = []
    
    # Tu khoa
    if query:
        q_parts.append(f"name contains '{query}'")
    
    # Loai file
    mime_map = {
        'spreadsheet': 'application/vnd.google-apps.spreadsheet',
        'document': 'application/vnd.google-apps.document',
        'presentation': 'application/vnd.google-apps.presentation',
        'folder': 'application/vnd.google-apps.folder',
        'pdf': 'application/pdf',
        'image': 'image/',
    }
    
    if file_type and file_type in mime_map:
        if file_type == 'image':
            q_parts.append(f"mimeType contains '{mime_map[file_type]}'")
        else:
            q_parts.append(f"mimeType='{mime_map[file_type]}'")
    
    if folder_only:
        q_parts.append("mimeType='application/vnd.google-apps.folder'")
    
    q = " and ".join(q_parts) if q_parts else "trashed=false"
    
    try:
        results = service.files().list(
            q=q,
            pageSize=20,
            fields="files(id, name, mimeType, webViewLink, createdTime, size)"
        ).execute()
        return results.get('files', [])
    except HttpError as e:
        print(f"[!] Loi API: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: python drive_search.py <tu_khoa> [--type spreadsheet|document|folder|pdf] [--folder]")
        print("  Vi du: python drive_search.py 'bao cao' --type spreadsheet")
        sys.exit(1)
    
    query = sys.argv[1]
    file_type = None
    folder_only = False
    
    for i, arg in enumerate(sys.argv):
        if arg == '--type' and i + 1 < len(sys.argv):
            file_type = sys.argv[i + 1]
        if arg == '--folder':
            folder_only = True
    
    print(f"[*] Dang tim: '{query}'" + (f" (type: {file_type})" if file_type else ""))
    
    service = get_drive_service()
    files = search_files(service, query, file_type, folder_only)
    
    if not files:
        print("[!] Khong tim thay file nao.")
        return
    
    print(f"\n[+] Tim thay {len(files)} file:\n")
    
    for i, f in enumerate(files, 1):
        name = f.get('name', 'Unknown')
        mime = f.get('mimeType', '').replace('application/vnd.google-apps.', '')
        link = f.get('webViewLink', 'N/A')
        created = f.get('createdTime', '')[:10] if f.get('createdTime') else ''
        
        print(f"  {i}. {name}")
        print(f"     Type: {mime} | Created: {created}")
        print(f"     Link: {link}")
        print()

if __name__ == "__main__":
    main()
