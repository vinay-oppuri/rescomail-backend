from agents.enhancer_agent import ats_analysis

async def calculate_ats(resume_data):
    result = await ats_analysis(resume_data)
    return result