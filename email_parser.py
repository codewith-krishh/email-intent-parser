import os, json
from groq import Groq
from schema import EMAIL_SCHEMA

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an email triage assistant for a SaaS support team.
Analyze the raw email and extract structured intent data.
Be conservative with urgency_score — only use 4-5 for genuine emergencies
(service down, data loss, security issue, active churn threat)."""



def parse_email(raw_email: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.3,  # low temp — this is extraction, not creativity
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_email}
        ],
        response_format=EMAIL_SCHEMA
    )
    return json.loads(response.choices[0].message.content)