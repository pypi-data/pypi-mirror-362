
# 🔐 ARES-X/Q: Quantum-Safe Encryption Library

**ARES-X/Q** (*Advanced Resilient Encryption Standard – eXtended*) is a modern, quantum-resistant encryption system co-created by **Joaquin Martinez** and **ChatGPT**. It combines post-quantum key exchange (Kyber-style), 512-bit symmetric encryption, and built-in authenticated encryption (AEAD) in a modular, developer-friendly library.

## ✨ Features
- 🛡️ Quantum-safe (simulated Kyber1024)
- 🔒 ARX-based symmetric cipher (ChaCha placeholder)
- ✅ Built-in AEAD with PolyMAC-256
- 📦 Modular: swap out cipher, MAC, or KDF
- 🧪 Easy testing, extensible, Python-first

## 🚀 Install

```bash
git clone https://github.com/fb6si15/aresxq.git
cd aresxq
pip install -r requirements.txt
```

## 🔧 Example

```python
from aresxq import encrypt, decrypt

plaintext = b"Secret message"
aad = b"header-info"

enc_data = encrypt(plaintext, aad)
decrypted = decrypt(enc_data, aad)

assert decrypted == plaintext
```

## 📁 Project Structure

```
aresxq/
├── pqc/        # Post-quantum key exchange (Kyber simulated)
├── kdf/        # HKDF-SHA3-512
├── cipher/     # ARX cipher (ChaCha20 for now)
├── aead/       # XAEAD (Authenticated Encryption)
├── demo/       # Example interface
├── tests/      # Unit tests
```

## 📜 License

MIT © 2025 Joaquin Martinez + ChatGPT
