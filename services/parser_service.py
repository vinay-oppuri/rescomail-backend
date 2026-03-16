import io
from pypdf import PdfReader
from agents.parser_agent import parse_with_llm

async def parse_resume(file):
    content = await file.read()
    if file.filename.lower().endswith('.pdf'):
        reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    else:
        text = content.decode('utf-8')
        
    if not text.strip():
        return {
            "error": "No text could be extracted from the file. It might be a scanned document or image.",
            "parsed_resume": {},
            "ats_analysis": {}
        }
        
    structured_data = await parse_with_llm(text)
    return structured_data