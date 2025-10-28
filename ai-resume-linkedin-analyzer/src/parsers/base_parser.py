"""
Base Parser
Abstract base class for all parsers
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from loguru import logger


class BaseParser(ABC):
    """Abstract base class for resume parsers"""
    
    def __init__(self):
        """Initialize parser"""
        self.supported_extensions: List[str] = []
    
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parse file and extract text
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text content
        """
        pass
    
    def is_supported(self, file_path: str) -> bool:
        """
        Check if file type is supported
        
        Args:
            file_path: Path to file
            
        Returns:
            True if supported
        """
        ext = Path(file_path).suffix.lower().lstrip('.')
        return ext in self.supported_extensions
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate file exists and is readable
        
        Args:
            file_path: Path to file
            
        Returns:
            True if valid
        """
        path = Path(file_path)
        
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        if not path.is_file():
            logger.error(f"Not a file: {file_path}")
            return False
        
        if path.stat().st_size == 0:
            logger.error(f"File is empty: {file_path}")
            return False
        
        return True
    
    def get_file_info(self, file_path: str) -> dict:
        """Get file information"""
        path = Path(file_path)
        return {
            'name': path.name,
            'extension': path.suffix.lstrip('.'),
            'size': path.stat().st_size,
            'size_mb': path.stat().st_size / (1024 * 1024)
        }