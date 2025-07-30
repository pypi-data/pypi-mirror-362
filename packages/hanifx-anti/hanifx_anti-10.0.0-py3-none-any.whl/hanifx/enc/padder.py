"""
Advanced Padding/Unpadding system
"""

def pad_data(data: str, block_size: int = 16) -> str:
    pad_len = block_size - (len(data) % block_size)
    return data + chr(pad_len) * pad_len

def unpad_data(data: str) -> str:
    pad_len = ord(data[-1])
    return data[:-pad_len]
