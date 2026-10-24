import os
import time
from Crypto.Cipher import AES, DES, ARC4
from Crypto.Util.Padding import pad, unpad

KEY_AES = b'HeavyRotationJKT' 
KEY_DES = b'Coldiac!'               
KEY_RC4 = b'MerinduLagiYovie'      

def encrypt_data(data_bytes: bytes, cipher_name: str) -> tuple[bytes, float]:
    cipher_name = cipher_name.upper()
    start_time = time.perf_counter()
    
    if cipher_name == 'AES':
        iv = os.urandom(16)
        cipher = AES.new(KEY_AES, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data_bytes, AES.block_size))
        final_payload = iv + ciphertext
        
    elif cipher_name == 'DES':
        iv = os.urandom(8)
        cipher = DES.new(KEY_DES, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(data_bytes, DES.block_size))
        final_payload = iv + ciphertext
        
    elif cipher_name == 'RC4':
        cipher = ARC4.new(KEY_RC4)
        ciphertext = cipher.encrypt(data_bytes)
        final_payload = ciphertext
        
    else:
        raise ValueError(f"Cipher {cipher_name} tidak didukung.")
        
    elapsed_time = time.perf_counter() - start_time
    return final_payload, elapsed_time


def decrypt_data(encrypted_bytes: bytes, cipher_name: str) -> tuple[bytes, float]:
    cipher_name = cipher_name.upper()
    start_time = time.perf_counter()
    
    if cipher_name == 'AES':
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]
        cipher = AES.new(KEY_AES, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, AES.block_size)
        
    elif cipher_name == 'DES':
        iv = encrypted_bytes[:8]
        ciphertext = encrypted_bytes[8:]
        cipher = DES.new(KEY_DES, DES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, DES.block_size)
        
    elif cipher_name == 'RC4':
        cipher = ARC4.new(KEY_RC4)
        plaintext = cipher.decrypt(encrypted_bytes)
        
    else:
        raise ValueError(f"Cipher {cipher_name} tidak didukung.")
        
    elapsed_time = time.perf_counter() - start_time
    return plaintext, elapsed_time