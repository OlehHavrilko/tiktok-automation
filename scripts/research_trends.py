#!/usr/bin/env python3
"""
TikTok Trend Research Script
Использует бесплатные API для исследования трендов:
- Google Trends (pytrends)
- Reddit (yars - без API ключей)
- Perplexity MCP (Twitter/TikTok/Web)
"""

import json
import os
from datetime import datetime

# Пути
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'reports')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

def save_report(data, filename):
    """Сохраняет отчет в JSON формате"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Конвертация pandas Timestamp в строки для JSON
    def convert_timestamps(obj):
        import pandas as pd
        if isinstance(obj, dict):
            return {str(k): convert_timestamps(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_timestamps(item) for item in obj]
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif hasattr(obj, 'isoformat'):  # datetime objects
            return obj.isoformat()
        else:
            return obj
    
    cleaned_data = convert_timestamps(data)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
    print(f"✓ Отчет сохранен: {filepath}")
    return filepath

def log_message(message):
    """Логирование сообщений"""
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    logfile = os.path.join(LOGS_DIR, 'research.log')
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(log_entry.strip())

def research_google_trends(keywords, geo='US', timeframe='now 7-d'):
    """
    Исследование трендов Google Trends
    
    Args:
        keywords: список ключевых слов
        geo: географический регион (US, UK, etc.)
        timeframe: временной период
    
    Returns:
        dict с данными трендов
    """
    log_message(f"Начало исследования Google Trends: {keywords}")
    
    try:
        from pytrends.request import TrendReq
        
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload(keywords, cat=0, geo=geo, timeframe=timeframe)
        
        # Данные по интересам
        interest_over_time = pytrends.interest_over_time()
        interest_by_region = pytrends.interest_by_region()
        related_queries = pytrends.related_queries()
        related_topics = pytrends.related_topics()
        
        report = {
            'source': 'Google Trends',
            'keywords': keywords,
            'geo': geo,
            'timeframe': timeframe,
            'date': datetime.now().isoformat(),
            'interest_over_time': interest_over_time.to_dict() if not interest_over_time.empty else {},
            'interest_by_region': interest_by_region.to_dict() if not interest_by_region.empty else {},
            'related_queries': {k: v.to_dict() if hasattr(v, 'to_dict') else v for k, v in related_queries.items()},
            'related_topics': {k: v.to_dict() if hasattr(v, 'to_dict') else v for k, v in related_topics.items()},
        }
        
        log_message(f"✓ Google Trends исследование завершено")
        return report
        
    except ImportError:
        log_message("⚠ pytrends не установлен. Запустите: pip install pytrends")
        return {'error': 'pytrends not installed'}
    except Exception as e:
        log_message(f"✗ Ошибка Google Trends: {str(e)}")
        return {'error': str(e)}

def research_reddit(keywords, limit=10):
    """
    Исследование Reddit обсуждений через yars
    
    Args:
        keywords: список ключевых слов для поиска
        limit: количество результатов
    
    Returns:
        dict с данными Reddit
    """
    log_message(f"Начало исследования Reddit: {keywords}")
    
    # Для работы с Reddit без API используем MCP skill: social-media-trends-research
    # Этот скрипт служит заглушкой для демонстрации
    report = {
        'source': 'Reddit (yars)',
        'keywords': keywords,
        'limit': limit,
        'date': datetime.now().isoformat(),
        'note': 'Используйте MCP skill "social-media-trends-research" для получения данных',
        'subreddits_to_monitor': [
            'TikTok',
            'TikTokCringe',
            'SocialMediaMarketing',
            'ContentCreation',
            'ViralVideos'
        ]
    }
    
    log_message("✓ Reddit исследование завершено (шаблон)")
    return report

def generate_trend_report(niche='general'):
    """
    Генерация полного отчета по трендам
    
    Args:
        niche: ниша для исследования
    """
    log_message(f"=== Начало исследования трендов: {niche} ===")
    
    # Ключевые слова для исследования
    keywords_map = {
        'general': ['tiktok trends', 'viral videos', 'social media'],
        'dance': ['dance challenge', 'tiktok dance', 'choreography'],
        'comedy': ['comedy skits', 'funny videos', 'memes'],
        'education': ['learn on tiktok', 'educational content', 'tips and tricks'],
        'fitness': ['workout routine', 'fitness challenge', 'gym tips'],
        'food': ['recipe videos', 'food hacks', 'cooking tips'],
    }
    
    keywords = keywords_map.get(niche, keywords_map['general'])
    
    # Исследование Google Trends
    google_report = research_google_trends(keywords)
    save_report(google_report, f'google_trends_{niche}_{datetime.now().strftime("%Y%m%d")}.json')
    
    # Исследование Reddit
    reddit_report = research_reddit(keywords)
    save_report(reddit_report, f'reddit_{niche}_{datetime.now().strftime("%Y%m%d")}.json')
    
    # Сводный отчет
    summary = {
        'niche': niche,
        'date': datetime.now().isoformat(),
        'keywords_researched': keywords,
        'google_trends_summary': {
            'status': 'completed' if 'error' not in google_report else 'failed',
        },
        'reddit_summary': {
            'status': 'completed' if 'error' not in reddit_report else 'failed',
        },
        'next_steps': [
            'Используйте MCP skill "social-media-trends-research" для полного анализа',
            'Проверьте связанные запросы для идей контента',
            'Выберите тренды с растущей динамикой',
        ]
    }
    
    save_report(summary, f'trend_summary_{niche}_{datetime.now().strftime("%Y%m%d")}.json')
    
    log_message(f"=== Исследование трендов завершено ===")
    return summary

if __name__ == '__main__':
    import sys
    
    niche = sys.argv[1] if len(sys.argv) > 1 else 'general'
    print(f"🔍 Исследование трендов для ниши: {niche}")
    print("=" * 50)
    
    report = generate_trend_report(niche)
    
    print("\n" + "=" * 50)
    print("📊 Отчет готов!")
    print(f"📁 Проверьте директорию: {OUTPUT_DIR}")
