"""
TXT Parser
Reads plain text files
"""

from loguru import logger

from src.parsers.base_parser import BaseParser


class TXTParser(BaseParser):
    """Parser for plain text files"""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['txt']
    
    def parse(self, file_path: str) -> str:
        """Parse TXT file"""
        if not self.validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path}")
        
        logger.info(f"Parsing TXT: {file_path}")
        
        encodings = ['utf-8', 'latin-1', 'cp1252', 'ascii']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
                    logger.info(f"Parsed TXT with {encoding}: {len(text)} chars")
                    return text
            except UnicodeDecodeError:
                continue
        
        # Last resort
        with open(file_path, 'rb') as file:
            text = file.read().decode('utf-8', errors='ignore')
            logger.warning(f"Parsed TXT with error handling: {len(text)} chars")
            return text