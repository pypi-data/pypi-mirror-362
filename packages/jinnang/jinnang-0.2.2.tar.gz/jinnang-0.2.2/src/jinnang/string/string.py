
import unicodedata
from string import Formatter
from typing import Optional


def get_numeric(value):
    """Convert value to float if possible, else return None."""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None
    

def get_int(value, default=0):
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


def safe_format(template: str, data: dict) -> str:
    """Safely format a string using only the keys present in the template.
    
    Args:
        template (str): String with placeholders (e.g., 'Hello {name}').
        data (dict): Dictionary containing key-value pairs for formatting.
    
    Returns:
        str: Formatted string with only the required keys applied.
        
    Example:
        >>> safe_format('a {haha}', {'haha': 1, 'eheh': 2})
        'a 1'
    """
    required_keys = [fn for _, fn, _, _ in Formatter().parse(template) if fn is not None]
    filtered_data = {k: data[k] for k in required_keys if k in data}
    return template.format(**filtered_data)


def remove_special_chars(text: str) -> str:
    """Remove characters with Unicode categories So, Cn, Co from a string."""
    return ''.join(
        char for char in text 
        if unicodedata.category(char) not in {'So', 'Cn', 'Co'}
    )


def truncate(s: str, max_length: int) -> str:
    """Truncate a string if it exceeds the specified maximum length."""
    return s[:max_length] + '...' if len(s) > max_length else s