#!/usr/bin/env python3
"""
Google Drive Upload Script
Загрузка файлов проекта в Google Drive через API
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Пути
PROJECT_DIR = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
CAPTIONS_DIR = OUTPUT_DIR / "captions"
DOCS_DIR = PROJECT_DIR

print("=" * 70)
print("📦 ПОДГОТОВКА ФАЙЛОВ ДЛЯ GOOGLE DRIVE")
print("=" * 70)

# Собираем все важные файлы
files_to_upload = {
    "reports": list(REPORTS_DIR.glob("*.json")),
    "captions": list(CAPTIONS_DIR.glob("*.json")),
    "docs": [
        PROJECT_DIR / "README.md",
        PROJECT_DIR / "NEXT_STEPS.md",
        PROJECT_DIR / "CONCRETE_RESULT.json" if (PROJECT_DIR / "CONCRETE_RESULT.json").exists() else None,
    ],
    "scripts": list((PROJECT_DIR / "scripts").glob("*.py")),
}

print("\n📁 Файлы для загрузки:")
total_size = 0
file_count = 0

for category, files in files_to_upload.items():
    if files:
        print(f"\n  {category.upper()}:")
        for f in files:
            if f and f.exists():
                size = f.stat().st_size
                total_size += size
                file_count += 1
                print(f"    ✓ {f.name} ({size:,} байт)")

print(f"\n📊 Итого: {file_count} файлов, {total_size:,} байт ({total_size/1024:.2f} KB)")

# Создаём итоговый отчёт
summary = {
    "project": "TikTok Automation - Итоговый Результат",
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "github": "https://github.com/OlehHavrilko/tiktok-automation",
    "files_count": file_count,
    "total_size_bytes": total_size,
    "contents": {
        "reports": [f.name for f in files_to_upload["reports"] if f],
        "captions": [f.name for f in files_to_upload["captions"] if f],
        "scripts": [f.name for f in files_to_upload["scripts"] if f],
        "documentation": ["README.md", "NEXT_STEPS.md", "USAGE.md", "IMPLEMENTATION.md"]
    },
    "what_ready": [
        "✅ Исследование трендов (Google Trends, Reddit)",
        "✅ План контента на неделю (3 видео)",
        "✅ Готовые описания для TikTok",
        "✅ Скрипты автоматизации (6 штук)",
        "✅ MCP skills активированы",
        "✅ Документация полная"
    ],
    "next_steps": [
        "1. Открыть NEXT_STEPS.md",
        "2. Найти видео на YouTube (skill: youtube-search)",
        "3. Создать клипы (skill: youtube-clipper)",
        "4. Опубликовать (skill: tiktok-automation)"
    ]
}

# Сохраняем summary
summary_path = REPORTS_DIR / "PROJECT_SUMMARY.json"
with open(summary_path, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"\n✅ Summary сохранён: {summary_path}")

# Создаём ZIP архив
import shutil
import zipfile

archive_name = f"tiktok_project_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
archive_path = f"{PROJECT_DIR}/{archive_name}.zip"

# Исключаемые файлы
exclude_dirs = {'venv', '.git', 'logs', '__pycache__', 'node_modules'}
exclude_ext = {'.pyc', '.pyo', '.log'}

with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Исключаем директории
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            # Исключаем файлы
            if Path(file).suffix in exclude_ext:
                continue
            if file.endswith('.zip'):  # Не включаем сам архив
                continue
                
            file_path = Path(root) / file
            arcname = file_path.relative_to(PROJECT_DIR)
            zipf.write(file_path, arcname)

print(f"✅ ZIP архив создан: {archive_path}")
print(f"   Размер: {os.path.getsize(archive_path):,} байт ({os.path.getsize(archive_path)/1024/1024:.2f} MB)")

# Выводим инструкцию
print("\n" + "=" * 70)
print("📤 ЗАГРУЗКА В GOOGLE DRIVE")
print("=" * 70)
print("""
Автоматическая загрузка через rclone НЕ работает (нужна авторизация через браузер).

Варианты загрузки:

1️⃣ ЧЕРЕЗ БРАУЗЕР (рекомендуется):
   - Открой https://drive.google.com
   - Перетащи файл: {archive_path}
   - Или загрузи через кнопку "+ Создать" → "Загрузить файлы"

2️⃣ ЧЕРЕЗ RCLONE (нужна авторизация):
   cd /root/tiktokproject
   ./scripts/sync_drive.sh sync

3️⃣ ЧЕРЕЗ GOOGLE DRIVE API:
   python scripts/upload_to_drive.py {archive_path}

📁 Файл для загрузки: {archive_path}
📦 Размер: {size_mb:.2f} MB
""".format(archive_path=archive_path, size_mb=os.path.getsize(archive_path)/1024/1024))

print("=" * 70)
print("✅ ГОТОВО! Все файлы подготовлены к загрузке.")
print("=" * 70)
