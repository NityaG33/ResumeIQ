
import pytest

from ml.skills.skill_extraction import (
    extract_skills,
    categorize_skills
)

from ml.skills.skill_coverage import compute_skill_coverage


def test_extract_skills():
    text = "I have experience with Python, React and MongoDB"

    skills = extract_skills(text)

    assert "python" in skills
    assert "react" in skills
    assert "mongodb" in skills


def test_extract_skill_aliases():
    text = "I have worked with ReactJS and Node.js"

    skills = extract_skills(text)

    assert "react" in skills
    assert "nodejs" in skills


def test_extract_skills_case_insensitive():
    skills = extract_skills("PYTHON AND FASTAPI")

    assert "python" in skills
    assert "fastapi" in skills


def test_no_skills_found():
    skills = extract_skills(
        "I enjoy reading books and playing football"
    )

    assert skills == set()


def test_categorize_skills():
    resume = "Python React MongoDB"
    jd = "Python React AWS"

    result = categorize_skills(resume, jd)

    assert result["matched"] == ["python", "react"]
    assert result["missing"] == ["aws"]
    assert result["extra"] == ["mongodb"]


def test_skill_coverage_calculation():
    resume = "Python React MongoDB"
    jd = "Python React AWS"

    result = compute_skill_coverage(resume, jd)

    assert result["coverage"] == pytest.approx(2 / 3, abs=0.0001)
    assert result["matched"] == ["python", "react"]
    assert result["missing"] == ["aws"]


def test_zero_skill_coverage():
    resume = "Python"
    jd = "AWS Docker"

    result = compute_skill_coverage(resume, jd)

    assert result["coverage"] == 0.0


def test_full_skill_coverage():
    resume = "Python React MongoDB"
    jd = "Python React"

    result = compute_skill_coverage(resume, jd)

    assert result["coverage"] == 1.0


def test_empty_job_description():
    result = compute_skill_coverage(
        "Python React",
        ""
    )

    assert result["coverage"] == 0.0
