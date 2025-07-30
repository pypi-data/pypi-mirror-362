from cryptography.fernet import Fernet
import os

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(APP_ROOT, "secret.key")

def generate_key():
    """Generates a new encryption key and saves it to a file."""
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Loads the encryption key from a file, or generates a new one if it doesn't exist."""
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()

_key = load_key()
_fernet = Fernet(_key)

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    if not data:
        return ""
    encrypted_data = _fernet.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string."""
    if not encrypted_data:
        return ""
    decrypted_data = _fernet.decrypt(encrypted_data.encode())
    return decrypted_data.decode() 