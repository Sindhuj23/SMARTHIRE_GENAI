
from pathlib import Path

from pypdf import PdfReader
from docx import Document


def load_pdf(file_bytes):
    """Extract text from PDF resume."""

    temp_path = Path("temp_resume.pdf")
    temp_path.write_bytes(file_bytes)

    reader = PdfReader(str(temp_path))

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    temp_path.unlink(missing_ok=True)

    return text


def load_docx(file_bytes):
    """Extract text from DOCX resume."""

    temp_path = Path("temp_resume.docx")
    temp_path.write_bytes(file_bytes)

    document = Document(str(temp_path))

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    temp_path.unlink(missing_ok=True)

    return text


def load_resume(file_bytes, filename):
    """Load a PDF or DOCX resume and extract its text."""

    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return load_pdf(file_bytes)

    elif extension == ".docx":
        return load_docx(file_bytes)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )
