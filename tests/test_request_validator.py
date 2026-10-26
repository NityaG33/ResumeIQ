
import pytest
from fastapi import HTTPException

from validators.request_validator import (
    validate_resume_text_input,
    validate_jd_text,
)


def test_resume_text_too_long():
    with pytest.raises(HTTPException) as exc:
        validate_resume_text_input("a" * 50_001)

    assert exc.value.status_code == 413


def test_jd_text_too_long():
    with pytest.raises(HTTPException) as exc:
        validate_jd_text("a" * 20_001)

    assert exc.value.status_code == 413


def test_resume_text_at_limit_is_allowed():
    validate_resume_text_input("a" * 50_000)


def test_jd_text_at_limit_is_allowed():
    validate_jd_text("a" * 20_000)
