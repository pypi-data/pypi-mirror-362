import json
import decimal
import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


def derive_key_from_ip(client_ip):
    seed = os.environ.get("ENCRYPTION_SEED")
    if not seed:
        raise ValueError("No ENCRYPTION_SEED environment variable set")
    key_material = f"{seed}:{client_ip}".encode("utf-8")
    derived = hashlib.sha256(key_material).digest()  # 32 bytes
    return derived


def encrypt_data(data, client_ip):
    try:
        key = derive_key_from_ip(client_ip)

        # Convert data to JSON string and pad
        data = json.dumps(data, cls=DecimalEncoder).encode("utf-8")
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()

        # Generate IV and encrypt
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return base64.b64encode(iv + ciphertext).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Encryption failed: {str(e)}")


def decrypt_data(encrypted_data, client_ip):
    try:
        key = derive_key_from_ip(client_ip)

        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

        return decrypted_data
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
