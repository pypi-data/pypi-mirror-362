"""
Key Generator:
- Generates strong yet human-readable keys
"""

import secrets
import string

def generate_key(length: int = 32) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))
