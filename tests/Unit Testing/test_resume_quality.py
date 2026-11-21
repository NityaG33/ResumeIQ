
import pytest

from ml.resume_quality import (
    detect_sections,
    detect_contact_information,
    detect_quantified_achievements,
    detect_action_verbs,
    detect_bullet_points,
    analyze_resume_length,
    compute_resume_quality_score,
    get_resume_grade,
    generate_resume_recommendations,
)


def test_detect_all_resume_sections():
    resume = """
    Skills
    Python, React

    Projects
    ResumeIQ

    Experience
    Software Developer

    Education
    Bachelor's Degree
    """

    result = detect_sections(resume)

    assert all(result.values())


def test_detect_missing_sections():
    result = detect_sections("Python developer with experience")

    assert result["skills"] is False
    assert result["projects"] is False
    assert result["education"] is False


def test_detect_contact_information():
    resume = """
    Email: test@example.com
    Phone: 987-654-3210
    GitHub: github.com/testuser
    LinkedIn: linkedin.com/in/testuser
    """

    result = detect_contact_information(resume)

    assert all(result.values())


def test_detect_missing_contact_information():
    result = detect_contact_information("Python developer")

    assert not any(result.values())


def test_detect_quantified_achievements():
    resume = """
    Developed APIs and reduced response time by 35%.
    Solved 400+ coding problems.
    """

    result = detect_quantified_achievements(resume)

    assert result["count"] == 2
    assert result["present"] is True
    assert len(result["examples"]) == 2


def test_detect_action_verbs():
    resume = "Developed APIs and deployed applications."

    result = detect_action_verbs(resume)

    assert result["count"] == 2
    assert "developed" in result["verbs"]
    assert "deployed" in result["verbs"]


def test_detect_bullet_points():
    resume = """
    • Developed REST APIs
    - Optimized database queries
    * Implemented authentication
    """

    result = detect_bullet_points(resume)

    assert result["count"] == 3
    assert result["present"] is True


def test_resume_length_categories():
    short_resume = "Python " * 100
    good_resume = "Python " * 300
    long_resume = "Python " * 701

    assert analyze_resume_length(short_resume)["category"] == "Short"
    assert analyze_resume_length(good_resume)["category"] == "Good"
    assert analyze_resume_length(long_resume)["category"] == "Long"


def test_resume_quality_score_for_complete_resume():
    report = {
        "sections": {
            "skills": True,
            "projects": True,
            "experience": True,
            "education": True
        },
        "contact_information": {
            "email": True,
            "phone": True,
            "github": True,
            "linkedin": True
        },
        "quantified_achievements": {"count": 5},
        "action_verbs": {"count": 5},
        "bullet_points": {
            "count": 6,
            "present": True
        },
        "resume_length": {"category": "Good"}
    }

    result = compute_resume_quality_score(report)

    assert result["overall_score"] == 100.0
    assert result["grade"] == "A+"

    assert result["score_breakdown"]["structure"]["score"] == 30
    assert result["score_breakdown"]["contact"]["score"] == 15
    assert result["score_breakdown"]["content"]["score"] == 40
    assert result["score_breakdown"]["ats"]["score"] == 15


def test_resume_grade_classification():
    assert get_resume_grade(95)[0] == "A+"
    assert get_resume_grade(85)[0] == "A"
    assert get_resume_grade(75)[0] == "B"
    assert get_resume_grade(65)[0] == "C"
    assert get_resume_grade(40)[0] == "Needs Improvement"


def test_resume_recommendations():
    report = {
        "sections": {
            "skills": False,
            "projects": False,
            "experience": False,
            "education": False
        },
        "contact_information": {
            "email": False,
            "phone": False,
            "github": False,
            "linkedin": False
        },
        "action_verbs": {"count": 1},
        "quantified_achievements": {"count": 0},
        "bullet_points": {"present": False},
        "resume_length": {"category": "Short"}
    }

    recommendations = generate_resume_recommendations(report)

    assert len(recommendations) > 0
    assert len(recommendations) == len(set(recommendations))
