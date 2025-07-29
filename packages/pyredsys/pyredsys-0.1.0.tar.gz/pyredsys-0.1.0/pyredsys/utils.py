import base64
import hashlib
import hmac

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_diversified_key(secret_key: str, order_number: str):
    # Read Step 1
    # tldr; diversifying the secret key with the order number
    # https://pagosonline.redsys.es/desarrolladores-inicio/documentacion-operativa/firmar-una-operacion/

    # Step 1: Trim or pad key to 16 characters
    key_16 = secret_key[:16].ljust(16, "0")  # force exactly 16 chars
    key_bytes = key_16.encode()

    # Step 2: Pad the order number (PKCS7 padding to 128-bit block size)
    padder = padding.PKCS7(128).padder()
    padded_order = padder.update(order_number.encode()) + padder.finalize()

    # Step 3: AES CBC with zero IV
    iv = b"\x00" * 16
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_order) + encryptor.finalize()

    # Step 4: Base64 encode the result
    encrypted_b64 = base64.urlsafe_b64encode(encrypted)
    return encrypted_b64


def sign_hmac_sha512(key: bytes, data: bytes):
    signature = hmac.new(key, data, hashlib.sha512).digest()
    return base64.urlsafe_b64encode(signature)
