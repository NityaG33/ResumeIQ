from .skill_extraction import categorize_skills


def explain_match(result: dict) -> list:
    """
    Generates a human-readable explanation of the
    Resume-JD match.
    """

    explanation = []

    coverage = result["skill_coverage"]
    report = result["resume_report"]
    components = result["component_scores"]

    explanation.append(
        f"Skill Coverage: {components['skill_coverage']}%"
    )

    explanation.append(
        f"Embedding Similarity: {components['embedding_similarity']}%"
    )

    explanation.append(
        f"Overall Resume Score: {report['overall_score']}/100"
    )

    explanation.append(
        f"Resume Grade: {report['grade']}"
    )

    explanation.append(
        f"Role Alignment: {components['role_alignment']}%"
    )

    explanation.append(
        report["summary"]
    )

    if coverage["matched"]:
        explanation.append(
            "Matched Skills: "
            + ", ".join(coverage["matched"])
        )

    missing = coverage["missing"]

    if missing:
        explanation.append(
            "Missing Skills: "
            + ", ".join(missing)
        )

    if report["strengths"]:
        explanation.append(
            "Resume Strengths: "
            + "; ".join(report["strengths"])
        )

    if report["priority_improvements"]:
        explanation.append(
            "Priority Improvements: "
            + "; ".join(report["priority_improvements"])
        )

    return explanation


def explainability_engine(result: dict) -> dict:
    """
    Generates explainability information
    from the complete match result.
    """

    return {
        "explanation_text": explain_match(result)
    }