import anthropic
import json
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/satyapramodr/Documents/ai-engineer-journey/.env')
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    temperature=0.1,
    system="""You are a data extraction assistant.
You MUST respond with valid JSON only.
No explanation. No markdown. No backticks.
Just the raw JSON object.

Schema:
{
  "name": string,
  "role": string,
  "skills": array of strings,
  "experience_years": number,
  "hire_recommendation": "yes" | "no" | "maybe"
}""",
    messages=[
        {"role": "user", "content": """
Evaluate this candidate:
John has been a software engineer for 6 years. 
He knows Python, React, and PostgreSQL. 
He has built 2 production apps but no AI experience.
"""}
    ]
)

# Get the raw text
raw = response.content[0].text
print("=== RAW RESPONSE ===")
print(raw)

# Parse it as actual JSON
parsed = json.loads(raw)
print("\n=== PARSED JSON ===")
print(f"Name: {parsed['name']}")
print(f"Role: {parsed['role']}")
print(f"Skills: {', '.join(parsed['skills'])}")
print(f"Experience: {parsed['experience_years']} years")
print(f"Hire: {parsed['hire_recommendation']}")