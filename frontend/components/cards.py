import streamlit as st
from components.icons import (
    icon,
    ICON_LOCK,
    ICON_SHIELD_CHECK,
    ICON_ALERT_TRIANGLE,
    ICON_ZAP,
    ICON_CPU,
    ICON_CHECK_CIRCLE,
    ICON_BINARY
)
from components.utils import clean_html

def render_cipher_selector():
    """
    Renders an interactive cipher selection component with Sovereign Trust specifications.
    Uses native SVG vector icons (Zero Emoticons).
    """
    st.markdown(
        clean_html(f"""
        <div style="font-weight: 700; font-size: 0.98rem; color: #0b0f19; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
            {icon(ICON_LOCK, size=18, color="#1d4ed8")}
            <span>Algoritma Kriptografi Pengaman</span>
        </div>
        <p style="color: #64748b; font-size: 0.84rem; margin-bottom: 0.75rem;">
            Pilih standar algoritma cipher yang akan digunakan untuk mengenkripsi teks narasi dan seluruh berkas fisik bukti secara lokal:
        </p>
        """),
        unsafe_allow_html=True
    )

    cipher_options = {
        "AES": {
            "title": "AES-128 (CBC Mode - Standar Tertinggi)",
            "badge": "Direkomendasikan (NIST Standard)",
            "badge_class": "badge-verified",
            "icon_name": ICON_SHIELD_CHECK,
            "desc": "Standar keamanan internasional tertinggi. Enkripsi blok 128-bit dengan Initialization Vector (IV) acak unik dan perlindungan anti-tamper.",
            "color": "#1d4ed8"
        },
        "DES": {
            "title": "DES (CBC Mode - Enkripsi Klasik)",
            "badge": "Komparasi Klasik 64-bit",
            "badge_class": "badge-warning",
            "icon_name": ICON_ALERT_TRIANGLE,
            "desc": "Algoritma klasik 64-bit CBC untuk perbandingan evaluasi komputasi dan benchmark akademis.",
            "color": "#d97706"
        },
        "RC4": {
            "title": "RC4 (ARC4 - Stream Cipher Cepat)",
            "badge": "Throughput Tinggi",
            "badge_class": "badge-primary",
            "icon_name": ICON_ZAP,
            "desc": "Stream cipher berkecepatan tinggi berbasis pseudo-random stream untuk throughput transmisi cepat berkas besar.",
            "color": "#2563eb"
        }
    }
    
    selected_cipher = st.radio(
        "Pilih Cipher:",
        options=list(cipher_options.keys()),
        format_func=lambda x: f"{x} - {cipher_options[x]['title']} ({cipher_options[x]['badge']})",
        index=0,
        horizontal=False,
        label_visibility="collapsed"
    )
    
    info = cipher_options[selected_cipher]
    st.markdown(
        clean_html(f"""
        <div style="background-color: #ffffff; border: 1.5px solid {info['color']}; border-radius: 8px; padding: 0.85rem 1.15rem; margin-top: 0.4rem; box-shadow: 0 1px 3px rgba(11,15,25,0.04);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="font-weight: 700; color: #0b0f19; font-size: 0.92rem; display: flex; align-items: center; gap: 0.4rem;">
                    {icon(info['icon_name'], size=16, color=info['color'])}
                    {info['title']}
                </span>
                <span class="sovereign-badge {info['badge_class']}">{info['badge']}</span>
            </div>
            <div style="color: #64748b; font-size: 0.83rem; margin-top: 0.35rem; line-height: 1.45;">
                {info['desc']}
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    
    return selected_cipher

def render_benchmark_summary(metrics: dict):
    """
    Renders the realtime cryptographic benchmark card according to Sovereign Trust telemetry standards.
    Strictly zero emoticons.
    """
    total_time = metrics.get("total_time", 0.0)
    total_bytes = metrics.get("total_bytes", 0)
    total_mb = total_bytes / (1024 * 1024)
    speed_mb_s = (total_mb / total_time) if total_time > 0 else 0.0

    st.markdown(
        clean_html(f"""
        <div class="sovereign-card" style="border-left: 4px solid #059669; margin-top: 1.25rem; background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #059669; border-radius: 10px; padding: 1.25rem 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <div style="font-weight: 700; font-size: 1.05rem; color: #0b0f19; display: flex; align-items: center; gap: 0.5rem;">
                    {icon(ICON_CPU, size=20, color="#059669")}
                    <span>Telemetri Realtime Benchmark Enkripsi</span>
                </div>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Terenkripsi Sempurna
                </span>
            </div>
            <div style="color: #64748b; font-size: 0.85rem; margin-bottom: 1rem;">
                Data payload dan seluruh lampiran telah diproteksi secara matematis sebelum disimpan ke media permanen.
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 0.75rem; margin-bottom: 1rem;">
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase;">Waktu Teks</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0b0f19; font-size: 1rem;">
                        {metrics.get('text_time', 0.0) * 1000:.3f} ms
                    </div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase;">Waktu KTP</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0b0f19; font-size: 1rem;">
                        {metrics.get('ktp_time', 0.0) * 1000:.3f} ms
                    </div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase;">Waktu PDF</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0b0f19; font-size: 1rem;">
                        {metrics.get('doc_time', 0.0) * 1000:.3f} ms
                    </div>
                </div>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #64748b; text-transform: uppercase;">Waktu Video</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #0b0f19; font-size: 1rem;">
                        {metrics.get('video_time', 0.0) * 1000:.3f} ms
                    </div>
                </div>
                <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #1d4ed8; text-transform: uppercase; font-weight: 600;">Total Waktu</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #1d4ed8; font-size: 1.05rem;">
                        {total_time:.4f} s
                    </div>
                </div>
                <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 0.6rem; text-align: center;">
                    <div style="font-size: 0.72rem; color: #1d4ed8; text-transform: uppercase; font-weight: 600;">Throughput</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #1d4ed8; font-size: 1.05rem;">
                        {speed_mb_s:.2f} MB/s
                    </div>
                </div>
            </div>
            <div style="font-size: 0.8rem; color: #64748b; display: flex; align-items: center; gap: 0.4rem;">
                {icon(ICON_BINARY, size=15, color="#1d4ed8")}
                <span>Tiket ID Laporan: <code style="font-family: 'JetBrains Mono', monospace; color: #1d4ed8; font-weight: 600;">WBS-{metrics.get('report_id', 0):05d}</code> | Cipher Aktif: <b>{metrics.get('cipher', 'N/A')}</b></span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
