"""
Input Validators
Validation functions for user inputs
"""

import re
from typing import Tuple, List
from pathlib import Path


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not email:
        return False, "Email is required"
    
    # Basic email pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    # Check length
    if len(email) > 254:
        return False, "Email too long"
    
    return True, "Valid email"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not phone:
        return False, "Phone number is required"
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\+]+', '', phone)
    
    # Check if all digits
    if not cleaned.isdigit():
        return False, "Phone number should contain only digits"
    
    # Check length (international format: 10-15 digits)
    if len(cleaned) < 10 or len(cleaned) > 15:
        return False, "Phone number should be 10-15 digits"
    
    return True, "Valid phone number"


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Validate URL format
    
    Args:
        url: URL to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not url:
        return False, "URL is required"
    
    # URL pattern
    pattern = r'^https?://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(/.*)?$'
    
    if not re.match(pattern, url):
        return False, "Invalid URL format. Must start with http:// or https://"
    
    # Check length
    if len(url) > 2048:
        return False, "URL too long"
    
    return True, "Valid URL"


def validate_file_size(file, max_size_mb: int = 10) -> Tuple[bool, str]:
    """
    Validate uploaded file size
    
    Args:
        file: Uploaded file object
        max_size_mb: Maximum size in megabytes
        
    Returns:
        Tuple of (is_valid, message)
    """
    if file is None:
        return False, "No file provided"
    
    # Get file size in MB
    size_mb = file.size / (1024 * 1024)
    
    if size_mb > max_size_mb:
        return False, f"File too large: {size_mb:.2f}MB (max: {max_size_mb}MB)"
    
    return True, f"File size OK: {size_mb:.2f}MB"


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
    """
    Validate file extension
    
    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not filename:
        return False, "No filename provided"
    
    # Get extension
    ext = Path(filename).suffix.lower().lstrip('.')
    
    if not ext:
        return False, "File has no extension"
    
    if ext not in [e.lower() for e in allowed_extensions]:
        return False, f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
    
    return True, f"Valid file type: {ext}"


def validate_text_length(text: str, min_length: int = 0, max_length: int = 10000) -> Tuple[bool, str]:
    """
    Validate text length
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not text:
        return False, "Text is empty"
    
    length = len(text)
    
    if length < min_length:
        return False, f"Text too short: {length} characters (min: {min_length})"
    
    if length > max_length:
        return False, f"Text too long: {length} characters (max: {max_length})"
    
    return True, f"Text length OK: {length} characters"


def validate_score(score: float) -> Tuple[bool, str]:
    """
    Validate score value
    
    Args:
        score: Score to validate
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        score = float(score)
    except (ValueError, TypeError):
        return False, "Score must be a number"
    
    if score < 0 or score > 100:
        return False, "Score must be between 0 and 100"
    
    return True, "Valid score"


def validate_api_key(api_key: str, provider: str = "openai") -> Tuple[bool, str]:
    """
    Validate API key format
    
    Args:
        api_key: API key to validate
        provider: API provider (openai, google, anthropic)
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not api_key:
        return False, "API key is required"
    
    # Check format based on provider
    if provider == "openai":
        if not api_key.startswith("sk-"):
            return False, "OpenAI API key should start with 'sk-'"
        if len(api_key) < 20:
            return False, "OpenAI API key too short"
    
    elif provider == "google":
        if len(api_key) < 20:
            return False, "Google API key too short"
    
    return True, "API key format valid"
