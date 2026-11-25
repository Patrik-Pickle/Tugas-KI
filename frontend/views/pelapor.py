import os
import time
import streamlit as st
import database
import crypto_utils
import html
from components.header import render_sovereign_header
from components.cards import render_cipher_selector, render_benchmark_summary
from components.icons import (
    icon,
    ICON_SHIELD_CHECK,
    ICON_LOCK,
    ICON_FILE_TEXT,
    ICON_ID_CARD,
    ICON_VIDEO,
    ICON_CPU,
    ICON_CHECK_CIRCLE,
    ICON_SCALE
)
from components.utils import clean_html
from components.layout import step_badge, callout
from components.footer import render_footer
from components.tracking_db import (
    get_report_disposition,
    render_status_badge,
    render_tracking_timeline
)

STORAGE_DIR = os.path.join("storage", "encrypted_files")

def render_pelapor_view():
    """
    Renders the Whistleblower Portal with sovereign sidebar and 2-column layout:
    Left Sidebar: User profile, workspace navigation, compliance status, logout
    Main Area: Guided report submission form or encrypted report history
    """
    user = st.session_state.get("user")
    if not user:
        st.warning("Silakan masuk terlebih dahulu.")
        return

    # Header in main content area with top-left profile popover
    render_sovereign_header(
        title="SecureReport : Portal Pelapor"
    )

    tab_create, tab_history = st.tabs(["Buat Laporan Terenkripsi", "Riwayat Laporan Saya"])

    with tab_create:
        col_main, col_side = st.columns([2.1, 1])

        with col_side:
            # Sticky-like reassurance and compliance panel
            st.markdown(
                clean_html(f"""
                <div class="sovereign-card-interactive" style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.35rem 1.5rem; box-shadow: 0 1px 3px rgba(11,15,25,0.05); margin-bottom: 1.25rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.85rem;">
                        {icon(ICON_SHIELD_CHECK, size=20, color="#1d4ed8")}
                        <span style="font-weight: 700; color: #0b0f19; font-size: 0.95rem;">Jaminan Kerahasiaan</span>
                    </div>
                    <p style="font-size: 0.84rem; color: #475569; line-height: 1.55; margin-bottom: 0.85rem;">
                        Seluruh kronologi dan 3 berkas bukti dienkripsi di peladen sebelum disimpan. Kunci enkripsi diturunkan dari kunci utama server dan tidak disimpan dalam bentuk teks biasa.
                    </p>
                    <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 0.65rem 0.85rem; font-size: 0.78rem; color: #1e40af; line-height: 1.45;">
                        <b>Dasar Hukum:</b> Dilindungi secara mutlak oleh UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi.
                    </div>
                </div>

                <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 1.25rem 1.5rem;">
                    <div style="font-weight: 700; color: #0b0f19; font-size: 0.88rem; margin-bottom: 0.65rem;">
                        Persyaratan Berkas Bukti:
                    </div>
                    <ul style="margin: 0; padding-left: 1.2rem; font-size: 0.82rem; color: #475569; line-height: 1.6;">
                        <li>Scan KTP resmi (JPG/PNG)</li>
                        <li>Dokumen pendukung (PDF)</li>
                        <li>Rekaman video pembuktian (MP4)</li>
                    </ul>
                </div>
                """),
                unsafe_allow_html=True
            )

        with col_main:
            st.markdown(
                callout(
                    title="Formulir Pengaduan Terlindungi & Terenkripsi Otomatis",
                    message="Identitas Anda dan seluruh berkas bukti dienkripsi di peladen sebelum disimpan. Kunci privat terlindungi penuh.",
                    icon_name=ICON_SHIELD_CHECK,
                    variant="blue"
                ),
                unsafe_allow_html=True
            )

            with st.form("form_report_submission"):
                # Step 1
                st.markdown(step_badge(1, "Informasi & Kronologi Kejadian"), unsafe_allow_html=True)
                report_title = st.text_input("Judul / Pokok Laporan", placeholder="Contoh: Dugaan Penyalahgunaan Wewenang Proyek Pengadaan...")
                report_chronology = st.text_area(
                    "Kronologi Lengkap Peristiwa (Teks)",
                    placeholder="Jelaskan secara rinci waktu kejadian, pihak terlibat, lokasi, dan modus operandi...",
                    height=150
                )

                st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)
                
                # Step 2
                st.markdown(step_badge(2, "Pemetaan Algoritma Kriptografis Spesifik"), unsafe_allow_html=True)
                render_cipher_selector()

                st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 1.5rem 0;'>", unsafe_allow_html=True)
                
                # Step 3
                st.markdown(step_badge(3, "Unggah Berkas Bukti Terlampir"), unsafe_allow_html=True)
                st.markdown(
                    "<p style='color: #64748b; font-size: 0.84rem; margin-bottom: 0.85rem;'>Lampirkan 3 jenis berkas pembuktian berikut untuk kelengkapan audit forensik:</p>",
                    unsafe_allow_html=True
                )

                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1:
                    uploaded_ktp = st.file_uploader("1. Scan KTP (JPG/PNG)", type=["jpg", "jpeg", "png"], help="Identitas resmi pelapor [AES-128-CBC]")
                with col_f2:
                    uploaded_doc = st.file_uploader("2. Dokumen Bukti (PDF)", type=["pdf"], help="Dokumen surat atau laporan [AES-128-CBC]")
                with col_f3:
                    uploaded_video = st.file_uploader("3. Video Rekaman (MP4)", type=["mp4"], help="Rekaman video kejadian [RC4 High-Throughput]")

                st.markdown("<div style='margin-top: 1.25rem;'></div>", unsafe_allow_html=True)
                submit_report = st.form_submit_button("Enkripsi Otomatis Sesuai Jenis Data & Kirim", use_container_width=True)

            if submit_report:
                if not report_title.strip() or not report_chronology.strip():
                    st.error("Judul laporan dan narasi kronologi wajib diisi.")
                elif not uploaded_ktp or not uploaded_doc or not uploaded_video:
                    st.warning("Harap lengkapi ketiga jenis berkas bukti (Scan KTP, Dokumen PDF, dan Video MP4) sesuai regulasi audit.")
                else:
                    with st.spinner("Mengenkripsi setiap data dengan algoritma spesifik (AES, DES, RC4) terisolasi..."):
                        try:
                            if not os.path.exists(STORAGE_DIR):
                                os.makedirs(STORAGE_DIR, exist_ok=True)

                            total_bytes = 0

                            # --- PENERAPAN CIPHER SPESIFIK PER JENIS DATA SESUAI PLAN ---
                            # 1. Teks Narasi / Kronologi -> DES-64-CBC (Perbandingan benchmark akademis)
                            # 2. Scan KTP & Dokumen PDF -> AES-128-CBC (Standar tertinggi NIST / data spesifik)
                            # 3. Video Bukti (MP4) -> RC4 (Stream cipher throughput tinggi dengan nonce unik per file)
                            
                            # --- [1] ENKRIPSI KRONOLOGI (DES) ---
                            salt_text = os.urandom(16)
                            key_text = crypto_utils.get_report_key(salt_text, 'DES')
                            chrono_bytes = report_chronology.encode("utf-8")
                            total_bytes += len(chrono_bytes)
                            enc_chrono, text_time = crypto_utils.encrypt_data(chrono_bytes, 'DES', key_text)

                            timestamp_str = str(int(time.time() * 1000))
                            
                            # --- [2] ENKRIPSI KTP (AES) ---
                            salt_ktp = os.urandom(16)
                            key_ktp = crypto_utils.get_report_key(salt_ktp, 'AES')
                            ktp_bytes = uploaded_ktp.read()
                            total_bytes += len(ktp_bytes)
                            enc_ktp, ktp_time = crypto_utils.encrypt_data(ktp_bytes, 'AES', key_ktp)
                            ktp_enc_filename = f"ktp_{timestamp_str}_{os.path.basename(uploaded_ktp.name)}.enc"
                            with open(os.path.join(STORAGE_DIR, ktp_enc_filename), "wb") as f:
                                f.write(enc_ktp)

                            # --- [3] ENKRIPSI DOKUMEN PDF (AES) ---
                            salt_doc = os.urandom(16)
                            key_doc = crypto_utils.get_report_key(salt_doc, 'AES')
                            doc_bytes = uploaded_doc.read()
                            total_bytes += len(doc_bytes)
                            enc_doc, doc_time = crypto_utils.encrypt_data(doc_bytes, 'AES', key_doc)
                            doc_enc_filename = f"doc_{timestamp_str}_{os.path.basename(uploaded_doc.name)}.enc"
                            with open(os.path.join(STORAGE_DIR, doc_enc_filename), "wb") as f:
                                f.write(enc_doc)

                            # --- [4] ENKRIPSI VIDEO MP4 (RC4 dengan Unique Salt per payload untuk keystream isolation) ---
                            salt_video = os.urandom(16)
                            key_video = crypto_utils.get_report_key(salt_video, 'RC4')
                            video_bytes = uploaded_video.read()
                            total_bytes += len(video_bytes)
                            enc_video, video_time = crypto_utils.encrypt_data(video_bytes, 'RC4', key_video)
                            video_enc_filename = f"vid_{timestamp_str}_{os.path.basename(uploaded_video.name)}.enc"
                            with open(os.path.join(STORAGE_DIR, video_enc_filename), "wb") as f:
                                f.write(enc_video)

                            # Master salt gabungan atau salt utama untuk laporan (disimpan salt AES KTP sebagai representatif utama)
                            report_salt = salt_ktp

                            # --- [5] SIMPAN KE DATABASE SQLITE (DENGAN SALT TERISOLASI PER KOMPONEN) ---
                            report_id = database.create_report(
                                user_id=user["id"],
                                title=report_title,
                                chronology_encrypted=enc_chrono,
                                ktp_filename=ktp_enc_filename,
                                doc_filename=doc_enc_filename,
                                video_filename=video_enc_filename,
                                cipher_used="AES-128-CBC / DES-64-CBC / RC4",
                                salt=salt_ktp,
                                salt_text=salt_text,
                                salt_ktp=salt_ktp,
                                salt_doc=salt_doc,
                                salt_video=salt_video
                            )

                            total_time = text_time + ktp_time + doc_time + video_time

                            disp = get_report_disposition(report_id)
                            ticket_code = disp.get("tracking_token", f"WBS-{report_id:05d}")
                            st.success(f"Laporan berhasil dienkripsi dengan pemetaan spesifik (DES Kronologi, AES KTP/Dokumen, RC4 Video). Kode Tiket: {ticket_code}")
                            
                            benchmark_metrics = {
                                "report_id": report_id,
                                "cipher": "AES-128-CBC / DES-64-CBC / RC4",
                                "ticket_code": ticket_code,
                                "text_time": text_time,
                                "ktp_time": ktp_time,
                                "doc_time": doc_time,
                                "video_time": video_time,
                                "total_time": total_time,
                                "total_bytes": total_bytes
                            }
                            render_benchmark_summary(benchmark_metrics)

                        except Exception as e:
                            st.error(f"Terjadi kegagalan saat proses enkripsi/penyimpanan: {str(e)}")

    with tab_history:
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        user_reports = database.get_reports_by_user(user["id"])

        if not user_reports:
            st.info("Anda belum memiliki riwayat pengiriman laporan.")
        else:
            for rep in user_reports:
                disp = get_report_disposition(rep["id"])
                ticket_code = disp.get("tracking_token", f"WBS-{rep['id']:05d}")
                st.markdown(
                    clean_html(f"""
                    <div class="sovereign-card-interactive" style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 1.15rem 1.35rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 2px rgba(11,15,25,0.04);">
                        <div>
                            <div style="font-weight: 700; color: #0b0f19; font-size: 0.98rem; display: flex; align-items: center; gap: 0.45rem;">
                                {icon(ICON_FILE_TEXT, size=18, color="#1d4ed8")}
                                <span>{ticket_code} : {html.escape(rep['title'])}</span>
                            </div>
                            <div style="color: #64748b; font-size: 0.82rem; margin-top: 0.25rem; margin-left: 1.55rem; display: flex; gap: 0.85rem; align-items: center;">
                                <span>Terkirim: {rep['created_at']}</span>
                                <span>•</span>
                                <span class="sovereign-badge badge-primary" style="font-size: 0.72rem; padding: 0.15rem 0.5rem;">{rep['cipher_used']}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            {render_status_badge(disp['status'])}
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )
                with st.expander(f"Detail Progres & Tindak Lanjut : {ticket_code}", expanded=False):
                    st.markdown(
                        render_tracking_timeline(
                            status=disp["status"],
                            created_at=rep["created_at"],
                            updated_at=disp["updated_at"],
                            notes=disp["notes"],
                            decision_number=disp.get("decision_number", ""),
                            verdict_category=disp.get("verdict_category", ""),
                            ticket_code=ticket_code
                        ),
                        unsafe_allow_html=True
                    )
                st.markdown("<div style='margin-bottom: 0.65rem;'></div>", unsafe_allow_html=True)

    # Footer
    st.markdown(render_footer(), unsafe_allow_html=True)
