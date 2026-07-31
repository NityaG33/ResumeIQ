import os
import shutil

from fastapi import UploadFile, HTTPException

from ml.pdf_parser import extract_text_from_pdf
from validators.request_validator import validate_resume_file


def extract_resume_text_from_upload(
    resume_file: UploadFile,
) -> str:

    validate_resume_file(resume_file)

    os.makedirs(
        "uploads",
        exist_ok=True,
    )

    upload_path = os.path.join(
        "uploads",
        resume_file.filename,
    )

    try:

        with open(
            upload_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                resume_file.file,
                buffer,
            )

        resume_text = extract_text_from_pdf(
            upload_path
        )

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from the uploaded PDF."
            )

        return resume_text

    finally:

        if os.path.exists(upload_path):
            os.remove(upload_path)