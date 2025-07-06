import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_receive_ticket_success():
    payload = {
        "subject": "Test subject",
        "description": "Test description",
        "priority": 1
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "received"
    assert data["data"] == payload

def test_receive_ticket_missing_field():
    payload = {
        "subject": "Test subject",
        "priority": 1
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == 422


def test_receive_ticket_invalid_priority():
    payload = {
        "subject": "Test subject",
        "description": "Test description",
        "priority": "high"  # Invalid type
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == 422 