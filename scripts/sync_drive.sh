#!/bin/bash
# Google Drive Sync Script
# Синхронизация файлов проекта с Google Drive через rclone

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Пути
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ARCHIVE_DIR="$PROJECT_DIR/archive"
LOGS_DIR="$PROJECT_DIR/logs"

# Rclone remote (должен быть настроен)
RCLONE_REMOTE="gdrive"
REMOTE_PATH="/tiktok-project/archive"

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
    exit 1
}

# Проверка наличия rclone
check_rclone() {
    if ! command -v rclone &> /dev/null; then
        error "rclone не найден! Установите: https://rclone.org/install/"
    fi
    log "✓ rclone найден"
}

# Проверка настройки remote
check_remote() {
    if ! rclone listremotes | grep -q "^${RCLONE_REMOTE}:$"; then
        warn "Remote '${RCLONE_REMOTE}' не настроен"
        echo ""
        echo "Для настройки выполните:"
        echo "  rclone config"
        echo "  → New remote → name: gdrive → drive → OAuth"
        echo ""
        echo "Или используйте авторизацию через браузер:"
        echo "  rclone authorize drive"
        echo ""
        exit 1
    fi
    log "✓ Remote '${RCLONE_REMOTE}' настроен"
}

# Синхронизация архива
sync_archive() {
    log "Синхронизация архива..."
    
    # Создание удаленной директории
    rclone mkdir "${RCLONE_REMOTE}:${REMOTE_PATH}" 2>/dev/null || true
    
    # Синхронизация (двусторонняя)
    rclone sync "$ARCHIVE_DIR" "${RCLONE_REMOTE}:${REMOTE_PATH}" \
        --progress \
        --transfers=4 \
        --checkers=8 \
        --exclude "*.log" \
        --exclude ".gitkeep"
    
    log "✓ Архив синхронизирован"
}

# Синхронизация логов (опционально)
sync_logs() {
    warn "Синхронизация логов не рекомендуется (локальные файлы)"
    # rclone sync "$LOGS_DIR" "${RCLONE_REMOTE}:/tiktok-project/logs"
}

# Резервное копирование конфигов
backup_configs() {
    log "Резервное копирование конфигурации..."
    
    CONFIG_BACKUP_PATH="${RCLONE_REMOTE}:/tiktok-project/config-backup"
    rclone sync "$PROJECT_DIR/config" "$CONFIG_BACKUP_PATH" \
        --exclude "secrets.json" \
        --exclude ".env"
    
    log "✓ Конфигурация сохранена"
}

# Показать использование хранилища
show_storage_usage() {
    log "Использование Google Drive:"
    echo ""
    rclone about "${RCLONE_REMOTE}:"
    echo ""
}

# Очистка старых файлов на remote (опционально)
cleanup_old_files() {
    warn "Очистка файлов старше 30 дней..."
    
    # Удаление файлов старше 30 дней
    rclone delete "${RCLONE_REMOTE}:${REMOTE_PATH}" \
        --min-age 30d \
        --exclude ".gitkeep"
    
    log "✓ Очистка завершена"
}

# Показать помощь
show_help() {
    echo "TikTok Project - Google Drive Sync"
    echo ""
    echo "Использование:"
    echo "  $0 [command]"
    echo ""
    echo "Команды:"
    echo "  sync      - Синхронизировать архив"
    echo "  backup    - Резервное копирование конфигурации"
    echo "  status    - Показать статус хранилища"
    echo "  cleanup   - Очистить старые файлы"
    echo "  all       - Выполнить всё (sync + backup)"
    echo "  help      - Показать эту справку"
    echo ""
    echo "Примеры:"
    echo "  $0 sync"
    echo "  $0 all"
}

# Основная функция
main() {
    local command="${1:-help}"
    
    case "$command" in
        sync)
            check_rclone
            check_remote
            sync_archive
            ;;
        backup)
            check_rclone
            check_remote
            backup_configs
            ;;
        status)
            check_rclone
            check_remote
            show_storage_usage
            ;;
        cleanup)
            check_rclone
            check_remote
            cleanup_old_files
            ;;
        all)
            check_rclone
            check_remote
            sync_archive
            backup_configs
            show_storage_usage
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Неизвестная команда: $command"
            show_help
            ;;
    esac
}

main "$@"
