import os, json
from openai import OpenAI  # swap to `from openai import OpenAI` if using OpenAI
from schema import EMAIL_SCHEMA

client = OpenAI(base_url="https://models.github.ai/inference",api_key=os.environ["GITHUB_OPENAI_AI_KEY"])

SYSTEM_PROMPT = """You are an email triage assistant for a SaaS support team.
Analyze the raw email and extract structured intent data.
Be conservative with urgency_score — only use 4-5 for genuine emergencies
(service down, data loss, security issue, active churn threat)."""



def parse_email(raw_email: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        temperature=0.3,  # low temp — this is extraction, not creativity
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_email}
        ],
        response_format=EMAIL_SCHEMA
    )
    return json.loads(response.choices[0].message.content)