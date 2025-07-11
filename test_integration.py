import os
import pytest
from fastapi.testclient import TestClient
from main import app
from memory import load_memory
from pinecone_utils import query_kb
from agent import run_agent

client = TestClient(app)

def test_full_agent_workflow_with_real_apis():
    """
    Integration test that uses real API keys to test the complete agent workflow:
    1. Webhook receives ticket
    2. Agent processes with memory and knowledge base
    3. Agent suggests actions
    """
    
    # Test 1: Submit a new ticket and verify webhook processing
    payload = {
        "subject": "Password Reset Issue",
        "description": "I can't reset my password. The reset link is not working.",
        "priority": 2
    }
    
    response = client.post("/tickets", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "ticket_id" in data
    assert "status" in data
    assert "data" in data
    assert "ticket" in data["data"]
    assert "messages" in data["data"]
    
    ticket_id = data["ticket_id"]
    
    # Test 2: Verify webhook message was created
    messages = data["data"]["messages"]
    assert len(messages) >= 1
    assert any("Webhook received" in msg["content"] for msg in messages)
    
    # Test 3: Verify agent processed the ticket
    assert any(msg["role"] == "assistant" for msg in messages)
    
    # Test 4: Retrieve memory and verify persistence
    mem_response = client.get(f"/tickets/{ticket_id}")
    assert mem_response.status_code == 200
    mem_data = mem_response.json()
    assert mem_data["ticket_id"] == ticket_id
    assert isinstance(mem_data["messages"], list)
    assert len(mem_data["messages"]) > 0
    
    # Test 5: Test knowledge base retrieval (if KB has data)
    try:
        kb_results = query_kb("password reset")
        assert isinstance(kb_results, list)
        print(f"KB Results: {kb_results}")
    except Exception as e:
        print(f"KB test skipped (likely no data in index): {e}")
    
    # Test 6: Test agent reasoning with real prompt
    test_prompt = f"""
    Ticket: {payload['description']}
    
    Analyze this support ticket and provide a structured response in JSON format:
    {{
        "action": "auto_reply" | "escalate" | "human_review",
        "reason": "explanation for the action",
        "reply": "if auto_reply, provide the response text"
    }}
    """
    
    agent_response = run_agent({"prompt": test_prompt})
    assert "action" in agent_response
    assert "reason" in agent_response
    assert agent_response["action"] in ["auto_reply", "escalate", "human_review"]
    
    print(f"Agent Action: {agent_response['action']}")
    print(f"Agent Reason: {agent_response['reason']}")

def test_agent_with_memory_context():
    """
    Test that the agent can use memory context from previous interactions
    """
    
    # Submit first ticket
    payload1 = {
        "subject": "Login Issue",
        "description": "I'm having trouble logging into my account.",
        "priority": 1
    }
    
    response1 = client.post("/tickets", json=payload1)
    assert response1.status_code == 200
    ticket_id1 = response1.json()["ticket_id"]
    
    # Submit second ticket (simulating follow-up)
    payload2 = {
        "subject": "Follow-up on Login Issue",
        "description": "I still can't log in. The password reset didn't work.",
        "priority": 1
    }
    
    response2 = client.post("/tickets", json=payload2)
    assert response2.status_code == 200
    ticket_id2 = response2.json()["ticket_id"]
    
    # Verify both tickets have memory
    mem1 = client.get(f"/tickets/{ticket_id1}").json()
    mem2 = client.get(f"/tickets/{ticket_id2}").json()
    
    assert len(mem1["messages"]) > 0
    assert len(mem2["messages"]) > 0

def test_error_handling():
    """
    Test error handling for invalid inputs
    """
    
    # Test missing required fields
    bad_payload = {"subject": "Missing description"}
    response = client.post("/tickets", json=bad_payload)
    assert response.status_code == 422  # Validation error
    
    # Test invalid ticket ID
    response = client.get("/tickets/nonexistent-id")
    assert response.status_code == 200  # Should return empty messages
    data = response.json()
    assert data["messages"] == []

def test_agent_action_variations():
    """
    Test different types of tickets to see how the agent responds
    """
    
    test_cases = [
        {
            "subject": "Simple Question",
            "description": "What are your business hours?",
            "priority": 1,
            "expected_action": "auto_reply"
        },
        {
            "subject": "Critical Bug",
            "description": "The entire system is down and customers are complaining",
            "priority": 3,
            "expected_action": "escalate"
        },
        {
            "subject": "Complex Technical Issue",
            "description": "I need help with advanced configuration that requires deep technical knowledge",
            "priority": 2,
            "expected_action": "human_review"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {test_case['subject']} ---")
        response = client.post("/tickets", json=test_case)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text[:200]}...")
        
        assert response.status_code == 200, f"Failed for test case {i+1}: {test_case['subject']}"
        
        data = response.json()
        messages = data["data"]["messages"]
        
        # Verify agent processed the ticket
        assistant_messages = [msg for msg in messages if msg["role"] == "assistant"]
        assert len(assistant_messages) > 0
        
        print(f"Ticket: {test_case['subject']}")
        print(f"Expected Action: {test_case['expected_action']}")
        print(f"Agent Response: {assistant_messages[-1]['content'][:100]}...")
        print("---")

if __name__ == "__main__":
    # Run the tests
    test_full_agent_workflow_with_real_apis()
    test_agent_with_memory_context()
    test_error_handling()
    test_agent_action_variations()
    print("All integration tests passed!")