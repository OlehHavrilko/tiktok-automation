#!/usr/bin/env python3
"""
AutoClipper - Автоматическая обработка видео для TikTok
Аналог OpenCLAW: скачивание, нарезка, конвертация, субтитры
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Пути
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / 'output'
VIDEOS_DIR = OUTPUT_DIR / 'videos'
TEMP_DIR = OUTPUT_DIR / 'temp'
LOGS_DIR = BASE_DIR / 'logs'

def log_message(message):
    """Логирование сообщений"""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    
    logfile = LOGS_DIR / 'autoclipper.log'
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')
    print(log_entry)

def ensure_dirs():
    """Создание необходимых директорий"""
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

def download_video(youtube_url, output_template=None):
    """
    Скачивание видео с YouTube
    
    Args:
        youtube_url: URL YouTube видео
        output_template: шаблон имени файла
    
    Returns:
        str: путь к скачанному файлу
    """
    log_message(f"📥 Скачивание: {youtube_url}")
    ensure_dirs()
    
    if output_template is None:
        video_id = youtube_url.split('v=')[1].split('&')[0] if 'v=' in youtube_url else f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_template = str(TEMP_DIR / f"{video_id}.%(ext)s")
    
    cmd = [
        'yt-dlp',
        '-f', 'best[ext=mp4]/best',
        '--no-merge',
        '-o', output_template,
        '--no-playlist',
        '--extractor-args', 'youtube:player_client=web',
        youtube_url
    ]
    
    log_message(f"Выполнение: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Находим скачанный файл
        downloaded_file = None
        for line in result.stdout.split('\n'):
            if 'Destination:' in line or 'Merging formats' in line:
                # Извлекаем имя файла
                pass
        
        # Ищем файл в temp директории
        video_id = youtube_url.split('v=')[1].split('&')[0] if 'v=' in youtube_url else None
        if video_id:
            for f in TEMP_DIR.glob(f"{video_id}.*"):
                if f.suffix in ['.mp4', '.mkv', '.webm']:
                    downloaded_file = str(f)
                    break
        
        if not downloaded_file:
            # Берем первый видеофайл в temp
            for f in TEMP_DIR.glob('*.*'):
                if f.suffix in ['.mp4', '.mkv', '.webm']:
                    downloaded_file = str(f)
                    break
        
        if downloaded_file:
            log_message(f"✓ Видео скачано: {downloaded_file}")
            return downloaded_file
        else:
            log_message("❌ Не удалось найти скачанный файл")
            return None
            
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Ошибка скачивания: {e.stderr}")
        return None

def get_video_duration(video_path):
    """Получение длительности видео"""
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return None

def extract_clip(source_path, start_time, end_time, output_path):
    """
    Вырезка клипа из видео
    
    Args:
        source_path: путь к исходному видео
        start_time: время начала (секунды или "mm:ss")
        end_time: время конца (секунды или "mm:ss")
        output_path: путь для сохранения
    
    Returns:
        str: путь к вырезанному клипу
    """
    log_message(f"✂️ Нарезка: {start_time} - {end_time}")
    
    # Конвертируем время в секунды если нужно
    def parse_time(t):
        if isinstance(t, (int, float)):
            return t
        if ':' in str(t):
            parts = str(t).split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        return float(t)
    
    start_sec = parse_time(start_time)
    end_sec = parse_time(end_time)
    duration = end_sec - start_sec
    
    cmd = [
        'ffmpeg',
        '-i', source_path,
        '-ss', str(start_sec),
        '-t', str(duration),
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',  # Перезаписать если существует
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_message(f"✓ Клип создан: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Ошибка нарезки: {e.stderr}")
        return None

def convert_to_tiktok_format(input_path, output_path):
    """
    Конвертация видео в формат TikTok (9:16, 1080x1920)
    
    Args:
        input_path: путь к исходному видео
        output_path: путь для сохранения
    
    Returns:
        str: путь к конвертированному видео
    """
    log_message("🔄 Конвертация в формат TikTok (9:16)")
    
    # Обрезаем до 9:16 и масштабируем до 1080x1920
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', 'crop=ih*(9/16):ih,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_message(f"✓ Конвертация завершена: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Ошибка конвертации: {e.stderr}")
        return None

def add_subtitles(input_path, subtitle_text, output_path, position='bottom'):
    """
    Добавление субтитров на видео
    
    Args:
        input_path: путь к видео
        subtitle_text: текст субтитров
        output_path: путь для сохранения
        position: позиция (top, bottom, center)
    
    Returns:
        str: путь к видео с субтитрами
    """
    log_message(f"📝 Добавление субтитров: {subtitle_text[:50]}...")
    
    # Позиция текста
    y_pos = {'top': 'h*0.1', 'center': 'h*0.5', 'bottom': 'h*0.85'}.get(position, 'h*0.85')
    
    # Экранирование текста для ffmpeg
    escaped_text = subtitle_text.replace("'", "'\\''").replace('"', '\\"')
    
    filter_complex = f"drawtext=text='{escaped_text}':fontsize=48:fontcolor=white:border=1:bordercolor=black:x=(w-text_w)/2:y={y_pos}"
    
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', filter_complex,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',
        '-y',
        output_path
    ]
    
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_message(f"✓ Субтитры добавлены: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        log_message(f"❌ Ошибка добавления субтитров: {e.stderr}")
        # Возвращаем оригинальное видео если не получилось
        return input_path

def process_content_plan(plan_path):
    """
    Обработка плана контента из JSON файла
    
    Args:
        plan_path: путь к JSON файлу с планом
    
    Returns:
        list: пути к созданным видео
    """
    log_message(f"📋 Обработка плана: {plan_path}")
    
    with open(plan_path, 'r', encoding='utf-8') as f:
        plan = json.load(f)
    
    created_videos = []
    
    # Получаем список клипов из плана
    clips = plan.get('clips', [])
    if not clips and 'content_plan' in plan:
        # Пробуем другую структуру
        content_plan = plan.get('content_plan', {})
        clips = content_plan.get('clips', [])
    
    if not clips:
        log_message("⚠️ В плане не найдено клипов для обработки")
        return created_videos
    
    for i, clip in enumerate(clips):
        log_message(f"\n🎬 Обработка клипа {i+1}/{len(clips)}")
        
        youtube_url = clip.get('source_url') or clip.get('url') or clip.get('youtube_url')
        start_time = clip.get('start_time', 0)
        end_time = clip.get('end_time', 60)
        caption = clip.get('caption', '')
        hook = clip.get('hook', '')
        
        if not youtube_url:
            log_message("⚠️ Нет URL для клипа, пропускаем")
            continue
        
        # Шаг 1: Скачивание
        downloaded_path = download_video(youtube_url)
        if not downloaded_path:
            continue
        
        # Шаг 2: Нарезка
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        clip_path = str(VIDEOS_DIR / f"clip_{timestamp}_{i+1}.mp4")
        extracted_path = extract_clip(downloaded_path, start_time, end_time, clip_path)
        
        if not extracted_path:
            continue
        
        # Шаг 3: Конвертация в TikTok формат
        converted_path = str(VIDEOS_DIR / f"tiktok_{timestamp}_{i+1}.mp4")
        final_path = convert_to_tiktok_format(extracted_path, converted_path)
        
        if not final_path:
            final_path = extracted_path
        
        # Шаг 4: Добавление субтитров (опционально)
        if hook or caption:
            subtitle_text = hook if hook else caption[:100]
            subtitled_path = str(VIDEOS_DIR / f"final_{timestamp}_{i+1}.mp4")
            result_path = add_subtitles(final_path, subtitle_text, subtitled_path)
            if result_path:
                final_path = result_path
        
        created_videos.append({
            'path': final_path,
            'caption': caption,
            'hook': hook,
            'source': youtube_url,
            'duration': end_time - start_time
        })
        
        log_message(f"✓ Клип {i+1} готов: {final_path}")
    
    # Сохраняем результат
    if created_videos:
        result_path = VIDEOS_DIR / f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump(created_videos, f, ensure_ascii=False, indent=2)
        log_message(f"✓ Результат сохранен: {result_path}")
    
    return created_videos

def auto_clip_from_search(topic, clips_count=3):
    """
    Полный цикл: поиск → скачивание → нарезка → конвертация
    
    Args:
        topic: тема для поиска
        clips_count: количество клипов
    
    Returns:
        list: пути к созданным видео
    """
    log_message(f"🚀 Авто-создание контента: {topic}")
    
    # Здесь должна быть интеграция с YouTube API или MCP skill
    # Для демонстрации создадим заглушку
    
    print("\n⚠️ Для автоматического поиска YouTube нужен API ключ или MCP skill")
    print("Используйте create_content.py для генерации плана, затем запустите:")
    print(f"python scripts/auto_clipper.py --plan <путь_к_плану.json>")
    
    return []

def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AutoClipper для TikTok')
    parser.add_argument('--plan', type=str, help='Путь к JSON плану контента')
    parser.add_argument('--url', type=str, help='YouTube URL для обработки')
    parser.add_argument('--start', type=str, default='0', help='Время начала (сек или mm:ss)')
    parser.add_argument('--end', type=str, default='60', help='Время конца (сек или mm:ss)')
    parser.add_argument('--caption', type=str, default='', help='Текст субтитров')
    parser.add_argument('--topic', type=str, help='Тема для авто-поиска')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎬 AutoClipper - Автоматическая обработка видео для TikTok")
    print("=" * 60)
    
    if args.plan:
        # Обработка плана
        videos = process_content_plan(args.plan)
        print(f"\n✓ Создано видео: {len(videos)}")
        for v in videos:
            print(f"  • {v['path']}")
    
    elif args.url:
        # Обработка одного URL
        ensure_dirs()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        downloaded = download_video(args.url)
        if downloaded:
            clip_path = str(VIDEOS_DIR / f"clip_{timestamp}.mp4")
            extracted = extract_clip(downloaded, args.start, args.end, clip_path)
            
            if extracted:
                final_path = str(VIDEOS_DIR / f"tiktok_{timestamp}.mp4")
                converted = convert_to_tiktok_format(extracted, final_path)
                
                if args.caption and converted:
                    subtitled_path = str(VIDEOS_DIR / f"final_{timestamp}.mp4")
                    converted = add_subtitles(converted, args.caption, subtitled_path)
                
                print(f"\n✓ Видео готово: {converted or final_path}")
    
    elif args.topic:
        # Авто-поиск и создание
        auto_clip_from_search(args.topic)
    
    else:
        print("\nПримеры использования:")
        print("  python auto_clipper.py --plan output/videos/content_plan.json")
        print("  python auto_clipper.py --url https://youtube.com/watch?v=XXX --start 10 --end 70")
        print("  python auto_clipper.py --topic 'comedy fails'")

if __name__ == '__main__':
    main()
