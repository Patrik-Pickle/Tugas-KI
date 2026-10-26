import os
import time
import tracemalloc
import psutil
import pandas as pd
import matplotlib.pyplot as plt
from backend import crypto_utils

# Buat folder sample_data jika belum ada
SAMPLE_DIR = "sample_data"
os.makedirs(SAMPLE_DIR, exist_ok=True)

TEST_FILES = {
    "Data Pribadi (Teks)": os.path.join(SAMPLE_DIR, "sample_text.txt"),
    "Scan Identitas (KTP)": os.path.join(SAMPLE_DIR, "sample_ktp.jpg"),
    "Dokumen Bukti (PDF)": os.path.join(SAMPLE_DIR, "sample_doc.pdf"),
    "Video Bukti (MP4)": os.path.join(SAMPLE_DIR, "sample_video.mp4")
}

CIPHERS = ['AES', 'DES', 'RC4']
DUMMY_PASSWORD = "UserSecurePass123!"
DUMMY_SALT = b'WBS_SecureSalt16'

def ensure_sample_files_exist():
    """Membuat file dummy otomatis jika sampel belum ada di folder sample_data"""
    if not os.path.exists(TEST_FILES["Data Pribadi (Teks)"]):
        with open(TEST_FILES["Data Pribadi (Teks)"], "wb") as f:
            f.write(b"Nama: Pelapor Rahasia\nNIK: 3578000000000001\nKronologi: Laporan tindak pidana..." * 50) # ~2 KB
            
    if not os.path.exists(TEST_FILES["Scan Identitas (KTP)"]):
        with open(TEST_FILES["Scan Identitas (KTP)"], "wb") as f:
            f.write(os.urandom(500 * 1024)) # ~500 KB dummy image
            
    if not os.path.exists(TEST_FILES["Dokumen Bukti (PDF)"]):
        with open(TEST_FILES["Dokumen Bukti (PDF)"], "wb") as f:
            f.write(os.urandom(2 * 1024 * 1024)) # ~2 MB dummy PDF
            
    if not os.path.exists(TEST_FILES["Video Bukti (MP4)"]):
        with open(TEST_FILES["Video Bukti (MP4)"], "wb") as f:
            f.write(os.urandom(10 * 1024 * 1024)) # ~10 MB dummy Video

def run_advanced_benchmark():
    ensure_sample_files_exist()
    results = []
    process = psutil.Process(os.getpid())
    
    print("[*] Memulai Advanced Benchmark (Time, RAM, CPU)...")
    
    for file_label, file_path in TEST_FILES.items():
        if not os.path.exists(file_path):
            print(f"[!] Warning: File {file_path} tidak ditemukan, melewati...")
            continue
            
        with open(file_path, "rb") as f:
            data_bytes = f.read()
            
        file_size_mb = len(data_bytes) / (1024 * 1024)
        
        for cipher in CIPHERS:
            # Generate key menggunakan PBKDF2
            key = crypto_utils.derive_key(DUMMY_PASSWORD, DUMMY_SALT, cipher)
            
            # --- UJUR ENKRIPSI ---
            tracemalloc.start()
            cpu_before = process.cpu_percent(interval=None)
            
            enc_bytes, enc_time = crypto_utils.encrypt_data(data_bytes, cipher, key)
            
            cpu_after = process.cpu_percent(interval=None)
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            ram_overhead_mb = peak_mem / (1024 * 1024)
            cpu_usage_pct = max(cpu_after - cpu_before, 0.1)
            
            # --- UJUR DEKRIPSI ---
            dec_bytes, dec_time = crypto_utils.decrypt_data(enc_bytes, cipher, key)
            is_valid = (data_bytes == dec_bytes)
            
            results.append({
                "Tipe Data": file_label,
                "Ukuran (MB)": round(file_size_mb, 2),
                "Cipher": cipher,
                "Waktu Enkripsi (s)": round(enc_time, 5),
                "Waktu Dekripsi (s)": round(dec_time, 5),
                "RAM Overhead (MB)": round(ram_overhead_mb, 3),
                "CPU Usage (%)": round(cpu_usage_pct, 1),
                "Integritas": "PASS" if is_valid else "FAIL"
            })
            
    if not results:
        print("[!] Gagal: Tidak ada data yang berhasil diuji.")
        return

    df = pd.DataFrame(results)
    print("\n=== HASIL BENCHMARK LENGKAP ===")
    print(df.to_string(index=False))
    
    # Simpan ke CSV
    csv_path = "benchmark_results.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n[+] Hasil berhasil disimpan ke '{csv_path}'")
    
    generate_charts(df)

def generate_charts(df):
    """Membuat grafik visual otomatis untuk laporan A4"""
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Chart 1: Waktu Enkripsi
    df_pivot_time = df.pivot(index='Tipe Data', columns='Cipher', values='Waktu Enkripsi (s)')
    df_pivot_time.plot(kind='bar', ax=axes[0], colormap='viridis')
    axes[0].set_title('Waktu Enkripsi (Detik)')
    axes[0].set_ylabel('Detik')
    axes[0].tick_params(axis='x', rotation=15)
    
    # Chart 2: RAM Overhead
    df_pivot_ram = df.pivot(index='Tipe Data', columns='Cipher', values='RAM Overhead (MB)')
    df_pivot_ram.plot(kind='bar', ax=axes[1], colormap='magma')
    axes[1].set_title('Penggunaan RAM (MB)')
    axes[1].set_ylabel('MB')
    axes[1].tick_params(axis='x', rotation=15)
    
    # Chart 3: CPU Usage
    df_pivot_cpu = df.pivot(index='Tipe Data', columns='Cipher', values='CPU Usage (%)')
    df_pivot_cpu.plot(kind='bar', ax=axes[2], colormap='coolwarm')
    axes[2].set_title('Penggunaan CPU (%)')
    axes[2].set_ylabel('Persentase (%)')
    axes[2].tick_params(axis='x', rotation=15)
    
    plt.tight_layout()
    chart_path = "benchmark_charts.png"
    plt.savefig(chart_path, dpi=300)
    print(f"[+] Grafik visual berhasil disimpan ke '{chart_path}'!")

if __name__ == "__main__":
    run_advanced_benchmark()