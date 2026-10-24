import os
import pandas as pd
import matplotlib.pyplot as plt
from backend.crypto_utils import encrypt_data, decrypt_data

SAMPLE_DIR = "sample_data"

TEST_FILES = {
    "Data Pribadi (Teks)": os.path.join(SAMPLE_DIR, "sample_text.txt"),
    "Scan Identitas (KTP)": os.path.join(SAMPLE_DIR, "sample_ktp.jpg"),
    "Dokumen (PDF)": os.path.join(SAMPLE_DIR, "sample_doc.pdf"),
    "Video Bukti (MP4)": os.path.join(SAMPLE_DIR, "sample_video.mp4")
}

CIPHERS = ['AES', 'DES', 'RC4']

def run_benchmark():
    results = []
    
    if not os.path.exists(SAMPLE_DIR):
        os.makedirs(SAMPLE_DIR)
        print(f"[!] Folder '{SAMPLE_DIR}' belum ada. Silakan taruh file sampel di dalamnya.")
        return

    print("[*] Memulai proses benchmark...")
    
    for file_label, file_path in TEST_FILES.items():
        if not os.path.exists(file_path):
            print(f"[!] File {file_path} tidak ditemukan. Melewati {file_label}...")
            continue
            
        with open(file_path, "rb") as f:
            data_bytes = f.read()
            
        file_size_mb = len(data_bytes) / (1024 * 1024)
        
        for cipher in CIPHERS:
            enc_bytes, enc_time = encrypt_data(data_bytes, cipher)
            enc_speed = file_size_mb / enc_time if enc_time > 0 else 0
            
            dec_bytes, dec_time = decrypt_data(enc_bytes, cipher)
            dec_speed = file_size_mb / dec_time if dec_time > 0 else 0
            
            is_valid = (data_bytes == dec_bytes)
            
            results.append({
                "Tipe Data": file_label,
                "Ukuran (MB)": round(file_size_mb, 2),
                "Cipher": cipher,
                "Waktu Enkripsi (s)": round(enc_time, 6),
                "Speed Enkripsi (MB/s)": round(enc_speed, 2),
                "Waktu Dekripsi (s)": round(dec_time, 6),
                "Speed Dekripsi (MB/s)": round(dec_speed, 2),
                "Integrity": "PASS" if is_valid else "FAIL"
            })
            
    if not results:
        print("[!] Tidak ada file sampel yang diproses. Pastikan file sampel sudah ada di folder 'sample_data/'.")
        return

    df = pd.DataFrame(results)
    print("\n=== HASIL BENCHMARK KRIPTOGRAFI ===")
    print(df.to_string(index=False))
    
    csv_path = "benchmark_results.csv"
    df.to_csv(csv_path, index=False)
    
    generate_charts(df)

def generate_charts(df):
    plt.figure(figsize=(10, 5))
    
    pivot_enc = df.pivot(index='Tipe Data', columns='Cipher', values='Waktu Enkripsi (s)')
    
    ax = pivot_enc.plot(kind='bar', figsize=(10, 6), rot=0)
    plt.title('Perbandingan Waktu Enkripsi (AES vs DES vs RC4)')
    plt.ylabel('Waktu (Detik)')
    plt.xlabel('Tipe Data / File')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    chart_path = "benchmark_chart.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    run_benchmark()