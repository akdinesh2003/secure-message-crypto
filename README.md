# Secure Message Encoder/Decoder PoC

## Structure
- `backend/app/` — FastAPI + cryptography backend
- `frontend/index.html` — Simple UI
- `tests/` — Unit tests for crypto

## Security design notes
- AES-256-GCM with random 12-byte nonce per message (never reused).
- ECDSA P-256 signatures over payload (not encryption).
- Encryption key, ECDSA private key, and ECDSA public key are kept separate.
- Private keys are never inside the shareable Base64 payload.
- Errors do not reveal key material or internal crypto details.
- `.gitignore` prevents committing secrets.

## Usage
1. Configure a local AES key or let the app generate one (PoC only).
2. Run backend: `cd backend && uvicorn app.main:app --reload`
3. Open `frontend/index.html` in browser (or serve via `python -m http.server`).
4. Encode a message, copy payload, send to another user.
5. Decode on second user’s browser with same backend/config.

## Key management
For this PoC both users must share the same AES key and ECDSA public key via a separate secure channel (not in the payload). The architecture clearly separates:
- Encryption key
- ECDSA private key (signer)
- ECDSA public key (verifier)
- Encrypted payload

Future extension: replace local key setup with proper public-key exchange / identity system.
