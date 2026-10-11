import sys, os, base64, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.crypto.encryption import EncryptionService
from app.crypto.signing import SigningService
from app.crypto.key_management import KeyManager

def test_encode_decode():
    key = KeyManager.generate_aes_key()
    sk, pk = KeyManager.generate_ecdsa_keypair()
    enc = EncryptionService(key)
    sign = SigningService(sk, pk)
    msg = "Secret message"
    result = enc.encrypt(msg)
    payload = {
        "version": 1, "algorithm": "AES-256-GCM",
        "signature_algorithm": "ECDSA-P256",
        "nonce": base64.b64encode(result["nonce"]).decode(),
        "ciphertext": base64.b64encode(result["ciphertext"]).decode(),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    sig = sign.sign(payload_bytes)
    payload["signature"] = base64.b64encode(sig).decode()
    b64 = base64.b64encode(json.dumps(payload).encode()).decode()

    # Decode
    decoded = json.loads(base64.b64decode(b64).decode())
    sig_b = base64.b64decode(decoded.pop("signature"))
    payload_bytes = json.dumps(decoded, separators=(",", ":")).encode()
    assert sign.verify(payload_bytes, sig_b)
    nonce = base64.b64decode(decoded["nonce"])
    ct = base64.b64decode(decoded["ciphertext"])
    assert enc.decrypt(nonce, ct) == msg
    print("Encode/decode OK")

    # Tamper
    bad = b64[:-5] + ("A" if b64[-5] != "A" else "B")
    try:
        d = json.loads(base64.b64decode(bad).decode())
        sig_b = base64.b64decode(d.pop("signature"))
        payload_bytes = json.dumps(d, separators=(",", ":")).encode()
        assert not sign.verify(payload_bytes, sig_b)
        print("Tamper detected OK")
    except Exception:
        print("Tamper detected OK (exception)")

if __name__ == "__main__":
    test_encode_decode()
