import json
from llm.gemini import GeminiClient

client = GeminiClient()

async def ats_analysis(resume_data):

    prompt = f"""
You are an ATS (Applicant Tracking System).

Evaluate the resume and return:

1. ATS score (0-100)
2. Missing keywords
3. Suggestions to improve the resume

Return JSON in this format:

{{
"ats_score": number,
"missing_keywords": [],
"suggestions": []
}}

Resume data:
{resume_data}
"""

    response = await client.generate(prompt)

    clean_response = response.strip()
    if clean_response.startswith("```json"):
        clean_response = clean_response[7:]
    elif clean_response.startswith("```"):
        clean_response = clean_response[3:]
    if clean_response.endswith("```"):
        clean_response = clean_response[:-3]
    clean_response = clean_response.strip()

    try:
        result = json.loads(clean_response)
        return result
    except Exception:
        return {
            "error": "Failed ATS analysis",
            "raw_output": response
        }