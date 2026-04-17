#!/usr/bin/env python3
"""
YouTube → TikTok Content Pipeline
Создание TikTok контента из YouTube видео
"""

import json
import os
from datetime import datetime

# Пути
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
VIDEOS_DIR = os.path.join(OUTPUT_DIR, 'videos')
CAPTIONS_DIR = os.path.join(OUTPUT_DIR, 'captions')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

def log_message(message):
    """Логирование сообщений"""
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    logfile = os.path.join(LOGS_DIR, 'content_creation.log')
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(log_entry.strip())

def save_metadata(video_data):
    """Сохраняет метаданные видео"""
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    filepath = os.path.join(VIDEOS_DIR, f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(video_data, f, ensure_ascii=False, indent=2)
    log_message(f"✓ Метаданные сохранены: {filepath}")
    return filepath

def create_content_plan(topic, target_duration=60):
    """
    Создание плана контента для TikTok
    
    Args:
        topic: тема видео
        target_duration: целевая длительность в секундах
    
    Returns:
        dict с планом контента
    """
    log_message(f"Создание плана контента: {topic}")
    
    plan = {
        'topic': topic,
        'target_duration': target_duration,
        'created_at': datetime.now().isoformat(),
        'structure': {
            'hook': {
                'duration': '0-3 сек',
                'description': 'Привлечение внимания (вопрос, шок, интрига)',
                'examples': [
                    'Вы не поверите, что...',
                    'Секрет, который скрывают...',
                    'Что будет, если...',
                ]
            },
            'content': {
                'duration': '3-45 сек',
                'description': 'Основной контент',
                'tips': [
                    'Быстрая смена кадров (2-3 сек)',
                    'Текст на экране',
                    'Динамичная музыка',
                ]
            },
            'call_to_action': {
                'duration': '45-60 сек',
                'description': 'Призыв к действию',
                'examples': [
                    'Подпишись для большего!',
                    'Напиши в комментариях...',
                    'Поделиться с другом!',
                ]
            }
        },
        'technical_requirements': {
            'aspect_ratio': '9:16 (вертикальное)',
            'resolution': '1080x1920 (минимум 720x1280)',
            'format': 'MP4 или MOV',
            'max_size': '287.6 MB (iOS), 75 MB (Android)',
            'framerate': '30 или 60 fps',
        }
    }
    
    log_message("✓ План контента создан")
    return plan

def youtube_search_query(topic, max_results=10):
    """
    Формирование запроса для YouTube поиска
    
    Args:
        topic: тема поиска
        max_results: максимальное количество результатов
    
    Returns:
        dict с параметрами поиска
    """
    log_message(f"Поиск YouTube: {topic}")
    
    search_params = {
        'query': f"{topic} tutorial OR tips OR hacks",
        'max_results': max_results,
        'filters': {
            'duration': 'short',  # Короткие видео (< 4 мин)
            'upload_date': 'this_month',
            'sort_by': 'view_count',
        },
        'note': 'Используйте MCP skill "youtube-search" для выполнения поиска'
    }
    
    return search_params

def clip_extraction_plan(source_video_url, clips_count=3):
    """
    План извлечения клипов из YouTube видео
    
    Args:
        source_video_url: URL исходного видео
        clips_count: количество клипов для создания
    
    Returns:
        dict с планом нарезки
    """
    log_message(f"План нарезки: {source_video_url}")
    
    plan = {
        'source_url': source_video_url,
        'clips_count': clips_count,
        'clip_duration': 60,  # секунд
        'note': 'Используйте MCP skill "youtube-clipper" для создания клипов',
        'extraction_strategy': {
            'method': 'highlights',
            'prioritize': [
                'Моменты с высокой энергией',
                'Ключевые моменты/выводы',
                'Визуально интересные сцены',
                'Забавные моменты',
            ]
        }
    }
    
    return plan

def prepare_for_tiktok(clip_path, caption_data):
    """
    Подготовка клипа для публикации в TikTok
    
    Args:
        clip_path: путь к видео файлу
        caption_data: данные для описания
    
    Returns:
        dict с готовыми данными для публикации
    """
    log_message(f"Подготовка для TikTok: {clip_path}")
    
    package = {
        'video_path': clip_path,
        'caption': caption_data.get('caption', ''),
        'hashtags': caption_data.get('hashtags', []),
        'ready_for_upload': True,
        'created_at': datetime.now().isoformat(),
    }
    
    return package

def main():
    """Основная функция"""
    import sys
    
    topic = sys.argv[1] if len(sys.argv) > 1 else 'viral trends'
    
    print(f"🎬 Создание контента для TikTok")
    print("=" * 50)
    print(f"Тема: {topic}")
    
    # Шаг 1: План контента
    content_plan = create_content_plan(topic)
    
    # Шаг 2: Поиск YouTube
    search_params = youtube_search_query(topic)
    print(f"\n📺 Поиск YouTube: {search_params['query']}")
    
    # Шаг 3: План нарезки (будет выполнен после выбора видео)
    print("\n💡 Следующие шаги:")
    print("1. Используйте MCP skill 'youtube-search' для поиска")
    print("2. Используйте MCP skill 'youtube-clipper' для создания клипа")
    print("3. Используйте MCP skill 'tiktok-captions' для генерации описания")
    print("4. Используйте MCP skill 'tiktok-automation' для публикации")
    
    # Сохранение плана
    save_metadata({
        'content_plan': content_plan,
        'search_params': search_params,
    })
    
    print("\n" + "=" * 50)
    print("✓ План контента готов!")

if __name__ == '__main__':
    main()
