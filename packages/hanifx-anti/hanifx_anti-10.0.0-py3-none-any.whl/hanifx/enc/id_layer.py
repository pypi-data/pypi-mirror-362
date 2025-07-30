"""
Device/Hardware locked encoding:
- Encode text tied to device identifier (like MAC or CPU ID)
- Decode only works on same device
"""

import platform
import hashlib
from .chain_layer import encode_pipeline, decode_pipeline

def get_device_id() -> str:
    """
    Simple unique device id based on platform data
    """
    info = platform.node() + platform.system() + platform.machine()
    return hashlib.sha256(info.encode()).hexdigest()

def encode_device_locked(text: str, layers: list[str]) -> str:
    device_id = get_device_id()
    combined = device_id + text
    return encode_pipeline(combined, layers)

def decode_device_locked(encoded: str, layers: list[str]) -> str:
    decoded = decode_pipeline(encoded, layers)
    device_id = get_device_id()
    if not decoded.startswith(device_id):
        raise ValueError("Device mismatch: Cannot decode on this device")
    return decoded[len(device_id):]
