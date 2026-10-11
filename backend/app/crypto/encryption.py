from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptionService:
    def __init__(self, key: bytes = None):
        if key is None:
            key = AESGCM.generate_key(bit_length=256)
        if len(key) != 32:
            raise ValueError("AES-256 key must be 32 bytes")
        self.key = key
        self.aesgcm = AESGCM(key)

    def encrypt(self, plaintext: str) -> dict:
        nonce = os.urandom(12)
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
        return {"nonce": nonce, "ciphertext": ciphertext}

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> str:
        plaintext = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode("utf-8")
