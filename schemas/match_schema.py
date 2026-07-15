from typing import Any, Dict, List
from pydantic import BaseModel

# Request Schemas
class MatchRequest(BaseModel):
    role: str
    resume_text: str
    jd_text: str


# Response Schemas
class JDMatchResponse(BaseModel):
    score: float
    confidence: str
    component_scores: Dict[str, float]
    skill_coverage: Dict[str, Any]
    role_alignment: Dict[str, Any]


class ResumeReportResponse(BaseModel):
    overall_score: float
    grade: str
    summary: str
    structure_score: int
    contact_score: int
    content_score: int
    professional_score: int
    ats_score: int
    analysis: Dict[str, Any]
    strengths: List[str]
    recommendations: List[str]
    priority_improvements: List[str]


class RecommendationResponse(BaseModel):
    resume: List[str]
    job_match: List[str]


class MatchResponse(BaseModel):
    jd_match: JDMatchResponse
    resume_report: ResumeReportResponse
    recommendations: RecommendationResponse
    explanation: List[str]

