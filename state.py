from typing_extensions import TypedDict

class SupportTicketState(TypedDict):
    ticket: dict
    status: str
    messages: list