import os
import sys

# Konfigurasi Path: Memastikan root proyek, backend, dan frontend dapat diimpor tanpa mengubah folder backend/
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

for p in [ROOT_DIR, BACKEND_DIR, FRONTEND_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Menjamin working directory selalu di root proyek
os.chdir(ROOT_DIR)

import streamlit as st
import database
import csprng_utils
import disposition_service
import forensic_utils
import importlib

import views.landing
import views.auth
import views.pelapor
import views.investigator
import components.header
import components.sidebar
import components.cards
import components.previewers
import components.icons
import components.utils
import components.layout
import components.footer
import components.tracking_db

# Hot-reload seluruh sub-modul agar Streamlit selalu menyajikan versi file terbaru
# Modul backend dan komponen harus di-reload terlebih dahulu sebelum views yang mengimpornya
importlib.reload(csprng_utils)
importlib.reload(disposition_service)
importlib.reload(forensic_utils)
importlib.reload(components.icons)
importlib.reload(components.utils)
importlib.reload(components.layout)
importlib.reload(components.sidebar)
importlib.reload(components.cards)
importlib.reload(components.previewers)
importlib.reload(components.footer)
importlib.reload(components.header)
importlib.reload(components.tracking_db)

importlib.reload(views.landing)
importlib.reload(views.auth)
importlib.reload(views.pelapor)
importlib.reload(views.investigator)

from views.landing import render_landing_view
from views.auth import render_auth_view
from views.pelapor import render_pelapor_view
from views.investigator import render_investigator_view
from components.sidebar import render_profile_menu

# Inisialisasi Database SQLite
database.init_db()
components.tracking_db.init_tracking_db()

# Pastikan folder penyimpanan berkas terenkripsi tersedia
STORAGE_DIR = os.path.join(ROOT_DIR, "storage", "encrypted_files")
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR, exist_ok=True)

# Konfigurasi Layar Streamlit
st.set_page_config(
    page_title="SecureReport : Layanan Pengaduan Aman",
    page_icon="https://api.iconify.design/lucide:shield-check.svg?color=%231d4ed8",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeksi CSS Desain Sovereign Trust
def inject_global_assets():
    css_file = os.path.join(FRONTEND_DIR, "assets", "style.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

inject_global_assets()

# State Manajemen Sesi & Halaman
if "user" not in st.session_state:
    st.session_state.user = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

if "auth_default_tab" not in st.session_state:
    st.session_state.auth_default_tab = "pelapor"

def main():
    user = st.session_state.user

    # Jika pengguna sudah login, arahkan ke ruang kerja sesuai peran
    if user:
        role = user.get("role", "pelapor")
        if role == "investigator":
            render_investigator_view()
        else:
            render_pelapor_view()
    else:
        # Kendalikan antara Landing Page dan Auth View
        if st.session_state.current_page == "auth":
            render_auth_view()
        else:
            render_landing_view()

if __name__ == "__main__":
    main()
