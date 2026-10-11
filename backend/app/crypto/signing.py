from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
import base64

class SigningService:
    def __init__(self, private_key=None, public_key=None):
        if private_key is None:
            private_key = ec.generate_private_key(ec.SECP256R1())
        self.private_key = private_key
        self.public_key = public_key if public_key else private_key.public_key()

    def sign(self, data: bytes) -> bytes:
        return self.private_key.sign(data, ec.ECDSA(hashes.SHA256()))

    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            self.public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False
