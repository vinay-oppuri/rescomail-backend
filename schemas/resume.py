from pydantic import BaseModel, Field
from typing import List, Optional

class ParsedResume(BaseModel):
    name: Optional[str] = Field(default="", description="Full name of the applicant")
    email: Optional[str] = Field(default="", description="Email address of the applicant")
    phone: Optional[str] = Field(default="", description="Phone number of the applicant")
    skills: List[str] = Field(default_factory=list, description="List of skills extracted from the resume")
    education: List[str] = Field(default_factory=list, description="List of educational qualifications")
    experience: List[str] = Field(default_factory=list, description="List of professional experiences")

class AtsAnalysis(BaseModel):
    ats_score: int = Field(default=0, description="ATS score from 0 to 100")
    missing_keywords: List[str] = Field(default_factory=list, description="Keywords missing from the resume")
    suggestions: List[str] = Field(default_factory=list, description="Actionable suggestions to improve the resume")

class ResumeProcessResponse(BaseModel):
    parsed_resume: ParsedResume
    ats_analysis: AtsAnalysis
    error: Optional[str] = None
