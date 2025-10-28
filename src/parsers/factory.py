import os
from typing import Dict, Any
from .pdf_parser import pdf_to_text
from .docx_parser import docx_to_text
from .ocr_parser import image_to_text
from .utils import extract_emails, extract_phones, first_nonempty_line
import json

def _get_bytes_from_uploaded(file_obj):
    """
    Accept either path str, file-like with .read(), or Streamlit InMemoryUploadedFile with .getvalue()
    """
    if isinstance(file_obj, (str,)):
        with open(file_obj, "rb") as f:
            return f.read()
    # streamlit's UploadedFile has getvalue()
    if hasattr(file_obj, "getvalue"):
        return file_obj.getvalue()
    if hasattr(file_obj, "read"):
        return file_obj.read()
    raise ValueError("Unsupported file object type")

def extract_text_from_file(file_obj, filename: str = None) -> str:
    """
    Determine type by filename extension and return extracted text.
    """
    raw = _get_bytes_from_uploaded(file_obj)
    name = filename or getattr(file_obj, "name", None) or ""
    ext = os.path.splitext(name)[1].lower()
    if ext in [".pdf"]:
        return pdf_to_text(raw, ocr_if_needed=True)
    if ext in [".docx", ".doc"]:
        return docx_to_text(raw)
    if ext in [".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif"]:
        return image_to_text(raw)
    # fallback: try pdf then image
    try:
        return pdf_to_text(raw, ocr_if_needed=True)
    except Exception:
        return image_to_text(raw)

def parse_resume_to_record(file_obj, filename: str = None) -> Dict[str, Any]:
    """
    Return a standardized dict for the resume: name, emails, phones, skills(empty), experiences(empty), raw_text, source_file
    """
    text = extract_text_from_file(file_obj, filename=filename)
    emails = extract_emails(text)
    phones = extract_phones(text)
    name_guess = first_nonempty_line(text)
    record = {
        "source_file": filename or getattr(file_obj, "name", None) or "unknown",
        "raw_text": text,
        "name": name_guess,
        "emails": emails,
        "phones": phones,
        "skills": [],  # placeholder
        "experiences": [],  # placeholder
    }
    return record
