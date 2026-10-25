import streamlit as st
import database
from components.icons import (
    icon,
    ICON_SCALE,
    ICON_SHIELD_CHECK,
    ICON_LOCK,
    ICON_USER,
    ICON_USER_CHECK,
    ICON_CHECK_CIRCLE,
    ICON_KEY,
    ICON_FILE_TEXT
)
from components.utils import clean_html
from components.sidebar import render_profile_menu

def render_auth_view():
    """
    Renders a modern split-screen (two-column) authentication page inspired by
    premium modern SaaS & Sovereign Trust designs:
    Left: Interactive Auth Form (Login Pelapor, Register Pelapor, Login Investigator)
    Right: Rich Institutional Hero Panel with security guarantees, encryption metrics, and legal compliance.
    """
    # 1. Minimal Header Bar with three-dot profile menu (Top-Left)
    col_menu, nav_col1, nav_col2 = st.columns([0.45, 4.0, 1.2])
    with col_menu:
        render_profile_menu()
    with nav_col1:
        st.markdown(
            clean_html(f"""
            <span class="nav-marker" style="display: none;"></span>
            <div style="display: flex; align-items: center; gap: 0.65rem; height: 40px; margin: 0; padding: 0;">
                <div style="display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {icon(ICON_SHIELD_CHECK, size=28, color="#1d4ed8")}
                </div>
                <span style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.25rem; color: #0b0f19; letter-spacing: -0.01em; line-height: 1; vertical-align: middle;">SecureReport</span>
            </div>
            """),
            unsafe_allow_html=True
        )
    with nav_col2:
        if st.button("Kembali ke Beranda", key="auth_nav_home", type="secondary", use_container_width=True):
            st.session_state.current_page = "landing"
            st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 2. Split Screen Two-Column Layout (Left: Form ~48%, Right: Hero Showcase ~52%)
    col_form, col_showcase = st.columns([1.1, 1.2], gap="large")

    with col_form:
        # Pre-select portal based on session state
        default_portal = st.session_state.get("auth_default_tab", "pelapor")
        portal_index = 1 if default_portal == "investigator" else 0

        st.markdown(
            clean_html(f"""
            <div style="margin-bottom: 1.25rem;">
                <h1 style="font-family: 'Merriweather', serif; font-size: 1.85rem; font-weight: 700; color: #0b0f19; margin: 0 0 0.35rem 0;">
                    Selamat Datang
                </h1>
                <p style="color: #64748b; font-size: 0.92rem; margin: 0; line-height: 1.5;">
                    Pilih portal akses sesuai dengan peran Anda untuk mengakses ruang kerja terenkripsi.
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )

        portal_choice = st.radio(
            "Pilih Portal Akses",
            ["Portal Pelapor Pengaduan", "Portal Petugas Investigasi"],
            index=portal_index,
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-bottom: 0.75rem;'></div>", unsafe_allow_html=True)

        if portal_choice == "Portal Pelapor Pengaduan":
            st.markdown(
                clean_html(f"""
                <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 0.65rem 0.85rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.45rem;">
                    {icon(ICON_CHECK_CIRCLE, size=16, color="#1d4ed8")}
                    <span style="font-size: 0.82rem; color: #1e40af; line-height: 1.4;">
                        <b>Jaminan Anonimitas:</b> Identitas dan berkas bukti terlindungi mutlak di bawah UU PDP No. 27/2022.
                    </span>
                </div>
                """),
                unsafe_allow_html=True
            )

            pelapor_mode = st.radio(
                "Pilih Tindakan",
                ["Masuk Akun", "Daftar Akun Baru"],
                horizontal=True
            )

            if pelapor_mode == "Masuk Akun":
                with st.form("form_login_pelapor"):
                    st.markdown("<div style='font-weight: 700; color: #0b0f19; font-size: 0.95rem; margin-bottom: 0.5rem;'>Autentikasi Akun Pelapor</div>", unsafe_allow_html=True)
                    username = st.text_input("Username Pelapor", placeholder="Masukkan username Anda...")
                    password = st.text_input("Kata Sandi", type="password", placeholder="Masukkan kata sandi...")
                    submit_login = st.form_submit_button("Masuk ke Ruang Pengaduan", use_container_width=True)

                    if submit_login:
                        if not username or not password:
                            st.error("Harap isi username dan kata sandi.")
                        else:
                            user = database.authenticate_user(username, password)
                            if user and user.get("role") == "pelapor":
                                st.session_state.user = user
                                st.success(f"Otentikasi berhasil. Selamat datang, {user['username']}!")
                                st.rerun()
                            elif user and user.get("role") != "pelapor":
                                st.warning("Akun ini terdaftar sebagai peran Petugas. Silakan beralih ke Portal Petugas Investigasi.")
                            else:
                                st.error("Username atau kata sandi tidak valid.")

            else: # Registrasi Akun Baru
                with st.form("form_register_pelapor"):
                    st.markdown("<div style='font-weight: 700; color: #0b0f19; font-size: 0.95rem; margin-bottom: 0.5rem;'>Registrasi Akun Pelapor Baru</div>", unsafe_allow_html=True)
                    reg_username = st.text_input("Username Baru", placeholder="Buat username unik...")
                    reg_password = st.text_input("Kata Sandi", type="password", placeholder="Minimal 6 karakter...")
                    reg_confirm = st.text_input("Konfirmasi Kata Sandi", type="password", placeholder="Ulangi kata sandi...")
                    submit_reg = st.form_submit_button("Daftarkan Akun Pelapor", use_container_width=True)

                    if submit_reg:
                        if not reg_username or not reg_password:
                            st.error("Username dan kata sandi wajib diisi.")
                        elif len(reg_password) < 6:
                            st.warning("Kata sandi minimal 6 karakter.")
                        elif reg_password != reg_confirm:
                            st.error("Konfirmasi kata sandi tidak cocok.")
                        else:
                            success, message = database.register_user(reg_username, reg_password, role="pelapor")
                            if success:
                                st.success("Akun berhasil dibuat. Mengotentikasi sesi Anda...")
                                user = database.authenticate_user(reg_username, reg_password)
                                st.session_state.user = user
                                st.rerun()
                            else:
                                st.error(f"Gagal: {message}")

        else: # Portal Petugas Investigasi
            st.markdown(
                clean_html(f"""
                <div style="background-color: #ecfdf5; border: 1px solid #a7f3d0; border-radius: 8px; padding: 0.65rem 0.85rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.45rem;">
                    {icon(ICON_LOCK, size=16, color="#047857")}
                    <span style="font-size: 0.82rem; color: #065f46; line-height: 1.4;">
                        <b>Akses Forensik Terbatas:</b> Khusus Tim Pemeriksa & Verifikator Hukum Resmi.
                    </span>
                </div>
                """),
                unsafe_allow_html=True
            )

            with st.form("form_login_investigator"):
                st.markdown("<div style='font-weight: 700; color: #0b0f19; font-size: 0.95rem; margin-bottom: 0.5rem;'>Autentikasi Petugas Forensik</div>", unsafe_allow_html=True)
                inv_username = st.text_input("ID Petugas", placeholder="admin_investigator")
                inv_password = st.text_input("Kunci Akses Forensik", type="password", placeholder="••••••••")
                submit_inv = st.form_submit_button("Otorisasi & Masuk Portal", use_container_width=True)

                if submit_inv:
                    if not inv_username or not inv_password:
                        st.error("Harap isi ID Petugas dan Kunci Akses.")
                    else:
                        user = database.authenticate_user(inv_username, inv_password)
                        if user and user.get("role") == "investigator":
                            st.session_state.user = user
                            st.success("Otorisasi petugas berhasil diverifikasi. Membuka portal pemeriksaan...")
                            st.rerun()
                        else:
                            st.error("Akses ditolak: Kredensial tidak valid atau akun bukan petugas resmi.")

    with col_showcase:
        # Right Column Showcase Card (Focused on Public Protection & Legal Guarantees, clean layout without trailing status badges)
        st.markdown(
            clean_html(f"""
            <div class="auth-showcase-box" style="background: linear-gradient(145deg, #1d4ed8 0%, #1e3a8a 100%); border-radius: 18px; padding: 2.25rem 2.25rem; color: #ffffff !important; box-shadow: 0 10px 25px -5px rgba(29,78,216,0.3); height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.25rem;">
                        <div style="display: inline-flex; align-items: center; gap: 0.5rem;">
                            {icon(ICON_SHIELD_CHECK, size=22, color="#ffffff")}
                            <span style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.2rem; color: #ffffff !important; letter-spacing: -0.01em;">SecureReport</span>
                        </div>
                        <div style="display: inline-flex; align-items: center; gap: 0.35rem; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); border-radius: 9999px; padding: 0.25rem 0.7rem; font-size: 0.75rem; font-weight: 600; color: #ffffff !important;">
                            <span style="color: #ffffff !important;">Layanan Pengaduan Resmi</span>
                        </div>
                    </div>
                    <div style="font-family: 'Merriweather', serif; font-size: 1.7rem; font-weight: 700; line-height: 1.35; color: #ffffff !important; margin: 0 0 0.85rem 0;">
                        Kerahasiaan Identitas dan Perlindungan Pelapor.
                    </div>
                    <p style="font-size: 0.92rem; color: #ffffff !important; opacity: 0.92; line-height: 1.6; margin: 0 0 1.75rem 0;">
                        Platform terintegrasi yang menjamin keamanan pelapor dalam menyampaikan dugaan pelanggaran secara aman, akuntabel, dan terlindungi penuh oleh regulasi hukum.
                    </p>

                    <!-- Feature Guarantee Cards (Clean icon + title + subtitle without trailing pills) -->
                    <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-bottom: 1.5rem;">
                        <div style="background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 10px; padding: 0.85rem 1.15rem; display: flex; align-items: center; gap: 0.75rem; backdrop-filter: blur(8px);">
                            <div style="width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                {icon(ICON_USER_CHECK, size=18, color="#ffffff")}
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #ffffff !important; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.03em;">Anonimitas & Kerahasiaan</div>
                                <div style="font-size: 0.92rem; font-weight: 700; color: #ffffff !important;">Identitas Pelapor Dilindungi Penuh</div>
                            </div>
                        </div>

                        <div style="background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 10px; padding: 0.85rem 1.15rem; display: flex; align-items: center; gap: 0.75rem; backdrop-filter: blur(8px);">
                            <div style="width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                {icon(ICON_SCALE, size=18, color="#ffffff")}
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #ffffff !important; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.03em;">Landasan Hukum Resmi</div>
                                <div style="font-size: 0.92rem; font-weight: 700; color: #ffffff !important;">UU PDP No. 27 Tahun 2022</div>
                            </div>
                        </div>

                        <div style="background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.18); border-radius: 10px; padding: 0.85rem 1.15rem; display: flex; align-items: center; gap: 0.75rem; backdrop-filter: blur(8px);">
                            <div style="width: 34px; height: 34px; border-radius: 8px; background: rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                                {icon(ICON_FILE_TEXT, size=18, color="#ffffff")}
                            </div>
                            <div>
                                <div style="font-size: 0.75rem; color: #ffffff !important; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.03em;">Penanganan Kasus</div>
                                <div style="font-size: 0.92rem; font-weight: 700; color: #ffffff !important;">Pemeriksaan Profesional & Akuntabel</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style="padding-top: 1.25rem; border-top: 1px solid rgba(255, 255, 255, 0.2); font-size: 0.8rem; color: #ffffff !important; display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #ffffff !important;">Hak Cipta 2026 SecureReport</span>
                    <span style="color: #ffffff !important;">Kerahasiaan Terjamin 100%</span>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

