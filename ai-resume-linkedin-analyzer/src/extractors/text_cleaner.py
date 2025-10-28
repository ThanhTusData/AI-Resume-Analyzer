"""
Text Cleaner
Cleans and normalizes extracted text
"""

import re
from typing import Optional


class TextCleaner:
    """Clean and normalize extracted text"""
    
    def clean(self, text: str) -> str:
        """Clean text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\-.,;:()\[\]/@#&]', '', text)
        
        # Fix OCR errors
        text = self._fix_ocr_errors(text)
        
        # Normalize line breaks
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove multiple newlines
        text = re.sub(r'\n\n+', '\n\n', text)
        
        return text.strip()
    
    def _fix_ocr_errors(self, text: str) -> str:
        """Fix common OCR errors"""
        replacements = {
            r'\b0\b': 'O',
            r'\|': 'I',
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text)
        
        return text