from fastapi import FastAPI
from pydantic import BaseModel
from graph import graph
from uuid import uuid4
from memory import save_memory, load_memory

app = FastAPI()

class Ticket(BaseModel):
    subject: str
    description: str
    priority: int

@app.post("/tickets")
async def receive_ticket(ticket: Ticket):
    print(f"Received ticket: {ticket}")

    ticket_id = str(uuid4())
    state = {
        "ticket": {**ticket.model_dump(), "id": ticket_id},
        "status": "",
        "messages": []
    }
    final_state = graph.invoke(state)
    save_memory(ticket_id, final_state["messages"])
    return {"ticket_id": ticket_id, "status": final_state["status"], "data": final_state}

@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    messages = load_memory(ticket_id)
    return {"ticket_id": ticket_id, "messages": messages}