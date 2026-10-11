import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.crypto.encryption import EncryptionService
from app.crypto.signing import SigningService
from app.crypto.key_management import KeyManager

def test_roundtrip():
    enc = EncryptionService(KeyManager.generate_aes_key())
    msg = "Hello secret"
    result = enc.encrypt(msg)
    decoded = enc.decrypt(result["nonce"], result["ciphertext"])
    assert decoded == msg
    print("Encryption roundtrip OK")

def test_sign_verify():
    sk, pk = KeyManager.generate_ecdsa_keypair()
    s = SigningService(sk, pk)
    sig = s.sign(b"test")
    assert s.verify(b"test", sig)
    assert not s.verify(b"bad", sig)
    print("ECDSA sign/verify OK")

if __name__ == "__main__":
    test_roundtrip()
    test_sign_verify()
