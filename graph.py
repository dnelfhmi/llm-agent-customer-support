from langgraph.graph import StateGraph, START, END
from state import SupportTicketState
from agent import run_agent

graph_builder = StateGraph(SupportTicketState)

def webhooks_node(state: SupportTicketState):
    print("Webhooks node executed")
    # Simulate receiving and logging a webhook event (e.g., ticket creation)
    # You can expand this to actually process incoming webhooks
    return {**state, "status": "webhook_received", "messages": state.get("messages", []) + [{"role": "system", "content": "Webhook received"}]}

def agent_node(state: SupportTicketState):
    print("Agent node executed")
    agent_response = run_agent({"prompt": state["ticket"].get("description", "")})
    return {**state, "status": agent_response["action"], "messages": state.get("messages", []) + [{"role": "assistant", "content": agent_response["reason"]}]}

# Nodes
graph_builder.add_node("webhooks_node", webhooks_node)
graph_builder.add_node("agent_node", agent_node)

# Edges
graph_builder.add_edge(START, "webhooks_node")
graph_builder.add_edge("webhooks_node", "agent_node")
graph_builder.add_edge("agent_node", END)

graph = graph_builder.compile()