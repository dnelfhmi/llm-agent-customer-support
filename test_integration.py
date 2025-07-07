from fastapi.testclient import TestClient
from main import app
from memory import load_memory

client = TestClient(app)

def test_full_ticket_flow():
    # 1. Submit a new ticket
    payload = {
        "subject": "Integration Test",
        "description": "This is an integration test ticket.",
        "priority": 2
    }
    response = client.post("/tickets", json=payload)
    assert response.status_code == 200
    data = response.json()
    ticket_id = data["ticket_id"]

    # 2. Check the response structure and content
    assert "status" in data
    assert "data" in data
    assert data["data"]["ticket"]["id"] == ticket_id
    assert data["data"]["messages"][0]["content"].startswith("Webhook received")
    assert data["data"]["messages"][1]["role"] == "assistant"

    # 3. Retrieve the memory for this ticket
    mem_response = client.get(f"/tickets/{ticket_id}")
    assert mem_response.status_code == 200
    mem_data = mem_response.json()
    assert mem_data["ticket_id"] == ticket_id
    assert isinstance(mem_data["messages"], list)
    assert mem_data["messages"][0]["content"].startswith("Webhook received")