import streamlit as st
from components.icons import (
    icon,
    ICON_ID_CARD,
    ICON_FILE_TEXT,
    ICON_VIDEO,
    ICON_DOWNLOAD,
    ICON_CHECK_CIRCLE
)
from components.utils import clean_html

def render_ktp_preview(image_bytes: bytes, original_filename: str):
    """
    Renders decrypted KTP image in a high-trust forensic inspection frame.
    Strictly zero emoticons.
    """
    st.markdown(
        clean_html(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; font-size: 0.9rem; color: #0b0f19; display: flex; align-items: center; gap: 0.4rem;">
                    {icon(ICON_ID_CARD, size=16, color="#1d4ed8")}
                    <span>Scan Identitas KTP: <code>{original_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Didekripsi
                </span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.image(image_bytes, caption=f"Pratinjau KTP Forensik ({original_filename})", use_container_width=True)
    with col2:
        st.download_button(
            label=f"Unduh KTP ({len(image_bytes)/1024:.1f} KB)",
            data=image_bytes,
            file_name=original_filename,
            mime="image/jpeg",
            key=f"dl_ktp_{original_filename}",
            use_container_width=True
        )

import base64
import streamlit as st
from components.icons import icon, ICON_FILE_TEXT, ICON_CHECK_CIRCLE
from components.utils import clean_html

def render_pdf_preview(pdf_bytes: bytes, original_filename: str):
    """
    Renders decrypted PDF document with direct Base64 download link.
    """
    if not original_filename.lower().endswith(".pdf"):
        download_filename = f"{original_filename}.pdf"
    else:
        download_filename = original_filename

    # Encode bytes ke Base64
    b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_size_mb = len(pdf_bytes) / (1024 * 1024)

    # Buat komponen HTML Link Download Langsung
    html_download_button = f"""
    <a href="data:application/pdf;base64,{b64_pdf}" 
       download="{download_filename}" 
       style="
            display: block;
            width: 100%;
            text-align: center;
            background-color: #1d4ed8;
            color: #ffffff;
            padding: 0.6rem 1rem;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.88rem;
            text-decoration: none;
            margin-top: 0.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
       ">
       Unduh Dokumen PDF ({pdf_size_mb:.2f} MB)
    </a>
    """

    st.markdown(
        clean_html(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; font-size: 0.9rem; color: #0b0f19; display: flex; align-items: center; gap: 0.4rem;">
                    {icon(ICON_FILE_TEXT, size=16, color="#1d4ed8")}
                    <span>Dokumen Bukti (PDF): <code>{download_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Didekripsi
                </span>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # Render tombol download buatan HTML murni
    st.markdown(html_download_button, unsafe_allow_html=True)

def render_video_preview(video_bytes: bytes, original_filename: str):
    """
    Renders decrypted MP4 video with embedded HTML5 video player and download button.
    Strictly zero emoticons.
    """
    st.markdown(
        clean_html(f"""
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 600; font-size: 0.9rem; color: #0b0f19; display: flex; align-items: center; gap: 0.4rem;">
                    {icon(ICON_VIDEO, size=16, color="#1d4ed8")}
                    <span>Video Bukti Rekaman (MP4): <code>{original_filename}</code></span>
                </span>
                <span class="sovereign-badge badge-verified">
                    {icon(ICON_CHECK_CIRCLE, size=13, color="#059669")} Didekripsi
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
