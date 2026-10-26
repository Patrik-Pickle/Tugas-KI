"""
frontend/components/previewers.py
Modul Pratinjau Berkas Forensik & Visualisasi Sandi Kriptografis.
Menyediakan inspeksi berkas terenkripsi (Visual Noise Canvas & Telemetri Entropi)
serta pratinjau berkas asli hasil dekripsi (KTP, Dokumen PDF, dan Video MP4).
"""

import base64
import hashlib
import streamlit as st
from components.icons import (
    icon,
    ICON_ID_CARD,
    ICON_FILE_TEXT,
    ICON_VIDEO,
    ICON_DOWNLOAD,
    ICON_CHECK_CIRCLE,
    ICON_LOCK,
    ICON_BINARY,
    ICON_ACTIVITY,
    ICON_SHIELD_CHECK
)
from components.utils import clean_html

def render_ciphertext_card(
    telemetry: dict,
    file_label: str,
    filename: str,
    cipher_used: str,
    is_image: bool = False
):
    """
    Renders an encrypted ciphertext forensic card before decryption:
    - Ciphertext visual static noise raster (Pillow grayscale matrix)
    - Shannon Entropy metric (H ~ 8.00 bits/byte)
    - SHA-256 integrity hash
    - 64-byte hex dump preview
    Strictly avoids emojis and em dashes.
    """
    if not telemetry or not telemetry.get("exists"):
        st.warning(f"Berkas terenkripsi tidak ditemukan di media server: <code>{filename}</code>")
        return

    entropy_val = telemetry.get("entropy", 0.0)
    # Status deskripsi entropi
    if entropy_val >= 7.95:
        entropy_status = "Acak Sempurna (Derau Maksimum / Bebas Kebocoran Pola)"
        entropy_color = "#059669"
    elif entropy_val >= 7.5:
        entropy_status = "Entropi Tinggi (Tingkat Keacakan Kuat)"
        entropy_color = "#1d4ed8"
    else:
        entropy_status = "Entropi Menengah"
        entropy_color = "#d97706"

    st.markdown(
        clean_html(f"""
        <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 0.9rem 1.15rem; margin-bottom: 0.75rem; box-shadow: 0 1px 3px rgba(11,15,25,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.5rem; margin-bottom: 0.75rem;">
                <span style="font-weight: 700; font-size: 0.92rem; color: #0b0f19; display: flex; align-items: center; gap: 0.45rem;">
                    {icon(ICON_LOCK, size=16, color="#1d4ed8")}
                    <span>{file_label}: <code>{filename}</code></span>
                </span>
                <div style="display: flex; gap: 0.45rem; align-items: center;">
                    <span class="sovereign-badge badge-primary" style="font-size: 0.74rem;">
                        Cipher: {cipher_used}
                    </span>
                    <span style="background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 9999px; padding: 0.15rem 0.55rem; font-size: 0.72rem; font-weight: 700;">
                        Ciphertext BLOB
                    </span>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        noise_bytes = telemetry.get("noise_png")
        if noise_bytes:
            caption_text = (
                f"Matriks Piksel Sandi (256x256 Grayscale / Mode {cipher_used}-CBC)"
                if is_image else
                f"Spektrum Sandi Biner (256x256 Raster / {cipher_used})"
            )
            b64_noise = base64.b64encode(noise_bytes).decode('utf-8')
            st.markdown(
                f'<div class="forensic-scanner-container" style="border: 1px solid #cbd5e1; border-radius: 8px; margin-bottom: 0.35rem;"><img src="data:image/png;base64,{b64_noise}" style="width: 100%; display: block; border-radius: 7px;" /></div>',
                unsafe_allow_html=True
            )
            st.caption(caption_text)
            st.caption(
                "Representasi visual byte ciphertext. Korelasi piksel asli hancur lebur menjadi derau putih statis (*pure noise*)."
                if is_image else
                "Pemetaan biner berkas sandi ke matriks visual 2D untuk inspeksi ketiadaan pola teratur."
            )

    with col2:
        st.markdown(
            clean_html(f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1rem; margin-bottom: 0.65rem;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em;">
                    Entropi Informasi Shannon:
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: {entropy_color}; margin-top: 0.15rem;">
                    {entropy_val:.4f} <span style="font-size: 0.8rem; font-weight: 600; color: #64748b;">/ 8.0000 bits per byte</span>
                </div>
                <div style="font-size: 0.78rem; font-weight: 600; color: {entropy_color}; margin-top: 0.2rem;">
                    {entropy_status}
                </div>
            </div>

            <div style="font-size: 0.8rem; color: #475569; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
                <span>Ukuran Berkas Sandi: <b>{telemetry.get('size_kb', 0)} KB</b> ({telemetry.get('size_bytes', 0)} bytes)</span>
            </div>

            <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 0.25rem;">
                Digest Hash Integritas (SHA-256):
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 0.35rem 0.5rem; word-break: break-all; margin-bottom: 0.65rem; color: #0f172a;">
                {telemetry.get('sha256', '-')}
            </div>

            <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 0.25rem;">
                Cuplikan Sandi Heksadesimal (Hex Dump 64-Byte):
            </div>
            <div class="cipher-telemetry-box" style="font-size: 0.75rem; line-height: 1.45; max-height: 75px; overflow-y: auto; background: #0f172a; color: #38bdf8; padding: 0.45rem 0.65rem; border-radius: 6px;">
                {telemetry.get('hex_preview', '')}
            </div>
            """),
            unsafe_allow_html=True
        )

