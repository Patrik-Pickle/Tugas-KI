# Secure Report App — Aplikasi Aduan & Pengamanan Data Berbasis Kriptografi Simetris

Aplikasi berbasis web ini dikembangkan untuk memenuhi **Tugas Mata Kuliah Keamanan Informasi** pada materi **Enkripsi Simetris**. 

Sistem ini mengusung studi kasus **Sistem Pengaduan / Pelaporan Aman**, di mana data kerahasiaan pelapor serta berkas bukti laporan wajib dilindungi dari pihak yang tidak berwenang menggunakan kombinasi algoritma enkripsi simetris modern dan klasik.

---

## Fitur Utama

Sistem dirancang untuk memenuhi seluruh spesifikasi sebagai berikut:

1. **Pengolahan & Pengamanan 4 Jenis Data**:
   - **Data Pribadi (Teks/Form)**: Nama pelapor, NIK, dan deskripsi kronologi kejadian.
   - **Pindaian Dokumen Identitas (Foto)**: Scan KTP / Paspor pelapor (`.jpg`, `.jpeg`, `.png`).
   - **Dokumen Perkantoran (File)**: Dokumen lampiran laporan/audit (`.pdf`, `.docx`).
   - **Video Bukti (Media)**: Rekaman video bukti pendukung (`.mp4`, `.avi`, `.mkv`).
2. **Autentikasi & Kontrol Akses (RBAC)**:
   - Hanya pengguna terautentikasi (*Pelapor* atau *Investigator*) yang dapat mengakses dan mendekripsi data sesuai dengan hak aksesnya.
3. **Integritas & Rekonstruksi Data**:
   - Menerapkan skema **Encrypt-then-MAC (HMAC-SHA256)** untuk menjamin bahwa data terhindar dari pemalsuan/manipulasi (*tamper-proof*) dan dapat didekripsi secara utuh (*lossless reconstruction*).
4. **Proteksi Multi-Cipher Simetris**:
   - Mengimplementasikan 3 algoritma enkripsi simetris: **AES**, **DES**, dan **RC4**.
   - Mode operasi untuk **AES** dan **DES** menggunakan mode **CBC (Cipher Block Chaining)**.

---

## Arsitektur Kriptografi

Semua berkas dan data sensitif yang diunggah diproses di sisi *backend* sebelum disimpan ke media penyimpanan:

| Algoritma Cipher | Mode Operasi | Ukuran Kunci / Param |
| :--- | :--- | :--- |
| **AES** | **CBC** (*Cipher Block Chaining*) | 128-bit + IV (16 byte) |
| **DES** | **CBC** (*Cipher Block Chaining*) | 64-bit + IV (8 byte) |
| **RC4** | Stream Cipher | Kunci variabel (128-bit) |

> **Manajemen Kunci (Key Management)**: Kunci enkripsi tidak disimpan secara statis di database. Kunci diturunkan secara dinamis (*Dynamic Key Derivation*) menggunakan **PBKDF2-HMAC-SHA256** dari kata sandi/identitas pengguna dan *salt* acak (16 byte) yang di-generate unik per transaksi laporan.

---

## Struktur Direktori Proyek

```text
Tugas-KI-bug-fixes/
├── backend/                  # Logic & Utility Kriptografi, DB, & Auth
│   ├── auth_utils.py         # Hashing password & autentikasi pengguna
│   ├── crypto_utils.py       # Implementasi AES-CBC, DES-CBC, dan RC4
│   ├── csprng_utils.py       # Generator acak aman (CSPRNG)
│   ├── database.py           # Manajemen basis data & enkripsi simpan
│   ├── disposition_service.py# Manajemen disposisi laporan
│   └── forensic_utils.py     # Verifikasi integritas & analisis forensic
├── frontend/                 # UI Berbasis Streamlit
│   ├── app.py                # Main Entry Point Aplikasi Web
│   ├── assets/               # Custom Styling (CSS)
│   ├── components/           # Komponen UI Reusable (Cards, Previewer, Layout)
│   └── views/                # Halaman (Landing, Auth, Pelapor, Investigator)
├── storage/                  # Direktori penyimpanan data terenkripsi
├── benchmark.py              # Script benchmark performa cipher (AES vs DES vs RC4)
├── benchmark_results.csv     # Hasil pengujian kecepatan enkripsi/dekripsi
├── benchmark_charts.png      # Grafik visualisasi performa enkripsi
├── requirements.txt          # Dependencies Python
└── README.md                 # Dokumentasi proyek
```

---

## Panduan Jalankan Aplikasi

### 1. Prasyarat (*Prerequisites*)
Pastikan Anda telah menginstal **Python 3.9** atau versi yang lebih baru di perangkat Anda.

### 2. Kloning Repositori & Persiapan Environment
```bash
# Clone repositori ini
git clone https://github.com/username/Tugas-KI-bug-fixes.git
cd Tugas-KI-bug-fixes

# Buat virtual environment (opsional tapi disarankan)
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Instalasi Dependencies
```bash
pip install -r requirements.txt
```

### 4. Inisialisasi Basis Data (SQLite)
Jalankan skrip berikut untuk membuat tabel dan skema database awal:
```bash
python backend/database.py
```

### 5. Menjalankan Aplikasi Web
Aplikasi dibangun menggunakan framework **Streamlit**. Jalankan perintah berikut:
```bash
streamlit run frontend/app.py
```
Aplikasi akan terbuka otomatis di browser Anda pada alamat `http://localhost:8501`.

---

## Pengujian & Benchmark

Proyek ini dilengkapi dengan script analisis benchmark untuk mengukur performa ketiga algoritma (**AES-CBC**, **DES-CBC**, dan **RC4**) terhadap 4 jenis data.

Untuk menjalankan pengujian benchmark:
```bash
python benchmark.py
```
Hasil pengujian akan diperbarui di `benchmark_results.csv` dan grafik visualisasi disintesis pada `benchmark_charts.png`.

---

## Peran Pengguna (*User Roles*)

1. **Pelapor (User)**:
   - Membuat akun / Login.
   - Mengisi form aduan (teks kronologi).
   - Mengunggah foto KTP, dokumen bukti PDF/Docx, dan video bukti.
   - Memilih algoritma cipher yang ingin digunakan untuk mengamankan laporannya.
   - Memantau status penanganan dan hasil penelaahan kasus.
2. **Investigator (Admin/Petugas)**:
   - Login sebagai petugas/investigator.
   - Melihat daftar laporan masuk yang terenkripsi.
   - Mendekripsi data laporan dan mengunduh berkas fisik secara utuh untuk kebutuhan investigasi.
   - Memberikan amar putusan dan status disposisi laporan.

---
*Dikembangkan untuk Tugas Mata Kuliah Keamanan Informasi.*
