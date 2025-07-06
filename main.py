from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Ticket(BaseModel):
    subject: str
    description: str
    priority: int

@app.post("/tickets")
async def receive_ticket(ticket: Ticket):
    print(f"Received ticket: {ticket}")
    return {"status": "received", "data": ticket}