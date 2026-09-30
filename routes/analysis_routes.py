import traceback
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from auth.dependencies import get_current_user
from services.match_service import run_match
from services.analysis_service import (
    create_analysis,
    get_user_analyses,
    get_user_analysis,
    delete_user_analysis,
)
from services.resume_service import create_resume
from ml.resume_quality import build_resume_report
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
from schemas.analysis_schema import AnalysisResponse


router = APIRouter(
    tags=["Analysis"],
)


# Resume JD Matching Endpoint
@router.post(
    "/match",
    response_model=MatchResponse,
)
def match_resume(
    request: MatchRequest,
    current_user: dict = Depends(get_current_user),
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

        create_analysis(
            user_id=str(current_user["_id"]),
            analysis_type="jd_match",
            input_type="text",
            result=result,
        )

        return MatchResponse(**result)

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )


# Resume JD Analysis Endpoint
@router.post(
    "/match-pdf",
    response_model=MatchResponse,
)
async def match_pdf(
    resume_file: UploadFile = File(...),
    role: str = Form(...),
    jd_text: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    validate_role(role)
    validate_jd_text(jd_text)

    try:
        resume_text = extract_resume_text_from_upload(resume_file)

        resume = create_resume(
            user_id=str(current_user["_id"]),
            filename=resume_file.filename,
            file_reference=resume_file.filename,
        )

        result = run_match(
            resume_text,
            jd_text,
            role,
        )

        create_analysis(
            user_id=str(current_user["_id"]),
            analysis_type="jd_match",
            input_type="pdf",
            result=result,
            resume_id=str(resume["_id"]),
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

    
# Resume Quality Analysis Endpoint
@router.post(
    "/resume-quality",
    response_model=ResumeQualityResponse,
)
def analyze_resume_quality_only(
    request: ResumeQualityRequest,
    current_user: dict = Depends(get_current_user),
):
    validate_resume_text_input(request.resume_text)

    resume_report = build_resume_report(
        request.resume_text
    )

    result = {
        "resume_report": resume_report,
        "recommendations": {
            "resume": resume_report["recommendations"],
            "job_match": [],
        },
        "explanation": [
            f"Overall Resume Score: "
            f"{resume_report['overall_score']}/100",
            resume_report["summary"],
        ],
    }

    create_analysis(
        user_id=str(current_user["_id"]),
        analysis_type="resume_quality",
        input_type="text",
        result=result,
    )

    return result


# Resume Quality PDF Analysis Endpoint
@router.post(
    "/resume-quality-pdf",
    response_model=ResumeQualityResponse,
)
async def analyze_resume_quality_pdf(
    resume_file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    try:
        resume_text = extract_resume_text_from_upload(resume_file)

        resume = create_resume(
            user_id=str(current_user["_id"]),
            filename=resume_file.filename,
            file_reference=resume_file.filename,
        )

        resume_report = build_resume_report(resume_text)

        result = {
            "resume_report": resume_report,
            "recommendations": {
                "resume": resume_report["recommendations"],
                "job_match": [],
            },
            "explanation": [
                f"Overall Resume Score: "
                f"{resume_report['overall_score']}/100",
                resume_report["summary"],
            ],
        }

        create_analysis(
            user_id=str(current_user["_id"]),
            analysis_type="resume_quality",
            input_type="pdf",
            result=result,
            resume_id=str(resume["_id"]),
        )

        return result

    except HTTPException:
        raise

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )
    

# User Analyses Retrieval Endpoint
@router.get(
    "/analyses",
    response_model=list[AnalysisResponse],
)
def get_analyses(
    current_user: dict = Depends(get_current_user),
):
    analyses = get_user_analyses(
        str(current_user["_id"])
    )

    for analysis in analyses:
        analysis["id"] = str(analysis.pop("_id"))

    return analyses


# Single Analysis Retrieval Endpoint
@router.get(
    "/analyses/{analysis_id}",
    response_model=AnalysisResponse,
)
def get_analysis(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    analysis = get_user_analysis(
        str(current_user["_id"]),
        analysis_id,
    )

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    analysis["id"] = str(analysis.pop("_id"))

    return analysis


# Delete Analysis Endpoint
@router.delete("/analyses/{analysis_id}")
def delete_analysis(
    analysis_id: str,
    current_user: dict = Depends(get_current_user),
):
    deleted = delete_user_analysis(
        str(current_user["_id"]),
        analysis_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return {
        "message": "Analysis deleted successfully"
    }


