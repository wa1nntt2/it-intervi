# Сидирование базы данных начальными данными
# Создает тестового пользователя, профессии, вопросы и достижения при первом запуске

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.profession import Profession
from app.models.question import Question
from app.models.user_progress import Achievement
from app.core.security import get_password_hash


def seed_database(db: Session):
    """
    Функция сидирования базы данных.
    Создает начальные данные если они еще не существуют.
    
    Args:
        db: Сессия SQLAlchemy для работы с БД
    """

    # === Создание тестового администратора ===
    if not db.query(User).first():
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin_user)

    # === Создание профессий ===
    if not db.query(Profession).first():
        professions = [
            Profession(name="Frontend Developer", description="React, Vue, Angular"),
            Profession(name="Backend Developer", description="Python, Node.js, Go"),
            Profession(name="Fullstack Developer", description="Frontend + Backend"),
            Profession(name="DevOps Engineer", description="CI/CD, Docker, Kubernetes"),
        ]
        db.add_all(professions)
        db.commit()

    # Получаем созданные профессии для добавления вопросов
    frontend = db.query(Profession).filter(Profession.name == "Frontend Developer").first()
    devops = db.query(Profession).filter(Profession.name == "DevOps Engineer").first()

    # === Frontend вопросы ===
    if frontend and not db.query(Question).filter(Question.profession_id == frontend.id).first():
        frontend_questions = [
            Question(
                text="Что такое HTML?",
                question_type="mcq",
                profession_id=frontend.id,
                difficulty="intern",
                options=["Язык разметки", "Язык программирования", "База данных", "Фреймворк"],
                correct_option=0,
                explanation="HTML (HyperText Markup Language) — это язык гипертекстовой разметки для структурирования веб-страниц."
            ),
            Question(
                text="Что такое Virtual DOM?",
                question_type="mcq",
                profession_id=frontend.id,
                difficulty="intern",
                options=["Прямая копия реального DOM", "Легковесная копия реального DOM", "База данных для DOM", "Библиотека для работы с DOM"],
                correct_option=1,
                explanation="Virtual DOM — это легковесная копия реального DOM в памяти. React сравнивает Virtual DOM и обновляет только изменённые узлы в реальном DOM."
            ),
            Question(
                text="Расположите этапы жизненного цикла React компонента в правильном порядке",
                question_type="ordering",
                profession_id=frontend.id,
                difficulty="junior",
                options=["Mounting", "Updating", "Unmounting"],
                correct_order=[0, 1, 2],
                explanation="Жизненный цикл React: 1. Mounting (создание), 2. Updating (обновление), 3. Unmounting (удаление)."
            ),
            Question(
                text="Что такое useEffect в React?",
                question_type="mcq",
                profession_id=frontend.id,
                difficulty="junior",
                options=["Хук для работы с состоянием", "Хук для побочных эффектов", "Хук для мемоизации", "Хук для навигации"],
                correct_option=1,
                explanation="useEffect — хук для выполнения побочных эффектов (запросы к API, подписки, изменение DOM). Заменяет методы жизненного цикла."
            ),
            Question(
                text="Что такое React Fiber?",
                question_type="mcq",
                profession_id=frontend.id,
                difficulty="middle",
                options=["Новая версия React", "Алгоритм перерисовки с приоритетами", "Библиотека для анимаций", "Инструмент отладки"],
                correct_option=1,
                explanation="React Fiber — архитектура движка согласования в React 16+. Позволяет разбивать рендеринг на части и назначать приоритеты."
            ),
            Question(
                text="Расположите по приоритету рендеринга в React Fiber",
                question_type="ordering",
                profession_id=frontend.id,
                difficulty="middle",
                options=["Анимации", "Задержка данных", "Смена вкладок"],
                correct_order=[0, 2, 1],
                explanation="Приоритеты в React Fiber: 1. Анимации (наивысший), 2. Смена вкладок, 3. Задержка данных (низкий)."
            ),
        ]
        db.add_all(frontend_questions)
        db.commit()

    # DevOps вопросы импортированы из внешнего файла (questions.md)
    # Не создаём seed вопросы для DevOps чтобы избежать дубликатов

    # === Создание достижений ===
    if not db.query(Achievement).first():
        achievements = [
            Achievement(
                name="Первый шаг",
                description="Пройдите первую сессию",
                icon="🌱",
                xp_reward=50,
                requirement_type="sessions_completed",
                requirement_value=1,
                category="general"
            ),
            Achievement(
                name="Начинающий",
                description="Пройдите 5 сессий",
                icon="📚",
                xp_reward=100,
                requirement_type="sessions_completed",
                requirement_value=5,
                category="general"
            ),
            Achievement(
                name="Опытный",
                description="Пройдите 20 сессий",
                icon="🎓",
                xp_reward=250,
                requirement_type="sessions_completed",
                requirement_value=20,
                category="general"
            ),
            Achievement(
                name="Эксперт",
                description="Пройдите 50 сессий",
                icon="🏆",
                xp_reward=500,
                requirement_type="sessions_completed",
                requirement_value=50,
                category="general"
            ),
            Achievement(
                name="Перфекционист",
                description="Получите 100% в сессии",
                icon="💯",
                xp_reward=150,
                requirement_type="perfect_score",
                requirement_value=1,
                category="special"
            ),
            Achievement(
                name="Знаток",
                description="Ответьте правильно на 100 вопросов",
                icon="🧠",
                xp_reward=200,
                requirement_type="correct_answers",
                requirement_value=100,
                category="general"
            ),
            Achievement(
                name="Серия побед",
                description="Получите серию из 5 идеальных сессий",
                icon="🔥",
                xp_reward=300,
                requirement_type="streak",
                requirement_value=5,
                category="streak"
            ),
            Achievement(
                name="DevOps Мастер",
                description="Пройдите все DevOps вопросы",
                icon="⚙️",
                xp_reward=400,
                requirement_type="sessions_completed",
                requirement_value=10,
                category="profession"
            ),
        ]
        db.add_all(achievements)
        db.commit()
