import streamlit as st
from components.icons import (
    icon,
    ICON_USER
)
from components.utils import clean_html

def render_profile_menu():
    """
    Renders the three-dot (vertical ellipsis) popover menu in the top-left of the navbar.
    Contains strictly:
    1. User Profile (Avatar, Username, ID)
    2. Role User (Petugas Investigator / Pelapor Resmi / Tamu Publik)
    3. Logout button (Keluar dari Sesi) / Login button
    """
    user = st.session_state.get("user")

    with st.popover("⋮", help="Menu Profil"):
        if not user:
            st.markdown(
                clean_html(f"""
                <div style="text-align: center; padding: 0.5rem 0.25rem 0.75rem 0.25rem;">
                    <div style="width: 52px; height: 52px; border-radius: 50%; background-color: #f1f5f9; border: 1.5px solid #cbd5e1; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 0.65rem;">
                        {icon(ICON_USER, size=26, color="#64748b")}
                    </div>
                    <div style="font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.25rem;">
                        Tamu Publik
                    </div>
                    <div style="display: inline-block; background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.6rem; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.04em;">
                        Belum Masuk
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("Masuk Akun", key="popover_btn_login", type="primary", use_container_width=True):
                st.session_state.current_page = "auth"
                st.session_state.auth_default_tab = "pelapor"
                st.rerun()
        else:
            role = user.get("role", "pelapor")
            is_investigator = role == "investigator"
            username = user.get("username", "Pengguna")
            user_id = user.get("id", "-")

            if is_investigator:
                role_label = "Petugas Investigator"
                avatar_bg = "#ecfdf5"
                avatar_border = "#a7f3d0"
                avatar_color = "#047857"
                badge_bg = "#ecfdf5"
                badge_color = "#047857"
                badge_border = "#a7f3d0"
                user_code = f"INV-{user_id}"
            else:
                role_label = "Pelapor Resmi"
                avatar_bg = "#eff6ff"
                avatar_border = "#bfdbfe"
                avatar_color = "#1d4ed8"
                badge_bg = "#eff6ff"
                badge_color = "#1d4ed8"
                badge_border = "#bfdbfe"
                user_code = f"PEL-{user_id}"

            st.markdown(
                clean_html(f"""
                <div style="text-align: center; padding: 0.5rem 0.25rem 0.75rem 0.25rem;">
                    <div style="width: 52px; height: 52px; border-radius: 50%; background-color: {avatar_bg}; border: 1.5px solid {avatar_border}; display: inline-flex; align-items: center; justify-content: center; margin-bottom: 0.65rem;">
                        {icon(ICON_USER, size=26, color=avatar_color)}
                    </div>
                    <div style="font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.25rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                        {username}
                    </div>
                    <div style="display: inline-block; background-color: {badge_bg}; color: {badge_color}; border: 1px solid {badge_border}; font-size: 0.72rem; font-weight: 700; padding: 0.15rem 0.6rem; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.5rem;">
                        {role_label}
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b;">
                        ID: #{user_code}
                    </div>
                </div>
                """),
                unsafe_allow_html=True
            )
            st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
            if st.button("Keluar dari Sesi", key="popover_btn_logout", type="secondary", use_container_width=True):
                st.session_state.user = None
                st.session_state.current_page = "landing"
                st.rerun()

def render_sovereign_sidebar():
    """
    Deprecated placeholder to prevent import errors.
    Profile and actions now reside in render_profile_menu().
    """
    pass
