# Seed данные перенесены в scripts/init_database.py
# Этот файл оставлен для обратной совместимости
# Все данные теперь хранятся ТОЛЬКО в базе данных

from sqlalchemy.orm import Session


def seed_database(db: Session) -> None:
    """
    Функция сидирования базы данных.
    ПУСТАЯ - все данные создаются через scripts/init_database.py
    
    Args:
        db: Сессия SQLAlchemy для работы с БД
    """
    # Данные создаются только через init_database.py при первом запуске
    # Этот файл оставлен для обратной совместимости
    pass
