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
    Enforces specific data type cipher mapping according to assignment rules:
    - AES-128-CBC for Identity Scan (KTP) & Document (PDF)
    - RC4 for Video Evidence (MP4) with unique nonce/salt isolation
    - DES-64-CBC for Text Narrative (Kronologi) for academic comparison
    """
    st.markdown(
        clean_html(f"""
        <div style="font-weight: 700; font-size: 0.98rem; color: #0b0f19; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.4rem;">
            {icon(ICON_LOCK, size=18, color="#1d4ed8")}
            <span>Pemetaan Otomatis Algoritma Kriptografi Per Jenis Data</span>
        </div>
        <p style="color: #64748b; font-size: 0.84rem; margin-bottom: 0.75rem;">
            Sistem menerapkan standar enkripsi simetris ganda sesuai klasifikasi GDPR / UU PDP No. 27/2022:
        </p>
        """),
        unsafe_allow_html=True
    )

    mapping_info = """
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.85rem 1.15rem; margin-top: 0.4rem; font-size: 0.84rem; color: #334155; line-height: 1.6;">
        <div style="font-weight: 700; color: #0b0f19; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
            {icon_shield}
            <span>Arsitektur Pemetaan Kriptografi Wajib:</span>
        </div>
        <ul style="margin: 0; padding-left: 1.2rem;">
            <li><b>Data Pribadi Spesifik / Identitas (Scan KTP) & Dokumen PDF:</b> Diproteksi menggunakan <b>AES-128-CBC</b> (NIST Standard, anti-ECB dengan Unique IV).</li>
            <li><b>Video Bukti (MP4 - Berukuran Besar):</b> Diproteksi menggunakan <b>RC4</b> (Stream Cipher dengan unique salt/nonce per payload untuk throughput tinggi & zero keystream reuse).</li>
            <li><b>Teks Narasi / Kronologi:</b> Diproteksi menggunakan <b>DES-64-CBC</b> sebagai komparasi benchmark akademis klasik.</li>
        </ul>
    </div>
    """
    st.markdown(clean_html(mapping_info.replace("{icon_shield}", icon(ICON_SHIELD_CHECK, size=16, color="#1d4ed8"))), unsafe_allow_html=True)
    
    # Return a unified mapping indicator or default auto cipher mode
    return "AUTO-MAPPED (AES/DES/RC4)"

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
                <span>Tiket ID Laporan: <code style="font-family: 'JetBrains Mono', monospace; color: #1d4ed8; font-weight: 600;">{metrics.get('ticket_code', '-')}</code> | Cipher Aktif: <b>{metrics.get('cipher', 'N/A')}</b></span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
