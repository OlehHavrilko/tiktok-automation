# TikTok Automation - Настройка и запуск

## ✅ Уже настроено:
- ✅ Python 3.13.7
- ✅ Node.js 24.13.0
- ✅ rclone (настроен Google Drive remote: `gdrive`)
- ✅ GitHub репозиторий: https://github.com/OlehHavrilko/tiktok-automation

## ⚠️ Требуется установка:

### 1. Установить Python пакеты

```bash
cd /root/tiktokproject
pip3 install pytrends requests python-dotenv
```

### 2. Проверить работу скриптов

```bash
# Тест главного скрипта
python3 scripts/main.py help

# Тест исследования трендов
python3 scripts/research_trends.py general
```

### 3. Настроить MCP Skills (через Qwen Code)

Для работы с TikTok, YouTube и другими сервисами через MCP, активируйте skills:

```
skill: social-media-trends-research
skill: youtube-search
skill: youtube-clipper
skill: tiktok-captions
skill: tiktok-automation
skill: telegram-bot-builder
```

### 4. (Опционально) Настроить Telegram бота

```bash
# Получить инструкцию
python3 scripts/telegram_bot.py guide

# После создания бота в @BotFather:
python3 scripts/telegram_bot.py setup <BOT_TOKEN> <CHAT_ID>
```

### 5. (Опционально) Проверить Google Drive синхронизацию

```bash
# Тест синхронизации
./scripts/sync_drive.sh status

# Синхронизация
./scripts/sync_drive.sh sync
```

---

## 🚀 Команды для запуска:

### Через Python:
```bash
# Главное меню
python3 scripts/main.py

# Полный пайплайн
python3 scripts/main.py full general

# Отдельные этапы
python3 scripts/research_trends.py general
python3 scripts/create_content.py "viral trends"
python3 scripts/publish.py analytics
```

### Через npm:
```bash
npm run start
npm run full
npm run research
npm run create-content
npm run publish
npm run sync-drive
```

---

## 📋 Чеклист готовности:

- [ ] Установить Python пакеты: `pip3 install pytrends requests python-dotenv`
- [ ] Протестировать главный скрипт: `python3 scripts/main.py help`
- [ ] Активировать MCP skills в Qwen Code
- [ ] (Опционально) Настроить Telegram бота
- [ ] (Опционально) Протестировать Google Drive sync

---

## 🔗 Ссылки:

- GitHub: https://github.com/OlehHavrilko/tiktok-automation
- Документация: `USAGE.md`, `IMPLEMENTATION.md`
