import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def run_agent(data):
    prompt = data.get("prompt", "Hello, world!")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    llm_output = response.choices[0].message.content
    print(llm_output) 
    return {
        "action": "auto_reply",
        "reason": llm_output
    }

# For testing
""" 
if __name__ == "__main__":
    run_agent({"prompt": "Can you tell me a joke?"}) 
"""