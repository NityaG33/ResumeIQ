from .skill_extraction import categorize_skills


def compute_skill_coverage(
    resume_text: str,
    jd_text: str,
    role: str,
) -> dict:
    """
    Computes the percentage of JD skills
    covered by the resume.
    """

    analysis = categorize_skills(
        resume_text,
        jd_text,
        role,
    )

    jd_skills = set(analysis["jd_skills"])
    resume_skills = set(analysis["resume_skills"])

    matched = set(analysis["matched"])

    coverage = 0.0

    if jd_skills:
        coverage = len(matched) / len(jd_skills)

    return {

        "coverage": round(coverage, 4),

        "matched": analysis["matched"],

        "missing": analysis["missing"],

        "extra": analysis["extra"],

        "resume_skills": analysis["resume_skills"],

        "jd_skills": analysis["jd_skills"],
    }


if __name__ == "__main__":

    resume = """
    Python SQL Docker FastAPI
    """

    jd = """
    Python SQL Docker AWS
    """

    print(
        compute_skill_coverage(
            resume,
            jd,
            "backend",
        )
    )