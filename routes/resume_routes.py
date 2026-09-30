from fastapi import APIRouter, Depends, HTTPException
from auth.dependencies import get_current_user
from schemas.resume_schema import ResumeResponse
from services.resume_service import (
    get_user_resumes,
    get_user_resume,
    delete_user_resume,
)


router = APIRouter(
    tags=["Resumes"],
)


@router.get(
    "/resumes",
    response_model=list[ResumeResponse],
)
def get_resumes(
    current_user: dict = Depends(get_current_user),
):
    resumes = get_user_resumes(
        str(current_user["_id"])
    )

    for resume in resumes:
        resume["id"] = str(resume.pop("_id"))

    return resumes


@router.get(
    "/resumes/{resume_id}",
    response_model=ResumeResponse,
)
def get_resume(
    resume_id: str,
    current_user: dict = Depends(get_current_user),
):
    resume = get_user_resume(
        str(current_user["_id"]),
        resume_id,
    )

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    resume["id"] = str(resume.pop("_id"))

    return resume


@router.delete("/resumes/{resume_id}")
def delete_resume(
    resume_id: str,
    current_user: dict = Depends(get_current_user),
):
    deleted = delete_user_resume(
        str(current_user["_id"]),
        resume_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    return {
        "message": "Resume deleted successfully"
    }