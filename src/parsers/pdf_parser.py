import io
from typing import Optional
import pdfplumber
from PIL import Image
import pytesseract

def pdf_to_text(file_bytes: bytes, ocr_if_needed: bool = True) -> str:
    """
    Try to extract text from PDF using pdfplumber.
    If extracted text is too short and ocr_if_needed=True, run OCR on pages.
    """
    text_parts = []
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                try:
                    ptext = page.extract_text() or ""
                except Exception:
                    ptext = ""
                text_parts.append(ptext)
            full_text = "\n".join(text_parts).strip()
            if len(full_text) > 80:
                return full_text
            # fallback OCR: convert each page to image then pytesseract
            if ocr_if_needed:
                ocr_texts = []
                for page in pdf.pages:
                    try:
                        pil_img = page.to_image(resolution=150).original
                        ocr = pytesseract.image_to_string(pil_img)
                        ocr_texts.append(ocr)
                    except Exception:
                        continue
                ocr_full = "\n".join(ocr_texts).strip()
                # if OCR yields more than original, use it
                return ocr_full if len(ocr_full) > len(full_text) else full_text
            return full_text
    except Exception as e:
        # last resort: try pytesseract on whole file (not ideal)
        try:
            img = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(img)
        except Exception:
            raise e
