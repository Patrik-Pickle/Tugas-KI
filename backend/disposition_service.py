"""
backend/disposition_service.py
Layanan Backend untuk Manajemen Disposisi, Putusan Investigasi, dan Pelacakan Aduan.
Mengelola tabel report_dispositions di database SQLite wbs_data.db.
"""

import sqlite3
import os

try:
    from csprng_utils import generate_csprng_ticket
except ImportError:
    from backend.csprng_utils import generate_csprng_ticket

DB_NAME = "wbs_data.db"

STATUS_PENDING = "Menunggu Penelaahan"
STATUS_INVESTIGATING = "Dalam Proses Investigasi"
STATUS_NEED_EVIDENCE = "Perlu Bukti Tambahan"
STATUS_COMPLETED = "Laporan Selesai & Ditindaklanjuti"
STATUS_REJECTED = "Laporan Ditolak / Tidak Memenuhi Syarat"

STATUS_CHOICES = [
    STATUS_PENDING,
    STATUS_INVESTIGATING,
    STATUS_NEED_EVIDENCE,
    STATUS_COMPLETED,
    STATUS_REJECTED
]

VERDICT_PENDING = "Dalam Proses Penelaahan (Belum Terbit Putusan)"
VERDICT_INTERNAL_SANCTION = "Rekomendasi Sanksi Disiplin Internal"
VERDICT_LAW_ENFORCEMENT = "Pelimpahan Perkara ke Aparat Penegak Hukum (APH)"
VERDICT_DISMISSED = "Penghentian Pemeriksaan (Kasus Ditutup / Tidak Terbukti)"

VERDICT_CHOICES = [
    VERDICT_PENDING,
    VERDICT_INTERNAL_SANCTION,
    VERDICT_LAW_ENFORCEMENT,
    VERDICT_DISMISSED
]

