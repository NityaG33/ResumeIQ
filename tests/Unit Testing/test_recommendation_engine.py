
from ml.recommendation_engine import generate_recommendations


def test_backend_missing_skill_recommendation():
    skill_analysis = {
        "missing": ["python"]
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert any(
        "FastAPI or Django" in recommendation
        for recommendation in result
    )


def test_frontend_missing_skill_recommendation():
    skill_analysis = {
        "missing": ["react"]
    }

    result = generate_recommendations(
        skill_analysis,
        "frontend"
    )

    assert any(
        "React application" in recommendation
        for recommendation in result
    )


def test_unknown_skill_gets_generic_recommendation():
    skill_analysis = {
        "missing": ["kubernetes"]
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert any(
        "kubernetes" in recommendation
        for recommendation in result
    )


def test_empty_missing_skills():
    skill_analysis = {
        "missing": []
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert len(result) == 4


def test_general_recommendations_are_always_added():
    skill_analysis = {
        "missing": []
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert any("Quantify achievements" in r for r in result)
    assert any("GitHub and LinkedIn" in r for r in result)
    assert any("Tailor your Skills section" in r for r in result)


def test_role_is_case_insensitive():
    skill_analysis = {
        "missing": ["python"]
    }

    result = generate_recommendations(
        skill_analysis,
        "BACKEND"
    )

    assert any(
        "FastAPI or Django" in recommendation
        for recommendation in result
    )


def test_duplicate_recommendations_are_removed():
    skill_analysis = {
        "missing": ["python", "python"]
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert len(result) == len(set(result))


def test_recommendations_are_sorted():
    skill_analysis = {
        "missing": ["python", "docker"]
    }

    result = generate_recommendations(
        skill_analysis,
        "backend"
    )

    assert result == sorted(result)
