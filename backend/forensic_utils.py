"""
backend/forensic_utils.py
Modul Forensik Kriptografi & Visualisasi Derau Sandi (Ciphertext Visualizer).
Menyediakan kalkulasi entropi informasi Shannon, pembentukan matriks piksel derau (noise canvas),
serta ekstraksi telemetri sandi untuk berkas bukti hukum.
"""

import math
import io
import hashlib
from collections import Counter
from PIL import Image

def calculate_shannon_entropy(data_bytes: bytes) -> float:
    """
    Menghitung entropi informasi Shannon dari data byte biner.
    H(X) = - sum(p(x) * log2(p(x)))
    Rentang nilai: 0.00 hingga 8.00 bits per byte.
    Data terenkripsi kuat (CBC/RC4) memiliki entropi mendekati 7.99 - 8.00 bits/byte.
    """
    if not data_bytes:
        return 0.0
    
    total_len = len(data_bytes)
    counts = Counter(data_bytes)
    
    entropy = 0.0
    for count in counts.values():
        p_x = count / total_len
        if p_x > 0:
            entropy -= p_x * math.log2(p_x)
            
    return round(entropy, 4)

def generate_ciphertext_noise_image(data_bytes: bytes, width: int = 256, height: int = 256) -> bytes:
    """
    Memetakan byte ciphertext menjadi gambar grayscale 8-bit (L mode).
    Setiap byte (0-255) langsung menjadi intensitas luminans sebuah piksel.
    Mengembalikan byte biner gambar berformat PNG di memori buffer.
    """
    required_bytes = width * height
    if not data_bytes:
        # Fallback jika data kosong
        img = Image.new("L", (width, height), color=128)
    else:
        if len(data_bytes) >= required_bytes:
            sample_bytes = data_bytes[:required_bytes]
        else:
            # Ulangi data jika ukuran berkas lebih kecil dari kanvas
            repeats = (required_bytes // len(data_bytes)) + 1
            sample_bytes = (data_bytes * repeats)[:required_bytes]
            
        img = Image.frombytes("L", (width, height), sample_bytes)
        
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def get_file_forensic_telemetry(file_path: str, canvas_dim: int = 256) -> dict:
    """
    Mengekstrak telemetri kriptografis lengkap dari berkas fisik terenkripsi:
    - Ukuran berkas (bytes dan KB)
    - Digest hash integritas SHA-256
    - Skor Entropi Shannon (bits/byte)
    - Cuplikan heksadesimal 64 byte pertama
    - Byte gambar derau acak (PNG visualizer)
    """
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except Exception as e:
        return {
            "error": f"Gagal membaca berkas: {str(e)}",
            "exists": False
        }
        
    if not data:
        return {
            "error": "Berkas kosong.",
            "exists": True,
            "size_bytes": 0,
            "size_kb": 0.0,
            "sha256": "-",
            "entropy": 0.0,
            "hex_preview": "",
            "noise_png": None
        }
        
    size_bytes = len(data)
    size_kb = round(size_bytes / 1024, 2)
    sha256_hash = hashlib.sha256(data).hexdigest()
    entropy_val = calculate_shannon_entropy(data)
    
    # Cuplikan 64 byte pertama dalam format heksadesimal berpasangan
    preview_slice = data[:64]
    hex_preview = " ".join(f"{b:02X}" for b in preview_slice)
    if size_bytes > 64:
        hex_preview += " ..."
        
    noise_png = generate_ciphertext_noise_image(data, canvas_dim, canvas_dim)
    
    return {
        "exists": True,
        "error": None,
        "size_bytes": size_bytes,
        "size_kb": size_kb,
        "sha256": sha256_hash,
        "entropy": entropy_val,
        "hex_preview": hex_preview,
        "noise_png": noise_png
    }
