import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

from .constants import SIZE_RANDOM_NONCE

class CryptoLogic:
    def __init__(self, key: bytes):
        if not isinstance(key, bytes):
            raise ValueError("Key must be bytes")
        self.key = key

    def encrypt(self, data: str) -> str:
        nonce = get_random_bytes(SIZE_RANDOM_NONCE)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
        return base64.b64encode(nonce + ciphertext + tag).decode('utf-8')

    def decrypt(self, data: str) -> str:
        enc_data = base64.b64decode(data)
        nonce, ciphertext, tag = enc_data[:SIZE_RANDOM_NONCE], enc_data[SIZE_RANDOM_NONCE:-16], enc_data[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')

    @staticmethod
    def generate_hash(data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
