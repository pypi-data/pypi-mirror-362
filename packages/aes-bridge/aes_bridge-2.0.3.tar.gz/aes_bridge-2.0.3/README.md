# AesBridge Python
![CI Status](https://github.com/mervick/aes-bridge-python/actions/workflows/python-tests.yml/badge.svg)

**AesBridge** is a modern, secure, and cross-language **AES** encryption library. It offers a unified interface for encrypting and decrypting data across multiple programming languages. Supports **GCM**, **CBC**, and **legacy AES Everywhere** modes.


This is the **Python implementation** of the core project.  
👉 Main repository: https://github.com/mervick/aes-bridge

## Features

- 🔐 AES-256 encryption in GCM (recommended) and CBC modes
- 🌍 Unified cross-language design
- 📦 Compact binary format or base64 output
- 🐍 Pure Python with zero dependencies (except `cryptography`)
- ✅ HMAC Integrity: CBC mode includes HMAC verification
- 🔄 Backward Compatible: Supports legacy AES Everywhere format

## Quick Start

### Installation

```
pip install aes-bridge
```

### Usage
```python
from aes_bridge import encrypt, decrypt

ciphertext = encrypt("My secret message", "MyStrongPass")
plaintext = decrypt(ciphertext, "MyStrongPass")
```

## API Reference

### Main Functions (GCM by default)

- `encrypt(data, passphrase)`  
  Encrypts a string using AES-GCM (default).  
  **Returns:** base64-encoded string.
  
- `decrypt(ciphertext, passphrase)`  
  Decrypts a base64-encoded string encrypted with AES-GCM.

### GCM Mode (recommended)

- `encrypt_gcm(data, passphrase)`  
  Encrypts a string using AES-GCM.
  **Returns:** base64-encoded string.

- `decrypt_gcm(ciphertext, passphrase)`  
  Decrypts a base64-encoded string encrypted with `encrypt_gcm`.

- `encrypt_gcm_bin(data, passphrase)`  
  Returns encrypted binary data using AES-GCM.

- `decrypt_gcm_bin(ciphertext, passphrase)`  
  Decrypts binary data encrypted with `encrypt_gcm_bin`.

### CBC Mode

- `encrypt_cbc(data, passphrase)`  
  Encrypts a string using AES-CBC. 
  HMAC is used for integrity verification.  
  **Returns:** base64-encoded string.  

- `decrypt_cbc(ciphertext, passphrase)`  
  Decrypts a base64-encoded string encrypted with `encrypt_cbc` and verifies HMAC.

- `encrypt_cbc_bin(data, passphrase)`  
  Returns encrypted binary data using AES-CBC with HMAC.

- `decrypt_cbc_bin(ciphertext, passphrase)`  
  Decrypts binary data encrypted with `encrypt_cbc_bin` and verifies HMAC.

### Legacy Compatibility

⚠️ These functions are kept for backward compatibility only.
Their usage is strongly discouraged in new applications.

- `encrypt_legacy(data, passphrase)`  
  Encrypts a string in the legacy AES Everywhere format.  

- `decrypt_legacy(ciphertext, passphrase)`  
  Decrypts a string encrypted in the legacy AES Everywhere format.

