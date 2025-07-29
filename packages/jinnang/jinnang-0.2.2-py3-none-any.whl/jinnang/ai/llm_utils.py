import math
from typing import Union, Dict, List
import logging
import re
logger = logging.getLogger(__name__)

def calculate_tokens(width: int, height: int) -> float:
    """Calculate tokens as (h * w) / 784"""
    return math.ceil((width * height) / 784)


def is_bad_llm_caption(caption: Union[str, Dict]) -> bool:
    """
    Check if input is a dict (return True) or contains too many question marks (>3)
    in either English ('?') or Chinese ('？').
    
    Args:
        caption: Input to check (str or dict)
        
    Returns:
        bool: True if dict or excessive question marks, False otherwise
    """
    if isinstance(caption, dict):
        return False
        
    english_questions = caption.count('?')
    chinese_questions = caption.count('？')
    
    return english_questions > 3 or chinese_questions > 3

def extract_fields(response_text: Union[str, Dict], fields: List[str]) -> Dict[str, str]:
    """
    Extracts specified fields from a formatted LLM API response.
    Special handling for multiline 'reasoning' field in either:
    - <think>reasoning content</think> (can span multiple lines)
    - reasoning: <reasoning content>
    
    Args:
        response_text: The raw text response from the LLM API
        fields: List of fields to extract (e.g., ['title', 'reasoning'])
    
    Returns:
        A dictionary with the requested fields and their values
    """

    if isinstance(response_text, dict):
        return response_text

    result = {}
    reasoning_parts = []
    need_reasoning = any(f.lower() == 'reasoning' for f in fields)
    
    # First extract all <think> blocks (including multiline)
    if need_reasoning:
        think_blocks = re.findall(r'<think>(.*?)</think>', response_text, re.DOTALL)
        reasoning_parts.extend([block.strip() for block in think_blocks])
    
    # Then process line by line for other fields
    lines = response_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle regular field: value format
        if ':' in line:
            parts = line.split(':', 1)
            field = parts[0].strip().lower()
            content = parts[1].strip()
            
            if field == 'reasoning' and need_reasoning:
                reasoning_parts.append(content)
            elif any(f.lower() == field for f in fields):
                result[field] = content
    
    # Combine all reasoning parts if they exist
    if need_reasoning and reasoning_parts:
        result['reasoning'] = '\n'.join(filter(None, reasoning_parts))
        
    logger.error(f'{response_text}')
    logger.error(f'{reasoning_parts}')
    logger.error(f'{result}')

    return result