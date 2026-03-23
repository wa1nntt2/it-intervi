#!/bin/bash
# =============================================================================
# Восстановление PostgreSQL из бэкапа для IT Interview Trainer
# =============================================================================
# Использование:
#   ./scripts/restore_postgres.sh <файл_бэкапа>         # Восстановление из файла
#   ./scripts/restore_postgres.sh --latest              # Последний бэкап
#   ./scripts/restore_postgres.sh --list                # Список доступных бэкапов
#   ./scripts/restore_postgres.sh --help                # Помощь
#
# Требования:
#   - PostgreSQL клиент (psql)
#   - Или Docker Compose для режима --docker
# =============================================================================

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Директории
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="$PROJECT_DIR/backups/postgresql"

# Параметры PostgreSQL по умолчанию
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5433}"
PG_USER="${PG_USER:-interview_admin}"
PG_DB="${PG_DB:-interview_trainer}"
PG_PASSWORD="${PG_PASSWORD:-}"

# Режимы работы
MODE="standard"  # standard, docker
DRY_RUN=false    # Тестовый запуск без изменений
FORCE=false      # Принудительное восстановление без подтверждения

# =============================================================================
# Функции
# =============================================================================

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

show_help() {
    cat << EOF
${GREEN}Восстановление PostgreSQL для IT Interview Trainer${NC}

${BLUE}Использование:${NC}
  $0 [OPTIONS] <файл_бэкапа>

${BLUE}Опции:${NC}
  --latest          Восстановить из последнего бэкапа
  --list            Показать доступные бэкапы
  --docker          Использовать Docker Compose
  --dry-run         Тестовый запуск (без изменений)
  --force           Без подтверждения
  --help            Показать эту справку

${BLUE}Примеры:${NC}
  $0 --latest                           # Последний бэкап
  $0 backups/postgresql/daily/....sql.gz  # Конкретный файл
  $0 --docker --latest                  # Через Docker

${BLUE}Переменные окружения:${NC}
  PG_HOST       Хост PostgreSQL (по умолчанию: localhost)
  PG_PORT       Порт PostgreSQL (по умолчанию: 5433)
  PG_USER       Пользователь PostgreSQL (по умолчанию: interview_admin)
  PG_DB         База данных (по умолчанию: interview_trainer)
  PG_PASSWORD   Пароль PostgreSQL (обязательно для восстановления)

${BLUE}Важно:${NC}
  ⚠️  Восстановление заменит все данные в базе данных!
  ⚠️  Рекомендуется сделать бэкап перед восстановлением.

EOF
    exit 0
}

list_backups() {
    echo ""
    echo "============================================================================="
    echo "📦 Доступные бэкапы"
    echo "============================================================================="
    echo ""
    
    if [ ! -d "$BACKUP_DIR" ]; then
        print_warning "Директория бэкапов не найдена: $BACKUP_DIR"
        exit 1
    fi
    
    print_info "Последние бэкапы:"
    echo ""
    
    # Daily бэкапы
    if [ -d "$BACKUP_DIR/daily" ] && [ "$(ls -A "$BACKUP_DIR/daily" 2>/dev/null)" ]; then
        echo "  📁 daily/ (ежедневные):"
        ls -lht "$BACKUP_DIR/daily/"*.sql* 2>/dev/null | head -10 | awk '{print "     " $9 " (" $5 ", " $6 " " $7 " " $8 ")"}'
        echo ""
    fi
    
    # Weekly бэкапы
    if [ -d "$BACKUP_DIR/weekly" ] && [ "$(ls -A "$BACKUP_DIR/weekly" 2>/dev/null)" ]; then
        echo "  📁 weekly/ (недельные):"
        ls -lht "$BACKUP_DIR/weekly/"*.sql* 2>/dev/null | head -5 | awk '{print "     " $9 " (" $5 ", " $6 " " $7 " " $8 ")"}'
        echo ""
    fi
    
    # Monthly бэкапы
    if [ -d "$BACKUP_DIR/monthly" ] && [ "$(ls -A "$BACKUP_DIR/monthly" 2>/dev/null)" ]; then
        echo "  📁 monthly/ (месячные):"
        ls -lht "$BACKUP_DIR/monthly/"*.sql* 2>/dev/null | head -5 | awk '{print "     " $9 " (" $5 ", " $6 " " $7 " " $8 ")"}'
        echo ""
    fi
    
    # Latest symlink
    if [ -L "$BACKUP_DIR/latest.sql.gz" ]; then
        print_info "Последний бэкап (symlink):"
        ls -lh "$BACKUP_DIR/latest.sql.gz" | awk '{print "  🔗 latest.sql.gz -> " $NF}'
        echo ""
    fi
}

