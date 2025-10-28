"""
Unit Tests for Parsers
"""

import pytest
from src.parsers.pdf_parser import PDFParser
from src.parsers.docx_parser import DOCXParser
from src.parsers.txt_parser import TXTParser
from src.parsers.parser_factory import ParserFactory


class TestParsers:
    """Unit tests for parsers"""
    
    def test_pdf_parser_initialization(self):
        """Test PDF parser initialization"""
        parser = PDFParser()
        assert parser is not None
        assert 'pdf' in parser.supported_extensions
    
    def test_docx_parser_initialization(self):
        """Test DOCX parser initialization"""
        parser = DOCXParser()
        assert parser is not None
        assert 'docx' in parser.supported_extensions
    
    def test_txt_parser_initialization(self):
        """Test TXT parser initialization"""
        parser = TXTParser()
        assert parser is not None
        assert 'txt' in parser.supported_extensions
    
    def test_parser_factory(self):
        """Test parser factory"""
        factory = ParserFactory()
        
        pdf_parser = factory.get_parser("test.pdf")
        assert isinstance(pdf_parser, PDFParser)
        
        docx_parser = factory.get_parser("test.docx")
        assert isinstance(docx_parser, DOCXParser)
    
    def test_invalid_file_type(self):
        """Test invalid file type"""
        factory = ParserFactory()
        
        with pytest.raises(ValueError):
            factory.get_parser("test.xyz")