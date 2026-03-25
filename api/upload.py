from fastapi import APIRouter, UploadFile, File
from services.resume_service import process_resume 
from schemas.resume import ResumeProcessResponse

router = APIRouter()

@router.post("/upload-resume", response_model=ResumeProcessResponse)
async def upload_resume(file: UploadFile = File(...)):
    result = await process_resume(file)
    return result