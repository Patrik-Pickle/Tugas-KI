import streamlit as st
from components.icons import (
    icon,
    ICON_SHIELD_CHECK,
    ICON_SCALE
)
from components.utils import clean_html
from components.sidebar import render_profile_menu

def render_sovereign_header(title="SecureReport", subtitle="Layanan Pengaduan Aman & Verifikasi Forensik"):
    """
    Renders a clean institutional header bar for workspace area:
    - Top-Left: Three-dot (⋮) Profile Menu
    - Center-Left: Brand Logo & Title + Subtitle
    - Right: Legal Compliance Badge
    Contains class 'nav-marker' to ensure sticky navbar CSS targets only this component.
    """
    col_menu, col_title, col_badge = st.columns([0.45, 4.2, 1.1])
    
    with col_menu:
        render_profile_menu()
    
    with col_title:
        st.markdown(
            clean_html(f"""
            <span class="nav-marker" style="display: none;"></span>
            <div style="display: flex; align-items: center; gap: 0.75rem; min-height: 40px; margin: 0; padding: 0;">
                <div style="display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {icon(ICON_SHIELD_CHECK, size=28, color="#1d4ed8")}
                </div>
                <div>
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.25rem; color: #0b0f19; line-height: 1.2; white-space: nowrap;">
                        {title}
                    </div>
                    <div style="font-size: 0.76rem; color: #64748b; line-height: 1.3; white-space: nowrap;">
                        {subtitle}
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col_badge:
        st.markdown(
            clean_html(f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; min-height: 40px; margin: 0; padding: 0;">
                <span class="sovereign-badge badge-primary" style="font-size: 0.72rem;">
                    {icon(ICON_SCALE, size=13, color="#1d4ed8")} UU PDP No. 27/2022
                </span>
            </div>
            """),
            unsafe_allow_html=True
        )