load_env() {
    ENV_FILE="$PROJECT_DIR/.env"
    if [ -f "$ENV_FILE" ]; then
        set -a
        source "$ENV_FILE"
        set +a
        
        PG_HOST="${POSTGRES_HOST:-$PG_HOST}"
        PG_PORT="${POSTGRES_PORT:-5432}"
        PG_USER="${POSTGRES_USER:-$PG_USER}"
        PG_PASSWORD="${POSTGRES_PASSWORD:-$PG_PASSWORD}"
        PG_DB="${POSTGRES_DB:-$PG_DB}"
    fi
    
    if [ "$MODE" = "docker" ]; then
        PG_HOST="postgres"
        PG_PORT="5432"
    fi
}

check_dependencies() {
    if [ "$MODE" = "docker" ]; then
        if ! command -v docker &> /dev/null; then
            print_error "Docker не найден."
            exit 1
        fi
    else
        if ! command -v psql &> /dev/null; then
            print_warning "psql не найден. Попробую использовать Docker режим..."
            MODE="docker"
        fi
    fi
}

find_latest_backup() {
    if [ -L "$BACKUP_DIR/latest.sql.gz" ]; then
        BACKUP_FILE="$BACKUP_DIR/latest.sql.gz"
    elif [ -d "$BACKUP_DIR/daily" ]; then
        BACKUP_FILE=$(ls -t "$BACKUP_DIR/daily/"*.sql* 2>/dev/null | head -1)
    fi
    
    if [ -z "$BACKUP_FILE" ] || [ ! -f "$BACKUP_FILE" ]; then
        print_error "Бэкапы не найдены в $BACKUP_DIR"
        exit 1
    fi
}

confirm_restore() {
    if [ "$FORCE" = true ]; then
        return
    fi
    
    if [ "$DRY_RUN" = true ]; then
        return
    fi
    
    echo ""
    print_warning "⚠️  ВНИМАНИЕ: Восстановление заменит все данные в базе данных!"
    echo ""
    echo "  База данных: $PG_DB"
    echo "  Бэкап файл:  $BACKUP_FILE"
    echo ""
    read -p "  Продолжить? (yes/no): " -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        print_info "Восстановление отменено"
        exit 0
    fi
}

restore_standard() {
    print_info "Выполняется восстановление PostgreSQL..."
    print_info "Хост: $PG_HOST, Порт: $PG_PORT, База: $PG_DB"
    
    if [ -z "$PG_PASSWORD" ]; then
        print_error "PG_PASSWORD не установлен!"
        exit 1
    fi
    
    export PGPASSWORD="$PG_PASSWORD"
    
    if [ "$DRY_RUN" = true ]; then
        print_info "[DRY RUN] Восстановление не выполняется"
        
        # Проверяем подключение
        if psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d postgres -c '\q' > /dev/null 2>&1; then
            print_success "Подключение к PostgreSQL работает"
        else
            print_error "Не удалось подключиться к PostgreSQL"
            exit 1
        fi
        
        return
    fi
    
    # Создаем временную базу для проверки бэкапа
    print_info "Проверка бэкапа..."
    
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        # Проверяем сжатый файл
        if ! gzip -t "$BACKUP_FILE"; then
            print_error "Бэкап поврежден"
            exit 1
        fi
        print_success "Бэкап цел"
        
        # Восстанавливаем
        print_info "Восстановление из сжатого бэкапа..."
        gunzip -c "$BACKUP_FILE" | psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" > /dev/null
    else
        # Восстанавливаем из несжатого
        print_info "Восстановление из бэкапа..."
        psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" < "$BACKUP_FILE" > /dev/null
    fi
    
    unset PGPASSWORD
}

