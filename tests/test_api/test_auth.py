import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_register_duplicate_email(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 400


def test_login_success(client: TestClient):
    client.post(
        "/api/auth/register",
        json={"email": "login@example.com", "password": "testpass123"}
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    response = client.post(
        "/api/auth/login",
        data={"username": "nonexistent@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
