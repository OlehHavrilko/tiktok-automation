#!/usr/bin/env python3
"""
Telegram Bot for TikTok Notifications
Бот для уведомлений о новых публикациях и управления контентом
"""

import json
import os
from datetime import datetime

# Пути
CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

def log_message(message):
    """Логирование сообщений"""
    os.makedirs(LOGS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}\n"
    
    logfile = os.path.join(LOGS_DIR, 'telegram_bot.log')
    with open(logfile, 'a', encoding='utf-8') as f:
        f.write(log_entry)
    print(log_entry.strip())

def load_bot_config():
    """Загрузка конфигурации бота"""
    config_path = os.path.join(CONFIG_DIR, 'settings.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('telegram', {})
    return {'enabled': False}

def save_bot_config(token, chat_id):
    """Сохранение конфигурации бота"""
    config_path = os.path.join(CONFIG_DIR, 'settings.json')
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config['telegram'] = {
        'enabled': True,
        'botToken': token,
        'chatId': chat_id
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    log_message("✓ Конфигурация бота сохранена")

def create_bot_setup_guide():
    """
    Создание руководства по настройке Telegram бота
    
    Returns:
        dict с инструкциями
    """
    guide = {
        'title': 'Telegram Bot Setup Guide',
        'steps': [
            {
                'step': 1,
                'action': 'Создать бота',
                'description': 'Напишите @BotFather в Telegram',
                'commands': [
                    '/newbot - создать нового бота',
                    'Введите имя бота (например: TikTok Notifier)',
                    'Введите username бота (должен заканчиваться на bot)',
                ]
            },
            {
                'step': 2,
                'action': 'Получить токен',
                'description': 'BotFather выдаст API токен',
                'warning': 'Никогда не публикуйте токен в открытом доступе!'
            },
            {
                'step': 3,
                'action': 'Получить Chat ID',
                'description': 'Напишите @userinfobot в Telegram',
                'result': 'Бот вернет ваш Chat ID'
            },
            {
                'step': 4,
                'action': 'Сохранить конфигурацию',
                'description': 'Запустите скрипт с токеном и chat ID',
                'command': 'python scripts/telegram_bot.py setup <TOKEN> <CHAT_ID>'
            }
        ],
        'features': [
            'Уведомления о новых публикациях',
            'Статистика по видео',
            'Напоминания о времени публикации',
            'Быстрые команды управления',
        ],
        'bot_commands': {
            '/start': 'Запустить бота',
            '/stats': 'Показать статистику',
            '/schedule': 'Расписание публикаций',
            '/settings': 'Настройки уведомлений',
            '/help': 'Помощь',
        }
    }
    
    return guide

def send_notification_template(message_type='new_video'):
    """
    Шаблон уведомления для отправки
    
    Args:
        message_type: тип уведомления
    
    Returns:
        dict с шаблоном сообщения
    """
    templates = {
        'new_video': {
            'text': '''
🎬 Новое видео опубликовано!

📹 {video_title}

📊 Статистика за 24 часа:
• Просмотры: {views}
• Лайки: {likes}
• Комментарии: {comments}

#TikTok #NewContent
            ''',
            'parse_mode': 'Markdown'
        },
        'weekly_summary': {
            'text': '''
📈 Недельный отчет

🎥 Видео опубликовано: {videos_count}
👁️ Всего просмотров: {total_views}
❤️ Всего лайков: {total_likes}
💬 Комментариев: {total_comments}

🔥 Лучшее видео: {top_video}

Продолжайте в том же духе! 🚀
            ''',
            'parse_mode': 'Markdown'
        },
        'reminder': {
            'text': '''
⏰ Напоминание о публикации

Пора публиковать новое видео!
Оптимальное время: {optimal_time}

Готовы к публикации? 🎬
            ''',
            'parse_mode': 'Markdown'
        }
    }
    
    return templates.get(message_type, templates['new_video'])

def bot_health_check():
    """
    Проверка статуса бота
    
    Returns:
        dict со статусом
    """
    config = load_bot_config()
    
    status = {
        'enabled': config.get('enabled', False),
        'token_configured': bool(config.get('botToken')),
        'chat_id_configured': bool(config.get('chatId')),
        'status': 'not_configured',
    }
    
    if config.get('enabled') and config.get('botToken') and config.get('chatId'):
        status['status'] = 'ready'
    elif config.get('botToken') and config.get('chatId'):
        status['status'] = 'configured_not_enabled'
    
    return status

def main():
    """Основная функция"""
    import sys
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'help'
    
    print(f"🤖 Telegram Bot для TikTok")
    print("=" * 50)
    
    if command == 'setup':
        if len(sys.argv) < 4:
            print("Использование: python telegram_bot.py setup <TOKEN> <CHAT_ID>")
            return
        
        token = sys.argv[2]
        chat_id = sys.argv[3]
        save_bot_config(token, chat_id)
        print("✓ Бот настроен!")
        
    elif command == 'guide':
        guide = create_bot_setup_guide()
        print(json.dumps(guide, indent=2, ensure_ascii=False))
        
    elif command == 'status':
        status = bot_health_check()
        print("Статус бота:")
        print(json.dumps(status, indent=2))
        
    elif command == 'template':
        msg_type = sys.argv[2] if len(sys.argv) > 2 else 'new_video'
        template = send_notification_template(msg_type)
        print(f"Шаблон: {msg_type}")
        print(template['text'])
        
    else:
        print("""
Команды:
  setup <TOKEN> <CHAT_ID>  - Настроить бота
  guide                    - Руководство по настройке
  status                   - Проверить статус
  template [type]          - Показать шаблон уведомления
  help                     - Показать эту справку

Для полноценной работы используйте MCP skill "telegram-bot-builder"
        """)
    
    log_message(f"Выполнена команда: {command}")

if __name__ == '__main__':
    main()
