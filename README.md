# TikTok Automation Project

Автоматизация создания и публикации TikTok контента с использованием бесплатных API и инструментов.

## 🚀 Возможности

- ✅ Исследование трендов (Google Trends, Reddit, Twitter)
- ✅ YouTube → TikTok конвертация
- ✅ Автоматическая генерация заголовков и хэштегов
- ✅ Публикация через TikTok API
- ✅ Аналитика производительности
- ✅ Google Drive архивация
- ✅ Telegram уведомления

## 📁 Структура

```
tiktokproject/
├── scripts/           # Скрипты автоматизации
├── config/           # Конфигурационные файлы
├── output/           # Результат работы
│   ├── videos/       # Готовые видео
│   ├── captions/     # Тексты и хэштеги
│   └── reports/      # Отчёты по аналитике
├── archive/          # Архив контента
└── logs/            # Логи
```

## 🛠️ Используемые инструменты

| Инструмент | Назначение | Стоимость |
|------------|------------|-----------|
| tiktok-automation | Публикация видео | Бесплатно (Composio) |
| tiktok-captions | Генерация контента | Бесплатно |
| social-media-trends-research | Исследование трендов | Бесплатно |
| youtube-search/clipper | Работа с YouTube | Бесплатно |
| Google Drive | Хранение | 15GB бесплатно |
| Telegram Bot API | Уведомления | Бесплатно |

## 📋 Быстрый старт

### 1. Исследование трендов
```bash
# Через MCP skill
skill: social-media-trends-research
```

### 2. Создание контента
```bash
# Поиск контента на YouTube
skill: youtube-search

# Создание клипа
skill: youtube-clipper
```

### 3. Генерация описания
```bash
# Создание заголовков и хэштегов
skill: tiktok-captions
```

### 4. Публикация
```bash
# Загрузка в TikTok
skill: tiktok-automation
```

### 5. Архивация в Google Drive
```bash
npm run sync-drive
```

## 🔧 Конфигурация

### Google Drive
Уже настроен через rclone. Remote name: `gdrive`

### TikTok API
Требуется активация через Composio/Rube MCP

## 📊 Ограничения бесплатной версии

- ~10-20 видео/месяц (лимиты API)
- 15GB Google Drive
- Базовая аналитика

## 📝 Лицензия

MIT
