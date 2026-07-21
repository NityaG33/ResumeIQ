from ml.utilities.skill_aliases import SKILL_ALIASES
from ml.utilities.role_profiles import get_role_profile
from .text_processing import clean_and_normalize
import re


def extract_skills(text: str) -> set:
    text = clean_and_normalize(text)
    found_skills = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"

            if re.search(pattern, text):
                found_skills.add(canonical_skill)
                break

    return found_skills


def categorize_skills(
    resume_text: str,
    jd_text: str,
    role: str,
) -> dict:
    """
    Categorizes skills found in the resume and job description.
    """

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)

    missing = jd_skills - resume_skills

    extra = resume_skills - jd_skills

    return {

        "matched": sorted(matched),

        "missing": sorted(missing),

        "extra": sorted(extra),

        "resume_skills": sorted(resume_skills),

        "jd_skills": sorted(jd_skills),
    }


