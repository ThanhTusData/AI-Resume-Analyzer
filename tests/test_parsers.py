# tests/test_parsers.py
import io
from src.parsers.factory import extract_text_from_file, parse_resume_to_record

def test_factory_imports():
    assert callable(extract_text_from_file)
    assert callable(parse_resume_to_record)

def test_parse_placeholder_text():
    # create a fake text file-like object
    content = b"John Doe\njohn@example.com\n+84 912345678\nExperience: Developer"
    class FakeFile:
        def __init__(self, b):
            self._b = b
            self.name = "test.txt"
        def getvalue(self):
            return self._b
    f = FakeFile(content)
    rec = parse_resume_to_record(f, filename="test.txt")
    assert "raw_text" in rec
    assert "emails" in rec
