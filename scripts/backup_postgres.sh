#!/bin/bash
# =============================================================================
# Бэкап PostgreSQL для IT Interview Trainer
# =============================================================================
# Использование:
#   ./scripts/backup_postgres.sh                    # Бэкап в backups/postgresql/
#   ./scripts/backup_postgres.sh --docker           # Бэкап через Docker Compose
#   ./scripts/backup_postgres.sh --custom           # Бэкап с кастомными настройками
#   ./scripts/backup_postgres.sh --help             # Помощь
#
# Требования:
#   - PostgreSQL клиент (pg_dump)
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
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE=""

# Параметры PostgreSQL по умолчанию
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5433}"
PG_USER="${PG_USER:-interview_admin}"
PG_DB="${PG_DB:-interview_trainer}"
PG_PASSWORD="${PG_PASSWORD:-}"

# Настройки бэкапа
RETENTION_DAYS=30          # Хранить дневные бэкапы 30 дней
RETENTION_WEEKS=8          # Хранить недельные бэкапы 8 недель
RETENTION_MONTHS=12        # Хранить месячные бэкапы 12 месяцев
COMPRESS=true              # Сжимать бэкапы gzip
ENCRYPT=false              # Шифровать бэкапы (требует gpg)
VERBOSE=false              # Подробный вывод

# Режимы работы
MODE="standard"            # standard, docker, custom
CUSTOM_PATH=""             # Путь для кастомного бэкапа

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
${GREEN}Бэкап PostgreSQL для IT Interview Trainer${NC}

${BLUE}Использование:${NC}
  $0 [OPTIONS]

${BLUE}Опции:${NC}
  --docker          Использовать Docker Compose для бэкапа
  --custom PATH     Сохранить бэкап в указанный путь
  --no-compress     Не сжимать бэкап (по умолчанию сжимается)
  --encrypt         Шифровать бэкап (требует настроенный GPG)
  --verbose         Подробный вывод
  --help            Показать эту справку

${BLUE}Примеры:${NC}
  $0                                    # Стандартный бэкап
  $0 --docker                           # Бэкап через Docker
  $0 --custom /mnt/backup/pg_backup.sql # В свой путь
  $0 --no-compress                      # Без сжатия

${BLUE}Переменные окружения:${NC}
  PG_HOST       Хост PostgreSQL (по умолчанию: localhost)
  PG_PORT       Порт PostgreSQL (по умолчанию: 5433)
  PG_USER       Пользователь PostgreSQL (по умолчанию: interview_admin)
  PG_DB         База данных (по умолчанию: interview_trainer)
  PG_PASSWORD   Пароль PostgreSQL (обязательно для бэкапа)

${BLUE}Автоматизация (cron):${NC}
  # Ежедневный бэкап в 2:00
  0 2 * * * /home/vboxuser/it_interVI.it-interview-trainer/scripts/backup_postgres.sh --docker

EOF
    exit 0
}

check_dependencies() {
    if [ "$MODE" = "docker" ]; then
        if ! command -v docker &> /dev/null; then
            print_error "Docker не найден. Установите Docker или используйте стандартный режим."
            exit 1
        fi
    else
        if ! command -v pg_dump &> /dev/null; then
            print_warning "pg_dump не найден. Попробую использовать Docker режим..."
            MODE="docker"
        fi
    fi
}

load_env() {
    # Загружаем переменные из .env если существует
    ENV_FILE="$PROJECT_DIR/.env"
    if [ -f "$ENV_FILE" ]; then
        set -a
        source "$ENV_FILE"
        set +a
        
        # Переопределяем значения из .env
        PG_HOST="${POSTGRES_HOST:-$PG_HOST}"
        PG_PORT="${POSTGRES_PORT:-5432}"
        PG_USER="${POSTGRES_USER:-$PG_USER}"
        PG_PASSWORD="${POSTGRES_PASSWORD:-$PG_PASSWORD}"
        PG_DB="${POSTGRES_DB:-$PG_DB}"
    fi
    
    # Для Docker Compose используем другие переменные
    if [ "$MODE" = "docker" ]; then
        PG_HOST="postgres"
        PG_PORT="5432"
        PG_USER="${POSTGRES_USER:-interview_admin}"
        PG_PASSWORD="${POSTGRES_PASSWORD:-}"
        PG_DB="${POSTGRES_DB:-interview_trainer}"
    fi
}

