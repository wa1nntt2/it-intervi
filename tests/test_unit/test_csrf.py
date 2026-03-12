"""
Unit тесты для CSRF защиты.
"""

import pytest
from fastapi import Request, Response, HTTPException
from app.core.csrf import CSRFProtect, csrf_protect


class TestCSRFProtect:
    """Тесты для CSRF защиты"""

    def test_generate_csrf_token(self):
        """Тест генерации CSRF токена"""
        csrf = CSRFProtect()
        token = csrf.generate_csrf_token()
        
        # Токен должен быть строкой
        assert isinstance(token, str)
        # Токен должен быть непустым
        assert len(token) > 0
        # Токен должен быть достаточно длинным (min 32 символа для безопасности)
        assert len(token) >= 32

    def test_generate_different_tokens(self):
        """Тест: каждая генерация дает уникальный токен"""
        csrf = CSRFProtect()
        token1 = csrf.generate_csrf_token()
        token2 = csrf.generate_csrf_token()
        
        assert token1 != token2

    def test_set_csrf_cookie(self):
        """Тест установки CSRF cookie"""
        csrf = CSRFProtect()
        response = Response()
        token = csrf.generate_csrf_token()
        
        csrf.set_csrf_cookie(response, token)
        
        # Проверяем, что cookie установлен
        cookies = [header for header in response.headers.getlist("set-cookie")]
        assert len(cookies) > 0
        
        cookie_header = cookies[0]
        assert "csrf_token" in cookie_header
        assert "HttpOnly" in cookie_header
        assert "SameSite=strict" in cookie_header or "samesite=strict" in cookie_header.lower()

    def test_get_csrf_token_from_cookie(self):
        """Тест получения CSRF токена из cookie"""
        csrf = CSRFProtect()
        
        # Создаем mock запрос с cookie
        class MockRequest:
            def __init__(self, cookies_dict):
                self._cookies = cookies_dict
            
            @property
            def cookies(self):
                return self._cookies
        
        token = csrf.generate_csrf_token()
        request = MockRequest({"csrf_token": token})
        
        retrieved_token = csrf.get_csrf_token_from_cookie(request)
        assert retrieved_token == token

    def test_get_csrf_token_from_header(self):
        """Тест получения CSRF токена из заголовка"""
        csrf = CSRFProtect()
        
        # Создаем mock запрос с заголовком
        class MockRequest:
            def __init__(self, headers_dict):
                self._headers = headers_dict
            
            @property
            def headers(self):
                return self._headers
        
        token = csrf.generate_csrf_token()
        request = MockRequest({"x-csrf-token": token})
        
        retrieved_token = csrf.get_csrf_token_from_header(request)
        assert retrieved_token == token

    @pytest.mark.asyncio
    async def test_validate_csrf_success(self):
        """Тест успешной валидации CSRF"""
        csrf = CSRFProtect()
        
        # Создаем mock запрос с правильными токенами
        class MockRequest:
            def __init__(self, token):
                self._cookies = {"csrf_token": token}
                self._headers = {"x-csrf-token": token}
            
            @property
            def cookies(self):
                return self._cookies
            
            @property
            def headers(self):
                return self._headers
        
        token = csrf.generate_csrf_token()
        request = MockRequest(token)
        
        result = await csrf.validate_csrf(request)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_csrf_missing_cookie(self):
        """Тест валидации CSRF без cookie"""
        csrf = CSRFProtect()
        
        class MockRequest:
            def __init__(self):
                self._cookies = {}
                self._headers = {"x-csrf-token": "some-token"}
            
            @property
            def cookies(self):
                return self._cookies
            
            @property
            def headers(self):
                return self._headers
        
        request = MockRequest()
        
        with pytest.raises(HTTPException) as exc_info:
            await csrf.validate_csrf(request)
        
        assert exc_info.value.status_code == 403
        assert "CSRF токен не найден в cookies" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_validate_csrf_missing_header(self):
        """Тест валидации CSRF без заголовка"""
        csrf = CSRFProtect()
        
        class MockRequest:
            def __init__(self, token):
                self._cookies = {"csrf_token": token}
                self._headers = {}
            
            @property
            def cookies(self):
                return self._cookies
            
            @property
            def headers(self):
                return self._headers
        
        token = csrf.generate_csrf_token()
        request = MockRequest(token)
        
        with pytest.raises(HTTPException) as exc_info:
            await csrf.validate_csrf(request)
        
        assert exc_info.value.status_code == 403
        assert "CSRF токен не найден в заголовке" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_validate_csrf_mismatched_tokens(self):
        """Тест валидации CSRF с несовпадающими токенами"""
        csrf = CSRFProtect()
        
        class MockRequest:
            def __init__(self, cookie_token, header_token):
                self._cookies = {"csrf_token": cookie_token}
                self._headers = {"x-csrf-token": header_token}
            
            @property
            def cookies(self):
                return self._cookies
            
            @property
            def headers(self):
                return self._headers
        
        request = MockRequest("token1", "token2")
        
        with pytest.raises(HTTPException) as exc_info:
            await csrf.validate_csrf(request)
        
        assert exc_info.value.status_code == 403
        assert "CSRF токены не совпадают" in str(exc_info.value.detail)


class TestCSRFConstants:
    """Тесты констант CSRF"""

    def test_cookie_name(self):
        """Тест имени CSRF cookie"""
        assert csrf_protect.CSRF_COOKIE_NAME == "csrf_token"

    def test_header_name(self):
        """Тест имени CSRF заголовка"""
        assert csrf_protect.CSRF_HEADER_NAME == "x-csrf-token"
