import os
import json
from .exceptions import KeyManagementError

SUPPORTED_KEY_SIZES_BITS = [256, 512]

def generate_key_file(path: str, key_size_bits: int):
    if key_size_bits not in SUPPORTED_KEY_SIZES_BITS:
        raise KeyManagementError(f"Unsupported key size. Must be one of {SUPPORTED_KEY_SIZES_BITS}.")
    
    if os.path.exists(path):
        raise KeyManagementError(f"File already exists at '{path}'. Cannot overwrite key file.")
    
    try:
        key_size_bytes = key_size_bits // 8
        key = os.urandom(key_size_bytes)
        
        key_data = {
            "key_size_bits": key_size_bits,
            "key_hex": key.hex()
        }
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(key_data, f, indent=4)
            
    except IOError as e:
        raise KeyManagementError(f"Failed to write key file to '{path}': {e}") from e

def load_key_from_file(path: str) -> bytes:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Key file not found at '{path}'. Please generate it first.")
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            key_data = json.load(f)

        if "key_size_bits" not in key_data or "key_hex" not in key_data:
            raise KeyManagementError("Invalid key file format: missing required fields.")

        key_size_bits = key_data["key_size_bits"]
        if key_size_bits not in SUPPORTED_KEY_SIZES_BITS:
            raise KeyManagementError(f"Key file contains unsupported key size: {key_size_bits}.")

        key = bytes.fromhex(key_data["key_hex"])
        
        expected_bytes = key_size_bits // 8
        if len(key) != expected_bytes:
            raise KeyManagementError(f"Key size mismatch in '{path}'. Expected {expected_bytes} bytes, but found {len(key)}.")
            
        return key
        
    except (IOError, json.JSONDecodeError, ValueError) as e:
        raise KeyManagementError(f"Failed to read or parse key file from '{path}': {e}") from e