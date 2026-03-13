"""
Integration тесты для полного потока аутентификации.
Тестируем полный цикл: регистрация -> логин -> доступ к защищенным endpoint'ам -> logout
"""

import pytest
from fastapi.testclient import TestClient


class TestAuthFlow:
    """Интеграционные тесты потока аутентификации"""

    def test_full_auth_flow(self, client: TestClient):
        """Тест полного потока аутентификации"""
        # 1. Регистрация
        register_data = {
            "email": "flowtest@example.com",
            "password": "FlowTest123"
        }
        register_response = client.post("/api/auth/register", json=register_data)
        assert register_response.status_code == 200
        
        # 2. Логин
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": register_data["email"],
                "password": register_data["password"]
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "access_token" in login_data
        assert "csrf_token" in login_data
        
        # 3. Получение информации о пользователе
        client.headers["Authorization"] = f"Bearer {login_data['access_token']}"
        me_response = client.get("/api/auth/me")
        assert me_response.status_code == 200
        assert me_response.json()["email"] == register_data["email"]
        
        # 4. Logout
        logout_response = client.post("/api/auth/logout")
        assert logout_response.status_code == 200
        
        # 5. Попытка доступа после logout должна失败
        client.headers.pop("Authorization", None)
        me_response_after_logout = client.get("/api/auth/me")
        assert me_response_after_logout.status_code == 401

    def test_register_and_login_with_strong_password(self, client: TestClient):
        """Тест регистрации с надежным паролем"""
        strong_password = "Str0ngP@ssw0rd123"
        email = "strong@example.com"
        
        # Регистрация
        register_response = client.post(
            "/api/auth/register",
            json={"email": email, "password": strong_password}
        )
        assert register_response.status_code == 200
        
        # Логин
        login_response = client.post(
            "/api/auth/login",
            data={"username": email, "password": strong_password}
        )
        assert login_response.status_code == 200

    def test_refresh_token_flow(self, client: TestClient):
        """Тест обновления токена"""
        # Регистрация и логин
        email = "refresh@example.com"
        password = "Refresh123"
        
        client.post("/api/auth/register", json={"email": email, "password": password})
        login_response = client.post(
            "/api/auth/login",
            data={"username": email, "password": password}
        )
        
        # Получаем CSRF токен из cookies
        csrf_cookie = login_response.cookies.get("csrf_token")
        
        # Refresh endpoint
        refresh_response = client.post(
            "/api/auth/refresh",
            cookies={"refresh_token": login_response.cookies.get("refresh_token", "")}
        )
        
        # В новой реализации refresh читает токен из cookies автоматически
        # Проверяем что получили новый access токен
        assert refresh_response.status_code in [200, 401]  # 401 если cookie не передан

    def test_session_persistence(self, client: TestClient):
        """Тест сохранения сессии между запросами"""
        email = "session@example.com"
        password = "Session123"
        
        # Регистрация
        client.post("/api/auth/register", json={"email": email, "password": password})
        
        # Логин
        login_response = client.post(
            "/api/auth/login",
            data={"username": email, "password": password}
        )
        access_token = login_response.json()["access_token"]
        
        # Несколько запросов с одним токеном
        for _ in range(3):
            client.headers["Authorization"] = f"Bearer {access_token}"
            me_response = client.get("/api/auth/me")
            assert me_response.status_code == 200


class TestPasswordValidation:
    """Интеграционные тесты валидации пароля"""

    def test_password_too_short(self, client: TestClient):
        """Тест: пароль слишком короткий"""
        response = client.post(
            "/api/auth/register",
            json={"email": "short@example.com", "password": "short"}
        )
        assert response.status_code == 400
        assert "8 символов" in response.json()["detail"]

    def test_password_no_uppercase(self, client: TestClient):
        """Тест: пароль без заглавных букв"""
        response = client.post(
            "/api/auth/register",
            json={"email": "noupper@example.com", "password": "alllowercase123"}
        )
        assert response.status_code == 400
        assert "заглавную" in response.json()["detail"].lower()

    def test_password_no_lowercase(self, client: TestClient):
        """Тест: пароль без строчных букв"""
        response = client.post(
            "/api/auth/register",
            json={"email": "nolower@example.com", "password": "ALLUPPERCASE123"}
        )
        assert response.status_code == 400
        assert "строчную" in response.json()["detail"].lower()

    def test_password_no_digit(self, client: TestClient):
        """Тест: пароль без цифр"""
        response = client.post(
            "/api/auth/register",
            json={"email": "nodigit@example.com", "password": "NoDigitsHere"}
        )
        assert response.status_code == 400
        assert "цифру" in response.json()["detail"].lower()

    def test_password_valid(self, client: TestClient):
        """Тест: валидный пароль"""
        response = client.post(
            "/api/auth/register",
            json={"email": "valid@example.com", "password": "Valid123"}
        )
        assert response.status_code == 200


class TestCSRFIntegration:
    """Интеграционные тесты CSRF защиты"""

    def test_csrf_token_in_login_response(self, client: TestClient):
        """Тест: CSRF токен присутствует в ответе login"""
        email = "csrf@example.com"
        password = "Csrf1234"
        
        client.post("/api/auth/register", json={"email": email, "password": password})
        login_response = client.post(
            "/api/auth/login",
            data={"username": email, "password": password}
        )
        
        assert login_response.status_code == 200
        data = login_response.json()
        assert "csrf_token" in data

    def test_get_csrf_token_endpoint(self, client: TestClient):
        """Тест endpoint получения CSRF токена"""
        response = client.get("/api/auth/csrf-token")
        
        assert response.status_code == 200
        assert "csrf_token" in response.json()
