from graph import graph

def test_graph_dummy_node():
    state = {
        "ticket": {},
        "status": "",
        "messages": []
    }
    result = graph.invoke(state)
    print("Graph output:", result)
    assert "messages" in result
    assert result["messages"][0]["content"] == "Hello from dummy node!"
