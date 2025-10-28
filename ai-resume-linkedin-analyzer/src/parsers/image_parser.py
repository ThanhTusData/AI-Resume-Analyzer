"""
Image Parser
Extracts text from images using OCR
"""

from loguru import logger

from src.parsers.base_parser import BaseParser


class ImageParser(BaseParser):
    """Parser for image files using OCR"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['png', 'jpg', 'jpeg', 'tiff', 'bmp']
    
    def parse(self, file_path: str) -> str:
        """Parse image using OCR"""
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        logger.info(f"Parsing image with OCR: {file_path}")
        
        try:
            import pytesseract
            from PIL import Image
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            
            if not text or len(text.strip()) < 10:
                logger.warning("OCR produced very little text")
            
            logger.info(f"OCR extracted: {len(text)} chars")
            return text
            
        except ImportError:
            logger.error("pytesseract not installed")
            raise RuntimeError("OCR dependencies not available")
        except Exception as e:
            logger.error(f"OCR failed: {str(e)}")
            raise
