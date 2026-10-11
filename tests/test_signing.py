import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.crypto.signing import SigningService
from app.crypto.key_management import KeyManager

def test_sign():
    sk, pk = KeyManager.generate_ecdsa_keypair()
    s = SigningService(sk, pk)
    data = b"payload"
    sig = s.sign(data)
    assert s.verify(data, sig)
    assert not s.verify(b"tampered", sig)
    print("Signing OK")
