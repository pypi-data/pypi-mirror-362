"""
Smart Input Handler:
- Detects whether input is a file path or direct text
- Returns the content safely as a string
"""

import os

def smart_input(input_data: str) -> str:
    """
    Detects if the input is a file or plain string. Reads file if exists.
    Args:
        input_data (str): File path or plain string

    Returns:
        str: Contents of file or original string
    """
    if not isinstance(input_data, str):
        raise TypeError("Input must be a string or path.")

    if os.path.isfile(input_data):
        with open(input_data, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return input_data
