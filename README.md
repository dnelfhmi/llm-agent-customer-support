## 🚀 Smart Support Agent — Autonomous Ticket Workflow with LangGraph & FastAPI

A repository for documenting the development of agentic LLM customer support.
An autonomous agentic support ticket workflow built with FastAPI, LangGraph, and Pinecone.

-----

### 🤖 What is this project?

This is an agentic customer support ticket system built from scratch (no low-code tools like n8n).
It shows how to build an LLM-powered support agent that:

	•	Understands incoming tickets
	•	Retrieves relevant policy knowledge dynamically
	•	Uses real-time tools (like courier tracking)
	•	Keeps conversation memory
	•	Plans actions autonomously (auto-reply, escalate, or human review)
	•	Executes routing — all in Python with LangGraph, Pinecone, and FastAPI.

-----

### 🛠️ How does it work?

1️⃣ Receive:
A FastAPI Webhook receives tickets.

2️⃣ Understand & Retrieve:
The agent:

	•	Generates embeddings for the ticket text.
	•	Queries Pinecone for relevant KB snippets.
	•	Optionally calls Courier Tracking API for live status.
	•	Pulls conversation Memory for context.

3️⃣ Plan Next Best Action:
Using LangGraph, the agent reasons:

	•	Should we auto-reply?
	•	Is this high urgency — escalate to manager?
	•	Or send for human review?

It outputs structured JSON only.

4️⃣ Route & Act:
The server routes the action:

	•	Auto-replies with KB snippets.
	•	Notifies manager via Slack/Email.
	•	Or pauses for human review.

Every step is logged for traceability and future fine-tuning.

-----

### ⚡ What tools & tech does it use?

✅ FastAPI — Webhook & API server

✅ LangGraph — LLM orchestration, planning & tool use

✅ Pinecone — Vector search for relevant knowledge

✅ OpenAI Embeddings — Semantic text search

✅ Session Memory — Keep context across messages

✅ Optional Tools — Real-time APIs: Courier, CRM, Weather

✅ Logging — JSON logs for replay & auditing

-----

### 📈 What's next?

TO-DO: 

⚠️ Pinecone vector DB integration

⚠️ Real-time tools (or any tools to add)

⚠️ Generating embedding and retrieving knowledge base for similarity search

⚠️ Action routing based on LLM agent suggestion

⚠️ UI for easy usage and navigation

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root with the following content:
   ```env
   OPENAI_API_KEY=your-openai-key-here
   ```
   **Do NOT commit your `.env` file to git.**

3. POST via /tickets endpoints.

