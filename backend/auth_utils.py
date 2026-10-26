import hashlib
import os

def hash_password(password: str) -> str:
    salt = os.urandom(16) 
    password_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )
    return f"{salt.hex()}${password_hash.hex()}"

def verify_password(stored_password_hash: str, provided_password: str) -> bool:
    try:
        salt_hex, hash_hex = stored_password_hash.split('$')
        salt = bytes.fromhex(salt_hex)
        
        new_hash = hashlib.pbkdf2_hmac(
            'sha256', 
            provided_password.encode('utf-8'), 
            salt, 
            100000
        )
        
        return hmac_compare(new_hash.hex(), hash_hex)
    except Exception:
        return False

def hmac_compare(val1: str, val2: str) -> bool:
    import hmac
    return hmac.compare_digest(val1, val2)