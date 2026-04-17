# TikTok Automation Project - Complete Implementation Guide

## 📋 Обзор проекта

Полностью функциональная система автоматизации TikTok, использующая **бесплатные API** и **trial версии** без необходимости локальной развертки сложных сервисов.

---

## 🎯 Реализованные возможности

### ✅ Этап 1: Исследование трендов
- **Google Trends** через pytrends (бесплатно)
- **Reddit мониторинг** через yars (бесплатно, без API)
- **Perplexity MCP** для Twitter/TikTok/Web анализа (бесплатно)

### ✅ Этап 2: Создание контента
- **YouTube поиск** через youtube-search MCP (бесплатно)
- **Создание клипов** через youtube-clipper MCP (бесплатно)
- **Генерация описаний** через tiktok-captions MCP (бесплатно)
- **Видео редактирование** через videoagent-video-studio (бесплатно)

### ✅ Этап 3: Публикация
- **TikTok публикация** через tiktok-automation MCP (бесплатно, ~10-20 видео/мес)
- **Планирование** по оптимальному времени
- **Автоматические хэштеги**

### ✅ Этап 4: Аналитика
- **Статистика видео** через tiktok-automation MCP
- **Engagement rate** расчет
- **Еженедельные отчеты**

### ✅ Этап 5: Инфраструктура
- **Telegram бот** для уведомлений (бесплатно)
- **Google Drive архив** 15GB через rclone (бесплатно)
- **Логирование** всех операций

---

## 📁 Структура проекта

```
/root/tiktokproject/
├── scripts/
│   ├── main.py                 # Главный оркестратор
│   ├── research_trends.py      # Исследование трендов
│   ├── create_content.py       # Создание контента
│   ├── publish.py              # Публикация и аналитика
│   ├── telegram_bot.py         # Telegram бот
│   └── sync_drive.sh           # Google Drive синхронизация
├── config/
│   └── settings.json           # Настройки проекта
├── output/
│   ├── videos/                 # Готовые видео
│   ├── captions/               # Описания и хэштеги
│   └── reports/                # Отчёты и аналитика
├── archive/                    # Архив (Google Drive sync)
├── logs/                       # Логи операций
├── README.md                   # Основная документация
├── USAGE.md                    # Инструкция по использованию
└── package.json                # NPM скрипты
```

---

## 🚀 Быстрый старт

### 1. Запуск через главное меню

```bash
cd /root/tiktokproject
python scripts/main.py
```

### 2. Использование npm скриптов

```bash
# Исследование трендов
npm run research

# Создание контента
npm run create-content

# Публикация
npm run publish

# Аналитика
npm run analytics

# Синхронизация с Google Drive
npm run sync-drive

# Полный пайплайн
npm run full
```

### 3. Прямой вызов скриптов

```bash
# Исследование для ниши "dance"
python scripts/research_trends.py dance

# Создание контента по теме
python scripts/create_content.py "viral trends"

# Подготовка к публикации
python scripts/publish.py prepare video.mp4 "Description #hashtags"

# Настройка Telegram бота
python scripts/telegram_bot.py guide
```

---

## 🔧 MCP Skills - Сердце системы

### Доступные бесплатные skills:

| Skill | Команда | Лимиты |
|-------|---------|--------|
| **social-media-trends-research** | `skill: social-media-trends-research` | Бесплатно |
| **youtube-search** | `skill: youtube-search` | Бесплатно |
| **youtube-clipper** | `skill: youtube-clipper` | Бесплатно |
| **tiktok-captions** | `skill: tiktok-captions` | Бесплатно |
| **tiktok-automation** | `skill: tiktok-automation` | ~10-20 видео/мес |
| **telegram-bot-builder** | `skill: telegram-bot-builder` | Бесплатно |
| **videoagent-video-studio** | `skill: videoagent-video-studio` | Бесплатно |

### Примеры использования:

