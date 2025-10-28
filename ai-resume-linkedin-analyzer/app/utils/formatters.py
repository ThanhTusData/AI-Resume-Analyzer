"""
Output Formatters
Functions for formatting output data
"""

from datetime import datetime, timedelta
from typing import Optional, Union


def format_date(
    date_obj: Optional[Union[datetime, str]],
    format_str: str = "%B %d, %Y"
) -> str:
    """
    Format datetime object to string
    
    Args:
        date_obj: Datetime object or string
        format_str: Strftime format string
        
    Returns:
        Formatted date string
    """
    if date_obj is None:
        return "N/A"
    
    try:
        if isinstance(date_obj, str):
            # Try to parse string to datetime
            date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
        
        return date_obj.strftime(format_str)
    except Exception:
        return str(date_obj)


def format_number(number: Union[int, float], decimals: int = 0, use_comma: bool = True) -> str:
    """
    Format number with optional decimals and comma separators
    
    Args:
        number: Number to format
        decimals: Number of decimal places
        use_comma: Use comma as thousands separator
        
    Returns:
        Formatted number string
    """
    try:
        if decimals == 0:
            formatted = f"{int(number)}"
        else:
            formatted = f"{float(number):.{decimals}f}"
        
        if use_comma:
            parts = formatted.split('.')
            parts[0] = f"{int(parts[0]):,}"
            formatted = '.'.join(parts)
        
        return formatted
    except Exception:
        return str(number)


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format value as percentage
    
    Args:
        value: Value to format
        decimals: Number of decimal places
        
    Returns:
        Formatted percentage string
    """
    try:
        return f"{float(value):.{decimals}f}%"
    except Exception:
        return f"{value}%"


def format_currency(
    amount: float,
    currency: str = "USD",
    decimals: int = 0,
    show_symbol: bool = True
) -> str:
    """
    Format amount as currency
    
    Args:
        amount: Amount to format
        currency: Currency code
        decimals: Number of decimal places
        show_symbol: Show currency symbol
        
    Returns:
        Formatted currency string
    """
    try:
        symbols = {
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
            'VND': '₫'
        }
        
        symbol = symbols.get(currency, '$') if show_symbol else ''
        formatted_amount = format_number(amount, decimals, use_comma=True)
        
        if currency == 'VND':
            return f"{formatted_amount}{symbol}"
        else:
            return f"{symbol}{formatted_amount}"
    except Exception:
        return str(amount)


def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "...",
    word_boundary: bool = True
) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add when truncated
        word_boundary: Break at word boundary
        
    Returns:
        Truncated text
    """
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    if word_boundary:
        # Find last space before max_length
        truncated = text[:max_length - len(suffix)]
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
        return truncated + suffix
    else:
        return text[:max_length - len(suffix)] + suffix


def format_duration(start_date: datetime, end_date: Optional[datetime] = None) -> str:
    """
    Format duration between two dates
    
    Args:
        start_date: Start date
        end_date: End date (None for current)
        
    Returns:
        Formatted duration string
    """
    if end_date is None:
        end_date = datetime.now()
    
    delta = end_date - start_date
    
    years = delta.days // 365
    months = (delta.days % 365) // 30
    
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months > 0:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    
    if not parts:
        return "Less than a month"
    
    return " ".join(parts)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} PB"


def format_time_ago(date_obj: datetime) -> str:
    """
    Format time as 'X time ago'
    
    Args:
        date_obj: Datetime object
        
    Returns:
        Formatted time ago string
    """
    now = datetime.now()
    delta = now - date_obj
    
    seconds = delta.total_seconds()
    
    if seconds < 60:
        return "Just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"
    else:
        return format_date(date_obj, "%b %d, %Y")


def format_list(items: list, max_items: int = 5, separator: str = ", ") -> str:
    """
    Format list of items with truncation
    
    Args:
        items: List of items
        max_items: Maximum items to show
        separator: Separator between items
        
    Returns:
        Formatted list string
    """
    if not items:
        return "None"
    
    if len(items) <= max_items:
        return separator.join(str(item) for item in items)
    else:
        shown = separator.join(str(item) for item in items[:max_items])
        remaining = len(items) - max_items
        return f"{shown}{separator}+{remaining} more"