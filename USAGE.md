# TikTok Automation - Инструкция по использованию

## 🚀 Быстрый старт

### 1. Исследование трендов

#### Через MCP Skill (рекомендуется):
```
skill: social-media-trends-research
```

#### Через Python скрипт:
```bash
cd /root/tiktokproject
python scripts/research_trends.py general
```

**Ниши для исследования:**
- `general` - общие тренды
- `dance` - танцы
- `comedy` - комедия
- `education` - образование
- `fitness` - фитнес
- `food` - еда/рецепты

---

### 2. Создание контента из YouTube

#### Шаг 1: Поиск видео
```
skill: youtube-search
```
**Промпт:** "Найди видео про [тема] для создания TikTok клипов"

#### Шаг 2: Создание клипа
```
skill: youtube-clipper
```
**Промпт:** "Создай 60-секундный клип из этого видео: [URL]"

#### Шаг 3: Генерация описания
```
skill: tiktok-captions
```
**Промпт:** "Создай заголовок и хэштеги для TikTok видео про [тема]"

#### Через Python скрипт:
```bash
python scripts/create_content.py "viral trends"
```

---

### 3. Публикация в TikTok

#### Через MCP Skill:
```
skill: tiktok-automation
```
**Промпт:** "Опубликуй видео с описанием: [текст] и хэштегами: #fyp #viral"

#### Через Python скрипт:
```bash
# Подготовка к публикации
python scripts/publish.py prepare output/videos/myvideo.mp4 "Amazing content! #fyp"

# Просмотр оптимального времени
python scripts/publish.py schedule

# Просмотр аналитики
python scripts/publish.py analytics
```

---

### 4. Telegram уведомления

#### Настройка бота:
```
skill: telegram-bot-builder
```

#### Или через скрипт:
```bash
# Руководство по настройке
python scripts/telegram_bot.py guide

# Настройка после получения токена
python scripts/telegram_bot.py setup <BOT_TOKEN> <CHAT_ID>

# Проверка статуса
python scripts/telegram_bot.py status
```

---

### 5. Google Drive синхронизация

#### Через shell скрипт:
```bash
# Синхронизация архива
./scripts/sync_drive.sh sync

# Резервное копирование
./scripts/sync_drive.sh backup

# Всё вместе
./scripts/sync_drive.sh all

# Показать использование хранилища
./scripts/sync_drive.sh status
```

#### Через npm скрипт:
```bash
npm run sync-drive
```

---

## 📊 Доступные MCP Skills

| Skill | Назначение | Команда |
|-------|------------|---------|
| **social-media-trends-research** | Исследование трендов | `skill: social-media-trends-research` |
| **youtube-search** | Поиск YouTube видео | `skill: youtube-search` |
| **youtube-clipper** | Создание клипов | `skill: youtube-clipper` |
| **tiktok-captions** | Генерация описаний | `skill: tiktok-captions` |
| **tiktok-automation** | Публикация видео | `skill: tiktok-automation` |
| **telegram-bot-builder** | Создание ботов | `skill: telegram-bot-builder` |
| **videoagent-video-studio** | Редактирование видео | `skill: videoagent-video-studio` |

---

## 📁 Структура проекта

```
/root/tiktokproject/
├── scripts/              # Python/Bash скрипты
│   ├── research_trends.py    # Исследование трендов
│   ├── create_content.py     # Создание контента
│   ├── publish.py            # Публикация и аналитика
│   ├── telegram_bot.py       # Telegram бот
│   └── sync_drive.sh         # Google Drive синхронизация
├── config/               # Конфигурация
│   └── settings.json         # Настройки проекта
├── output/               # Результаты работы
│   ├── videos/               # Готовые видео
│   ├── captions/             # Тексты и хэштеги
│   └── reports/              # Отчёты и аналитика
├── archive/              # Архив (синхронизируется с GD)
└── logs/               # Логи
```

---

## 🔧 Конфигурация

### config/settings.json

```json
{
  "tiktok": {
    "maxVideosPerMonth": 20,
    "defaultHashtagCount": 5,
    "autoPublish": false
  },
  "youtube": {
    "maxClipDuration": 60,
    "preferredQuality": "720p"
  },
  "storage": {
    "provider": "google-drive",
    "rcloneRemote": "gdrive"
  },
  "telegram": {
    "enabled": false,
    "botToken": "",
    "chatId": ""
  }
}
```

---

## 💡 Примеры использования

### Пример 1: Создание видео про тренды

1. Исследуем тренды:
   ```
   skill: social-media-trends-research
   ```

2. Ищем контент на YouTube:
   ```
   skill: youtube-search
   Промпт: "Найди популярные видео про тренды 2024"
   ```

3. Создаем клип:
   ```
   skill: youtube-clipper
   Промпт: "Создай 60-секундный клип из [URL]"
   ```

4. Генерируем описание:
   ```
   skill: tiktok-captions
   Промпт: "Создай описание для видео про тренды"
   ```

5. Публикуем:
   ```
   skill: tiktok-automation
   Промпт: "Опубликуй видео [путь] с описанием [текст]"
   ```

### Пример 2: Еженедельная аналитика

```bash
# Запуск аналитики
python scripts/publish.py analytics

# Синхронизация с Google Drive
./scripts/sync_drive.sh all
```

---

## ⚠️ Ограничения бесплатной версии

| Сервис | Лимит |
|--------|-------|
| TikTok API (Composio) | ~10-20 видео/месяц |
| Google Drive | 15 GB бесплатно |
| YouTube API | 10000 единиц/день |
| Telegram Bot API | Безлимитно |

---

## 🔐 Безопасность

**Важно:** Никогда не коммитьте файлы с секретами:
- `prompts-instructions/QWEN.md`
- `prompts-instructions/oauth_creds.json`
- `config/secrets.json`
- `config/.env`

Эти файлы добавлены в `.gitignore`.

---

## 📞 Поддержка

GitHub: https://github.com/OlehHavrilko/tiktok-automation
