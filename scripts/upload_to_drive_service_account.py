#!/usr/bin/env python3
"""
Google Drive Upload via Service Account
Загрузка файлов в Google Drive через сервисный аккаунт
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Пути
PROJECT_DIR = Path("/root/tiktokproject")
SERVICE_ACCOUNT_FILE = PROJECT_DIR / "config" / "service_account.json"
ZIP_FILE = list(PROJECT_DIR.glob("tiktok_project_result_*.zip"))[0] if list(PROJECT_DIR.glob("tiktok_project_result_*.zip")) else None

print("=" * 70)
print("📤 ЗАГРУЗКА В GOOGLE DRIVE ЧЕРЕЗ СЕРВИСНЫЙ АККАУНТ")
print("=" * 70)

# Проверка файлов
if not SERVICE_ACCOUNT_FILE.exists():
    print(f"❌ Файл сервисного аккаунта не найден: {SERVICE_ACCOUNT_FILE}")
    sys.exit(1)

if not ZIP_FILE or not ZIP_FILE.exists():
    print(f"❌ ZIP файл не найден!")
    sys.exit(1)

print(f"\n✅ Сервисный аккаунт: {SERVICE_ACCOUNT_FILE}")
print(f"✅ Файл для загрузки: {ZIP_FILE.name}")
print(f"📊 Размер: {ZIP_FILE.stat().st_size:,} байт ({ZIP_FILE.stat().st_size/1024:.2f} KB)")

# Загрузка через Google Drive API
try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    print("\n🔐 Авторизация через сервисный аккаунт...")
    
    # Загрузка кредов
    creds = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=SCOPES
    )
    
    print("✅ Авторизация успешна!")
    print(f"   Email: {creds.service_account_email}")
    
    # Создание сервиса Drive
    service = build('drive', 'v3', credentials=creds)
    
    # Создание папки проекта
    print("\n📁 Создание папки 'TikTok Automation Project'...")
    
    folder_metadata = {
        'name': 'TikTok Automation Project',
        'mimeType': 'application/vnd.google-apps.folder'
    }
    
    try:
        folder = service.files().create(body=folder_metadata, fields='id, name, webViewLink').execute()
        folder_id = folder.get('id')
        print(f"✅ Папка создана: {folder.get('name')}")
        print(f"   ID: {folder_id}")
        print(f"   Ссылка: {folder.get('webViewLink')}")
    except HttpError as e:
        if e.resp.status == 409:  # Folder already exists
            # Поиск существующей папки
            results = service.files().list(
                q="name='TikTok Automation Project' and mimeType='application/vnd.google-apps.folder' and trashed=false",
                fields="files(id, name, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            if files:
                folder = files[0]
                folder_id = folder.get('id')
                print(f"✅ Найдена существующая папка: {folder.get('name')}")
                print(f"   ID: {folder_id}")
                print(f"   Ссылка: {folder.get('webViewLink')}")
            else:
                print("❌ Ошибка создания/поиска папки")
                raise
        else:
            raise
    
    # Загрузка ZIP файла
    print(f"\n📦 Загрузка файла: {ZIP_FILE.name}")
    
    file_metadata = {
        'name': f'{ZIP_FILE.stem}_uploaded_{datetime.now().strftime("%Y%m%d_%H%M%S")}{ZIP_FILE.suffix}',
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(str(ZIP_FILE), mimetype='application/zip', resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, name, size, webViewLink, webContentLink'
    ).execute()
    
    print(f"\n✅ ЗАГРУЗКА УСПЕШНА!")
    print(f"   Файл: {file.get('name')}")
    print(f"   ID: {file.get('id')}")
    print(f"   Размер: {file.get('size', 'N/A')} байт")
    print(f"   Просмотр: {file.get('webViewLink')}")
    print(f"   Скачать: {file.get('webContentLink')}")
    
    # Загрузка остальных файлов проекта
    print("\n📂 Загрузка дополнительных файлов...")
    
    files_to_upload = [
        ("README.md", "text/markdown"),
        ("NEXT_STEPS.md", "text/markdown"),
        ("UPLOAD_NOW.md", "text/markdown"),
        ("IMPLEMENTATION.md", "text/markdown"),
        ("USAGE.md", "text/markdown"),
    ]
    
    for filename, mimetype in files_to_upload:
        filepath = PROJECT_DIR / filename
        if filepath.exists():
            print(f"   📄 {filename}...")
            
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(str(filepath), mimetype=mimetype, resumable=True)
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
    
    print("\n✅ ВСЕ ФАЙЛЫ ЗАГРУЖЕНЫ!")
    
    # Загрузка отчётов
    print("\n📊 Загрузка отчётов...")
    
    reports_dir = PROJECT_DIR / "output" / "reports"
    if reports_dir.exists():
        for report_file in reports_dir.glob("*.json"):
            print(f"   📄 {report_file.name}...")
            
            file_metadata = {
                'name': f"reports/{report_file.name}",
                'parents': [folder_id]
            }
            
            media = MediaFileUpload(str(report_file), mimetype='application/json', resumable=True)
            
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, name'
            ).execute()
    
    print("\n" + "=" * 70)
    print("🎉 ГОТОВО! ВСЁ ЗАГРУЖЕНО В GOOGLE DRIVE!")
    print("=" * 70)
    print(f"\n📁 Папка проекта: {folder.get('webViewLink')}")
    print("\n📝 Содержимое:")
    print("   ✅ tiktok_project_result_*.zip (архив проекта)")
    print("   ✅ README.md")
    print("   ✅ NEXT_STEPS.md")
    print("   ✅ UPLOAD_NOW.md")
    print("   ✅ IMPLEMENTATION.md")
    print("   ✅ USAGE.md")
    print("   ✅ reports/*.json (отчёты)")
    
except ImportError as e:
    print(f"\n❌ Ошибка импорта: {e}")
    print("\nУстанови библиотеки:")
    print("  pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
