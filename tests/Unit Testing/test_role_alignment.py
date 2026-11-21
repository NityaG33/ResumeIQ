
import pytest

from ml.roles.role_alignment import compute_role_alignment


def test_backend_role_alignment():
    resume = "Python FastAPI Docker MongoDB"

    result = compute_role_alignment(
        resume,
        "backend"
    )

    assert result["role"] == "Backend Developer"
    assert result["alignment_score"] == 0.5

    assert result["matched_role_skills"] == [
        "docker",
        "fastapi",
        "mongodb",
        "python"
    ]


def test_frontend_role_alignment():
    resume = "React JavaScript HTML CSS"

    result = compute_role_alignment(
        resume,
        "frontend"
    )

    assert result["role"] == "Frontend Developer"

    assert result["alignment_score"] == 0.25

    assert len(result["matched_role_skills"]) == 2


def test_zero_role_alignment():
    resume = "Cooking photography gardening"

    result = compute_role_alignment(
        resume,
        "backend"
    )

    assert result["alignment_score"] == 0.0
    assert result["matched_role_skills"] == []


def test_role_alignment_is_capped_at_one():
    resume = """
    Python Java SQL PostgreSQL MySQL
    FastAPI Django Flask Node.js Express
    Docker Git GitHub AWS MongoDB Redis
    """

    result = compute_role_alignment(
        resume,
        "backend"
    )

    assert result["alignment_score"] == 1.0


def test_role_is_case_insensitive():
    result = compute_role_alignment(
        "Python FastAPI",
        "BACKEND"
    )

    assert result["role"] == "Backend Developer"


def test_invalid_role_defaults_to_software_engineer():
    result = compute_role_alignment(
        "Python Java SQL",
        "invalid_role"
    )

    assert result["role"] == "Software Engineer"


def test_empty_resume():
    result = compute_role_alignment(
        "",
        "backend"
    )

    assert result["alignment_score"] == 0.0
    assert result["matched_role_skills"] == []


def test_missing_role_skills_are_returned():
    result = compute_role_alignment(
        "Python FastAPI",
        "backend"
    )

    assert "docker" in result["additional_technologies"]
    assert "mongodb" in result["additional_technologies"]
