"""
backend/csprng_utils.py
Modul Kriptografis CSPRNG (Cryptographically Secure Pseudo-Random Number Generator).
Menyediakan utilitas pembangkitan dan validasi token tiket laporan dengan entropi tinggi
menggunakan modul secrets Python (berbasis os.urandom).
"""

import secrets
import re

TICKET_PATTERN = re.compile(r"^WBS-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}$")

def generate_csprng_ticket(prefix: str = "WBS", hex_bytes: int = 6) -> str:
    """
    Membangkitkan tanda terima tiket acak berkeamanan tinggi (CSPRNG).
    Menggunakan secrets.token_hex(6) (12 karakter heksadesimal acak).
    Format keluaran: WBS-XXXX-XXXX-XXXX.
    Ruang entropi: 16^12 = 281.474.976.710.656 kemungkinan kombinasi acak.
    """
    raw = secrets.token_hex(hex_bytes).upper()
    return f"{prefix}-{raw[:4]}-{raw[4:8]}-{raw[8:12]}"

def validate_ticket_format(ticket_code: str) -> bool:
    """
    Memvalidasi apakah string tiket memenuhi format resmi WBS-XXXX-XXXX-XXXX.
    """
    if not isinstance(ticket_code, str):
        return False
    return bool(TICKET_PATTERN.match(ticket_code.strip().upper()))

def generate_secure_token(nbytes: int = 16) -> str:
    """
    Membangkitkan token heksadesimal acak untuk keperluan sesi atau digest verifikasi.
    """
    return secrets.token_hex(nbytes)
