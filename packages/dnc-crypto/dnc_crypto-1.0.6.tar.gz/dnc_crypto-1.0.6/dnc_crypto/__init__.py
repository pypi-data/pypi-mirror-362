import os
import json
import struct
import hmac
import importlib

# از cryptography فقط برای یک تابع استفاده می‌شود، پس import آن را به داخل تابع منتقل می‌کنیم
# تا زمان بارگذاری اولیه کتابخانه سریع‌تر شود.
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.backends import default_backend

from .core import ChainedEncryptor
from .key_manager import generate_key_file, load_key_from_file
from .exceptions import DNCCryptoError, DecryptionError, KeyManagementError

# --- تشخیص خودکار GPU و انتخاب Backend ---
CUPY_AVAILABLE = False
try:
    cupy_spec = importlib.util.find_spec("cupy")
    if cupy_spec is not None:
        cupy = importlib.util.module_from_spec(cupy_spec)
        cupy_spec.loader.exec_module(cupy)
        if cupy.is_available():
            CUPY_AVAILABLE = True
        else:
            print("Warning: CuPy is installed but no compatible NVIDIA GPU was found. Falling back to CPU mode.")
except ImportError:
    pass

# برای جلوگیری از import کردن numpy اگر از cupy استفاده می‌شود، از import شرطی استفاده می‌کنیم
if CUPY_AVAILABLE:
    import cupy as active_backend
else:
    import numpy as active_backend

__version__ = "1.0.6"
__author__ = "Mohammadmoein Pisoude"

class DNCCrypto:
    MAGIC_BYTES = b'DNCE'
    CURRENT_VERSION_TUPLE = (2, 1, 0) # نسخه پروتکل را هم می‌توان افزایش داد
    HEADER_FORMAT = "!4sH H" 
    HMAC_KEY_SALT = b"dnc-hmac-integrity-key-salt-v2"

    def __init__(self, key_path: str, num_chains: int = 8):
        self._key = load_key_from_file(key_path)
        self.num_chains = num_chains
        self._hmac_key = self._derive_hmac_key()
        
        # این backend پیش‌فرض است، اما در هر فراخوانی قابل تغییر است
        self._default_backend = active_backend
        
        # نمایش وضعیت اولیه
        print(f"DNC-Crypto Initialized. GPU Available: {CUPY_AVAILABLE}. Default backend: {self._default_backend.__name__}")

    @staticmethod
    def generate_key(key_path: str, key_size_bits: int = 256):
        generate_key_file(key_path, key_size_bits)

    def _derive_hmac_key(self):
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.backends import default_backend
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend()); 
        digest.update(self._key + self.HMAC_KEY_SALT)
        return digest.finalize()

    def _create_header(self) -> bytes:
        header_data = {
            "key_size_bits": len(self._key) * 8,
            "num_chains": self.num_chains,
            "cipher_engine": "DNC-v2-GPU"
        }
        return json.dumps(header_data, separators=(',', ':')).encode('utf-8')

    def encrypt(self, plaintext: bytes, use_gpu: bool = True) -> bytes:
        if not isinstance(plaintext, bytes): raise TypeError("Plaintext must be of type bytes.")
        
        # انتخاب backend برای این عملیات خاص
        backend_to_use = self._default_backend if use_gpu and CUPY_AVAILABLE else __import__('numpy')
        
        engine = ChainedEncryptor(self._key, backend=backend_to_use, num_chains=self.num_chains)
        ciphertext = engine.encrypt(plaintext)
        
        header_json_bytes = self._create_header()
        version_packed = (self.CURRENT_VERSION_TUPLE[0] << 8) | self.CURRENT_VERSION_TUPLE[1]
        packet_prefix = struct.pack(self.HEADER_FORMAT, self.MAGIC_BYTES, version_packed, len(header_json_bytes))
        header_hmac = hmac.new(self._hmac_key, packet_prefix + header_json_bytes, 'sha256').digest()
        return packet_prefix + header_json_bytes + header_hmac + ciphertext

    def decrypt(self, data: bytes, use_gpu: bool = True) -> bytes:
        if not isinstance(data, bytes): raise TypeError("Data to decrypt must be of type bytes.")
        
        try:
            prefix_len = struct.calcsize(self.HEADER_FORMAT)
            if len(data) < prefix_len: raise DecryptionError("Data is too short to be a valid payload.")
            magic, version_packed, header_len = struct.unpack(self.HEADER_FORMAT, data[:prefix_len])
            
            if magic != self.MAGIC_BYTES: raise DecryptionError("Invalid data format or not a DNCCrypto file.")
            
            header_end = prefix_len + header_len
            hmac_end = header_end + 32
            if len(data) < hmac_end: raise DecryptionError("Data is truncated or corrupt (header section).")
            
            header_json_bytes = data[prefix_len:header_end]
            received_hmac = data[header_end:hmac_end]
            
            expected_hmac = hmac.new(self._hmac_key, data[:header_end], 'sha256').digest()
            if not hmac.compare_digest(received_hmac, expected_hmac): raise DecryptionError("Header integrity check failed! Data may have been tampered with.")
            
            header_data = json.loads(header_json_bytes)
            if header_data.get("key_size_bits") != len(self._key) * 8: raise DecryptionError("Key size mismatch.")

            ciphertext = data[hmac_end:]
            
            backend_to_use = self._default_backend if use_gpu and CUPY_AVAILABLE else __import__('numpy')
            engine = ChainedEncryptor(self._key, backend=backend_to_use, num_chains=self.num_chains)
            
            return engine.decrypt(ciphertext)
            
        except (struct.error, json.JSONDecodeError, ValueError, IndexError) as e:
            raise DecryptionError("Decryption failed due to corrupted data or incorrect format.") from e