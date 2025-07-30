"""
Logic based encoding:
- XOR encode/decode
- Caesar cipher (encrypt/decrypt)
- ROT13 (special case of Caesar)
"""

def xor_encode(text: str, key: int = 7) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    return ''.join(chr((ord(c) ^ key) % 256) for c in text)

def xor_decode(encoded: str, key: int = 7) -> str:
    if not isinstance(encoded, str):
        raise TypeError("Input must be string")
    return ''.join(chr((ord(c) ^ key) % 256) for c in encoded)

def caesar_encrypt(text: str, shift: int = 3) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be string")

    result = []
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            result.append(chr((ord(c) - base + shift) % 26 + base))
        else:
            result.append(c)
    return ''.join(result)

def caesar_decrypt(text: str, shift: int = 3) -> str:
    return caesar_encrypt(text, -shift)

def rot13(text: str) -> str:
    return caesar_encrypt(text, 13)
