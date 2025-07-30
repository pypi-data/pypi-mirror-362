# DNC-Crypto: A High-Performance, Next-Generation Cipher

![PyPI Version](https://img.shields.io/pypi/v/dnc-crypto)
![Python Support](https://img.shields.io/pypi/pyversions/dnc-crypto)
![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/pypi/l/dnc-crypto)

Hey everyone! This is **DNC-Crypto**, a project I've been passionately working on to explore a fresh approach to encryption. My goal was to build something from the ground up that was not only unique and incredibly resilient, but also exceptionally fast for large-scale tasks.

This library is the result of that journey—a powerful, multi-layered encryption tool with a clean API and optional **NVIDIA GPU acceleration**.

## Key Features

*   **Blazing-Fast GPU Acceleration:** Encrypt and decrypt large files at incredible speeds by leveraging the parallel processing power of NVIDIA GPUs via CuPy. The library automatically falls back to a highly-optimized NumPy backend if a GPU is not available.
*   **Deeply Layered "Defense-in-Depth":** Your data is processed through an **8-layer cascade**, with each layer using a unique, independently derived key. This exponentially increases the work required for brute-force attacks.
*   **Quantum-Ready Security:** With support for **256-bit** and **512-bit** keys, this library is built for the long term, providing theoretical resistance against future quantum computing threats.
*   **Authenticated & Tamper-Proof:** Every message is sealed in a "secure envelope" with a strong **HMAC-SHA256** signature, guaranteeing both confidentiality and data integrity.
*   **Resilience Through Dynamic Structure:** The core DNC engine is a "moving target." Its internal operations change dynamically in every round, making it theoretically highly resistant to standard cryptanalysis.

## Installation

Install the base library (CPU-only) directly from PyPI:
```bash
pip install dnc-crypto
```

### Optional: GPU Support

To enable GPU acceleration, you need an NVIDIA GPU, the CUDA Toolkit, and CuPy. First, install the CUDA Toolkit that matches your driver, then install the appropriate CuPy version.

For example, if you have CUDA 11.x installed:
```bash
pip install cupy-cuda11x
pip install dnc-crypto  # or upgrade if already installed
```
The library will automatically detect and use your GPU if it's available.

## Quick Start Guide

Here’s how you can protect your data in just a few lines of code, with the option to use your GPU.

```python
from dnc_crypto import DNCCrypto, DecryptionError
import os
import time

# Let's define a name for our key file
KEY_FILE = "my_secret.key"

# 1. Generate and Load Your Key
try:
    crypto = DNCCrypto(key_path=KEY_FILE)
    print("✅ Key loaded successfully!")
except FileNotFoundError:
    print(f"⚠️ Key file not found. Let's create a new 512-bit key...")
    DNCCrypto.generate_key(key_path=KEY_FILE, key_size_bits=512)
    crypto = DNCCrypto(key_path=KEY_FILE)
    print(f"✅ New 512-bit key created and loaded.")

# 2. Encrypt a large chunk of data to see the performance
file_size_mb = 20
print(f"\nEncrypting {file_size_mb}MB of random data...")
plaintext = os.urandom(file_size_mb * 1024 * 1024)

start_time = time.time()
# use_gpu=True is the default. The library will use the GPU if available.
encrypted_data = crypto.encrypt(plaintext, use_gpu=True)
duration = time.time() - start_time

print(f"    Encrypted in: {duration:.4f} seconds")
print(f"    Ciphertext size: {len(encrypted_data) / (1024*1024):.2f} MB")


# 3. Decrypt It Back
print("\nDecrypting the data...")
try:
    start_time = time.time()
    decrypted_text = crypto.decrypt(encrypted_data, use_gpu=True)
    duration = time.time() - start_time
    print(f"    Decrypted in: {duration:.4f} seconds")

    # Verify that everything worked perfectly
    assert plaintext == decrypted_text
    print("\n🎉 Success! The message is back, safe and sound.")

except DecryptionError as e:
    # This will catch errors from a wrong key or tampered data.
    print(f"\n❌ Oops! Decryption failed: {e}")

finally:
    # Just cleaning up the key file for this example
    if os.path.exists(KEY_FILE):
        os.remove(KEY_FILE)
```

## License

This project is shared under the MIT License. Feel free to use it in your own projects!

## Feedback & Collaboration

This project is a labor of love. If you're interested in cryptography, find a bug, or have ideas for improvement, feel free to open an issue on the [GitHub repository](https://github.com/your_username/dnc_crypto).

---

Hope you enjoy using it as much as I enjoyed building it!