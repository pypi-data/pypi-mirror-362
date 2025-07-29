import unicodedata

def is_bad_llm_caption(caption: str) -> bool:
    """
    Check if a caption contains too many question marks (more than 3)
    in either English ('?') or Chinese ('？').
    
    Args:
        caption: The text to check
        
    Returns:
        bool: True if there are more than 3 question marks of either type, False otherwise
    """
    english_questions = caption.count('?')
    chinese_questions = caption.count('？')
    
    return english_questions > 3 or chinese_questions > 3

def is_bad_folder_name(name):
    """
    Check if folder name is invalid according to multiple criteria:
    - Empty/None/whitespace-only
    - Contains forbidden ASCII characters: {}<>:"/\|?*
    - Contains Chinese punctuation: ，。？、
    - Windows reserved names (CON, PRN, AUX, etc.)
    - Starts/ends with whitespace or dot
    - Contains control characters
    - Too long (> 255 chars)
    - Contains emoji or other unusual Unicode
    """
    if not name or not isinstance(name, str):  # None, empty, or not string
        return True
    
    if len(name.strip()) != len(name):
        return True
    
    name = name.strip().lower()
    if not name:  # Whitespace-only
        return True
    
    # Forbidden ASCII characters
    forbidden_ascii = {'{', '}', '<', '>', ':', '"', '/', '\\', '|', '?', '*', '_', '.'}
    
    # Chinese/Japanese punctuation
    forbidden_cjk = {'，', '。', '？', '、', '『', '』', '【', '】'}

    # Forbidden words
    forbidden_words = {'未知', '未提', '图中', 'unknown', 'none', 'null'}
    
    # Windows reserved names (case insensitive)
    windows_reserved = {
        'CON', 'PRN', 'AUX', 'NUL',
        'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
        'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
    }
    
    # Check various conditions
    return any([
        # Structural problems
        len(name) > 50,
        name.startswith(('.', ' ')),
        name.endswith(('.', ' ')),
        any(ord(char) < 32 for char in name),  # Control characters
        
        # Forbidden character sets
        any(char in forbidden_ascii for char in name),
        any(char in forbidden_cjk for char in name),
        any(w in name for w in forbidden_words),
        
        # Reserved names
        name.upper() in windows_reserved,
        name.upper().startswith('~$'),  # Temporary files
        
        # Unusual Unicode categories
        any(
            unicodedata.category(char) in ('So', 'Cn', 'Co')  # Symbols/Other, control, private use
            for char in name
        )
    ])