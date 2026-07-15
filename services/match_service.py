from ml.scoring import compute_match_score
from ml.explainability import explainability_engine
from ml.recommendation_engine import generate_recommendations


def run_match(
    resume_text: str,
    jd_text: str,
    role: str,
):
    
    """ Runs the complete Resume-JD matching pipeline. """

    # Match Score
    result = compute_match_score(
        resume_text,
        jd_text,
        role,
    )


    # Explainability
    explanation = explainability_engine(
        result
    )


    # JD Recommendations
    recommendations = generate_recommendations(
        result["skill_coverage"],
        role,
    )

    return {

        # JD Match
        "jd_match": {
            "score": result["final_score"],
            "confidence": result["confidence"],
            "component_scores": result["component_scores"],
            "skill_coverage": result["skill_coverage"],
            "role_alignment": result["role_alignment"],
        },
        
        # Resume Report
        "resume_report": result["resume_report"],

        # Recommendations
        "recommendations": {
            "resume": result["resume_report"]["recommendations"],

            "job_match": recommendations
        },

        # Explainability
        "explanation": explanation["explanation_text"],
    }