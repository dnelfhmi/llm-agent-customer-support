from langgraph.graph import StateGraph, START, END
from state import SupportTicketState
from agent import run_agent
from uuid import uuid4
import datetime

graph_builder = StateGraph(SupportTicketState)

def webhooks_node(state: SupportTicketState):
    print("Webhooks node executed")
    ticket = state.get("ticket", {})
    ticket.setdefault("created_at", datetime.datetime.now().isoformat())
    if "id" not in ticket:
        print("Warning: ticket ID missing, generating new one.")
        ticket["id"] = str(uuid4())
    return {
        **state,
        "ticket": ticket,
        "status": "webhook_received",
        "messages": state.get("messages", []) + [{"role": "system", "content": f"Webhook received for ticket {ticket['id']}"}]
    }

def agent_node(state: SupportTicketState):
    print("Agent node executed")
    ticket = state.get("ticket", {})
    ticket_id = ticket.get("id", "")
    
    agent_response = run_agent({
        "prompt": ticket.get("description", ""),
        "ticket_id": ticket_id
    })
    
    # Include the agent's reply in the message if it's an auto_reply
    message_content = agent_response["reason"]
    if agent_response["action"] == "auto_reply" and agent_response.get("reply"):
        message_content = agent_response["reply"]
    
    return {
        **state,
        "status": agent_response["action"],
        "messages": state.get("messages", []) + [
            {
                "role": "assistant",
                "content": message_content
            }
        ]
    }

# Nodes
graph_builder.add_node("webhooks_node", webhooks_node)
graph_builder.add_node("agent_node", agent_node)

# Edges
graph_builder.add_edge(START, "webhooks_node")
graph_builder.add_edge("webhooks_node", "agent_node")
graph_builder.add_edge("agent_node", END)

graph = graph_builder.compile()