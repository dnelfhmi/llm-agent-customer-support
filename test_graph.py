from graph import graph

def test_graph_webhooks_and_agent_nodes():
    state = {
        "ticket": {"description": "Test ticket for agent."},
        "status": "",
        "messages": []
    }
    result = graph.invoke(state)
    print("Graph output:", result)
    assert "messages" in result
    assert result["messages"][0]["content"].startswith("Webhook received")
    assert result["messages"][1]["role"] == "assistant"
    assert isinstance(result["messages"][1]["content"], str)
    assert len(result["messages"][1]["content"].strip()) > 0
