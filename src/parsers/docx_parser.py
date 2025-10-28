import io
from docx import Document

def docx_to_text(file_bytes: bytes) -> str:
    """
    Extract text from docx bytes.
    """
    try:
        stream = io.BytesIO(file_bytes)
        doc = Document(stream)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        raise
