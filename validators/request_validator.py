from fastapi import (
    FastAPI,
    HTTPException,
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


def validate_text_input(
    resume_text: str,
    jd_text: str,
):

    if not resume_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Resume text cannot be empty."
        )

    if not jd_text.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )
