import pytest
from fastapi.testclient import TestClient
import uuid


def generate_unique_email():
    """Генерирует уникальный email для теста"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def test_register_user(client: TestClient):
    email = generate_unique_email()
    response = client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    email = generate_unique_email()
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )
    assert response.status_code == 400


def test_login_success(client: TestClient):
    email = generate_unique_email()
    # Сначала регистрируем пользователя
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )

    # Затем логинимся
    response = client.post(
        "/api/auth/login",
        data={"username": email, "password": "TestPass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Проверяем что токены установлены в cookies
    assert "refresh_token" in response.cookies
    assert "csrf_token" in response.cookies


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


def test_logout(client: TestClient):
    """Тест выхода из системы"""
    email = generate_unique_email()
    # Регистрируемся и логинимся
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )
    client.post(
        "/api/auth/login",
        data={"username": email, "password": "TestPass123"}
    )

    # Выходим
    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200


def test_get_csrf_token(client: TestClient):
    """Тест получения CSRF токена"""
    response = client.get("/api/auth/csrf-token")
    assert response.status_code == 200
    assert "csrf_token" in response.json()


def test_get_current_user(client: TestClient):
    """Тест получения текущего пользователя"""
    email = generate_unique_email()
    # Регистрируемся и логинимся
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "TestPass123"}
    )
    login_response = client.post(
        "/api/auth/login",
        data={"username": email, "password": "TestPass123"}
    )

    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    # Получаем информацию о пользователе
    me_response = client.get("/api/auth/me")
    assert me_response.status_code == 200
    assert me_response.json()["email"] == email