def get_db_connection():
    """
    Mengembalikan koneksi ke SQLite database wbs_data.db dengan Row factory.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_tracking_db():
    """
    Inisialisasi tabel report_dispositions dan memastikan kolom
    decision_number, verdict_category, dan tracking_token tersedia.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS report_dispositions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'Menunggu Penelaahan',
            notes TEXT DEFAULT '',
            decision_number TEXT DEFAULT '',
            verdict_category TEXT DEFAULT '',
            tracking_token TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (report_id) REFERENCES reports (id)
        )
    """)
    conn.commit()

    # Validasi migrasi kolom tambahan jika tabel sudah ada dari versi sebelumnya
    cursor.execute("PRAGMA table_info(report_dispositions)")
    existing_columns = [row["name"] for row in cursor.fetchall()]

    if "decision_number" not in existing_columns:
        cursor.execute("ALTER TABLE report_dispositions ADD COLUMN decision_number TEXT DEFAULT ''")
        conn.commit()

    if "verdict_category" not in existing_columns:
        cursor.execute("ALTER TABLE report_dispositions ADD COLUMN verdict_category TEXT DEFAULT ''")
        conn.commit()

    if "tracking_token" not in existing_columns:
        cursor.execute("ALTER TABLE report_dispositions ADD COLUMN tracking_token TEXT DEFAULT ''")
        conn.commit()

    # Backfill tracking_token untuk baris yang belum memiliki token CSPRNG
    cursor.execute("SELECT id, tracking_token FROM report_dispositions WHERE tracking_token IS NULL OR tracking_token = ''")
    rows_to_backfill = cursor.fetchall()
    for row in rows_to_backfill:
        new_token = generate_csprng_ticket()
        cursor.execute("UPDATE report_dispositions SET tracking_token = ? WHERE id = ?", (new_token, row["id"]))
    if rows_to_backfill:
        conn.commit()

    conn.close()

def get_report_disposition(report_id: int) -> dict:
    """
    Mengambil data disposisi laporan dari basis data SQLite.
    Jika laporan belum memiliki disposisi, baris default akan dibuat otomatis
    lengkap dengan tracking_token berbasis CSPRNG.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, notes, decision_number, verdict_category, tracking_token, updated_at
        FROM report_dispositions
        WHERE report_id = ?
    """, (report_id,))
    row = cursor.fetchone()

    if not row:
        token = generate_csprng_ticket()
        cursor.execute("""
            INSERT OR IGNORE INTO report_dispositions (report_id, status, notes, decision_number, verdict_category, tracking_token)
            VALUES (?, 'Menunggu Penelaahan', '', '', '', ?)
        """, (report_id, token))
        conn.commit()
        cursor.execute("""
            SELECT status, notes, decision_number, verdict_category, tracking_token, updated_at
            FROM report_dispositions
            WHERE report_id = ?
        """, (report_id,))
        row = cursor.fetchone()

    conn.close()

    if row:
        token_val = row["tracking_token"]
        if not token_val:
            token_val = generate_csprng_ticket()
            conn = get_db_connection()
            c2 = conn.cursor()
            c2.execute("UPDATE report_dispositions SET tracking_token = ? WHERE report_id = ?", (token_val, report_id))
            conn.commit()
            conn.close()

        return {
            "status": row["status"] or STATUS_PENDING,
            "notes": row["notes"] or "",
            "decision_number": row["decision_number"] or "",
            "verdict_category": row["verdict_category"] or "",
            "tracking_token": token_val,
            "updated_at": row["updated_at"] or ""
        }
    
    return {
        "status": STATUS_PENDING,
        "notes": "",
        "decision_number": "",
        "verdict_category": "",
        "tracking_token": generate_csprng_ticket(),
        "updated_at": ""
    }

def update_report_disposition(
    report_id: int,
    status: str,
    notes: str = "",
    decision_number: str = "",
    verdict_category: str = ""
) -> bool:
    """
    Memperbarui status penanganan, catatan temuan, nomor putusan, dan klasifikasi amar putusan.
    Mempertahankan tracking_token yang sudah ada agar tidak berubah.
    """
    existing = get_report_disposition(report_id)
    token = existing.get("tracking_token") or generate_csprng_ticket()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO report_dispositions (report_id, status, notes, decision_number, verdict_category, tracking_token, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(report_id) DO UPDATE SET
            status = excluded.status,
            notes = excluded.notes,
            decision_number = excluded.decision_number,
            verdict_category = excluded.verdict_category,
            updated_at = CURRENT_TIMESTAMP
    """, (report_id, status, notes, decision_number, verdict_category, token))
    conn.commit()
    conn.close()
    return True

def find_report_for_tracking(query_code: str):
    """
    Mencari informasi aduan berdasarkan kode token CSPRNG atau ID laporan.
    Mengembalikan metadata aduan dan disposisi saat ini.
    """
    clean_code = query_code.strip().upper()
    report_id = None

    conn = get_db_connection()
    cursor = conn.cursor()

    # Cek pencarian berdasarkan tracking_token CSPRNG
    cursor.execute("""
        SELECT report_id FROM report_dispositions WHERE tracking_token = ?
    """, (clean_code,))
    disp_match = cursor.fetchone()
    if disp_match:
        report_id = disp_match["report_id"]

    if not report_id:
        conn.close()
        return None

    cursor.execute("""
        SELECT id, title, cipher_used, created_at
        FROM reports
        WHERE id = ?
    """, (report_id,))
    report = cursor.fetchone()
    conn.close()

    if not report:
        return None

    disp = get_report_disposition(report["id"])
    return {
        "id": report["id"],
        "ticket_code": disp.get("tracking_token", f"WBS-{report['id']:05d}"),
        "title": report["title"],
        "cipher_used": report["cipher_used"],
        "created_at": report["created_at"],
        "status": disp["status"],
        "notes": disp["notes"],
        "decision_number": disp["decision_number"],
        "verdict_category": disp["verdict_category"],
        "updated_at": disp["updated_at"]
    }
