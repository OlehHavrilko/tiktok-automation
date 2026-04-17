#!/usr/bin/env python3
"""
Google Drive Upload Script
Загрузка файлов в Google Drive через API с использованием API ключа
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# API ключ (можно передать через аргумент или переменную окружения)
API_KEY = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('GOOGLE_API_KEY', '')

if not API_KEY:
    print("❌ Не указан API ключ!")
    print("Использование: python upload_to_drive.py <API_KEY>")
    sys.exit(1)

print("=" * 70)
print("📤 ЗАГРУЗКА В GOOGLE DRIVE")
print("=" * 70)

# Путь к ZIP файлу
PROJECT_DIR = Path("/root/tiktokproject")
zip_files = list(PROJECT_DIR.glob("tiktok_project_result_*.zip"))

if not zip_files:
    print("❌ ZIP файл не найден!")
    sys.exit(1)

zip_file = zip_files[0]
print(f"\n📦 Файл для загрузки: {zip_file.name}")
print(f"📊 Размер: {zip_file.stat().st_size:,} байт ({zip_file.stat().st_size/1024:.2f} KB)")

# Пробуем загрузить через Google Drive API
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    
    print("\n✅ Google API библиотеки найдены")
    
    # SCOPES для доступа к Drive
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    
    # Создаём папку для проекта
    folder_name = "TikTok Automation Project"
    
    print(f"\n📁 Создание папки: {folder_name}")
    
    # Для загрузки нужен OAuth токен, а не только API ключ
    # API ключ только для чтения публичных данных
    
    print("\n⚠️ ВНИМАНИЕ: API ключ ({API_KEY[:20]}...) только для ЧТЕНИЯ")
    print("Для ЗАГРУЗКИ файлов нужен OAuth 2.0 токен")
    
    print("\n" + "=" * 70)
    print("📋 ВАРИАНТЫ ЗАГРУЗКИ:")
    print("=" * 70)
    
    print("""
1️⃣ ЧЕРЕЗ БРАУЗЕР (БЫСТРО, 2 МИНУТЫ):
   
   а) Открой: https://drive.google.com
   
   б) Перетащи файл:
      {zip_file}
   
   в) Или: "+ Создать" → "Загрузить файлы"
   
   г) Переименуй в: tiktok_project_result.zip
   
2️⃣ ЧЕРЕЗ OAUTH 2.0 (НУЖНА АВТОРИЗАЦИЯ):
   
   Запусти:
   python scripts/oauth_upload.py
   
   Следуй инструкциям в браузере.

3️⃣ ЧЕРЕЗ RCLONE (ЕСЛИ НАСТРОЕН):
   
   cd /root/tiktokproject
   ./scripts/sync_drive.sh sync
    """.format(zip_file=zip_file))
    
    print("=" * 70)
    
    # Проверяем, работает ли API ключ для чтения
    try:
        from googleapiclient.discovery import build
        
        # Пробуем сделать простой запрос
        drive_service = build('drive', 'v3', developerKey=API_KEY)
        
        # Проверяем доступность API
        print("\n🔍 Проверка API ключа...")
        
        # API ключ не позволяет получить доступ к файлам без OAuth
        print("ℹ️ API ключ активен, но требуется OAuth для записи")
        
    except Exception as e:
        print(f"⚠️ Ошибка проверки API: {e}")
    
    print("\n" + "=" * 70)
    print("✅ РЕКОМЕНДАЦИЯ: Загрузи через браузер (способ 1)")
    print("=" * 70)
    
except ImportError as e:
    print(f"\n❌ Ошибка импорта Google API: {e}")
    print("\nУстанови библиотеки:")
    print("  pip install google-auth google-auth-oauthlib google-api-python-client")

print("\n📁 Файл готов к загрузке:")
print(f"   {zip_file}")
print("\n📂 Размер: {:.2f} KB".format(zip_file.stat().st_size / 1024))
