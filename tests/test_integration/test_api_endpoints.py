"""
Integration тесты для вопросов и сессий.
"""

import pytest
import uuid
from fastapi.testclient import TestClient


def generate_unique_email():
    """Генерирует уникальный email для теста"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def authenticated_client(client: TestClient, test_profession):
    """Фикстура с аутентифицированным клиентом"""
    email = generate_unique_email()
    
    # Регистрируем тестового пользователя
    client.post("/api/auth/register", json={
        "email": email,
        "password": "Questions123"
    })

    # Логинимся
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": "Questions123"
        }
    )

    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    yield client

    client.headers.pop("Authorization", None)


class TestQuestionsAPI:
    """Интеграционные тесты для вопросов"""

    def test_get_questions_empty(self, authenticated_client: TestClient):
        """Тест получения пустого списка вопросов"""
        response = authenticated_client.get("/api/questions/")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "meta" in data
        assert data["meta"]["total"] == 0

    def test_create_question(self, authenticated_client: TestClient, test_profession):
        """Тест создания вопроса (требуется админ)"""
        question_data = {
            "text": "Integration test question?",
            "question_type": "mcq",
            "profession_id": test_profession.id,
            "difficulty": "junior",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_option": 0
        }

        response = authenticated_client.post("/api/questions/", json=question_data)

        # Может быть 403 если пользователь не админ
        if response.status_code == 403:
            pytest.skip("Требуется права администратора")

        assert response.status_code == 200
        data = response.json()
        assert data["text"] == question_data["text"]
        assert data["question_type"] == question_data["question_type"]

    def test_get_question_templates(self, authenticated_client: TestClient):
        """Тест получения шаблонов вопросов"""
        response = authenticated_client.get("/api/questions/templates")
        assert response.status_code == 200

        templates = response.json()
        assert isinstance(templates, list)
        assert len(templates) > 0


class TestSessionsAPI:
    """Интеграционные тесты для сессий"""

    def test_create_session(self, authenticated_client: TestClient, test_profession):
        """Тест создания сессии"""
        session_data = {
            "profession_id": test_profession.id,
            "difficulty": "junior"
        }

        response = authenticated_client.post("/api/sessions/", json=session_data)
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "question_ids" in data
        assert data["profession_id"] == test_profession.id

    def test_get_sessions_list(self, authenticated_client: TestClient):
        """Тест получения списка сессий"""
        response = authenticated_client.get("/api/sessions/")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "meta" in data

    def test_get_session_stats(self, authenticated_client: TestClient):
        """Тест получения статистики сессий"""
        response = authenticated_client.get("/api/sessions/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total" in data
        assert "active" in data
        assert "completed" in data
        assert "average_score" in data


class TestProfessionsAPI:
    """Интеграционные тесты для профессий"""

    def test_get_professions_list(self, authenticated_client: TestClient, test_profession):
        """Тест получения списка профессий"""
        response = authenticated_client.get("/api/professions/")
        assert response.status_code == 200

        professions = response.json()
        assert isinstance(professions, list)

        # Проверяем что профессии существуют (из seed данных или тестовой фикстуры)
        assert len(professions) > 0
        assert "id" in professions[0]
        assert "name" in professions[0]

    def test_get_profession_by_id(self, authenticated_client: TestClient, test_profession):
        """Тест получения профессии по ID"""
        # Получаем по ID
        response = authenticated_client.get(f"/api/professions/{test_profession.id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == test_profession.id


class TestPaginationIntegration:
    """Интеграционные тесты пагинации"""

    def test_questions_pagination(self, authenticated_client: TestClient):
        """Тест пагинации вопросов"""
        # Запрос с пагинацией
        response = authenticated_client.get("/api/questions/?page=1&page_size=5")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "meta" in data

        meta = data["meta"]
        assert "total" in meta
        assert "page" in meta
        assert "page_size" in meta
        assert "total_pages" in meta

        assert meta["page"] == 1
        assert meta["page_size"] == 5

    def test_sessions_pagination(self, authenticated_client: TestClient):
        """Тест пагинации сессий"""
        response = authenticated_client.get("/api/sessions/?page=1&page_size=10")
        assert response.status_code == 200

        data = response.json()
        meta = data["meta"]

        assert meta["page"] == 1
        assert meta["page_size"] == 10
        assert 1 <= meta["page_size"] <= 100  # Проверка лимитов


class TestFilteringIntegration:
    """Интеграционные тесты фильтрации"""

    def test_filter_questions_by_profession(self, authenticated_client: TestClient, test_profession):
        """Тест фильтрации вопросов по профессии"""
        response = authenticated_client.get(f"/api/questions/?profession_id={test_profession.id}")
        assert response.status_code == 200

        data = response.json()
        # Все вопросы должны быть для указанной профессии
        for question in data["items"]:
            assert question["profession_id"] == test_profession.id

    def test_filter_sessions_by_status(self, authenticated_client: TestClient):
        """Тест фильтрации сессий по статусу"""
        response = authenticated_client.get("/api/sessions/?status=active")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "meta" in data
