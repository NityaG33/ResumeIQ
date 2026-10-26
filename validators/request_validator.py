
from fastapi import HTTPException, UploadFile

SUPPORTED_ROLES = {
    "backend",
    "frontend",
    "software_engineer",
    "ml_engineer",
}

# Maximum text lengths
MAX_RESUME_TEXT_LENGTH = 50_000
MAX_JD_TEXT_LENGTH = 20_000


def validate_role(role: str):
    if role.lower() not in SUPPORTED_ROLES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role '{role}'.",
        )


def validate_resume_text_input(resume_text: str):
    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty.",
        )

    if len(resume_text) > MAX_RESUME_TEXT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail="Resume text must be 50,000 characters or fewer.",
        )


def validate_text_input(resume_text: str, jd_text: str):
    validate_resume_text_input(resume_text)
    validate_jd_text(jd_text)


def validate_jd_text(jd_text: str):
    if not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty.",
        )

    if len(jd_text) > MAX_JD_TEXT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail="Job description must be 20,000 characters or fewer.",
        )


def validate_resume_file(resume_file: UploadFile):
    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )
