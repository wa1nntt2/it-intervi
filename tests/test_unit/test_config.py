"""
Unit тесты для конфигурации приложения.
"""

import os
import pytest
from app.core.config import Settings


class TestSettings:
    """Тесты для настроек приложения"""

    def test_default_settings(self):
        """Тест настроек по умолчанию"""
        # Временно очищаем переменные окружения
        original_secret = os.environ.get("SECRET_KEY")
        original_debug = os.environ.get("DEBUG")
        
        try:
            os.environ["SECRET_KEY"] = "test-secret-key-min-32-chars-for-testing"
            os.environ["DEBUG"] = "true"
            
            settings = Settings()
            
            assert settings.PROJECT_NAME == "IT Interview Trainer"
            assert settings.VERSION == "0.1.0"
            assert settings.DEBUG is True
            assert settings.ALGORITHM == "HS256"
            assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
            assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7
            
        finally:
            # Восстанавливаем переменные окружения
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret
            if original_debug:
                os.environ["DEBUG"] = original_debug

    def test_secret_key_validation_in_debug(self):
        """Тест валидации SECRET_KEY в debug режиме"""
        original_secret = os.environ.get("SECRET_KEY")
        original_debug = os.environ.get("DEBUG")
        
        try:
            os.environ["DEBUG"] = "true"
            os.environ["SECRET_KEY"] = ""  # Пустой ключ
            
            # В debug режиме должен сгенерироваться временный ключ
            settings = Settings()
            
            # Ключ должен быть сгенерирован
            assert settings.SECRET_KEY != ""
            assert len(settings.SECRET_KEY) >= 32
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret
            if original_debug:
                os.environ["DEBUG"] = original_debug

    def test_secret_key_validation_in_production(self):
        """Тест валидации SECRET_KEY в production режиме"""
        original_secret = os.environ.get("SECRET_KEY")
        original_debug = os.environ.get("DEBUG")
        
        try:
            os.environ["DEBUG"] = "false"
            os.environ["SECRET_KEY"] = ""  # Пустой ключ
            
            # В production режиме должна быть ошибка
            with pytest.raises(ValueError) as exc_info:
                Settings()
            
            assert "SECRET_KEY не установлен" in str(exc_info.value)
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret
            if original_debug:
                os.environ["DEBUG"] = original_debug

    def test_short_secret_key_in_production(self):
        """Тест короткого SECRET_KEY в production режиме"""
        original_secret = os.environ.get("SECRET_KEY")
        original_debug = os.environ.get("DEBUG")
        
        try:
            os.environ["DEBUG"] = "false"
            os.environ["SECRET_KEY"] = "short"  # Короткий ключ
            
            with pytest.raises(ValueError) as exc_info:
                Settings()
            
            assert "слишком короткий" in str(exc_info.value).lower()
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret
            if original_debug:
                os.environ["DEBUG"] = original_debug

    def test_cors_origins_parsing(self):
        """Тест парсинга CORS_ORIGINS"""
        original_secret = os.environ.get("SECRET_KEY")
        
        try:
            os.environ["SECRET_KEY"] = "test-secret-key-min-32-chars-for-testing"
            os.environ["DEBUG"] = "true"
            os.environ["CORS_ORIGINS"] = "http://localhost:3000,http://example.com"
            
            settings = Settings()
            
            origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
            assert "http://localhost:3000" in origins
            assert "http://example.com" in origins
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret


class TestPaginationSettings:
    """Тесты настроек пагинации"""

    def test_default_pagination_settings(self):
        """Тест настроек пагинации по умолчанию"""
        original_secret = os.environ.get("SECRET_KEY")
        
        try:
            os.environ["SECRET_KEY"] = "test-secret-key-min-32-chars-for-testing"
            os.environ["DEBUG"] = "true"
            
            settings = Settings()
            
            assert settings.DEFAULT_PAGE_SIZE == 20
            assert settings.MAX_PAGE_SIZE == 100
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret


class TestSessionSettings:
    """Тесты настроек сессий"""

    def test_default_session_settings(self):
        """Тест настроек сессий по умолчанию"""
        original_secret = os.environ.get("SECRET_KEY")
        
        try:
            os.environ["SECRET_KEY"] = "test-secret-key-min-32-chars-for-testing"
            os.environ["DEBUG"] = "true"
            
            settings = Settings()
            
            assert settings.QUESTIONS_PER_SESSION == 20
            assert settings.MIN_QUESTIONS_IN_SESSION == 5
            
        finally:
            if original_secret:
                os.environ["SECRET_KEY"] = original_secret
