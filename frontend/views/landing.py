import streamlit as st
from components.icons import (
    icon,
    ICON_SHIELD_CHECK,
    ICON_LOCK,
    ICON_FILE_TEXT,
    ICON_ID_CARD,
    ICON_KEY,
    ICON_CHECK_CIRCLE,
    ICON_SCALE,
    ICON_USER_CHECK,
    ICON_ARROW_RIGHT
)
from components.utils import clean_html
from components.footer import render_footer
from components.sidebar import render_profile_menu

def render_landing_view():
    """
    Renders Layar 0: Public Landing Page for SecureReport.
    Refined architectural layout: scoped sticky navbar with top-left profile menu,
    top-aligned hero, consistent rhythmic card grids, closing call-to-action banner, and formal footer.
    """

    # 1. Sticky Navigation Bar with three-dot profile menu (Top-Left)
    col_menu, col_brand, nav_col_links, nav_col_btn1, nav_col_btn2 = st.columns([0.45, 1.6, 3.6, 0.9, 0.9])

    with col_menu:
        render_profile_menu()

    with col_brand:
        st.markdown(
            clean_html(f"""
            <span class="nav-marker" style="display: none;"></span>
            <div style="display: flex; align-items: center; gap: 0.65rem; height: 40px; margin: 0; padding: 0;">
                <div style="display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    {icon(ICON_SHIELD_CHECK, size=26, color="#1d4ed8")}
                </div>
                <span style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.22rem; color: #0b0f19; letter-spacing: -0.01em; line-height: 1; vertical-align: middle;">SecureReport</span>
            </div>
            """),
            unsafe_allow_html=True
        )

    with nav_col_links:
        st.markdown(
            clean_html("""
            <div style="display: flex; align-items: center; justify-content: center; gap: 1.6rem; height: 40px; margin: 0; padding: 0;">
                <a href="#hero" class="sovereign-nav-link">Beranda</a>
                <a href="#keunggulan" class="sovereign-nav-link">Keunggulan</a>
                <a href="#alur-pengaduan" class="sovereign-nav-link">Alur Pengaduan</a>
                <a href="#bantuan" class="sovereign-nav-link">Bantuan</a>
            </div>
            """),
            unsafe_allow_html=True
        )

    with nav_col_btn1:
        if st.button("Masuk Petugas", key="nav_btn_petugas", type="secondary", use_container_width=True):
            st.session_state.auth_default_tab = "investigator"
            st.session_state.current_page = "auth"
            st.rerun()

    with nav_col_btn2:
        if st.button("Buat Pengaduan", key="nav_btn_lapor", type="primary", use_container_width=True):
            st.session_state.auth_default_tab = "pelapor"
            st.session_state.current_page = "auth"
            st.rerun()

    st.markdown("<div id='hero' style='scroll-margin-top: 5rem;'></div>", unsafe_allow_html=True)

    # 2. Hero Section (Aligned top-to-bottom with 2 balanced columns)
    col_hero_text, col_hero_card = st.columns([1.35, 1])

    with col_hero_text:
        st.markdown(
            clean_html(f"""
            <div style="margin-bottom: 1.25rem;">
                <div style="display: inline-flex; align-items: center; gap: 0.45rem; background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 9999px; padding: 0.25rem 0.75rem; margin-bottom: 1rem;">
                    {icon(ICON_SCALE, size=14, color="#1d4ed8")}
                    <span style="font-size: 0.76rem; font-weight: 600; color: #1d4ed8;">Kepatuhan UU PDP No. 27/2022</span>
                </div>
                <h1 style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 2.25rem; line-height: 1.25; color: #0b0f19; margin-top: 0; margin-bottom: 1rem;">
                    Sampaikan Laporan Anda dengan Jaminan Kerahasiaan Penuh.
                </h1>
                <p style="font-size: 1rem; color: #4b5563; line-height: 1.6; margin-bottom: 1.5rem;">
                    Platform whistleblowing system resmi untuk menciptakan lingkungan yang bersih dan berintegritas. Identitas Anda, kronologi kejadian, serta seluruh berkas bukti dilindungi secara otomatis dengan standar enkripsi terverifikasi.
                </p>
            </div>
            """),
            unsafe_allow_html=True
        )

        btn_c1, btn_c2, _ = st.columns([1.1, 1.2, 0.7])
        with btn_c1:
            if st.button("Mulai Buat Pengaduan", key="hero_cta_lapor", type="primary", use_container_width=True):
                st.session_state.auth_default_tab = "pelapor"
                st.session_state.current_page = "auth"
                st.rerun()
        with btn_c2:
            if st.button("Portal Petugas Investigasi", key="hero_cta_inv", type="secondary", use_container_width=True):
                st.session_state.auth_default_tab = "investigator"
                st.session_state.current_page = "auth"
                st.rerun()

    with col_hero_card:
        # Hero Assurance Card
        st.markdown(
            clean_html(f"""
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.5rem 1.75rem; box-shadow: 0 4px 6px -1px rgba(11,15,25,0.05);">
                <div style="font-weight: 700; font-size: 1.05rem; color: #0b0f19; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                    {icon(ICON_SHIELD_CHECK, size=22, color="#1d4ed8")}
                    <span>Jaminan dan Komitmen Layanan</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 0.86rem; color: #334155;">Kerahasiaan Identitas</span>
                        <span class="sovereign-badge badge-verified">{icon(ICON_CHECK_CIRCLE, size=14, color="#059669")} Dijamin 100%</span>
                    </div>
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 0.86rem; color: #334155;">Perlindungan Berkas Bukti</span>
                        <span class="sovereign-badge badge-primary">{icon(ICON_LOCK, size=14, color="#1d4ed8")} Terkunci Aman</span>
                    </div>
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; display: flex; align-items: center; justify-content: space-between;">
                        <span style="font-size: 0.86rem; color: #334155;">Payung Hukum Resmi</span>
                        <span class="sovereign-badge badge-verified">{icon(ICON_SCALE, size=14, color="#059669")} UU PDP No. 27/2022</span>
                    </div>
                    <div style="background-color: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 0.85rem 1rem; font-size: 0.82rem; color: #1e40af; line-height: 1.45; display: flex; align-items: center; gap: 0.55rem;">
                        {icon(ICON_USER_CHECK, size=18, color="#1d4ed8")}
                        <span>Laporan hanya dapat dibuka dan ditelaah oleh tim pemeriksa resmi yang memiliki wewenang hukum.</span>
                    </div>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    st.markdown("<div style='margin-top: 3.5rem;'></div><div id='keunggulan' style='scroll-margin-top: 5rem;'></div>", unsafe_allow_html=True)

    # 3. Bagian Nilai Manfaat Utama
    st.markdown(
        clean_html(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-family: 'Merriweather', serif; font-size: 1.65rem; color: #0b0f19; margin-bottom: 0.35rem;">
                Mengapa Memilih SecureReport?
            </h2>
            <p style="color: #64748b; font-size: 0.92rem; max-width: 680px; margin: 0 auto;">
                Tiga keunggulan utama yang memastikan kenyamanan, keamanan, dan kepastian tindak lanjut bagi setiap pelapor.
            </p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; align-items: stretch;">
            <!-- Card 1 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-top: 4px solid #1d4ed8; border-radius: 12px; padding: 1.75rem 1.5rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
                <div>
                    <div style="font-weight: 700; font-size: 1.15rem; color: #0b0f19; margin-bottom: 0.65rem; display: flex; align-items: center; gap: 0.5rem;">
                        {icon(ICON_USER_CHECK, size=24, color="#1d4ed8")}
                        <span>Identitas Dijamin Rahasia</span>
                    </div>
                    <p style="font-size: 0.88rem; color: #4b5563; line-height: 1.6; margin-bottom: 1.25rem;">
                        Identitas pribadi Anda disamarkan secara otomatis sehingga tidak dapat dibaca oleh pihak lain. Anda dapat menyampaikan laporan secara tenang tanpa khawatir terhadap ancaman atau intimidasi.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: #1d4ed8; font-weight: 600; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.35rem;">
                    {icon(ICON_CHECK_CIRCLE, size=15, color="#1d4ed8")}
                    <span>Bebas rasa takut dan terlindungi secara hukum.</span>
                </div>
            </div>

            <!-- Card 2 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-top: 4px solid #059669; border-radius: 12px; padding: 1.75rem 1.5rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
                <div>
                    <div style="font-weight: 700; font-size: 1.15rem; color: #0b0f19; margin-bottom: 0.65rem; display: flex; align-items: center; gap: 0.5rem;">
                        {icon(ICON_LOCK, size=24, color="#059669")}
                        <span>Berkas Bukti Terkunci Aman</span>
                    </div>
                    <p style="font-size: 0.88rem; color: #4b5563; line-height: 1.6; margin-bottom: 1.25rem;">
                        Seluruh dokumen pembuktian seperti foto identitas, berkas pendukung, dan rekaman video dikunci dalam format terenkripsi sehingga tidak ada risiko kebocoran data di peladen.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: #059669; font-weight: 600; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.35rem;">
                    {icon(ICON_CHECK_CIRCLE, size=15, color="#059669")}
                    <span>Hanya dapat dibuka dalam ruang pemeriksaan resmi.</span>
                </div>
            </div>

            <!-- Card 3 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-top: 4px solid #2563eb; border-radius: 12px; padding: 1.75rem 1.5rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
                <div>
                    <div style="font-weight: 700; font-size: 1.15rem; color: #0b0f19; margin-bottom: 0.65rem; display: flex; align-items: center; gap: 0.5rem;">
                        {icon(ICON_KEY, size=24, color="#2563eb")}
                        <span>Nomor Tiket Pemantauan</span>
                    </div>
                    <p style="font-size: 0.88rem; color: #4b5563; line-height: 1.6; margin-bottom: 1.25rem;">
                        Setelah mengirimkan laporan, Anda akan menerima nomor tiket unik. Kode ini dapat Anda gunakan untuk memantau status perkembangan kasus tanpa perlu mengungkap data pribadi Anda.
                    </p>
                </div>
                <div style="font-size: 0.8rem; color: #2563eb; font-weight: 600; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.35rem;">
                    {icon(ICON_CHECK_CIRCLE, size=15, color="#2563eb")}
                    <span>Transparan, akuntabel, dan tetap rahasia.</span>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 3.5rem;'></div><div id='alur-pengaduan' style='scroll-margin-top: 5rem;'></div>", unsafe_allow_html=True)

    # 4. Alur 4 Langkah Mudah bagi Pelapor
    st.markdown(
        clean_html(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="font-family: 'Merriweather', serif; font-size: 1.65rem; color: #0b0f19; margin-bottom: 0.35rem;">
                Alur Mudah Menyampaikan Pengaduan
            </h2>
            <p style="color: #64748b; font-size: 0.92rem;">
                Empat langkah cepat dari pengisian laporan hingga penanganan oleh tim petugas resmi.
            </p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.25rem; align-items: stretch;">
            <!-- Step 1 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.5rem 1.25rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 220px;">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 6px; padding: 0.2rem 0.55rem; letter-spacing: 0.05em;">
                            LANGKAH 01
                        </span>
                        <div style="width: 38px; height: 38px; border-radius: 8px; background-color: #eff6ff; border: 1px solid #bfdbfe; display: flex; align-items: center; justify-content: center;">
                            {icon(ICON_FILE_TEXT, size=20, color="#1d4ed8")}
                        </div>
                    </div>
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.5rem;">
                        Isi Kronologi
                    </div>
                    <p style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0;">
                        Tuliskan rincian kejadian dan pihak yang terlibat secara jelas pada formulir pengaduan.
                    </p>
                </div>
                <div style="margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 600; color: #1d4ed8;">
                    {icon(ICON_CHECK_CIRCLE, size=14, color="#1d4ed8")}
                    <span>Formulir Terenkripsi</span>
                </div>
            </div>

            <!-- Step 2 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.5rem 1.25rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 220px;">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 6px; padding: 0.2rem 0.55rem; letter-spacing: 0.05em;">
                            LANGKAH 02
                        </span>
                        <div style="width: 38px; height: 38px; border-radius: 8px; background-color: #eff6ff; border: 1px solid #bfdbfe; display: flex; align-items: center; justify-content: center;">
                            {icon(ICON_ID_CARD, size=20, color="#1d4ed8")}
                        </div>
                    </div>
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.5rem;">
                        Unggah Bukti
                    </div>
                    <p style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0;">
                        Lampirkan foto identitas, dokumen pendukung, dan rekaman video yang relevan secara aman.
                    </p>
                </div>
                <div style="margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 600; color: #1d4ed8;">
                    {icon(ICON_CHECK_CIRCLE, size=14, color="#1d4ed8")}
                    <span>KTP, PDF & Video Aman</span>
                </div>
            </div>

            <!-- Step 3 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.5rem 1.25rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 220px;">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 6px; padding: 0.2rem 0.55rem; letter-spacing: 0.05em;">
                            LANGKAH 03
                        </span>
                        <div style="width: 38px; height: 38px; border-radius: 8px; background-color: #eff6ff; border: 1px solid #bfdbfe; display: flex; align-items: center; justify-content: center;">
                            {icon(ICON_KEY, size=20, color="#1d4ed8")}
                        </div>
                    </div>
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.5rem;">
                        Dapatkan Tiket CSPRNG
                    </div>
                    <p style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0;">
                        Simpan kode tiket kriptografis berentropi tinggi yang diterbitkan sistem untuk identitas pengaduan Anda.
                    </p>
                </div>
                <div style="margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 600; color: #1d4ed8;">
                    {icon(ICON_CHECK_CIRCLE, size=14, color="#1d4ed8")}
                    <span>Kode Kriptografis Unik</span>
                </div>
            </div>

            <!-- Step 4 -->
            <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.5rem 1.25rem; box-shadow: 0 1px 3px rgba(11, 15, 25, 0.05); display: flex; flex-direction: column; justify-content: space-between; height: 100%; min-height: 220px;">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; background-color: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; border-radius: 6px; padding: 0.2rem 0.55rem; letter-spacing: 0.05em;">
                            LANGKAH 04
                        </span>
                        <div style="width: 38px; height: 38px; border-radius: 8px; background-color: #eff6ff; border: 1px solid #bfdbfe; display: flex; align-items: center; justify-content: center;">
                            {icon(ICON_SHIELD_CHECK, size=20, color="#1d4ed8")}
                        </div>
                    </div>
                    <div style="font-family: 'Merriweather', serif; font-weight: 700; color: #0b0f19; font-size: 1.05rem; margin-bottom: 0.5rem;">
                        Pantau di Portal Pelapor
                    </div>
                    <p style="font-size: 0.85rem; color: #475569; line-height: 1.6; margin: 0;">
                        Masuk ke akun Anda untuk meninjau perkembangan investigasi dan amar putusan resmi secara privat dan terenkripsi.
                    </p>
                </div>
                <div style="margin-top: 1.25rem; padding-top: 0.75rem; border-top: 1px solid #f1f5f9; display: flex; align-items: center; gap: 0.4rem; font-size: 0.78rem; font-weight: 600; color: #1d4ed8;">
                    {icon(ICON_CHECK_CIRCLE, size=14, color="#1d4ed8")}
                    <span>Pelacakan Terotentikasi</span>
                </div>
            </div>
        </div>
        """),
        unsafe_allow_html=True
    )

    # 5. Closing CTA Section with generous vertical rhythm
    st.markdown("<div style='margin-top: 4.5rem;'></div><div id='dasar-hukum' style='scroll-margin-top: 5rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        clean_html(f"""
        <div style="background-color: #ffffff; border: 1.5px solid #e2e8f0; border-top: 4px solid #1d4ed8; border-radius: 14px; padding: 2.5rem 2.25rem 2rem 2.25rem; text-align: center; box-shadow: 0 1px 3px rgba(11,15,25,0.04); margin-bottom: 1.75rem;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 46px; height: 46px; border-radius: 50%; background-color: #eff6ff; border: 1.5px solid #bfdbfe; margin-bottom: 0.95rem;">
                {icon(ICON_SHIELD_CHECK, size=24, color="#1d4ed8")}
            </div>
            <div style="font-family: 'Merriweather', serif; font-size: 1.5rem; font-weight: 700; color: #0b0f19; margin-bottom: 0.5rem;">
                Siap Menyampaikan Laporan Secara Aman?
            </div>
            <p style="font-size: 0.95rem; color: #64748b; max-width: 660px; margin: 0 auto; line-height: 1.65;">
                Kerahasiaan identitas dan seluruh berkas bukti Anda terlindungi secara penuh di bawah payung hukum UU PDP No. 27/2022 dengan enkripsi kriptografis tingkat tinggi.
            </p>
        </div>
        """),
        unsafe_allow_html=True
    )

    _, col_b1, col_b2, _ = st.columns([1.2, 1.1, 1.1, 1.2])
    with col_b1:
        if st.button("Mulai Buat Pengaduan", key="cta_bottom_lapor", type="primary", use_container_width=True):
            st.session_state.auth_default_tab = "pelapor"
            st.session_state.current_page = "auth"
            st.rerun()
    with col_b2:
        if st.button("Portal Petugas Investigasi", key="cta_bottom_inv", type="secondary", use_container_width=True):
            st.session_state.auth_default_tab = "investigator"
            st.session_state.current_page = "auth"
            st.rerun()

    # 6. Global Formal Footer
    st.markdown("<div id='bantuan' style='scroll-margin-top: 5rem;'></div>", unsafe_allow_html=True)
    st.markdown(render_footer(), unsafe_allow_html=True)
