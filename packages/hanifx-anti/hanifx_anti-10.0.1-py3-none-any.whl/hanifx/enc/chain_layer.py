"""
Multi-layer encoding and decoding pipeline,
যেখানে layers দেওয়া হয় list আকারে,
সেটা ক্রমান্বয়ে encode ও reverse ক্রমান্বয়ে decode হয়।
"""

from .base_layer import encode_base64, decode_base64
from .logic_layer import xor_encode, xor_decode, caesar_encrypt, caesar_decrypt, rot13

ENCODE_FUNCTIONS = {
    "base64": encode_base64,
    "xor": xor_encode,
    "caesar": caesar_encrypt,
    "rot13": rot13,
}

DECODE_FUNCTIONS = {
    "base64": decode_base64,
    "xor": xor_decode,
    "caesar": caesar_decrypt,
    "rot13": rot13,
}

def encode_pipeline(text: str, layers: list[str]) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    for layer in layers:
        func = ENCODE_FUNCTIONS.get(layer)
        if func is None:
            raise ValueError(f"Unknown encode layer: {layer}")
        text = func(text)
    return text

def decode_pipeline(text: str, layers: list[str]) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be string")
    for layer in reversed(layers):
        func = DECODE_FUNCTIONS.get(layer)
        if func is None:
            raise ValueError(f"Unknown decode layer: {layer}")
        text = func(text)
    return text
