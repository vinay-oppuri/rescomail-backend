import io
import json
from pypdf import PdfReader
from llm.gemini import GeminiClient
from schemas.resume import ParsedResume, AtsAnalysis, ResumeProcessResponse

client = GeminiClient()

async def _parse_with_llm(resume_text: str) -> ParsedResume:
    prompt = f"""
You are an expert resume parser.

Extract structured data from the resume.

Return ONLY valid JSON.

Format exactly like this strictly matching keys:
{{
"name": "",
"email": "",
"phone": "",
"skills": ["skill1", "skill2"],
"education": ["edu1", "edu2"],
"experience": ["exp1", "exp2"]
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
        return ParsedResume(**parsed)
    except Exception as e:
        return ParsedResume(name="Error parsing resume", skills=[])

async def _ats_analysis(resume_data: str) -> AtsAnalysis:
    prompt = f"""
You are an ATS (Applicant Tracking System).

Evaluate the resume and return:

1. ATS score (0-100)
2. Missing keywords
3. Suggestions to improve the resume

Return ONLY strictly valid JSON in this exact format:

{{
"ats_score": 85,
"missing_keywords": ["keyword1"],
"suggestions": ["suggestion1"]
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
        return AtsAnalysis(**result)
    except Exception as e:
        return AtsAnalysis(ats_score=0, missing_keywords=[], suggestions=[])

async def _extract_base_text(file) -> str:
    content = await file.read()
    if file.filename.lower().endswith('.pdf'):
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    else:
        text = content.decode('utf-8')
    return text

async def process_resume(file) -> ResumeProcessResponse:
    text = await _extract_base_text(file)
        
    if not text.strip():
        return ResumeProcessResponse(
            parsed_resume=ParsedResume(),
            ats_analysis=AtsAnalysis(),
            error="No text could be extracted from the file. It might be a scanned document or image."
        )
        
    parsed_data = await _parse_with_llm(text)
    # Convert validated pydantic object to json string for ATS analysis
    resume_json_str = parsed_data.model_dump_json()
    ats_result = await _ats_analysis(resume_json_str)
    
    return ResumeProcessResponse(
        parsed_resume=parsed_data,
        ats_analysis=ats_result
    )