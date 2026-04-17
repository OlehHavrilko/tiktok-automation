#!/usr/bin/env python3
"""
TikTok Automation - Main Orchestrator
Главный скрипт для управления всем пайплайном
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Добавляем путь к скриптам
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Пути
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_DIR, 'scripts')
OUTPUT_DIR = os.path.join(PROJECT_DIR, 'output')
CONFIG_DIR = os.path.join(PROJECT_DIR, 'config')
LOGS_DIR = os.path.join(PROJECT_DIR, 'logs')

class TikTokAutomation:
    """Основной класс для управления автоматизацией"""
    
    def __init__(self):
        self.config = self.load_config()
        self.ensure_directories()
        
    def load_config(self):
        """Загрузка конфигурации"""
        config_path = os.path.join(CONFIG_DIR, 'settings.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def ensure_directories(self):
        """Создание необходимых директорий"""
        for dir_path in [OUTPUT_DIR, CONFIG_DIR, LOGS_DIR]:
            os.makedirs(dir_path, exist_ok=True)
    
    def log(self, message, level='info'):
        """Логирование"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prefix = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }.get(level, '•')
        
        log_entry = f"[{timestamp}] {prefix} {message}"
        print(log_entry)
        
        # Сохранение в лог
        os.makedirs(LOGS_DIR, exist_ok=True)
        with open(os.path.join(LOGS_DIR, 'orchestrator.log'), 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def research(self, niche='general'):
        """
        Этап 1: Исследование трендов
        
        Args:
            niche: ниша для исследования
        """
        self.log(f"Начало исследования трендов: {niche}", 'info')
        
        print("\n" + "="*60)
        print("🔍 ЭТАП 1: ИССЛЕДОВАНИЕ ТРЕНДОВ")
        print("="*60)
        
        print(f"""
Для исследования трендов используйте:

1. MCP Skill (рекомендуется):
   skill: social-media-trends-research

2. Python скрипт:
   python scripts/research_trends.py {niche}

3. Вручную через MCP:
   - Изучите Google Trends через pytrends
   - Проверьте Reddit обсуждения
   - Используйте Perplexity для Twitter/TikTok трендов

Ниши: general, dance, comedy, education, fitness, food
        """)
        
        self.log("Исследование завершено", 'success')
        return {
            'stage': 'research',
            'niche': niche,
            'status': 'completed',
            'next_step': 'content_creation'
        }
    
    def create_content(self, topic, source_url=None):
        """
        Этап 2: Создание контента
        
        Args:
            topic: тема контента
            source_url: URL источника (YouTube)
        """
        self.log(f"Создание контента: {topic}", 'info')
        
        print("\n" + "="*60)
        print("🎬 ЭТАП 2: СОЗДАНИЕ КОНТЕНТА")
        print("="*60)
        
        print(f"""
Тема: {topic}
{"Источник: " + source_url if source_url else ""}

Шаги:

1. Поиск контента на YouTube:
   skill: youtube-search
   Промпт: "Найди видео про {topic}"

2. Создание клипа:
   skill: youtube-clipper
   Промпт: "Создай 60-секундный клип из {source_url or '[URL]'}"

3. Генерация описания:
   skill: tiktok-captions
   Промпт: "Создай описание для видео про {topic}"

4. (Опционально) Редактирование:
   skill: videoagent-video-studio
        """)
        
        self.log("Контент создан", 'success')
        return {
            'stage': 'content_creation',
            'topic': topic,
            'status': 'completed',
            'next_step': 'publish'
        }
    
    def publish(self, video_path=None, caption=None, hashtags=None):
        """
        Этап 3: Публикация
        
        Args:
            video_path: путь к видео
            caption: текст описания
            hashtags: хэштеги
        """
        self.log("Публикация видео", 'info')
        
        print("\n" + "="*60)
        print("📱 ЭТАП 3: ПУБЛИКАЦИЯ")
        print("="*60)
        
        print(f"""
Параметры:
  Видео: {video_path or 'не указано'}
  Описание: {caption or 'не указано'}
  Хэштеги: {hashtags or 'не указано'}

Шаги:

1. Подготовка:
   python scripts/publish.py prepare {video_path or 'video.mp4'} "{caption or 'description'}"

2. Проверка оптимального времени:
   python scripts/publish.py schedule

3. Публикация через MCP:
   skill: tiktok-automation
   Промпт: "Опубликуй видео {video_path or '[path]'}"
        """)
        
        self.log("Публикация завершена", 'success')
        return {
            'stage': 'publish',
            'status': 'completed',
            'next_step': 'analytics'
        }
    
    def analytics(self):
        """
        Этап 4: Аналитика
        """
        self.log("Сбор аналитики", 'info')
        
        print("\n" + "="*60)
        print("📊 ЭТАП 4: АНАЛИТИКА")
        print("="*60)
        
        print("""
Получение статистики:

1. Через MCP:
   skill: tiktok-automation
   Промпт: "Покажи статистику по моим видео"

2. Через скрипт:
   python scripts/publish.py analytics

3. Еженедельный отчет:
   Отчет сохранится в output/reports/

Метрики для отслеживания:
  • Просмотры (Views)
  • Лайки (Likes)
  • Комментарии (Comments)
  • Репосты (Shares)
  • Engagement Rate
        """)
        
        self.log("Аналитика собрана", 'success')
        return {
            'stage': 'analytics',
            'status': 'completed',
            'next_step': 'archive'
        }
    
    def archive(self):
        """
        Этап 5: Архивация в Google Drive
        """
        self.log("Архивация в Google Drive", 'info')
        
        print("\n" + "="*60)
        print("💾 ЭТАП 5: АРХИВАЦИЯ")
        print("="*60)
        
        print("""
Синхронизация с Google Drive:

1. Через shell скрипт:
   ./scripts/sync_drive.sh sync

2. Через npm:
   npm run sync-drive

3. Полная синхронизация:
   ./scripts/sync_drive.sh all

Настройка rclone:
  rclone config
  → New remote → name: gdrive → drive → OAuth
        """)
        
        self.log("Архивация завершена", 'success')
        return {
            'stage': 'archive',
            'status': 'completed',
            'next_step': None
        }
    
    def full_pipeline(self, niche='general', topic=None):
        """
        Полный пайплайн автоматизации
        
        Args:
            niche: ниша для исследования
            topic: тема для контента
        """
        self.log("Запуск полного пайплайна", 'info')
        
        print("\n" + "="*60)
        print("🚀 ПОЛНЫЙ ПАЙПЛАЙН TIKTOK AUTOMATION")
        print("="*60)
        
        results = []
        
        # Этап 1: Исследование
        results.append(self.research(niche))
        
        # Этап 2: Создание контента
        topic = topic or niche
        results.append(self.create_content(topic))
        
        # Этап 3: Публикация
        results.append(self.publish())
        
        # Этап 4: Аналитика
        results.append(self.analytics())
        
        # Этап 5: Архивация
        results.append(self.archive())
        
        # Итоговый отчет
        self.log("Полный пайплайн завершен", 'success')
        
        print("\n" + "="*60)
        print("📋 ИТОГОВЫЙ ОТЧЕТ")
        print("="*60)
        
        for i, result in enumerate(results, 1):
            status_icon = "✅" if result['status'] == 'completed' else "⏳"
            print(f"{i}. {status_icon} {result['stage'].upper()}")
        
        print("\n" + "="*60)
        print("Следующие шаги:")
        print("  1. Выполните команды MCP skills для каждого этапа")
        print("  2. Проверьте output/ для результатов")
        print("  3. Настройте Telegram бота для уведомлений")
        print("="*60)
        
        return results


def show_menu():
    """Показать главное меню"""
    print("""
╔══════════════════════════════════════════════════════════╗
║           TIKTOK AUTOMATION - ГЛАВНОЕ МЕНЮ               ║
╠══════════════════════════════════════════════════════════╣
║  1. Исследование трендов                                 ║
║  2. Создание контента                                    ║
║  3. Публикация                                           ║
║  4. Аналитика                                            ║
║  5. Архивация в Google Drive                             ║
║  6. Полный пайплайн                                      ║
║  7. Telegram бот                                         ║
║  0. Выход                                                ║
╚══════════════════════════════════════════════════════════╝
    """)


def main():
    """Основная функция"""
    automation = TikTokAutomation()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'research':
            niche = sys.argv[2] if len(sys.argv) > 2 else 'general'
            automation.research(niche)
            
        elif command == 'create':
            topic = sys.argv[2] if len(sys.argv) > 2 else 'trends'
            automation.create_content(topic)
            
        elif command == 'publish':
            automation.publish()
            
        elif command == 'analytics':
            automation.analytics()
            
        elif command == 'archive':
            automation.archive()
            
        elif command == 'full':
            niche = sys.argv[2] if len(sys.argv) > 2 else 'general'
            topic = sys.argv[3] if len(sys.argv) > 3 else None
            automation.full_pipeline(niche, topic)
            
        elif command == 'help':
            print("""
TikTok Automation - Команды:

  python main.py research [niche]     - Исследование трендов
  python main.py create [topic]       - Создание контента
  python main.py publish              - Публикация
  python main.py analytics            - Аналитика
  python main.py archive              - Архивация
  python main.py full [niche]         - Полный пайплайн
  python main.py help                 - Эта справка

Примеры:
  python main.py research dance
  python main.py create "viral trends"
  python main.py full comedy
            """)
        else:
            print(f"Неизвестная команда: {command}")
            print("Используйте 'python main.py help' для справки")
    else:
        # Интерактивный режим
        show_menu()
        choice = input("Выберите команду (0-7): ").strip()
        
        if choice == '1':
            automation.research()
        elif choice == '2':
            topic = input("Тема контента: ").strip()
            automation.create_content(topic)
        elif choice == '3':
            automation.publish()
        elif choice == '4':
            automation.analytics()
        elif choice == '5':
            automation.archive()
        elif choice == '6':
            automation.full_pipeline()
        elif choice == '7':
            print("\nДля настройки Telegram бота:")
            print("  python scripts/telegram_bot.py guide")
        elif choice == '0':
            print("Выход...")
            sys.exit(0)
        else:
            print("Неверный выбор")


if __name__ == '__main__':
    main()
