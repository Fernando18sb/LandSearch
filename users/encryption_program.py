import json

from cryptography.fernet import Fernet
from decouple import config

FERNET_KEY = config('ENCRYPTION_KEY')
fernet = Fernet(FERNET_KEY)

def encryption(data: dict) -> str:
    # Convert dict to JSON string
    json_str = json.dumps(data)
    # Encode to bytes and encrypt
    encrypted = fernet.encrypt(json_str.encode())
    return encrypted.decode()

def decryption(encrypted_data: str) -> dict:
    # Decode and decrypt
    decrypted_bytes = fernet.decrypt(encrypted_data.encode())
    # Convert back to dict
    return json.loads(decrypted_bytes.decode())