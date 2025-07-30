"""
Time based encoding:
- Encode text with embedded timestamp
- Validate expiry duration during decode
"""

import time
from .base_layer import encode_base64, decode_base64

def encode_with_time(text: str, valid_seconds: int = 3600) -> str:
    """
    Encode text with timestamp, expires after valid_seconds
    """
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    current_time = int(time.time())
    payload = f"{current_time}:{text}"
    encoded = encode_base64(payload)
    return encoded

def decode_with_time(encoded: str, valid_seconds: int = 3600) -> str:
    decoded = decode_base64(encoded)
    try:
        timestamp_str, original_text = decoded.split(':', 1)
        timestamp = int(timestamp_str)
    except Exception:
        raise ValueError("Invalid encoded format")

    current_time = int(time.time())
    if current_time - timestamp > valid_seconds:
        raise ValueError("Encoded text has expired")

    return original_text
