import json
from llm.gemini import GeminiClient

client = GeminiClient()

async def parse_with_llm(resume_text: str):

    prompt = f"""
You are an expert resume parser.

Extract structured data from the resume.

Return ONLY valid JSON.

Format:
{{
"name": "",
"email": "",
"phone": "",
"skills": [],
"education": [],
"experience": []
}}

Resume:
{resume_text}
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
        parsed = json.loads(clean_response)
        return parsed
    except Exception:
        return {
            "error": "Failed to parse resume",
            "raw_output": response
        }