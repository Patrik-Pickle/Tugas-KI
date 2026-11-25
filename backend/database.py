import sqlite3
import os
from auth_utils import hash_password, verify_password

DB_NAME = "wbs_data.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'pelapor',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            chronology_encrypted BLOB NOT NULL,
            ktp_filename TEXT NOT NULL,
            doc_filename TEXT NOT NULL,
            video_filename TEXT NOT NULL,
            cipher_used TEXT NOT NULL,
            salt BLOB NOT NULL,
            salt_text BLOB,
            salt_ktp BLOB,
            salt_doc BLOB,
            salt_video BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin_investigator",))
    if not cursor.fetchone():
        admin_pass_hash = hash_password("AdminWBS2026!")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            ("admin_investigator", admin_pass_hash, "investigator")
        )
        conn.commit()
        print("[+] Akun investigator default dibuat: admin_investigator / AdminWBS2026!")

    conn.close()
    print("[+] Database SQLite berhasil diinisialisasi!")

# Fungsi Authentication

def register_user(username, password, role="pelapor"):
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed_pwd = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, hashed_pwd, role)
        )
        conn.commit()
        return True, "Registrasi berhasil!"
    except sqlite3.IntegrityError:
        return False, "Username sudah digunakan!"
    finally:
        conn.close()

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and verify_password(user['password_hash'], password):
        return {
            "id": user['id'],
            "username": user['username'],
            "role": user['role']
        }
    return None

# Fungsi Report Management

def create_report(user_id, title, chronology_encrypted, ktp_filename, doc_filename, video_filename, cipher_used, salt, salt_text=None, salt_ktp=None, salt_doc=None, salt_video=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Enkripsi metadata judul (title) menggunakan AES untuk perlindungan privasi GDPR / UU PDP No. 27/2022
    from backend import crypto_utils
    title_salt = os.urandom(16)
    title_key = crypto_utils.get_report_key(title_salt, "AES")
    enc_title, _ = crypto_utils.encrypt_data(title.encode("utf-8"), "AES", title_key)
    
    import base64
    enc_title_b64 = base64.b64encode(title_salt + enc_title).decode('utf-8')

    # Jika salt spesifik komponen tidak diberikan, gunakan salt utama
    s_text = salt_text if salt_text is not None else salt
    s_ktp = salt_ktp if salt_ktp is not None else salt
    s_doc = salt_doc if salt_doc is not None else salt
    s_video = salt_video if salt_video is not None else salt

    cursor.execute('''
        INSERT INTO reports (
            user_id, title, chronology_encrypted, 
            ktp_filename, doc_filename, video_filename, cipher_used, salt,
            salt_text, salt_ktp, salt_doc, salt_video
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, enc_title_b64, chronology_encrypted, ktp_filename, doc_filename, video_filename, cipher_used, salt, s_text, s_ktp, s_doc, s_video))
    
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def decrypt_report_title(title_field):
    if not title_field:
        return "Untitled Report"
    try:
        import base64
        from backend import crypto_utils
        raw = base64.b64decode(title_field.encode('utf-8'))
        if len(raw) <= 16:
            return title_field # fallback jika plain lama
        title_salt = raw[:16]
        enc_data = raw[16:]
        title_key = crypto_utils.get_report_key(title_salt, "AES")
        dec_bytes, _ = crypto_utils.decrypt_data(enc_data, "AES", title_key)
        return dec_bytes.decode('utf-8')
    except Exception:
        return title_field # fallback jika bukan format terenkripsi

def get_reports_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, cipher_used, created_at 
        FROM reports 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Decrypt title for each row
    reports = []
    for r in rows:
        d = dict(r)
        d['title'] = decrypt_report_title(d['title'])
        reports.append(d)
    return reports

def get_all_reports():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.id, r.title, r.cipher_used, r.created_at, u.username as reporter
        FROM reports r
        JOIN users u ON r.user_id = u.id
        ORDER BY r.created_at DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    reports = []
    for r in rows:
        d = dict(r)
        d['title'] = decrypt_report_title(d['title'])
        reports.append(d)
    return reports

def get_report_by_id(report_id, current_user_id=None, is_investigator=False):
    conn = get_connection()
    cursor = conn.cursor()
    
    if is_investigator:
        cursor.execute('''
            SELECT r.*, u.username as reporter
            FROM reports r
            JOIN users u ON r.user_id = u.id
            WHERE r.id = ?
        ''', (report_id,))
    else:
        cursor.execute('''
            SELECT r.*, u.username as reporter
            FROM reports r
            JOIN users u ON r.user_id = u.id
            WHERE r.id = ? AND r.user_id = ?
        ''', (report_id, current_user_id))
        
    row = cursor.fetchone()
    conn.close()
    
    if row:
        d = dict(row)
        d['title'] = decrypt_report_title(d['title'])
        # Fallback jika kolom salt spesifik belum ada (database lama sebelum migrasi)
        if 'salt_text' not in d or d['salt_text'] is None:
            d['salt_text'] = d['salt']
        if 'salt_ktp' not in d or d['salt_ktp'] is None:
            d['salt_ktp'] = d['salt']
        if 'salt_doc' not in d or d['salt_doc'] is None:
            d['salt_doc'] = d['salt']
        if 'salt_video' not in d or d['salt_video'] is None:
            d['salt_video'] = d['salt']
        return d
    return None

if __name__ == "__main__":
    init_db()