from fastapi import (
    HTTPException,
    UploadFile,
)

SUPPORTED_ROLES = {
    "backend",
    "frontend",
    "software_engineer",
    "ml_engineer",
}

# Validation Helpers

def validate_role(role: str):
    if role.lower() not in SUPPORTED_ROLES:

        raise HTTPException(
            status_code=400,
            detail=f"Unsupported role '{role}'."
        )


def validate_resume_text_input(
    resume_text: str,
):

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )


def validate_text_input(
    resume_text: str,
    jd_text: str,
):

    validate_resume_text_input(resume_text)

    if not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )


def validate_jd_text(jd_text: str):
    if not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    

def validate_resume_file(resume_file: UploadFile):  
    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )