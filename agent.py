import os
from openai import OpenAI
from dotenv import load_dotenv
from pinecone_utils import query_kb
from memory import load_memory

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def run_agent(data):
    """
    Run the agent with context from memory and knowledge base
    """
    ticket_description = data.get("prompt", "")
    ticket_id = data.get("ticket_id", "")
    
    # Get memory context if ticket_id is provided
    memory_context = ""
    if ticket_id:
        memory = load_memory(ticket_id)
        if memory:
            memory_context = f"\nPrevious conversation context: {memory[-3:] if len(memory) > 3 else memory}"
    
    # Get knowledge base results
    kb_context = ""
    try:
        kb_results = query_kb(ticket_description)
        if kb_results:
            kb_context = f"\nRelevant knowledge base information: {kb_results[:2]}"  # Limit to 2 results
    except Exception as e:
        print(f"KB query failed: {e}")
    
    # Construct the full prompt
    full_prompt = f"""
You are a customer support agent. Analyze the following ticket and provide a structured response.

Ticket Description: {ticket_description}
{memory_context}
{kb_context}

Based on the ticket description, available knowledge base information, and conversation history, determine the best action to take.

Respond ONLY in the following JSON format:
{{
    "action": "auto_reply" | "escalate" | "human_review",
    "reason": "explanation for your decision",
    "reply": "if action is auto_reply, provide a helpful response to the customer"
}}

Guidelines:
- Use "auto_reply" for simple questions, password resets, basic troubleshooting
- Use "escalate" for urgent issues, system outages, security concerns
- Use "human_review" for complex technical issues, billing disputes, or unclear requests
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.1  # Lower temperature for more consistent structured output
    )
    
    llm_output = response.choices[0].message.content
    print(f"LLM Output: {llm_output}")
    
    # Try to parse JSON from the response
    import json
    try:
        # Extract JSON from the response (in case there's extra text)
        import re
        json_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
        if json_match:
            parsed_response = json.loads(json_match.group())
            return {
                "action": parsed_response.get("action", "human_review"),
                "reason": parsed_response.get("reason", "Unable to parse response"),
                "reply": parsed_response.get("reply", "")
            }
        else:
            # Fallback if no JSON found
            return {
                "action": "human_review",
                "reason": "Could not parse structured response from LLM",
                "reply": llm_output
            }
    except json.JSONDecodeError:
        # Fallback if JSON parsing fails
        return {
            "action": "human_review",
            "reason": "Invalid JSON response from LLM",
            "reply": llm_output
        }

# For testing
if __name__ == "__main__":
    result = run_agent({
        "prompt": "I can't reset my password. The reset link is not working.",
        "ticket_id": "test-123"
    })
    print(f"Agent Result: {result}")