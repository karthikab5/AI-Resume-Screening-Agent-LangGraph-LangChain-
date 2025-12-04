import os
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from typing import TypedDict, Optional, Literal
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import Optional
from docx import Document  
from langchain_openai import ChatOpenAI

#client = Client(api_key=os.environ.get("langsmith_API_KEY"))

#LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")

load_dotenv(override=True)
OPENAI_API_KEY = os.environ.get("API_KEY") 


llm =  ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

def read_docx(file_path: str) -> str:
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

JOB_DESCRIPTIONS = {
    "software_engineer": {
        "title": "Software Engineer",
        "description": "Requires 3-5 years experience with Python, Django, and deep knowledge of PostgreSQL. Focus on REST API development and data integrity."
    }
}
class State(TypedDict):
    application: str
    job_description: str 
    skills_reasoning: Optional[str] = None
    skill_score:Optional[int] 
    experience: str = None
    email: Optional[str] = None


def skill_identifier(state:State)->State:
    prompt = ChatPromptTemplate.from_template(
        """
        Read the following application and return exactly:
        1. A skill match score from 0 - 100
        2. A short reason explaining why

        Respond in JSON:
        {{
            "score": <number>,
            "reason": "<text>"
        }}

        Application: {application}
        Job_description:{job_description}
        """
    )

    response = llm.invoke(prompt.format(application=state["application"],job_description=state["job_description"])).content
    
    
    
    import json, re

    response_clean = re.sub(r"```json|```", "", response).strip()

    try:
        parsed = json.loads(response_clean)
        score = parsed.get("score")
        reason = parsed.get("reason")
    except:
        score = None
        reason = response
    
    return {
        "skill_score": score,
        "skills_reasoning": reason
    }

def experience_identifier(state:State)->State:
    prompt  = ChatPromptTemplate.from_template("""
You are an HR assistant. Read the following job application and classify the experience level.

Job Application:
{application}

Instructions:
- Junior: < 3 years of experience
- Mid: 3–7 years
- Senior: > 7 years

Reply ONLY with one of the following labels: 'junior_level', 'mid_level', 'senior_level'.
""")

    experience = llm.invoke(prompt.format(application=state['application'])).content
    return {"experience":experience}
    
def save_candidate(state:State)->State:
    print("\n\n applicant details has been saved into database for future")
    email ="We will not be moving forward with your application at the moment but will let you know when their is a job that matches your experince"
    return {"email":email}
      
def pass_hr(state:State)->State:
    print("\n\n applicant details has been saved into database for future")
    email ="candidate profile meets JD"
    return {"email":email}

def rejected_candidate(state:State)->State:
    print("\n\n applicant details has been saved into database for future")
    email = "We will not be moving forward with your application at the moment"
    return {"email":email}
def router_agent(state:State)->State:
    if state['skill_score'] >75 :
        if state['experience'] in ['senior_level' ,'mid_level','junior_level']  :
            return 'pass_hr'
        else:
            return "rejected_candidate"

    elif state['skill_score'] <75:
        if state['experience'] in ['senior_level', 'mid_level']:
            return 'save_candidate'
        else:
            return "rejected_candidate"


    else:
        return END

    
graph = StateGraph(State)

graph.add_node("skill_identifier",skill_identifier)
graph.add_node("experience_identifier",experience_identifier)
graph.add_node("pass_hr",pass_hr)
graph.add_node("rejected_candidate",rejected_candidate)
graph.add_node("save_candidate",save_candidate)



graph.add_edge(START,"skill_identifier")
graph.add_edge("skill_identifier","experience_identifier")
graph.add_conditional_edges("experience_identifier", router_agent, {
    "pass_hr": "pass_hr",
    "save_candidate": "save_candidate",
    "rejected_candidate": "rejected_candidate",
    END: END
})

chain = graph.compile()

png_bytes = chain.get_graph(xray=True).draw_mermaid_png()

# Save as a file
with open("langgraph_flow.png", "wb") as f:
    f.write(png_bytes)

print("Graph saved as langgraph_flow.png")