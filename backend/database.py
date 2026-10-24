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

def create_report(user_id, title, chronology_encrypted, ktp_filename, doc_filename, video_filename, cipher_used):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO reports (
            user_id, title, chronology_encrypted, 
            ktp_filename, doc_filename, video_filename, cipher_used
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, chronology_encrypted, ktp_filename, doc_filename, video_filename, cipher_used))
    
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def get_reports_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, cipher_used, created_at 
        FROM reports 
        WHERE user_id = ? 
        ORDER BY created_at DESC
    ''', (user_id,))
    
    reports = cursor.fetchall()
    conn.close()
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
    
    reports = cursor.fetchall()
    conn.close()
    return reports

def get_report_by_id(report_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT r.*, u.username as reporter
        FROM reports r
        JOIN users u ON r.user_id = u.id
        WHERE r.id = ?
    ''', (report_id,))
    
    report = cursor.fetchone()
    conn.close()
    return report

if __name__ == "__main__":
    init_db()