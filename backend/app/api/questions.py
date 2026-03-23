from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
import json
import csv
import io
from math import ceil

from app.database.engine import get_db
from app.models.question import Question
from app.models.profession import Profession
from app.models.user import User
from app.api.schemas import (
    QuestionCreate, QuestionUpdate, QuestionResponse,
    PaginatedQuestions, ImportResult, BulkUpdateResult, DuplicateResult
)
from app.api.deps import get_current_user, get_current_admin_user
from app.core.exceptions import NotFoundException, ImportException, ValidationException
from app.core.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=PaginatedQuestions)
def get_questions(
    profession_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None, description="Поиск по тексту вопроса"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    difficulty: Optional[str] = Query(None, description="Фильтр по сложности"),
    question_type: Optional[str] = Query(None, description="Фильтр по типу вопроса"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Получить вопросы с пагинацией и фильтрами.

    Args:
        profession_id: Фильтр по профессии
        search: Поиск по тексту вопроса
        category_id: Фильтр по категории
        difficulty: Фильтр по сложности
        question_type: Фильтр по типу вопроса
        page: Номер страницы (начиная с 1)
        page_size: Размер страницы (1-100)
        db: Сессия базы данных
    """
    logger.debug(f"📖 Запрос вопросов: profession_id={profession_id}, search={search}, page={page}, page_size={page_size}")

    query = db.query(Question)
    if profession_id:
        query = query.filter(Question.profession_id == profession_id)
    
    # Поиск по тексту вопроса
    if search:
        query = query.filter(Question.text.ilike(f"%{search}%"))
    
    # Фильтр по категории
    if category_id:
        query = query.filter(Question.categories.any(id=category_id))
    
    # Фильтр по сложности
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    # Фильтр по типу вопроса
    if question_type:
        query = query.filter(Question.question_type == question_type)

    # Получаем общее количество
    total = query.count()
    total_pages = ceil(total / page_size) if total > 0 else 1

    # Применяем пагинацию
    offset = (page - 1) * page_size
    questions = query.options(joinedload(Question.categories)).offset(offset).limit(page_size).all()

    logger.debug(f"✅ Получено {len(questions)} вопросов из {total} всего")
    return PaginatedQuestions(
        items=questions,
        meta={
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }
    )


@router.post("/", response_model=QuestionResponse)
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    logger.info(f"📝 Создание вопроса для профессии ID={question.profession_id} (админ: {current_user.email})")
    
    question_data = question.model_dump()
    category_ids = question_data.pop('category_ids', None)

    new_question = Question(**question_data)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    # Привязываем категории если указаны
    if category_ids:
        from app.models.category import Category
        categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
        new_question.categories.extend(categories)
        db.commit()
        db.refresh(new_question)
        logger.debug(f"🏷️  Привязано категорий: {len(categories)}")

    logger.info(f"✅ Вопрос создан: ID={new_question.id}")
    return new_question


@router.get("/templates")
def get_question_templates():
    """Шаблоны вопросов для быстрого добавления"""
    templates = [
        {
            "id": 1,
            "name": "MCQ - Базовый вопрос",
            "description": "Простой вопрос с одним правильным ответом",
            "template": {
                "text": "Ваш вопрос здесь?",
                "question_type": "mcq",
                "difficulty": "medium",
                "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
                "correct_option": 0
            }
        },
        {
            "id": 2,
            "name": "Ordering - Упорядочивание",
            "description": "Вопрос на правильную последовательность",
            "template": {
                "text": "Расположите в правильном порядке:",
                "question_type": "ordering",
                "difficulty": "medium",
                "options": ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"],
                "correct_order": [0, 1, 2, 3]
            }
        },
        {
            "id": 3,
            "name": "MCQ - Сложный вопрос",
            "description": "Вопрос с 5 вариантами ответов",
            "template": {
                "text": "Ваш сложный вопрос?",
                "question_type": "mcq",
                "difficulty": "hard",
                "options": ["Вариант A", "Вариант B", "Вариант C", "Вариант D", "Вариант E"],
                "correct_option": 0
            }
        },
        {
            "id": 4,
            "name": "MCQ - Легкий вопрос",
            "description": "Простой вопрос для начинающих",
            "template": {
                "text": "Что такое...?",
                "question_type": "mcq",
                "difficulty": "easy",
                "options": ["Правильный ответ", "Неправильный 1", "Неправильный 2", "Неправильный 3"],
                "correct_option": 0
            }
        }
    ]
    return templates


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    logger.debug(f"📖 Запрос вопроса ID={question_id}")
    
    question = db.query(Question).options(joinedload(Question.categories)).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"⚠️  Вопрос не найден: ID={question_id}")
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    logger.debug(f"✅ Вопрос получен: ID={question.id}")
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    logger.info(f"✏️  Обновление вопроса ID={question_id} (админ: {current_user.email})")
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"⚠️  Вопрос не найден для обновления: ID={question_id}")
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    update_data = question_data.model_dump(exclude_unset=True)
    category_ids = update_data.pop('category_ids', None)

    for field, value in update_data.items():
        setattr(question, field, value)

    # Обновляем категории если указаны
    if category_ids is not None:
        from app.models.category import Category
        # Очищаем текущие категории
        question.categories = []
        db.flush()

        # Добавляем новые
        if category_ids:
            categories = db.query(Category).filter(Category.id.in_(category_ids)).all()
            question.categories.extend(categories)
            logger.debug(f"🏷️  Обновлены категории: {len(categories)}")

    db.commit()
    db.refresh(question)
    logger.info(f"✅ Вопрос обновлен: ID={question.id}")
    return question


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    logger.info(f"🗑️  Удаление вопроса ID={question_id} (админ: {current_user.email})")
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        logger.warning(f"⚠️  Вопрос не найден для удаления: ID={question_id}")
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    # Удаляем связанные ответы
    from app.models.answer import Answer
    db.query(Answer).filter(Answer.question_id == question_id).delete()

    # Удаляем вопрос
    db.delete(question)
    db.commit()
    
    logger.info(f"✅ Вопрос удален: ID={question_id}")
    return {"message": "Вопрос успешно удален"}


@router.get("/export/json")
def export_questions_json(
    profession_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Экспорт вопросов в JSON"""
    query = db.query(Question)
    if profession_id:
        query = query.filter(Question.profession_id == profession_id)
    questions = query.all()
    
    data = []
    for q in questions:
        data.append({
            "text": q.text,
            "question_type": q.question_type,
            "profession_id": q.profession_id,
            "difficulty": q.difficulty,
            "options": q.options,
            "correct_option": q.correct_option,
            "correct_order": q.correct_order
        })
    
    return {
        "version": "1.0",
        "count": len(data),
        "questions": data
    }


@router.get("/export/csv")
def export_questions_csv(
    profession_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Экспорт вопросов в CSV"""
    query = db.query(Question).join(Profession)
    if profession_id:
        query = query.filter(Question.profession_id == profession_id)
    questions = query.all()
    
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # Заголовки
    writer.writerow([
        'ID', 'Текст вопроса', 'Тип', 'Профессия', 'Сложность', 
        'Варианты (JSON)', 'Правильный ответ', 'Правильный порядок'
    ])
    
    for q in questions:
        writer.writerow([
            q.id,
            q.text,
            q.question_type,
            q.profession.name,
            q.difficulty,
            json.dumps(q.options, ensure_ascii=False),
            q.correct_option if q.correct_option is not None else '',
            json.dumps(q.correct_order, ensure_ascii=False) if q.correct_order else ''
        ])
    
    output.seek(0)
    return output.getvalue()


@router.post("/import/json", response_model=ImportResult)
async def import_questions_json(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    """Импорт вопросов из JSON. Доступно только администраторам."""
    logger.info(f"📥 Импорт вопросов из JSON: {file.filename} (админ: {current_user.email})")
    
    if not file.filename.endswith('.json'):
        logger.warning(f"⚠️  Неверный формат файла: {file.filename}")
        raise ValidationException("Файл должен быть в формате JSON")

    try:
        content = await file.read()
        data = json.loads(content.decode('utf-8'))
        logger.debug(f"📊 Размер загруженных данных: {len(content)} байт")

        if isinstance(data, dict) and "questions" in data:
            questions_data = data["questions"]
        elif isinstance(data, list):
            questions_data = data
        else:
            logger.warning(f"⚠️  Неверная структура JSON")
            raise ValidationException("Неверный формат JSON")

        logger.info(f"📊 В файле {len(questions_data)} вопросов")
        
        created = []
        errors = []

        professions_cache = {}
        for p in db.query(Profession).all():
            professions_cache[p.name.lower()] = p.id
            professions_cache[str(p.id)] = p.id

        for idx, q_data in enumerate(questions_data):
            try:
                # Определяем profession_id
                prof_id = q_data.get('profession_id')
                if prof_id is None:
                    prof_name = q_data.get('profession_name', '')
                    if prof_name.lower() in professions_cache:
                        prof_id = professions_cache[prof_name.lower()]
                    else:
                        errors.append({
                            "index": idx,
                            "error": f"Профессия не найдена: {prof_name}"
                        })
                        continue

                # Валидация обязательных полей
                if not q_data.get('text'):
                    errors.append({"index": idx, "error": "Отсутствует текст вопроса"})
                    continue

                if not q_data.get('options'):
                    errors.append({"index": idx, "error": "Отсутствуют варианты ответов"})
                    continue

                question = Question(
                    text=q_data['text'],
                    question_type=q_data.get('question_type', 'mcq'),
                    profession_id=int(prof_id),
                    difficulty=q_data.get('difficulty', 'medium'),
                    options=q_data['options'],
                    correct_option=q_data.get('correct_option'),
                    correct_order=q_data.get('correct_order')
                )
                db.add(question)
                created.append(question.text)

            except Exception as e:
                logger.error(f"❌ Ошибка импорта вопроса #{idx}: {e}")
                errors.append({"index": idx, "error": str(e)})

        db.commit()

        logger.info(f"✅ Импорт завершен: {len(created)} создано, {len(errors)} ошибок")
        return ImportResult(
            message="Импорт завершен",
            created=len(created),
            errors=len(errors),
            created_questions=created,
            error_details=errors
        )

    except json.JSONDecodeError:
        logger.error("❌ Неверный формат JSON")
        raise ValidationException("Неверный формат JSON")
    except Exception as e:
        logger.error(f"❌ Ошибка импорта данных: {e}", exc_info=True)
        raise ImportException("Ошибка импорта данных", errors=[{"error": str(e)}])


@router.post("/import/csv")
async def import_questions_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    """Импорт вопросов из CSV. Доступно только администраторам."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Файл должен быть в формате CSV")
    
    try:
        content = await file.read()
        lines = content.decode('utf-8').splitlines()
        
        reader = csv.DictReader(lines, delimiter=';')
        
        created = []
        errors = []
        
        professions_cache = {}
        for p in db.query(Profession).all():
            professions_cache[p.name.lower()] = p.id
        
        for idx, row in enumerate(reader):
            try:
                prof_name = row.get('Профессия', '').strip()
                if not prof_name:
                    errors.append({"index": idx, "error": "Не указана профессия"})
                    continue
                
                prof_id = professions_cache.get(prof_name.lower())
                if not prof_id:
                    errors.append({"index": idx, "error": f"Профессия не найдена: {prof_name}"})
                    continue
                
                text = row.get('Текст вопроса', '').strip()
                if not text:
                    errors.append({"index": idx, "error": "Не указан текст вопроса"})
                    continue
                
                options_str = row.get('Варианты (JSON)', '[]')
                try:
                    options = json.loads(options_str)
                except:
                    options = options_str.split('|') if options_str else []
                
                question_type = row.get('Тип', 'mcq').strip()
                difficulty = row.get('Сложность', 'medium').strip()
                
                correct_option_str = row.get('Правильный ответ', '').strip()
                correct_option = int(correct_option_str) if correct_option_str.isdigit() else None
                
                correct_order_str = row.get('Правильный порядок', '').strip()
                correct_order = json.loads(correct_order_str) if correct_order_str else None
                
                question = Question(
                    text=text,
                    question_type=question_type,
                    profession_id=prof_id,
                    difficulty=difficulty,
                    options=options,
                    correct_option=correct_option,
                    correct_order=correct_order
                )
                db.add(question)
                created.append(text)
                
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})
        
        db.commit()
        
        return {
            "message": "Импорт завершен",
            "created": len(created),
            "errors": len(errors),
            "created_questions": created,
            "error_details": errors
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка импорта: {str(e)}")


@router.post("/bulk-update", response_model=BulkUpdateResult)
def bulk_update_questions(
    question_ids: list[int],
    profession_id: Optional[int] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    """Массовое обновление вопросов. Доступно только администраторам."""
    updated = 0
    for qid in question_ids:
        question = db.query(Question).filter(Question.id == qid).first()
        if question:
            if profession_id is not None:
                question.profession_id = profession_id
            if difficulty is not None:
                question.difficulty = difficulty
            updated += 1
    db.commit()
    return BulkUpdateResult(
        message=f"Обновлено {updated} вопросов",
        updated=updated
    )


@router.post("/{question_id}/duplicate", response_model=DuplicateResult)
def duplicate_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)  # Требуется админ
):
    """Дублирование вопроса. Доступно только администраторам."""
    """Дублирование вопроса"""
    original = db.query(Question).filter(Question.id == question_id).first()
    if not original:
        raise NotFoundException("Вопрос", question_id)
    
    duplicate = Question(
        text=f"{original.text} (копия)",
        question_type=original.question_type,
        profession_id=original.profession_id,
        difficulty=original.difficulty,
        options=original.options.copy(),
        correct_option=original.correct_option,
        correct_order=original.correct_order.copy() if original.correct_order else None
    )
    db.add(duplicate)
    db.commit()
    db.refresh(duplicate)

    return DuplicateResult(
        message="Вопрос дублирован",
        new_id=duplicate.id
    )


@router.post("/{question_id}/answers", response_model=dict)
def submit_answer(
    question_id: int,
    answer: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Вопрос не найден")

    selected_option = answer.get("selected_option")
    is_correct = selected_option == question.correct_option

    from app.models.answer import Answer
    new_answer = Answer(
        question_id=question_id,
        user_id=current_user.id,  # Сохраняем ID пользователя
        selected_option=selected_option,
        is_correct=is_correct
    )
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)

    return {
        "id": new_answer.id,
        "question_id": question_id,
        "selected_option": selected_option,
        "is_correct": is_correct
    }
