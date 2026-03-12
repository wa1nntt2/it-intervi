"""
Unit тесты для модулей безопасности.
Тестируем функции хеширования паролей и JWT токенов.
"""

import pytest
from datetime import datetime, timedelta
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_refresh_token,
)


class TestPasswordHashing:
    """Тесты для функций хеширования паролей"""

    def test_hash_password(self):
        """Тест хеширования пароля"""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        
        # Хеш должен быть строкой
        assert isinstance(hashed, str)
        # Хеш должен быть непустым
        assert len(hashed) > 0
        # Хеш не должен совпадать с паролем
        assert hashed != password

    def test_verify_correct_password(self):
        """Тест проверки правильного пароля"""
        password = "TestPassword123"
        hashed = get_password_hash(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        """Тест проверки неправильного пароля"""
        password = "TestPassword123"
        wrong_password = "WrongPassword456"
        hashed = get_password_hash(password)
        
        assert verify_password(wrong_password, hashed) is False

    def test_different_hashes_for_same_password(self):
        """Тест: одинаковые пароли дают разные хеши (из-за соли)"""
        password = "TestPassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Хешы должны быть разными из-за случайной соли
        assert hash1 != hash2


class TestAccessToken:
    """Тесты для access токенов"""

    def test_create_access_token(self):
        """Тест создания access токена"""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)
        
        # Токен должен быть строкой
        assert isinstance(token, str)
        # Токен должен быть непустым
        assert len(token) > 0

    def test_decode_valid_access_token(self):
        """Тест декодирования валидного токена"""
        data = {"sub": "test@example.com", "extra": "data"}
        token = create_access_token(data)
        
        payload = decode_token(token, expected_type="access")
        
        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["extra"] == "data"
        assert "exp" in payload

    def test_decode_expired_token(self):
        """Тест декодирования истекшего токена"""
        data = {"sub": "test@example.com"}
        # Создаем токен с истекшим сроком (1 минуту назад)
        token = create_access_token(data, expires_delta=timedelta(minutes=-1))
        
        payload = decode_token(token, expected_type="access")
        
        # Токен должен быть невалиден
        assert payload is None

    def test_decode_with_wrong_type(self):
        """Тест декодирования с неправильным типом"""
        data = {"sub": "test@example.com"}
        access_token = create_access_token(data)
        
        # Пытаемся декодировать как refresh
        payload = decode_token(access_token, expected_type="refresh")
        
        assert payload is None


class TestRefreshToken:
    """Тесты для refresh токенов"""

    def test_create_refresh_token(self):
        """Тест создания refresh токена"""
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_validate_valid_refresh_token(self):
        """Тест валидации правильного refresh токена"""
        data = {"sub": "test@example.com"}
        token = create_refresh_token(data)
        
        payload = validate_refresh_token(token)
        
        assert payload is not None
        assert payload["sub"] == "test@example.com"

    def test_refresh_token_longer_expiration(self):
        """Тест: refresh токен живет дольше access токена"""
        data = {"sub": "test@example.com"}
        
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        
        # Декодируем оба токена
        access_payload = decode_token(access_token, expected_type="access")
        refresh_payload = validate_refresh_token(refresh_token)
        
        # Refresh токен должен истекать позже
        assert refresh_payload["exp"] > access_payload["exp"]


class TestTokenSecurity:
    """Тесты безопасности токенов"""

    def test_invalid_token_format(self):
        """Тест невалидного формата токена"""
        invalid_token = "not.a.valid.token"
        
        payload = decode_token(invalid_token, expected_type="access")
        
        assert payload is None

    def test_tampered_token(self):
        """Тест подделанного токена"""
        data = {"sub": "test@example.com", "role": "user"}
        token = create_access_token(data)
        
        # "Подделываем" токен (меняем payload)
        parts = token.split(".")
        if len(parts) == 3:
            # Меняем payload (вторая часть)
            tampered_token = parts[0] + "." + "tampered" + "." + parts[2]
            
            payload = decode_token(tampered_token, expected_type="access")
            
            # Токен должен быть невалиден
            assert payload is None

    def test_empty_subject(self):
        """Тест токена с пустым subject"""
        data = {"sub": ""}
        token = create_access_token(data)
        
        payload = decode_token(token, expected_type="access")
        
        assert payload is not None
        assert payload["sub"] == ""
