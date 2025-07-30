"""
Integrity Checker:
- Generates hash signature to verify tampering or corruption
"""

import hashlib

def generate_checksum(data: str) -> str:
    """
    Return SHA-256 checksum of data
    """
    if not isinstance(data, str):
        raise TypeError("Input must be string")
    return hashlib.sha256(data.encode()).hexdigest()

def verify_checksum(data: str, checksum: str) -> bool:
    return generate_checksum(data) == checksum
