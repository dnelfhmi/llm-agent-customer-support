from memory import save_memory, load_memory

def test_save_and_load_memory():
    ticket_id = "UNITTEST1"
    messages = [
        {"role": "system", "content": "Unit test webhook"},
        {"role": "assistant", "content": "Unit test reply"}
    ]
    save_memory(ticket_id, messages)
    loaded = load_memory(ticket_id)
    assert loaded == messages
