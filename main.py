from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

class Ticket(BaseModel):
    subject: str
    description: str
    priority: int

@app.post("/tickets")
async def receive_ticket(ticket: Ticket):
    print(f"Received ticket: {ticket}")
    agent_response = run_agent(ticket)
    return {"status": "received", "data": agent_response}