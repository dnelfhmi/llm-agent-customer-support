# Main.py also tested with curl and Postman with Uvicorn.

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_receive_ticket_graph_workflow():
    payload = {
        "subject": "Test subject",
        "description": "Test description for the agent.",
        "priority": 1
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Check that the workflow status is as expected (e.g., 'auto_reply')
    assert "status" in data
    assert "data" in data
    # Check that the messages include both webhook and agent responses
    assert data["data"]["messages"][0]["content"].startswith("Webhook received")
    assert data["data"]["messages"][1]["role"] == "assistant"
    assert isinstance(data["data"]["messages"][1]["content"], str)
    assert len(data["data"]["messages"][1]["content"].strip()) > 0