import pytest
import os
from agent import run_agent

@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
def test_run_agent_llm_real():
    data = {"prompt": "Can you tell me a joke?"}
    result = run_agent(data)
    assert result["action"] == "auto_reply"
    assert isinstance(result["reason"], str)
    assert len(result["reason"].strip()) > 0 