"""
LifeLock Encoding:
- One way irreversible encoding using layered encryption
- Cannot be decoded by any method once applied
"""

import hashlib
from .base_layer import encode_base64

def life_lock_encode(text: str) -> str:
    """
    Irreversible secure encoding.
    Steps:
      - SHA-256 Hash
      - Then Base64 encode (for readable safe form)
    """
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    
    hashed = hashlib.sha256(text.encode()).hexdigest()
    return encode_base64(hashed)
