from langgraph.graph import StateGraph, START, END
from state import SupportTicketState

graph_builder = StateGraph(SupportTicketState)

def dummy_node(state: SupportTicketState):
    print("Dummy node executed")
    return {"messages": [{"role": "assistant", "content": "Hello from dummy node!"}]}

graph_builder.add_node("dummy_node", dummy_node)

graph_builder.add_edge(START, "dummy_node")
graph_builder.add_edge("dummy_node", END)

graph = graph_builder.compile()