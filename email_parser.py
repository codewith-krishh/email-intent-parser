import os, json
from groq import Groq
from schema import EmailAnalysis

client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are an email triage assistant for a SaaS support team.
Analyze the raw email and extract structured intent data.
Be conservative with urgency_score — only use 4-5 for genuine emergencies
(service down, data loss, security issue, active churn threat)."""

def parse_email(raw_email: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + f"\n\nRespond ONLY with valid JSON matching this structure: {EmailAnalysis.model_json_schema()}"},
            {"role": "user", "content": raw_email}
        ],
        response_format={"type": "json_object"}
    )
    raw_json = json.loads(response.choices[0].message.content)
    validated = EmailAnalysis.model_validate(raw_json)  # catches bad output here, not downstream in the UI
    return validated.model_dump()