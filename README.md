# AI-Resume Screening Agent


A lightweight, fast, and cheap LLM-powered pipeline that screens job applications using LangGraph and GPT-4o-mini.
It evaluates skills, experience level, matches against a job description, and routes the candidate to the right HR action.

This project is optimized for low-cost LLM calls, clean modular design, and real-world HR workflows.

🚀 Features

✅ 1. Skill Matching (0–100 Score)

Reads the candidate’s resume (.docx)

Gives a score

Provides an explanation with reasons

Uses structured JSON extraction for reliable parsing

✅ 2. Experience Classification

Classifies into:

junior_level

mid_level

senior_level

Based on extracted experience from the application.

✅ 3. Routing Logic (AI Agent Router)

Your pipeline decides:

Skill Score	Experience	Route
> 75	any	pass_hr
< 75	senior/mid	save_candidate
< 75	junior	rejected_candidate
✅ 4. End-to-End AI Workflow Using LangGraph

Graph nodes:

skill_identifier

experience_identifier

pass_hr

save_candidate

rejected_candidate

LangGraph allows branching/conditional execution like a real AI agent system.

✅ 5. Low-Cost LLM Usage

The project uses:

gpt-4o-mini → super cheap, fast, reliable

Minimal prompt size

No unnecessary model calls

🧩 Architecture (Graph Overview)
<img width="545" height="432" alt="image" src="https://github.com/user-attachments/assets/15b37a4a-0067-4f52-a924-be166c64e02f" />


📦 Installation

Clone the repo:

git clone https://github.com/YOUR_USERNAME/ai-resume-screening.git
cd ai-resume-screening


Install dependencies:

pip install -r requirements.txt

🔑 Environment Variable

Create a .env file:

API_KEY=your_openai_api_key_here

▶️ Run the Script

Place your resume .docx file in the folder.

Then run:

python app.py

📄 Example Output
{
  'skill_score': 82,
  'skills_reasoning': 'Strong Python, SQL, ETL background…',
  'experience': 'mid_level',
  'email': 'candidate profile meets JD'
}

📚 Tech Stack

LangChain

LangGraph

OpenAI GPT-4o-mini

Python DOCX

Pydantic

dotenv

⭐ Why This Project Is Impressive for Recruiters

Demonstrates agentic workflows (hot skill in Canada tech roles)

Shows understanding of routing, structured LLM reasoning, JSON parsing, workflow automation

Uses LangGraph — highly in-demand for enterprise AI

Clean architecture recruiters love

Your own end-to-end AI system, not just typical RAG
