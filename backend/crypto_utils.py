import os
import time
from Crypto.Cipher import AES, DES, ARC4
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
import hashlib

def derive_key(password: str, salt: bytes, cipher_name: str) -> bytes:
    cipher_name = cipher_name.upper()
    key_len = 8 if cipher_name == 'DES' else 16
    
    # Standar PBKDF2 bawaan Python (SHA256)
    return hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8') if isinstance(password, str) else password,
        salt,
        100000,
        dklen=key_len
    )

def get_report_key(salt: bytes, cipher_name: str) -> bytes:
    master = os.environ.get("WBS_MASTER_KEY")
    if not master:
        raise RuntimeError("Environment variable WBS_MASTER_KEY belum di-set.")
    return derive_key(master, salt, cipher_name)


def encrypt_data(data_bytes: bytes, cipher_name: str, key: bytes) -> tuple[bytes, float]:
    cipher_name = cipher_name.upper()
    start_time = time.perf_counter()
    
    if cipher_name == 'AES':
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data_bytes, AES.block_size))
        final_payload = iv + ciphertext
        
    elif cipher_name == 'DES':
        iv = os.urandom(8)
        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data_bytes, DES.block_size))
        final_payload = iv + ciphertext
        
    elif cipher_name == 'RC4':
        cipher = ARC4.new(key)
        ciphertext = cipher.encrypt(data_bytes)
        final_payload = ciphertext
        
    else:
        raise ValueError(f"Cipher {cipher_name} tidak didukung.")
        
    elapsed_time = time.perf_counter() - start_time
    return final_payload, elapsed_time


def decrypt_data(encrypted_bytes: bytes, cipher_name: str, key: bytes) -> tuple[bytes, float]:
    cipher_name = cipher_name.upper()
    start_time = time.perf_counter()
    
    if cipher_name == 'AES':
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, AES.block_size)
        
    elif cipher_name == 'DES':
        iv = encrypted_bytes[:8]
        ciphertext = encrypted_bytes[8:]
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, DES.block_size)
        
    elif cipher_name == 'RC4':
        cipher = ARC4.new(key)
        plaintext = cipher.decrypt(encrypted_bytes)
        
    else:
        raise ValueError(f"Cipher {cipher_name} tidak didukung.")
        
    elapsed_time = time.perf_counter() - start_time
    return plaintext, elapsed_time