def render_ktp_preview(image_bytes: bytes, original_filename: str):
    """
    Renders decrypted KTP image in a high-trust forensic inspection frame.
    Strictly zero emoticons.
    """
    ktp_size_kb = len(image_bytes) / 1024
    ktp_hash = hashlib.sha256(image_bytes).hexdigest()

    st.markdown(
        clean_html(f"""
        <div class="decrypted-card-reveal sovereign-card-interactive" style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 0.85rem; box-shadow: 0 1px 3px rgba(11,15,25,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.65rem; margin-bottom: 0.85rem;">
                <span style="font-weight: 700; font-size: 0.95rem; color: #0b0f19; display: flex; align-items: center; gap: 0.45rem;">
                    {icon(ICON_ID_CARD, size=18, color="#1d4ed8")}
                    <span>Scan Identitas KTP: <code>{original_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Berhasil Didekripsi
                </span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(image_bytes, caption=f"Pratinjau KTP Forensik ({original_filename})", use_container_width=True)

    with col2:
        st.markdown(
            clean_html(f"""
            <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1.1rem; margin-bottom: 0.75rem;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em;">
                    Status Berkas Forensik KTP:
                </div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #059669; margin-top: 0.2rem;">
                    Plaintext Gambar Valid & Terverifikasi
                </div>
                <div style="margin-top: 0.5rem; font-size: 0.82rem; color: #475569; display: flex; flex-direction: column; gap: 0.35rem;">
                    <div>Ukuran Berkas: <b>{ktp_size_kb:.1f} KB</b> ({len(image_bytes)} bytes)</div>
                    <div>Format: <b>Gambar Identitas Resmi (JPG/PNG)</b></div>
                </div>
            </div>

            <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 0.25rem;">
                Digest Hash Integritas Plaintext (SHA-256):
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 4px; padding: 0.35rem 0.55rem; color: #0f172a; word-break: break-all; margin-bottom: 0.85rem;">
                {ktp_hash}
            </div>
            """),
            unsafe_allow_html=True
        )
        st.download_button(
            label=f"Unduh Gambar KTP ({ktp_size_kb:.1f} KB)",
            data=image_bytes,
            file_name=original_filename,
            mime="image/jpeg",
            key=f"dl_ktp_{original_filename}",
            use_container_width=True
        )

def render_pdf_preview(pdf_bytes: bytes, original_filename: str):
    """
    Renders decrypted PDF document with document details, SHA-256 integrity hash,
    embedded iframe reader, and direct Base64 download button.
    """
    if not original_filename.lower().endswith(".pdf"):
        download_filename = f"{original_filename}.pdf"
    else:
        download_filename = original_filename

    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_size_kb = len(pdf_bytes) / 1024
    pdf_size_mb = pdf_size_kb / 1024
    pdf_hash = hashlib.sha256(pdf_bytes).hexdigest()

    st.markdown(
        clean_html(f"""
        <div class="decrypted-card-reveal sovereign-card-interactive" style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 0.75rem; box-shadow: 0 1px 3px rgba(11,15,25,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.65rem; margin-bottom: 0.75rem;">
                <span style="font-weight: 700; font-size: 0.95rem; color: #0b0f19; display: flex; align-items: center; gap: 0.45rem;">
                    {icon(ICON_FILE_TEXT, size=18, color="#1d4ed8")}
                    <span>Dokumen Bukti (PDF): <code>{download_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Berhasil Didekripsi
                </span>
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; font-size: 0.82rem; color: #475569; margin-bottom: 0.75rem;">
                <div>Format: <b>PDF / Dokumen Bukti</b></div>
                <div>Ukuran: <b>{pdf_size_kb:.1f} KB</b> ({pdf_size_mb:.2f} MB)</div>
                <div>Status: <b>Plaintext Valid</b></div>
            </div>
            <div style="font-size: 0.72rem; color: #64748b; font-weight: 700; text-transform: uppercase; margin-bottom: 0.25rem;">
                SHA-256 Integritas Berkas Hasil Dekripsi:
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 0.35rem 0.65rem; color: #0f172a; word-break: break-all; margin-bottom: 0.85rem;">
                {pdf_hash}
            </div>
            <div style="display: flex; gap: 0.75rem; align-items: center;">
                <a href="data:application/pdf;base64,{b64_pdf}" download="{download_filename}" style="display: inline-flex; align-items: center; justify-content: center; background-color: #1d4ed8; color: #ffffff; padding: 0.55rem 1.25rem; border-radius: 6px; font-weight: 600; font-size: 0.85rem; text-decoration: none; box-shadow: 0 1px 2px rgba(0,0,0,0.05);">
                    Unduh Dokumen PDF ({pdf_size_kb:.1f} KB)
                </a>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    with st.expander(f"Pratinjau Lembar Dokumen PDF Terbuka ({download_filename})", expanded=True):
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=0" width="100%" height="480px" style="border: 1px solid #cbd5e1; border-radius: 6px;"></iframe>',
            unsafe_allow_html=True
        )

def render_video_preview(video_bytes: bytes, original_filename: str):
    """
    Renders decrypted MP4 video with embedded HTML5 video player and download button.
    Strictly zero emoticons.
    """
    st.markdown(
        clean_html(f"""
        <div class="decrypted-card-reveal sovereign-card-interactive" style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; font-size: 0.9rem; color: #0b0f19; display: flex; align-items: center; gap: 0.4rem;">
                    {icon(ICON_VIDEO, size=16, color="#1d4ed8")}
                    <span>Video Bukti Rekaman (MP4): <code>{original_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Berhasil Didekripsi
                </span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    st.video(video_bytes)
    st.download_button(
        label=f"Unduh Video Bukti ({len(video_bytes)/(1024*1024):.2f} MB)",
        data=video_bytes,
        file_name=original_filename,
        mime="video/mp4",
        key=f"dl_video_{original_filename}",
        use_container_width=True
    )
