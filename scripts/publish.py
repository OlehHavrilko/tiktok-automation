#!/usr/bin/env python3
"""
TikTok Publishing & Analytics Script
Публикация видео и сбор аналитики через бесплатные API
"""

import json
import os
from datetime import datetime, timedelta

# Пути
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
VIDEOS_DIR = os.path.join(OUTPUT_DIR, 'videos')
CAPTIONS_DIR = os.path.join(OUTPUT_DIR, 'captions')
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')

def log_message(message):
    """Логирование сообщений"""
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    logfile = os.path.join(LOGS_DIR, 'publish.log')
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(log_entry.strip())

def load_config():
    """Загрузка конфигурации"""
    config_path = os.path.join(CONFIG_DIR, 'settings.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_publish_log(video_data):
    """Сохранение лога публикации"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filepath = os.path.join(REPORTS_DIR, f'publish_log_{datetime.now().strftime("%Y%m%d")}.json')
    
    # Загрузка существующих записей
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(video_data)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    
    log_message(f"✓ Лог публикации сохранен: {filepath}")

def prepare_video_for_upload(video_path, caption, hashtags, schedule_time=None):
    """
    Подготовка видео к загрузке
    
    Args:
        video_path: путь к видео файлу
        caption: текст описания
        hashtags: список хэштегов
        schedule_time: время публикации (ISO format)
    
    Returns:
        dict с данными для публикации
    """
    log_message(f"Подготовка видео: {video_path}")
    
    config = load_config()
    tiktok_config = config.get('tiktok', {})
    
    # Проверка лимитов
    current_month = datetime.now().strftime('%Y-%m')
    max_videos = tiktok_config.get('maxVideosPerMonth', 20)
    
    upload_data = {
        'video_path': video_path,
        'caption': caption,
        'hashtags': hashtags if isinstance(hashtags, list) else hashtags.split(),
        'schedule_time': schedule_time,
        'auto_publish': tiktok_config.get('autoPublish', False),
        'max_videos_per_month': max_videos,
        'current_month': current_month,
        'status': 'ready',
        'created_at': datetime.now().isoformat(),
        'note': 'Используйте MCP skill "tiktok-automation" для публикации'
    }
    
    log_message(f"✓ Видео готово к загрузке")
    return upload_data

def schedule_posts(content_calendar):
    """
    Планирование публикаций
    
    Args:
        content_calendar: список постов с датами
    
    Returns:
        dict с расписанием
    """
    log_message("Планирование публикаций")
    
    schedule = {
        'created_at': datetime.now().isoformat(),
        'posts': []
    }
    
    for i, post in enumerate(content_calendar):
        post_schedule = {
            'post_id': i + 1,
            'content': post.get('content', ''),
            'scheduled_date': post.get('date'),
            'scheduled_time': post.get('time', '18:00'),  # Оптимальное время
            'status': 'scheduled',
        }
        schedule['posts'].append(post_schedule)
    
    log_message(f"✓ Запланировано {len(schedule['posts'])} постов")
    return schedule

def get_optimal_posting_times():
    """
    Получение оптимального времени для публикаций
    
    Returns:
        dict с рекомендациями по времени
    """
    return {
        'best_times': {
            'monday': ['6:00', '10:00', '22:00'],
            'tuesday': ['2:00', '4:00', '9:00'],
            'wednesday': ['7:00', '8:00', '23:00'],
            'thursday': ['9:00', '12:00', '19:00'],
            'friday': ['5:00', '13:00', '15:00'],
            'saturday': ['11:00', '19:00', '20:00'],
            'sunday': ['7:00', '8:00', '16:00'],
        },
        'timezone': 'UTC',
        'note': 'Время может варьироваться в зависимости от вашей аудитории',
        'tip': 'Экспериментируйте с разным временем для поиска оптимального'
    }

def analytics_report(video_stats):
    """
    Создание отчета по аналитике
    
    Args:
        video_stats: статистика по видео
    
    Returns:
        dict с аналитическим отчетом
    """
    log_message("Создание аналитического отчета")
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'videos_analyzed': len(video_stats) if isinstance(video_stats, list) else 1,
        'metrics': {
            'total_views': sum(v.get('views', 0) for v in video_stats) if isinstance(video_stats, list) else video_stats.get('views', 0),
            'total_likes': sum(v.get('likes', 0) for v in video_stats) if isinstance(video_stats, list) else video_stats.get('likes', 0),
            'total_comments': sum(v.get('comments', 0) for v in video_stats) if isinstance(video_stats, list) else video_stats.get('comments', 0),
            'total_shares': sum(v.get('shares', 0) for v in video_stats) if isinstance(video_stats, list) else video_stats.get('shares', 0),
        },
        'engagement_rate': 'calculate: (likes + comments + shares) / views * 100',
        'note': 'Используйте MCP skill "tiktok-automation" для получения актуальной статистики'
    }
    
    # Расчет engagement rate
    if report['metrics']['total_views'] > 0:
        engagement = (
            report['metrics']['total_likes'] + 
            report['metrics']['total_comments'] + 
            report['metrics']['total_shares']
        ) / report['metrics']['total_views'] * 100
        report['engagement_rate'] = f"{engagement:.2f}%"
    
    log_message(f"✓ Аналитический отчет создан")
    return report

def weekly_analytics_summary():
    """
    Генерация еженедельного отчета
    
    Returns:
        dict с недельной сводкой
    """
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    summary = {
        'period': {
            'start': week_start.strftime('%Y-%m-%d'),
            'end': today.strftime('%Y-%m-%d'),
        },
        'generated_at': datetime.now().isoformat(),
        'metrics': {
            'videos_published': 0,
            'total_views': 0,
            'total_engagement': 0,
        },
        'top_performing_video': None,
        'recommendations': [
            'Публикуйте в часы пик активности',
            'Используйте трендовые хэштеги',
            'Создавайте контент длиной 15-60 секунд',
            'Добавляйте призыв к действию',
        ],
        'note': 'Используйте MCP skill "tiktok-automation" для получения актуальных данных'
    }
    
    return summary

def main():
    """Основная функция"""
    import sys
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'help'
    
    print(f"📱 TikTok Publishing & Analytics")
    print("=" * 50)
    
    if command == 'prepare':
        # Подготовка видео к загрузке
        video_path = sys.argv[2] if len(sys.argv) > 2 else 'output/videos/sample.mp4'
        caption = sys.argv[3] if len(sys.argv) > 3 else 'Amazing content! #fyp #viral'
        
        upload_data = prepare_video_for_upload(video_path, caption, '#fyp #viral')
        print(json.dumps(upload_data, indent=2))
        
    elif command == 'schedule':
        # Планирование публикаций
        optimal_times = get_optimal_posting_times()
        print("Оптимальное время для публикаций:")
        print(json.dumps(optimal_times, indent=2))
        
    elif command == 'analytics':
        # Аналитика
        summary = weekly_analytics_summary()
        print("Еженедельный отчет:")
        print(json.dumps(summary, indent=2))
        
    else:
        print("""
Команды:
  prepare [video_path] [caption]  - Подготовка видео к загрузке
  schedule                        - Показать оптимальное время для публикаций
  analytics                       - Еженедельный аналитический отчет
  help                            - Показать эту справку

MCP Skills для использования:
  - tiktok-automation: публикация видео и получение статистики
  - tiktok-captions: генерация описаний и хэштегов
        """)
    
    log_message(f"Выполнена команда: {command}")

if __name__ == '__main__':
    main()
