#!/usr/bin/env python3
"""
Скрипт для применения миграций Alembic.
Использование: python migrate.py upgrade
"""

import sys
from alembic import command
from alembic.config import Config
from pathlib import Path


def run_migrations(direction: str = "upgrade"):
    """
    Запуск миграций Alembic.
    
    Args:
        direction: "upgrade" для применения, "downgrade" для отката
    """
    # Получаем путь к директории backend
    backend_dir = Path(__file__).parent
    alembic_cfg = Config(backend_dir / "alembic.ini")
    
    if direction == "upgrade":
        print("🔄 Применяем миграции...")
        command.upgrade(alembic_cfg, "head")
        print("✅ Миграции успешно применены!")
    elif direction == "downgrade":
        print("🔄 Откатываем миграции...")
        command.downgrade(alembic_cfg, "-1")
        print("✅ Миграции успешно откатаны!")
    elif direction == "current":
        print("📊 Текущая версия:")
        command.current(alembic_cfg)
    elif direction == "history":
        print("📜 История миграций:")
        command.history(alembic_cfg)
    else:
        print(f"❌ Неизвестная команда: {direction}")
        print("Используйте: upgrade, downgrade, current, history")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python migrate.py [upgrade|downgrade|current|history]")
        sys.exit(1)
    
    run_migrations(sys.argv[1])
