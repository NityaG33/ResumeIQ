"""
Role Alignment Module

Measures how well a resume aligns with the selected
role profile based on representative skills.
"""

from .skill_extraction import extract_skills
from ml.utilities.role_profiles import get_role_profile


def compute_role_alignment(
    resume_text: str,
    role: str,
) -> dict:
    """
    Computes how closely the resume matches
    the representative skill set of a role.
    """

    resume_skills = extract_skills(resume_text)

    role_profile = get_role_profile(role)

    role_skills = role_profile["skills"]

    matched = resume_skills.intersection(role_skills)

    missing = role_skills - resume_skills

    alignment_score = 0.0

    if len(role_skills) > 0:
        expected = role_profile["expected_skills"]

        alignment_score = min(len(matched) / expected, 1.0)

    return {

        "role": role_profile["name"],

        "alignment_score": round(alignment_score, 4),

        "matched_role_skills": sorted(matched),

        "missing_role_skills": sorted(missing)
    }

if __name__ == "__main__":

    resume = """
    Python
    SQL
    FastAPI
    Docker
    Git
    """

    print(
        compute_role_alignment(
            resume,
            "backend"
        )
    )