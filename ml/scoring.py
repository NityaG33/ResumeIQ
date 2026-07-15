from ml.utilities.config import (
    SKILL_COVERAGE_WEIGHT,
    EMBEDDING_WEIGHT,
    RESUME_QUALITY_WEIGHT,
    TFIDF_WEIGHT,
    ROLE_ALIGNMENT_WEIGHT,
)

from .skill_coverage import compute_skill_coverage
from .embedding_similarity import embedding_similarity
from .similarity import text_similarity
from .role_alignment import compute_role_alignment
from .resume_quality import (
    build_resume_report,
)


def compute_match_score(
    resume_text: str,
    jd_text: str,
    role: str,
) -> dict:
    """ Computes the final Resume-JD match score by combining
    independent scoring modules."""

    
    # Skill Coverage
    
    coverage = compute_skill_coverage(
        resume_text,
        jd_text,
        role,
    )

    coverage_score = coverage["coverage"]

    
    # Embedding Similarity

    embedding_score = embedding_similarity(
        resume_text,
        jd_text,
    )

    
    # Resume Report

    resume_report = build_resume_report(
        resume_text,
    )

    resume_quality_score = (
        resume_report["overall_score"] / 100
    )

    
    # TF-IDF
    
    tfidf_score = text_similarity(
        resume_text,
        jd_text,
    )

    
    # Role Alignment
    
    role_alignment = compute_role_alignment(
        resume_text,
        role,
    )

    role_alignment_score = (
        role_alignment["alignment_score"]
    )

    
    # Final Weighted Score
    
    final_score = (
        coverage_score * SKILL_COVERAGE_WEIGHT
        + embedding_score * EMBEDDING_WEIGHT
        + resume_quality_score * RESUME_QUALITY_WEIGHT
        + tfidf_score * TFIDF_WEIGHT
        + role_alignment_score * ROLE_ALIGNMENT_WEIGHT
    )

    final_percentage = round(
        final_score * 100,
        2,
    )

    confidence = classify_match_confidence(
        final_percentage,
        coverage_score,
        embedding_score,
    )

    return {

        "final_score": final_percentage,

        "confidence": confidence,

        "skill_coverage": coverage,

        "resume_report": resume_report,

        "role_alignment": role_alignment,

        "component_scores": {

            "skill_coverage": round(
                coverage_score * 100,
                2,
            ),

            "embedding_similarity": round(
                embedding_score * 100,
                2,
            ),

            "resume_quality": round(
                resume_quality_score * 100,
                2,
            ),

            "tfidf_similarity": round(
                tfidf_score * 100,
                2,
            ),

            "role_alignment": round(
                role_alignment_score * 100,
                2,
            ),
        },
    }


def classify_match_confidence(
    final_score: float,
    coverage_score: float,
    embedding_score: float,
) -> str:
    """
    Rule-based confidence classification.
    """

    coverage = coverage_score * 100
    embedding = embedding_score * 100

    # Strong Match
    if (
        final_score >= 80
        and coverage >= 70
        and embedding >= 70
    ):
        return "Strong Match"

    # Moderate Match
    if final_score >= 60:
        return "Moderate Match"

    # Weak Match
    return "Weak Match"