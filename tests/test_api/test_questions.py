import pytest
from fastapi.testclient import TestClient


def test_get_questions(client: TestClient):
    response = client.get("/api/questions/")
    assert response.status_code == 200
    # API возвращает объект с пагинацией, а не список
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_questions_by_profession(client: TestClient, test_profession):
    response = client.get(f"/api/questions/?profession_id={test_profession.id}")
    assert response.status_code == 200


def test_create_question(client: TestClient, test_profession):
    question_data = {
        "text": "Тестовый вопрос?",
        "question_type": "mcq",
        "profession_id": test_profession.id,
        "difficulty": "easy",
        "options": ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"],
        "correct_option": 0
    }
    response = client.post("/api/questions/", json=question_data)
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == question_data["text"]
    assert data["question_type"] == question_data["question_type"]


def test_get_question_by_id(client: TestClient, test_profession):
    question_data = {
        "text": "Вопрос для получения по ID?",
        "question_type": "mcq",
        "profession_id": test_profession.id,
        "difficulty": "medium",
        "options": ["A", "B", "C", "D"],
        "correct_option": 1
    }
    create_response = client.post("/api/questions/", json=question_data)
    question_id = create_response.json()["id"]

    response = client.get(f"/api/questions/{question_id}")
    assert response.status_code == 200
    assert response.json()["id"] == question_id


def test_get_nonexistent_question(client: TestClient):
    response = client.get("/api/questions/99999")
    assert response.status_code == 404
