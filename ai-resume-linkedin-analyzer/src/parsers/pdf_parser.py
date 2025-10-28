"""
PDF Parser
Extracts text from PDF files
"""

from pathlib import Path
import PyPDF2
import pdfplumber
from loguru import logger

from src.parsers.base_parser import BaseParser


class PDFParser(BaseParser):
    """Parser for PDF resume files"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['pdf']
    
    def parse(self, file_path: str) -> str:
        """Parse PDF file"""
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        logger.info(f"Parsing PDF: {file_path}")
        
        # Try pdfplumber first
        try:
            text = self._parse_with_pdfplumber(file_path)
            if text and len(text.strip()) > 50:
                logger.info(f"Parsed with pdfplumber: {len(text)} chars")
                return text
        except Exception as e:
            logger.warning(f"pdfplumber failed: {str(e)}")
        
        # Fallback to PyPDF2
        try:
            text = self._parse_with_pypdf2(file_path)
            if text:
                logger.info(f"Parsed with PyPDF2: {len(text)} chars")
                return text
        except Exception as e:
            logger.error(f"PyPDF2 failed: {str(e)}")
        
        raise RuntimeError("Failed to parse PDF")
    
    def _parse_with_pdfplumber(self, file_path: str) -> str:
        """Parse using pdfplumber"""
        text_parts = []
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return "\n\n".join(text_parts)
    
    def _parse_with_pypdf2(self, file_path: str) -> str:
        """Parse using PyPDF2"""
        text_parts = []
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return "\n\n".join(text_parts)
