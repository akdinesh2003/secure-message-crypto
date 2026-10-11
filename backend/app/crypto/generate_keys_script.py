from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
import base64

sk = ec.generate_private_key(ec.SECP256R1())
pk = sk.public_key()

with open("ecdsa_key.pem", "wb") as f:
    f.write(sk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("ecdsa_pub.pem", "wb") as f:
    f.write(pk.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Keys generated: ecdsa_key.pem, ecdsa_pub.pem")
print("DO NOT COMMIT THESE TO GIT.")
