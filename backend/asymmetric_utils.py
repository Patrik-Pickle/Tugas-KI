"""
backend/asymmetric_utils.py
Asymmetric cryptography utilities using RSA-2048 with PKCS#1 OAEP (SHA-256) padding
for SecureReport Tugas 2 (Key Exchange & Secure Data Sharing).
"""

import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keypair(public_exponent: int = 65537, key_size: int = 2048) -> tuple[str, str]:
    """
    Generates an RSA keypair (Public and Private keys).
    Returns a tuple of PEM-encoded strings: (public_key_pem, private_key_pem).
    """
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size
    )
    
    public_key = private_key.public_key()
    
    # Serialize Public Key to PEM (PKCS#1 / SubjectPublicKeyInfo)
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    # Serialize Private Key to PEM (PKCS#8 unencrypted format; note: password/passphrase encryption
    # can be applied at the storage layer or higher-level auth helper if desired)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    return public_pem, private_pem


def encrypt_key_with_rsa(public_key_pem: str, symmetric_key_bytes: bytes) -> str:
    """
    Encrypts a symmetric key (or session/share key) using the recipient's RSA Public Key
    with PKCS#1 OAEP padding and SHA-256 hash algorithm.
    Returns the ciphertext encoded as a Base64 string.
    """
    public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
    
    ciphertext = public_key.encrypt(
        symmetric_key_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return base64.b64encode(ciphertext).decode('utf-8')


def decrypt_key_with_rsa(private_key_pem: str, encrypted_b64: str) -> bytes:
    """
    Decrypts an RSA-OAEP encrypted symmetric key using the owner's RSA Private Key.
    Accepts the Base64-encoded encrypted key and returns the original raw symmetric key bytes.
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None
    )
    
    ciphertext = base64.b64decode(encrypted_b64.encode('utf-8'))
    
    symmetric_key_bytes = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return symmetric_key_bytes