```
# Исследование трендов
skill: social-media-trends-research
Промпт: "Найди тренды для ниши dance в TikTok"

# Поиск YouTube
skill: youtube-search
Промпт: "Найди популярные видео про fitness tips"

# Создание клипа
skill: youtube-clipper
Промпт: "Создай 60-секундный клип из https://youtube.com/watch?v=..."

# Генерация описания
skill: tiktok-captions
Промпт: "Создай описание и хэштеги для fitness видео"

# Публикация
skill: tiktok-automation
Промпт: "Опубликуй видео с описанием: ..."
```

---

## 📊 Ограничения бесплатной реализации

| Сервис | Бесплатный лимит | Примечание |
|--------|------------------|------------|
| **TikTok API (Composio)** | 10-20 видео/мес | Достаточно для старта |
| **Google Drive** | 15 GB | ~100 видео в сжатом формате |
| **YouTube API** | 10000 квот/день | Очень много |
| **Telegram Bot** | Безлимитно | Полностью бесплатно |
| **Perplexity MCP** | Бесплатно | Web/Twitter/TikTok поиск |
| **Reddit (yars)** | Безлимитно | Без API ключа |

---

## 💡 Типовые сценарии использования

### Сценарий 1: Создание вирусного видео

```bash
# 1. Исследуем тренды
python scripts/research_trends.py general

# 2. Ищем контент на YouTube
skill: youtube-search
Промпт: "Найди вирусные видео про life hacks"

# 3. Создаем клип
skill: youtube-clipper
Промпт: "Создай 60-секундный клип из [URL]"

# 4. Генерируем описание
skill: tiktok-captions
Промпт: "Создай описание для life hacks видео"

# 5. Публикуем
skill: tiktok-automation
Промпт: "Опубликуй видео [path] с описанием [text]"

# 6. Архивируем
./scripts/sync_drive.sh sync
```

### Сценарий 2: Еженедельная аналитика

```bash
# Получаем статистику
python scripts/publish.py analytics

# Проверяем отчеты
ls -la output/reports/

# Синхронизируем с Google Drive
./scripts/sync_drive.sh all
```

### Сценарий 3: Настройка уведомлений

```bash
# Получаем инструкцию
python scripts/telegram_bot.py guide

# Создаем бота через @BotFather
# Получаем токен и chat ID

# Настраиваем
python scripts/telegram_bot.py setup TOKEN CHAT_ID

# Проверяем статус
python scripts/telegram_bot.py status
```

---

## 🔐 Безопасность

### Файлы, которые НЕЛЬЗЯ коммитить:

```
prompts-instructions/QWEN.md
prompts-instructions/oauth_creds.json
config/secrets.json
config/.env
*.log
```

Эти файлы уже в `.gitignore`.

### GitHub репозиторий:

https://github.com/OlehHavrilko/tiktok-automation

---

## 📈 Roadmap

### Реализовано (Этапы 1-5):
- ✅ Исследование трендов
- ✅ Создание контента из YouTube
- ✅ Публикация в TikTok
- ✅ Аналитика и отчеты
- ✅ Telegram уведомления
- ✅ Google Drive архив

### Опционально (Этап 6):
- ⏳ TikTok Ads (Trial версия)
- ⏳ TON Blockchain интеграция
- ⏳ Telegram Mini App

---

## 🛠️ Требования

### Системные:
- Python 3.9+
- Node.js 18+
- rclone (для Google Drive)
- Git

### Python зависимости:
```bash
pip install pytrends requests python-dotenv
```

### Настройка rclone:
```bash
# Установка
curl https://rclone.org/install.sh | sudo bash

# Настройка Google Drive
rclone config
→ New remote → name: gdrive → drive → OAuth
```

---

## 📞 Поддержка и контакты

- **GitHub**: https://github.com/OlehHavrilko/tiktok-automation
- **Автор**: Oleh Havrilko

---

## 📄 Лицензия

MIT License - свободное использование с указанием авторства.
