from services.parser_service import parse_resume
from services.ats_service import calculate_ats

async def process_resume(file):
    parsed_data = await parse_resume(file)
    ats_result = await calculate_ats(parsed_data)
    return {
        "parsed_resume": parsed_data,
        "ats_analysis": ats_result
    }