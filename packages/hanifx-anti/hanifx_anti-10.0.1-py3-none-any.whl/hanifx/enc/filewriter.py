"""
File Writer:
- Write encoded text to SD card or desired output path
"""

import os

def write_to_file(encoded_text: str, filename: str = "hanifx_enc.py") -> str:
    """
    Writes encoded text to file (defaults to hanifx_enc.py)

    Returns saved path
    """
    path = os.path.join(os.getcwd(), filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(encoded_text)
    return path
