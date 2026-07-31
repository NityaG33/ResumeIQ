import traceback
from services.match_service import run_match
from ml.resume_quality import build_resume_report
from fastapi.middleware.cors import CORSMiddleware
from utils.pdf_utils import extract_resume_text_from_upload

from schemas.match_schema import (
    MatchRequest,
    MatchResponse,
    ResumeQualityRequest,
    ResumeQualityResponse,
)

from validators.request_validator import (
    validate_jd_text,
    validate_role,
    validate_resume_text_input,
    validate_text_input,
)

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
)


# FastAPI App

app = FastAPI(
    title="AI Resume Intelligence Platform",
    description=(
        "An explainable AI-powered Resume Intelligence Platform "
        "that evaluates Resume Quality, ATS Friendliness "
        "and Resume-JD Matching."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Constants

SUPPORTED_ROLES = {
    "backend",
    "frontend",
    "software_engineer",
    "ml_engineer",
}


# Root Endpoint

@app.get("/")
def root():

    return {
        "application": "AI Resume Intelligence Platform",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs"
    }


# Resume Text Matching Endpoint

@app.post(
    "/api/v1/match",
    response_model=MatchResponse,
)
def match_resume(
    request: MatchRequest,
):

    try:
        validate_role(request.role)

        validate_text_input(
            request.resume_text,
            request.jd_text,
        )

        result = run_match(
            request.resume_text,
            request.jd_text,
            request.role,
        )

        return MatchResponse(**result)

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


# Resume Quality Endpoint

@app.post(
    "/api/v1/resume-quality",
    response_model=ResumeQualityResponse,
)
def analyze_resume_quality_only(
    request: ResumeQualityRequest,
):

    validate_resume_text_input(request.resume_text)

    resume_report = build_resume_report(request.resume_text)

    return {
        "resume_report": resume_report,
        "recommendations": {
            "resume": resume_report["recommendations"],
            "job_match": [],
        },
        "explanation": [
            f"Overall Resume Score: {resume_report['overall_score']}/100",
            resume_report["summary"],
        ],
    }


# Resume PDF Matching Endpoint

@app.post(
    "/api/v1/match-pdf",
    response_model=MatchResponse,
)
async def match_pdf(
    resume_file: UploadFile = File(...),
    role: str = Form(...),
    jd_text: str = Form(...),
):

    validate_role(role)
    validate_jd_text(jd_text)

    try:
        resume_text = extract_resume_text_from_upload(resume_file)

        result = run_match(
            resume_text,
            jd_text,
            role,
        )

        return MatchResponse(**result)

    except HTTPException:
        raise


    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


# Resume PDF Quality Endpoint

@app.post(
    "/api/v1/resume-quality-pdf",
    response_model=ResumeQualityResponse,
)
async def analyze_resume_quality_pdf(
    resume_file: UploadFile = File(...),
):


    try:
        resume_text = extract_resume_text_from_upload(resume_file)

        resume_report = build_resume_report(
            resume_text,
        )

        return {
            "resume_report": resume_report,
            "recommendations": {
                "resume": resume_report["recommendations"],
                "job_match": [],
            },
            "explanation": [
                f"Overall Resume Score: {resume_report['overall_score']}/100",
                resume_report["summary"],
            ],
        }

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
