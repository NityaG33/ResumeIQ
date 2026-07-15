# ==================================================
# Imports & Configuration
# ==================================================

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import CORE_SKILLS, OPTIONAL_SKILLS, SKILLS
from skill_normalizer import SKILL_SYNONYMS
import re

CORE_SKILL_PENALTY = 0.25      # 25% penalty per missing core skill
OPTIONAL_SKILL_PENALTY = 0.05 # 5% penalty per missing optional skill


# ==================================================
# 1. TEXT NORMALIZATION
# ==================================================

def normalize_text(text: str) -> str:
    """
    Normalize text by lowercasing and expanding skill synonyms
    (e.g., ML -> machine learning).
    """
    text = text.lower()

    for short, full in SKILL_SYNONYMS.items():
        pattern = r"\b" + re.escape(short) + r"\b"
        text = re.sub(pattern, full, text)

    return text


def clean_and_normalize(text: str) -> str:
    return normalize_text(text)


# ==================================================
# 2. SKILL EXTRACTION
# ==================================================

def extract_skills(text: str) -> set:
    """
    Extract only valid skills from text using a whitelist.
    """
    tokens = set(text.split())
    return {token for token in tokens if token in SKILLS}


# ==================================================
# 3. SIMILARITY CALCULATIONS
# ==================================================

def skill_similarity(resume_text: str, jd_text: str) -> float:
    """
    Measures how many required skills from the JD
    are present in the resume.
    """
    resume_text = clean_and_normalize(resume_text)
    jd_text = clean_and_normalize(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    if not jd_skills:
        return 0.0

    matched = resume_skills.intersection(jd_skills)
    return len(matched) / len(jd_skills)


def calculate_similarity(resume_text: str, jd_text: str) -> float:
    """
    Computes overall textual similarity using TF-IDF + cosine similarity.
    """
    documents = [
        clean_and_normalize(resume_text),
        clean_and_normalize(jd_text)
    ]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return score[0][0]


# ==================================================
# 4. SKILL CATEGORIZATION (CORE LOGIC)
# ==================================================

def categorize_skills(resume_text: str, jd_text: str) -> dict:
    """
    Categorizes skills into matched, missing core, and missing optional.
    """
    resume_text = clean_and_normalize(resume_text)
    jd_text = clean_and_normalize(jd_text)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched = resume_skills.intersection(jd_skills)
    missing = jd_skills - resume_skills

    return {
        "matched": list(matched),
        "missing_core": list(missing.intersection(CORE_SKILLS)),
        "missing_optional": list(missing.intersection(OPTIONAL_SKILLS))
    }


# ==================================================
# 5. EXPLAINABILITY ENGINE
# ==================================================

def explain_match(resume_text: str, jd_text: str) -> list:
    """
    Generates human-readable explanations for the match result.
    """
    categories = categorize_skills(resume_text, jd_text)
    explanation = []

    if categories["matched"]:
        explanation.append(
            "Matched skills: " + ", ".join(categories["matched"])
        )

    if categories["missing_core"]:
        explanation.append(
            "Missing CORE skills: " + ", ".join(categories["missing_core"])
        )

    if categories["missing_optional"]:
        explanation.append(
            "Missing OPTIONAL skills: " + ", ".join(categories["missing_optional"])
        )

    if not categories["missing_core"]:
        explanation.append("No critical skill gaps detected.")

    return explanation


def explainability_engine(resume_text: str, jd_text: str) -> dict:
    """
    Structured explainability output (JSON-ready).
    """
    return {
        "skill_analysis": categorize_skills(resume_text, jd_text),
        "explanation_text": explain_match(resume_text, jd_text)
    }


# ==================================================
# 6. SKILL PENALTY ENGINE
# ==================================================

def compute_skill_penalty(skill_analysis: dict) -> float:
    """
    Computes penalty based on missing core and optional skills.
    """
    missing_core = skill_analysis["missing_core"]
    missing_optional = skill_analysis["missing_optional"]

    core_penalty = len(missing_core) * CORE_SKILL_PENALTY
    optional_penalty = len(missing_optional) * OPTIONAL_SKILL_PENALTY

    total_penalty = core_penalty + optional_penalty

    return min(total_penalty, 0.9)


# ==================================================
# 7. DECISION-AWARE FINAL SCORE
# ==================================================

def decision_aware_final_score(resume_text: str, jd_text: str) -> dict:
    """
    Computes the final hiring-aware score by applying
    penalties to the base ML score.
    """
    text_score = calculate_similarity(resume_text, jd_text)
    skill_score = skill_similarity(resume_text, jd_text)

    base_score = (0.7 * skill_score) + (0.3 * text_score)

    skill_analysis = categorize_skills(resume_text, jd_text)
    penalty = compute_skill_penalty(skill_analysis)

    final_score = base_score * (1 - penalty)

    return {
        "final_score": round(final_score * 100, 2),
        "base_score": round(base_score * 100, 2),
        "penalty_applied": round(penalty * 100, 2),
        "skill_analysis": skill_analysis
    }


# ==================================================
# 8. TESTING / DEMO
# ==================================================

if __name__ == "__main__":
    resume = """
    Python developer with experience in ml, data analysis,
    Flask, and REST APIs.
    """

    jd = """
    Looking for a software engineer with strong Python skills,
    experience in machine learning and backend development.
    """

    print("Text Similarity Score:",
          round(calculate_similarity(resume, jd) * 100, 2), "%")

    explanation = explainability_engine(resume, jd)
    print("\nExplainability Report:")
    for line in explanation["explanation_text"]:
        print("-", line)

    result = decision_aware_final_score(resume, jd)
    print("\nDecision-Aware Scoring:")
    print("Base Score:", result["base_score"], "%")
    print("Penalty Applied:", result["penalty_applied"], "%")
    print("Final Score:", result["final_score"], "%")
