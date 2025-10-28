import io
from PIL import Image
import pytesseract

def image_to_text(file_bytes: bytes) -> str:
    img = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(img)