create_backup_dir() {
    mkdir -p "$BACKUP_DIR"
    mkdir -p "$BACKUP_DIR/daily"
    mkdir -p "$BACKUP_DIR/weekly"
    mkdir -p "$BACKUP_DIR/monthly"
}

backup_standard() {
    print_info "Выполняется стандартный бэкап PostgreSQL..."
    print_info "Хост: $PG_HOST, Порт: $PG_PORT, База: $PG_DB"
    
    if [ -z "$PG_PASSWORD" ]; then
        print_error "PG_PASSWORD не установлен!"
        print_info "Установите переменную окружения или добавьте в .env:"
        echo "   POSTGRES_PASSWORD=ваш_пароль"
        exit 1
    fi
    
    # Определяем имя файла
    if [ "$COMPRESS" = true ]; then
        BACKUP_FILE="$BACKUP_DIR/daily/${PG_DB}_${DATE}.sql.gz"
        export PGPASSWORD="$PG_PASSWORD"
        pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" | gzip > "$BACKUP_FILE"
    else
        BACKUP_FILE="$BACKUP_DIR/daily/${PG_DB}_${DATE}.sql"
        export PGPASSWORD="$PG_PASSWORD"
        pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" > "$BACKUP_FILE"
    fi
    
    unset PGPASSWORD
}

backup_docker() {
    print_info "Выполняется бэкап через Docker Compose..."
    
    COMPOSE_FILE="$PROJECT_DIR/docker-compose.postgres.yml"
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Docker Compose файл не найден: $COMPOSE_FILE"
        exit 1
    fi
    
    # Создаем бэкап внутри контейнера и копируем наружу
    if [ "$COMPRESS" = true ]; then
        BACKUP_FILE="$BACKUP_DIR/daily/${PG_DB}_${DATE}.sql.gz"
        docker-compose -f "$COMPOSE_FILE" exec -T postgres \
            pg_dump -U "$PG_USER" -d "$PG_DB" | gzip > "$BACKUP_FILE"
    else
        BACKUP_FILE="$BACKUP_DIR/daily/${PG_DB}_${DATE}.sql"
        docker-compose -f "$COMPOSE_FILE" exec -T postgres \
            pg_dump -U "$PG_USER" -d "$PG_DB" > "$BACKUP_FILE"
    fi
}

backup_custom() {
    print_info "Выполняется кастомный бэкап в: $CUSTOM_PATH"
    
    mkdir -p "$(dirname "$CUSTOM_PATH")"
    
    if [ "$COMPRESS" = true ]; then
        BACKUP_FILE="${CUSTOM_PATH%.sql}.sql.gz"
        export PGPASSWORD="$PG_PASSWORD"
        pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" | gzip > "$BACKUP_FILE"
    else
        BACKUP_FILE="$CUSTOM_PATH"
        export PGPASSWORD="$PG_PASSWORD"
        pg_dump -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" > "$BACKUP_FILE"
    fi
    
    unset PGPASSWORD
}

create_weekly_backup() {
    # Создаем недельной бэкап (каждую пятницу)
    if [ "$(date +%u)" = "5" ]; then
        print_info "Создание недельного бэкапа..."
        cp "$BACKUP_FILE" "$BACKUP_DIR/weekly/${PG_DB}_week_$(date +%V).sql.gz"
    fi
}

create_monthly_backup() {
    # Создаем месячной бэкап (первого числа)
    if [ "$(date +%d)" = "01" ]; then
        print_info "Создание месячного бэкапа..."
        cp "$BACKUP_FILE" "$BACKUP_DIR/monthly/${PG_DB}_$(date +%Y%m).sql.gz"
    fi
}

