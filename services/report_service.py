from ml.resume_quality import (
    build_resume_report,
)

def generate_resume_report(
    resume_text: str,
) -> dict:
    """
    Generates the complete Resume Report.
    """

    return build_resume_report(
        resume_text
    )