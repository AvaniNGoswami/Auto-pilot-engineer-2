import pytest

def test_log_event_success(client):
    payload = {
        "user_id": 1,
        "activity_type": "coding",
        "start_time": "2026-01-19T09:00:00",
        "end_time": "2026-01-19T10:30:00"
    }
    response = client.post("/log_event", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["user_id"] == payload["user_id"]

def test_get_suggestion(client):
    response = client.get("/get_suggestion?user_id=1")
    assert response.status_code == 200
    data = response.json()
    assert "suggestion_text" in data

def test_feedback(client):
    payload = {
        "suggestion_id": 1,
        "user_id": 1,
        "accepted": True
    }
    response = client.post("/feedback", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