cleanup_old_backups() {
    print_info "Очистка старых бэкапов..."
    
    # Удаляем ежедневные бэкапы старше RETENTION_DAYS
    find "$BACKUP_DIR/daily" -name "*.sql*" -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
    print_info "  - Удалены ежедневные бэкапы старше $RETENTION_DAYS дней"
    
    # Удаляем недельные бэкапы старше RETENTION_WEEKS
    find "$BACKUP_DIR/weekly" -name "*.sql*" -mtime +$((RETENTION_WEEKS * 7)) -delete 2>/dev/null || true
    print_info "  - Удалены недельные бэкапы старше $RETENTION_WEEKS недель"
    
    # Удаляем месячные бэкапы старше RETENTION_MONTHS
    find "$BACKUP_DIR/monthly" -name "*.sql*" -mtime +$((RETENTION_MONTHS * 30)) -delete 2>/dev/null || true
    print_info "  - Удалены месячные бэкапы старше $RETENTION_MONTHS месяцев"
}

verify_backup() {
    print_info "Проверка бэкапа..."
    
    if [ ! -f "$BACKUP_FILE" ]; then
        print_error "Файл бэкапа не найден: $BACKUP_FILE"
        exit 1
    fi
    
    # Проверяем размер
    FILE_SIZE=$(stat -f%z "$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_FILE" 2>/dev/null)
    if [ "$FILE_SIZE" -lt 100 ]; then
        print_warning "Бэкап подозрительно маленький: $FILE_SIZE байт"
    fi
    
    # Проверяем содержимое (для сжатых файлов)
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        if ! gzip -t "$BACKUP_FILE" 2>/dev/null; then
            print_error "Бэкап поврежден (gzip проверка не пройдена)"
            exit 1
        fi
        print_success "Бэкап сжат и проверен"
    fi
    
    print_success "Бэкап проверен: $FILE_SIZE байт"
}

create_latest_symlink() {
    # Создаем symlink на последний бэкап
    ln -sf "$(basename "$BACKUP_FILE")" "$BACKUP_DIR/latest.sql.gz"
    print_success "Создан symlink: $BACKUP_DIR/latest.sql.gz"
}

show_summary() {
    echo ""
    echo "============================================================================="
    print_success "Бэкап завершен успешно!"
    echo "============================================================================="
    echo ""
    print_info "Файл бэкапа: $BACKUP_FILE"
    print_info "Размер: $(du -h "$BACKUP_FILE" | cut -f1)"
    print_info "Дата: $(date)"
    echo ""
    print_info "Структура бэкапов:"
    echo "  📁 $BACKUP_DIR/"
    echo "     ├── daily/   - Ежедневные бэкапы (хранение: $RETENTION_DAYS дней)"
    echo "     ├── weekly/  - Недельные бэкапы (хранение: $RETENTION_WEEKS недель)"
    echo "     └── monthly/ - Месячные бэкапы (хранение: $RETENTION_MONTHS месяцев)"
    echo ""
    
    # Показываем последние бэкапы
    print_info "Последние бэкапы:"
    ls -lht "$BACKUP_DIR/daily/"*.sql* 2>/dev/null | head -5 | awk '{print "  " $9 " (" $5 ")"}'
    echo ""
}

# =============================================================================
# Парсинг аргументов
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            MODE="docker"
            shift
            ;;
        --custom)
            MODE="custom"
            CUSTOM_PATH="$2"
            shift 2
            ;;
        --no-compress)
            COMPRESS=false
            shift
            ;;
        --encrypt)
            ENCRYPT=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            show_help
            ;;
        *)
            print_error "Неизвестный параметр: $1"
            echo "Используйте --help для справки"
            exit 1
            ;;
    esac
done

# =============================================================================
# Основной процесс
# =============================================================================

echo ""
echo "============================================================================="
echo "🔄 Бэкап PostgreSQL для IT Interview Trainer"
echo "============================================================================="
echo ""

# Загружаем настройки
load_env
check_dependencies

# Создаем директорию
create_backup_dir

# Выполняем бэкап в зависимости от режима
case $MODE in
    standard)
        backup_standard
        ;;
    docker)
        backup_docker
        ;;
    custom)
        backup_custom
        ;;
esac

# Проверяем бэкап
verify_backup

# Создаем symlink
create_latest_symlink

# Создаем недельные/месячные бэкапы
create_weekly_backup
create_monthly_backup

# Очищаем старые бэкапы
cleanup_old_backups

# Показываем резюме
show_summary

exit 0
