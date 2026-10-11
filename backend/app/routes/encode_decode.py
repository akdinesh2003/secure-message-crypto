from fastapi import APIRouter, HTTPException
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.crypto.encryption import EncryptionService
from app.crypto.signing import SigningService
from app.crypto.key_management import KeyManager
from app.models.schemas import EncodeRequest, DecodeRequest
import base64, json, os

# PoC local keys (separate from payload)
AES_KEY = os.environ.get("AES_KEY")
if AES_KEY is None:
    AES_KEY = base64.b64encode(KeyManager.generate_aes_key()).decode()
AES_KEY_BYTES = base64.b64decode(AES_KEY)

private_key, public_key = KeyManager.generate_ecdsa_keypair()
signing = SigningService(private_key, public_key)
enc_service = EncryptionService(AES_KEY_BYTES)

router = APIRouter()

@router.post("/encode")
def encode(req: EncodeRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty input.")
    enc = enc_service.encrypt(req.message)
    payload = {
        "version": 1,
        "algorithm": "AES-256-GCM",
        "signature_algorithm": "ECDSA-P256",
        "nonce": base64.b64encode(enc["nonce"]).decode(),
        "ciphertext": base64.b64encode(enc["ciphertext"]).decode(),
    }
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    sig = signing.sign(payload_bytes)
    payload["signature"] = base64.b64encode(sig).decode()
    b64_payload = base64.b64encode(json.dumps(payload).encode()).decode()
    return {"payload": b64_payload, "status": "Message encrypted successfully."}

@router.post("/decode")
def decode(req: DecodeRequest):
    try:
        payload_json = base64.b64decode(req.payload).decode("utf-8")
        payload = json.loads(payload_json)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted encrypted message.")

    if payload.get("version") != 1:
        raise HTTPException(status_code=400, detail="Unsupported payload version.")

    sig_b64 = payload.get("signature")
    if not sig_b64:
        raise HTTPException(status_code=400, detail="Invalid payload: missing signature.")

    payload_for_sig = {k: v for k, v in payload.items() if k != "signature"}
    payload_bytes = json.dumps(payload_for_sig, separators=(",", ":")).encode()
    sig = base64.b64decode(sig_b64)

    if not signing.verify(payload_bytes, sig):
        raise HTTPException(status_code=400, detail="Signature verification failed.")

    try:
        nonce = base64.b64decode(payload["nonce"])
        ciphertext = base64.b64decode(payload["ciphertext"])
        msg = enc_service.decrypt(nonce, ciphertext)
    except Exception:
        raise HTTPException(status_code=400, detail="Decryption failed.")

    return {"message": msg, "status": "Message decrypted successfully."}
