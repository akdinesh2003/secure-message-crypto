import os, base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

class KeyManager:
    """Local key setup for PoC. In production, replace with proper key exchange."""

    @staticmethod
    def generate_aes_key() -> bytes:
        return os.urandom(32)

    @staticmethod
    def generate_ecdsa_keypair():
        private_key = ec.generate_private_key(ec.SECP256R1())
        return private_key, private_key.public_key()

    @staticmethod
    def serialize_public_key(public_key) -> str:
        return base64.b64encode(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )).decode("ascii")
