import pdfplumber

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts all text from a PDF resume.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a single string.
    """

    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

    return extracted_text
