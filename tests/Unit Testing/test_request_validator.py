
import pytest
from io import BytesIO

from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from validators.request_validator import (
    validate_role,
    validate_resume_text_input,
    validate_text_input,
    validate_jd_text,
    validate_resume_file,
)


# Resume text validation

def test_resume_text_too_long():
    with pytest.raises(HTTPException) as exc:
        validate_resume_text_input("a" * 50_001)

    assert exc.value.status_code == 413


def test_resume_text_at_limit_is_allowed():
    validate_resume_text_input("a" * 50_000)


def test_empty_resume_text():
    with pytest.raises(HTTPException) as exc:
        validate_resume_text_input("")

    assert exc.value.status_code == 400


def test_whitespace_resume_text():
    with pytest.raises(HTTPException) as exc:
        validate_resume_text_input("   ")

    assert exc.value.status_code == 400


# Job description validation

def test_jd_text_too_long():
    with pytest.raises(HTTPException) as exc:
        validate_jd_text("a" * 20_001)

    assert exc.value.status_code == 413


def test_jd_text_at_limit_is_allowed():
    validate_jd_text("a" * 20_000)


def test_empty_jd_text():
    with pytest.raises(HTTPException) as exc:
        validate_jd_text("")

    assert exc.value.status_code == 400


def test_whitespace_jd_text():
    with pytest.raises(HTTPException) as exc:
        validate_jd_text("   ")

    assert exc.value.status_code == 400


# Combined text validation

def test_valid_resume_and_jd():
    validate_text_input("Python developer", "FastAPI developer")


# Role validation

def test_valid_role():
    validate_role("backend")


def test_role_is_case_insensitive():
    validate_role("BACKEND")


def test_invalid_role():
    with pytest.raises(HTTPException) as exc:
        validate_role("designer")

    assert exc.value.status_code == 400


# PDF file validation

def test_valid_pdf_file():
    file = UploadFile(
        file=BytesIO(b"%PDF-1.4"),
        filename="resume.pdf",
        headers=Headers({
            "content-type": "application/pdf"
        })
    )

    validate_resume_file(file)


def test_invalid_file_type():
    file = UploadFile(
        file=BytesIO(b"some text"),
        filename="resume.txt",
        headers=Headers({
            "content-type": "text/plain"
        })
    )

    with pytest.raises(HTTPException) as exc:
        validate_resume_file(file)

    assert exc.value.status_code == 400
