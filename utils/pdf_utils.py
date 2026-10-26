
import os
import tempfile

from fastapi import HTTPException, UploadFile

from ml.pdf_parser import extract_text_from_pdf

MAX_PDF_SIZE = 5 * 1024 * 1024  # 5 MB
CHUNK_SIZE = 64 * 1024


def extract_resume_text_from_upload(
    resume_file: UploadFile,
) -> str:
    """
    Validate and temporarily store a PDF, extract its text,
    and remove the temporary file even if processing fails.
    """

    if resume_file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported.",
        )

    temp_path = None
    total_size = 0

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".pdf",
            delete=False,
        ) as temp_file:
            temp_path = temp_file.name

            while True:
                chunk = resume_file.file.read(CHUNK_SIZE)

                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_PDF_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="PDF must be 5 MB or smaller.",
                    )

                temp_file.write(chunk)

        # Basic content signature check. This is not a complete
        # security check; pdfplumber must still parse the document.
        with open(temp_path, "rb") as uploaded_pdf:
            if not uploaded_pdf.read(5).startswith(b"%PDF-"):
                raise HTTPException(
                    status_code=400,
                    detail="The uploaded file is not a valid PDF.",
                )

        resume_text = extract_text_from_pdf(temp_path)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Unable to extract text from the uploaded PDF.",
            )

        return resume_text

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        resume_file.file.close()