restore_docker() {
    print_info "Выполняется восстановление через Docker Compose..."
    
    COMPOSE_FILE="$PROJECT_DIR/docker-compose.postgres.yml"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Docker Compose файл не найден: $COMPOSE_FILE"
        exit 1
    fi
    
    if [ "$DRY_RUN" = true ]; then
        print_info "[DRY RUN] Восстановление не выполняется"
        
        # Проверяем контейнер
        if docker-compose -f "$COMPOSE_FILE" ps | grep -q postgres; then
            print_success "PostgreSQL контейнер запущен"
        else
            print_warning "PostgreSQL контейнер не запущен"
        fi
        
        return
    fi
    
    # Копируем файл бэкапа в контейнер
    TEMP_CONTAINER_PATH="/tmp/restore_backup.sql"
    
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        print_info "Распаковка и восстановление..."
        gunzip -c "$BACKUP_FILE" | docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U "$PG_USER" -d "$PG_DB"
    else
        print_info "Восстановление..."
        docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -U "$PG_USER" -d "$PG_DB" < "$BACKUP_FILE"
    fi
}

verify_restore() {
    if [ "$DRY_RUN" = true ]; then
        return
    fi
    
    print_info "Проверка восстановления..."
    
    if [ "$MODE" = "docker" ]; then
        COMPOSE_FILE="$PROJECT_DIR/docker-compose.postgres.yml"
        COUNT=$(docker-compose -f "$COMPOSE_FILE" exec -T postgres psql -h localhost -U "$PG_USER" -d "$PG_DB" -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ')
    else
        export PGPASSWORD="$PG_PASSWORD"
        COUNT=$(psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -t -c "SELECT COUNT(*) FROM users;" 2>/dev/null | tr -d ' ')
        unset PGPASSWORD
    fi
    
    if [ -n "$COUNT" ]; then
        print_success "База данных доступна, найдено пользователей: $COUNT"
    else
        print_warning "Не удалось проверить базу данных"
    fi
}

# =============================================================================
# Парсинг аргументов
# =============================================================================

BACKUP_FILE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --latest)
            find_latest_backup
            shift
            ;;
        --list)
            list_backups
            exit 0
            ;;
        --docker)
            MODE="docker"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        --help)
            show_help
            ;;
        -*)
            print_error "Неизвестный параметр: $1"
            echo "Используйте --help для справки"
            exit 1
            ;;
        *)
            BACKUP_FILE="$1"
            shift
            ;;
    esac
done

# =============================================================================
# Основной процесс
# =============================================================================

echo ""
echo "============================================================================="
echo "🔄 Восстановление PostgreSQL для IT Interview Trainer"
echo "============================================================================="
echo ""

# Загружаем настройки
load_env
check_dependencies

# Если файл не указан, ищем последний
if [ -z "$BACKUP_FILE" ]; then
    find_latest_backup
fi

# Проверяем существование файла
if [ ! -f "$BACKUP_FILE" ]; then
    print_error "Файл не найден: $BACKUP_FILE"
    echo "Используйте --list для просмотра доступных бэкапов"
    exit 1
fi

print_info "Бэкап файл: $BACKUP_FILE"
print_info "Размер: $(du -h "$BACKUP_FILE" | cut -f1)"

# Подтверждение
confirm_restore

# Восстановление
case $MODE in
    standard)
        restore_standard
        ;;
    docker)
        restore_docker
        ;;
esac

# Проверка
verify_restore

echo ""
print_success "Восстановление завершено!"
echo ""

exit 0
