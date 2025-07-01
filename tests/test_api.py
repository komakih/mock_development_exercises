import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_conversation():
    response = client.post("/history/", json={
        "user_id": 1,
        "message": "Hello",
        "response": "Hi! How can I help you?"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["message"] == "Hello"

def test_get_conversation_history():
    user_id = 1
    response = client.get(f"/history/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["user_id"] == user_id
