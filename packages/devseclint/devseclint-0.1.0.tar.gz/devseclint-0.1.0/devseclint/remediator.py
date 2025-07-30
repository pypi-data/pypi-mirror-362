# devseclint/remediator.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

def init_gemini(api_key: str):
    model = "gemma-3-4b-it"
    gemini_client = genai.Client(api_key=api_key)
    return gemini_client, model

def suggest_fix(issue: dict, gemini_client, model) -> str:
    prompt = f"""
You are a security configuration expert.

A user has shared this potentially insecure configuration snippet:

File: {issue['file']}
Line: {issue['line']}
Severity: {issue['severity']}
Problem: {issue['message']}
Code:
{issue['code']}

Please suggest a secure and corrected version with a short explanation.
Return only the FIXED CODE.
"""

    response = gemini_client.models.generate_content(
                model=model,
                contents=[prompt]
            )    
    return response.text.strip()
