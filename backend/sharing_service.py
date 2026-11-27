"""
backend/sharing_service.py
Service handling report access requests, out-of-band key wrapping (RSA-OAEP),
and share key claiming / envelope encryption for SecureReport Tugas 2.
"""

import os
import base64
from backend.database import get_connection
from backend.asymmetric_utils import encrypt_key_with_rsa, decrypt_key_with_rsa
from backend import crypto_utils

def request_report_access(report_id: int, requester_id: int) -> tuple[bool, str]:
    """
    Submits an access request from a user (requester) to a report owner.
    Prevents duplicate pending or approved requests for the same report.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get report owner and verify report existence
    cursor.execute("SELECT user_id FROM reports WHERE id = ?", (report_id,))
    report = cursor.fetchone()
    if not report:
        conn.close()
        return False, "Laporan tidak ditemukan."
    
    owner_id = report['user_id']
    if owner_id == requester_id:
        conn.close()
        return False, "Anda adalah pemilik laporan ini."
        
    # Check if a pending or approved request already exists
    cursor.execute("""
        SELECT id, status FROM access_requests 
        WHERE report_id = ? AND requester_id = ?
    """, (report_id, requester_id))
    existing = cursor.fetchone()
    
    if existing:
        if existing['status'] == 'approved':
            conn.close()
            return False, "Anda sudah memiliki akses yang disetujui untuk laporan ini."
        elif existing['status'] == 'pending':
            conn.close()
            return False, "Permintaan akses sedang menunggu persetujuan pemilik."
            
    try:
        cursor.execute("""
            INSERT INTO access_requests (report_id, requester_id, owner_id, status)
            VALUES (?, ?, ?, 'pending')
        """, (report_id, requester_id, owner_id))
        conn.commit()
        return True, "Permintaan akses berhasil dikirim ke pemilik laporan."
    except Exception as e:
        return False, f"Gagal mengirim permintaan: {str(e)}"
    finally:
        conn.close()

def get_incoming_access_requests(owner_id: int):
    """
    Retrieves incoming access requests for reports owned by the specified user.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.id, ar.report_id, ar.status, ar.created_at, 
               u.username as requester_username,
               r.title as report_title_enc
        FROM access_requests ar
        JOIN users u ON ar.requester_id = u.id
        JOIN reports r ON ar.report_id = r.id
        WHERE ar.owner_id = ?
        ORDER BY ar.created_at DESC
    """, (owner_id,))
    rows = cursor.fetchall()
    conn.close()
    
    from backend.database import decrypt_report_title
    requests = []
    for row in rows:
        d = dict(row)
        d['report_title'] = decrypt_report_title(d['report_title_enc'])
        requests.append(d)
    return requests

def get_outgoing_access_requests(requester_id: int):
    """
    Retrieves access requests sent by the specified requester.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ar.id, ar.report_id, ar.status, ar.created_at,
               u.username as owner_username,
               r.title as report_title_enc
        FROM access_requests ar
        JOIN users u ON ar.owner_id = u.id
        JOIN reports r ON ar.report_id = r.id
        WHERE ar.requester_id = ?
        ORDER BY ar.created_at DESC
    """, (requester_id,))
    rows = cursor.fetchall()
    conn.close()
    
    from backend.database import decrypt_report_title
    requests = []
    for row in rows:
        d = dict(row)
        d['report_title'] = decrypt_report_title(d['report_title_enc'])
        requests.append(d)
    return requests

def approve_access_request(request_id: int, owner_id: int) -> tuple[bool, str, str | None]:
    """
    Approves an access request using Envelope Encryption / Key Wrapping.
    1. Generates a fresh random Share Symmetric Key (32 bytes).
    2. Retrieves or derives the report's original DEK (Data Encryption Key) using the owner's salt/cipher.
    3. Wraps the report DEK using the Share Symmetric Key (Encrypt-then-MAC style or AES-CBC) and stores it in wrapped_report_key.
    4. Wraps the Share Symmetric Key using the requester's RSA Public Key via RSA-OAEP (SHA-256) 
       to return as an out-of-band token (Base64 string for WhatsApp/Email), without storing the RSA-encrypted share key in DB.
    Returns (success, message, rsa_encrypted_share_key_b64_for_out_of_band).
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ar.*, u.rsa_public_key as requester_rsa_pub, r.salt, r.cipher_used, r.user_id
        FROM access_requests ar
        JOIN users u ON ar.requester_id = u.id
        JOIN reports r ON ar.report_id = r.id
        WHERE ar.id = ? AND ar.owner_id = ?
    """, (request_id, owner_id))
    req = cursor.fetchone()
    
    if not req:
        conn.close()
        return False, "Permintaan akses tidak ditemukan atau Anda bukan pemilik laporan.", None
        
    if req['status'] == 'approved':
        conn.close()
        return False, "Permintaan ini sudah disetujui sebelumnya. Silakan salin kembali kunci out-of-band jika diperlukan.", None
        
    requester_pub_key = req['requester_rsa_pub']
    if not requester_pub_key:
        conn.close()
        return False, "Peminta tidak memiliki kunci publik RSA yang valid.", None
        
    try:
        # 1. Obtain the report's original DEK (Data Encryption Key) using report's salt and cipher
        report_salt = req['salt']
        cipher_used = req['cipher_used']
        original_report_key = crypto_utils.get_report_key(report_salt, cipher_used)
        
        # 2. Generate fresh random share symmetric key (32 bytes for AES-256)
        share_symmetric_key = os.urandom(32)
        
        # 3. Wrap original report key with the share symmetric key using AES-CBC + HMAC (or encrypt_data)
        # We use share_symmetric_key to encrypt original_report_key
        wrap_iv = os.urandom(16 if cipher_used != "DES" else 8)
        wrapped_key_ciphertext, _ = crypto_utils.encrypt_data(original_report_key, "AES", share_symmetric_key)
        # Store IV + ciphertext + HMAC payload as Base64 in wrapped_report_key
        wrapped_report_key_b64 = base64.b64encode(wrapped_key_ciphertext).decode('utf-8')
        
        # 4. Wrap share symmetric key with requester's RSA Public Key (RSA-OAEP SHA-256)
        rsa_encrypted_share_key_b64 = encrypt_key_with_rsa(requester_pub_key, share_symmetric_key)
        
        # 5. Update access request status and store wrapped_report_key (DO NOT store RSA-encrypted share key permanently in DB)
        cursor.execute("""
            UPDATE access_requests 
            SET status = 'approved', wrapped_report_key = ?
            WHERE id = ?
        """, (wrapped_report_key_b64, request_id))
        conn.commit()
        
        return True, "Akses berhasil disetujui! Kunci simetris telah dibungkus secara aman.", rsa_encrypted_share_key_b64
    except Exception as e:
        conn.rollback()
        return False, f"Gagal menyetujui akses: {str(e)}", None
    finally:
        conn.close()

def reject_access_request(request_id: int, owner_id: int) -> tuple[bool, str]:
    """
    Rejects an incoming access request.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE access_requests 
        SET status = 'rejected'
        WHERE id = ? AND owner_id = ?
    """, (request_id, owner_id))
    conn.commit()
    conn.close()
    return True, "Permintaan akses ditolak."

def claim_shared_report(request_id: int, requester_id: int, requester_private_key_pem: str, rsa_encrypted_share_key_b64_input: str) -> tuple[bool, str, bytes | None]:
    """
    Claims an approved access request via out-of-band workflow:
    1. Requester provides the Base64 RSA-encrypted share key received via WhatsApp/Email.
    2. Decrypts the share key using the requester's RSA Private Key (RSA-OAEP SHA-256).
    3. Retrieves wrapped_report_key from database and decrypts it using the recovered share key
       to obtain the original report DEK (Data Encryption Key).
    Returns (success, message, original_report_key_bytes).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM access_requests 
        WHERE id = ? AND requester_id = ?
    """, (request_id, requester_id))
    req = cursor.fetchone()
    conn.close()
    
    if not req:
        return False, "Permintaan akses tidak ditemukan.", None
        
    if req['status'] != 'approved':
        return False, f"Permintaan belum disetujui (Status: {req['status']}).", None
        
    wrapped_report_key_b64 = req['wrapped_report_key']
    if not wrapped_report_key_b64:
        wrapped_report_key_b64 = req.get('encrypted_share_key') # Fallback for backward compatibility if any
        if not wrapped_report_key_b64:
            return False, "Data kunci terbungkus tidak tersedia pada permintaan ini.", None
        
    if not rsa_encrypted_share_key_b64_input or not rsa_encrypted_share_key_b64_input.strip():
        return False, "Mohon masukkan string kunci terenkripsi RSA yang diterima via WhatsApp/Email.", None
        
    try:
        # 1. Decrypt share key using RSA Private Key (RSA-OAEP SHA-256)
        share_symmetric_key = decrypt_key_with_rsa(requester_private_key_pem, rsa_encrypted_share_key_b64_input.strip())
        
        # 2. Decrypt wrapped_report_key using the recovered share symmetric key
        wrapped_ciphertext = base64.b64decode(wrapped_report_key_b64.encode('utf-8'))
        original_report_key, _ = crypto_utils.decrypt_data(wrapped_ciphertext, "AES", share_symmetric_key)
        
        return True, "Kunci laporan berhasil diklaim dan didekripsi dengan sukses!", original_report_key
    except Exception as e:
        return False, f"Gagal mendekripsi kunci (pastikan Private Key dan string WhatsApp valid): {str(e)}", None
