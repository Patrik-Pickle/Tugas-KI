import streamlit as st
from components.icons import (
    icon,
    ICON_SHIELD_CHECK,
    ICON_SCALE
)
from components.utils import clean_html
from components.sidebar import render_profile_menu

def render_sovereign_header(title="SecureReport", subtitle=None):
    """
    Renders a clean institutional header bar for workspace area:
    - Top-Left: Three-dot Profile Menu
    - Center-Left: Brand Logo & Title (with optional Subtitle)
    - Right: Legal Compliance Badge
    Contains class 'nav-marker' to ensure sticky navbar CSS targets only this component.
    """
    col_menu, col_title, col_badge = st.columns([0.45, 4.4, 1.4])
    
    with col_menu:
        render_profile_menu()
    
    subtitle_html = (
        f'<div style="font-size: 0.78rem; color: #64748b; line-height: 1.35; margin-top: 0.15rem; word-break: break-word;">{subtitle}</div>'
        if subtitle else ""
    )

    with col_title:
        st.markdown(
            clean_html(f"""
            <span class="nav-marker" style="display: none;"></span>
            <div style="display: flex; align-items: center; gap: 0.75rem; min-height: 40px; margin: 0; padding: 0;">
                <div style="display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {icon(ICON_SHIELD_CHECK, size=28, color="#1d4ed8")}
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.25rem; color: #0b0f19; line-height: 1.2; white-space: nowrap;">
                        {title}
                    </div>
                    {subtitle_html}
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    with col_badge:
        st.markdown(
            clean_html(f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; min-height: 40px; margin: 0; padding: 0;">
                <span class="sovereign-badge badge-primary" style="font-size: 0.72rem; white-space: nowrap; display: inline-flex; align-items: center; gap: 0.35rem;">
                    {icon(ICON_SCALE, size=13, color="#1d4ed8")} UU PDP No. 27/2022
                </span>
            </div>
            """),
            unsafe_allow_html=True
        )
