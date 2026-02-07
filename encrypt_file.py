import os
import json
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


PBKDF2_ITERATIONS = 200_000
KEY_LENGTH = 32  # AES-256


def encrypt_file(input_path, output_path, password: str):
    # Read arbitrary file as raw bytes
    with open(input_path, "rb") as f:
        plaintext = f.read()

    salt = os.urandom(16)
    iv = os.urandom(12)  # AES-GCM standard nonce size

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    key = kdf.derive(password.encode("utf-8"))

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    envelope = {
        "kdf": "PBKDF2",
        "hash": "SHA-256",
        "iterations": PBKDF2_ITERATIONS,
        "salt": base64.b64encode(salt).decode("ascii"),
        "iv": base64.b64encode(iv).decode("ascii"),
        "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(envelope, f, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        print("Usage: python encrypt_file.py <input_file> <output.json> <password>")
        sys.exit(1)

    encrypt_file(sys.argv[1], sys.argv[2], sys.argv[3])
