
import pytest

from ml.tfidf.similarity import text_similarity


def test_identical_text_similarity():
    text = "Python developer with FastAPI and MongoDB experience"

    score = text_similarity(text, text)

    assert score == pytest.approx(1.0)


def test_similar_text_similarity():
    resume = "Python developer with FastAPI and MongoDB experience"
    jd = "Python developer with FastAPI experience"

    score = text_similarity(resume, jd)

    assert 0 < score < 1


def test_no_common_words_similarity():
    resume = "Python developer builds software applications"
    jd = "Chef prepares delicious food recipes"

    score = text_similarity(resume, jd)

    assert score == pytest.approx(0.0)


def test_similarity_score_is_within_range():
    resume = "React frontend developer with JavaScript"
    jd = "JavaScript developer with React experience"

    score = text_similarity(resume, jd)

    assert 0.0 <= score <= 1.0


def test_skill_alias_normalization():
    resume = "ReactJS developer"
    jd = "React developer"

    score = text_similarity(resume, jd)

    assert score == pytest.approx(1.0)
