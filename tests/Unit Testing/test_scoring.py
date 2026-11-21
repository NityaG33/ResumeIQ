
import pytest

from ml import scoring
from ml.utilities.config import (
    EMBEDDING_CALIBRATION_MIN,
    EMBEDDING_CALIBRATION_MAX,
    TFIDF_CALIBRATION_MIN,
    TFIDF_CALIBRATION_MAX,
)


# Normalization tests

def test_normalize_score_midpoint():
    score = scoring.normalize_score(
        0.5,
        0.0,
        1.0
    )

    assert score == pytest.approx(0.5)


def test_normalize_score_below_minimum():
    score = scoring.normalize_score(
        0.1,
        0.2,
        0.8
    )

    assert score == 0.0


def test_normalize_score_above_maximum():
    score = scoring.normalize_score(
        0.9,
        0.2,
        0.8
    )

    assert score == 1.0


# Confidence classification tests

def test_strong_match_confidence():
    result = scoring.classify_match_confidence(
        final_score=85,
        coverage_score=0.80,
        embedding_score=0.80
    )

    assert result == "Strong Match"


def test_moderate_match_confidence():
    result = scoring.classify_match_confidence(
        final_score=65,
        coverage_score=0.50,
        embedding_score=0.50
    )

    assert result == "Moderate Match"


def test_weak_match_confidence():
    result = scoring.classify_match_confidence(
        final_score=45,
        coverage_score=0.40,
        embedding_score=0.40
    )

    assert result == "Weak Match"


def test_strong_match_requires_component_thresholds():
    result = scoring.classify_match_confidence(
        final_score=85,
        coverage_score=0.60,
        embedding_score=0.90
    )

    assert result == "Moderate Match"


# Final weighted score test

def test_final_weighted_match_score(monkeypatch):

    monkeypatch.setattr(
        scoring,
        "compute_skill_coverage",
        lambda resume, jd: {
            "coverage": 0.8,
            "matched": ["python"],
            "missing": ["aws"],
            "extra": [],
            "resume_skills": ["python"],
            "jd_skills": ["python", "aws"]
        }
    )

    monkeypatch.setattr(
        scoring,
        "embedding_similarity",
        lambda resume, jd: (
            EMBEDDING_CALIBRATION_MIN
            + 0.5 * (
                EMBEDDING_CALIBRATION_MAX
                - EMBEDDING_CALIBRATION_MIN
            )
        )
    )

    monkeypatch.setattr(
        scoring,
        "text_similarity",
        lambda resume, jd: (
            TFIDF_CALIBRATION_MIN
            + 0.5 * (
                TFIDF_CALIBRATION_MAX
                - TFIDF_CALIBRATION_MIN
            )
        )
    )

    monkeypatch.setattr(
        scoring,
        "compute_role_alignment",
        lambda resume, role: {
            "alignment_score": 0.6,
            "role": "Backend Developer",
            "matched_role_skills": ["python"],
            "additional_technologies": ["aws"]
        }
    )

    monkeypatch.setattr(
        scoring,
        "build_resume_report",
        lambda resume: {
            "quality_score": 80
        }
    )

    result = scoring.compute_match_score(
        "Python developer",
        "Python AWS developer",
        "backend"
    )

    # (0.8 * 0.5) + (0.5 * 0.3)
    # + (0.5 * 0.1) + (0.6 * 0.1)
    # = 0.66 = 66%

    assert result["final_score"] == 66.0
    assert result["confidence"] == "Moderate Match"

    assert result["component_scores"] == {
        "skill_coverage": 80.0,
        "embedding_similarity": 50.0,
        "tfidf_similarity": 50.0,
        "role_alignment": 60.0
    }
