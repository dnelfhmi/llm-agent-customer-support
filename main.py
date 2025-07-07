from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph

app = FastAPI()

class Ticket(BaseModel):
    subject: str
    description: str
    priority: int

@app.post("/tickets")
async def receive_ticket(ticket: Ticket):
    print(f"Received ticket: {ticket}")

    # Construct initial state for the graph
    state = {
        "ticket": ticket.model_dump(),
        "status": "",
        "messages": []
    }

    final_state = graph.invoke(state)
    return {"status": final_state["status"], "data": final_state}