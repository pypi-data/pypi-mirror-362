"""
Base encoding/decoding logic:
- Base64 (manual, no libs)
- Base32 (optional, can extend)
- Hex encoding/decoding (native)
"""

BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

def encode_base64(text: str) -> str:
    """
    Encode text into base64 without external libs.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be string")

    binary = ''.join(format(ord(c), '08b') for c in text)
    padding_len = (6 - len(binary) % 6) % 6
    binary += '0' * padding_len

    encoded = ''.join(BASE64_CHARS[int(binary[i:i+6], 2)] for i in range(0, len(binary), 6))
    padding = '=' * (padding_len // 2)
    return encoded + padding


def decode_base64(encoded: str) -> str:
    """
    Decode base64 string back to original text.
    """
    if not isinstance(encoded, str):
        raise TypeError("Input must be string")

    encoded = encoded.rstrip('=')
    binary = ''.join(format(BASE64_CHARS.index(c), '06b') for c in encoded)
    decoded = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return decoded


def encode_hex(text: str) -> str:
    """
    Encode text into hex string.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    return ''.join(format(ord(c), '02x') for c in text)


def decode_hex(hex_str: str) -> str:
    """
    Decode hex string back to text.
    """
    if not isinstance(hex_str, str):
        raise TypeError("Input must be string")
    if len(hex_str) % 2 != 0:
        raise ValueError("Hex string length must be even")
    return ''.join(chr(int(hex_str[i:i+2], 16)) for i in range(0, len(hex_str), 2))
