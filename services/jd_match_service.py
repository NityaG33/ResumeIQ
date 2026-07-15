from ml.scoring import (
    compute_match_score,
)

def generate_jd_match(
    resume_text: str,
    jd_text: str,
    role: str,
):

    return compute_match_score(
        resume_text,
        jd_text,
        role,
    )