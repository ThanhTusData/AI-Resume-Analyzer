"""
Parser Factory
Selects appropriate parser based on file type
"""

from pathlib import Path
from loguru import logger

from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DOCXParser
from src.parsers.txt_parser import TXTParser
from src.parsers.image_parser import ImageParser


class ParserFactory:
    """Factory for creating appropriate parsers"""
    
    def __init__(self):
        self.parsers = {
            'pdf': PDFParser(),
            'docx': DOCXParser(),
            'doc': DOCXParser(),
            'txt': TXTParser(),
            'png': ImageParser(),
            'jpg': ImageParser(),
            'jpeg': ImageParser(),
            'tiff': ImageParser(),
            'bmp': ImageParser()
        }
    
    def get_parser(self, file_path: str):
        """Get appropriate parser for file"""
        ext = Path(file_path).suffix.lower().lstrip('.')
        
        parser = self.parsers.get(ext)
        
        if parser is None:
            raise ValueError(f"Unsupported file type: {ext}")
        
        logger.info(f"Selected parser for .{ext}")
        return parser
    
    def get_supported_extensions(self):
        """Get list of supported extensions"""
        return list(self.parsers.keys())