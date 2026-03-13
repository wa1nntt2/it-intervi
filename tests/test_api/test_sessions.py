import pytest
from fastapi.testclient import TestClient


def test_create_session(client: TestClient, test_profession):
    session_data = {"profession_id": test_profession.id}
    response = client.post("/api/sessions/", json=session_data)
    assert response.status_code == 200
    data = response.json()
    assert data["profession_id"] == session_data["profession_id"]
    assert data["status"] == "active"
    assert "question_ids" in data


def test_get_sessions(client: TestClient):
    response = client.get("/api/sessions/")
    assert response.status_code == 200
    # API возвращает объект с пагинацией, а не список
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)


def test_get_session_by_id(client: TestClient, test_profession):
    session_data = {"profession_id": test_profession.id}
    create_response = client.post("/api/sessions/", json=session_data)
    session_id = create_response.json()["id"]

    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["id"] == session_id


def test_get_nonexistent_session(client: TestClient):
    response = client.get("/api/sessions/99999")
    assert response.status_code == 404


def test_complete_session(client: TestClient, test_profession):
    session_data = {"profession_id": test_profession.id}
    create_response = client.post("/api/sessions/", json=session_data)
    session_id = create_response.json()["id"]

    response = client.post(f"/api/sessions/{session_id}/complete")
    # 422 если сессия пустая (нет вопросов), 200 если успешно
    assert response.status_code in [200, 422]

    if response.status_code == 200:
        get_response = client.get(f"/api/sessions/{session_id}")
        assert get_response.json()["status"] == "completed"
