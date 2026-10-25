from components.utils import clean_html
from components.icons import icon, ICON_SHIELD_CHECK

def render_footer():
    """
    Renders an institutional, compliant 3-column footer without emoticons or em dashes.
    """
    return clean_html(f"""
    <div style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 0.83rem;">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: 1.5rem; margin-bottom: 1.5rem;">
            <div style="max-width: 380px;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.4rem;">
                    {icon(ICON_SHIELD_CHECK, size=20, color="#1d4ed8")}
                    <span style="font-family: 'Merriweather', serif; font-weight: 700; font-size: 1.05rem; color: #0b0f19;">SecureReport</span>
                </div>
                <div style="color: #64748b; font-size: 0.82rem; line-height: 1.5;">
                    Sistem Pengaduan Pelanggaran Aman (Whistleblowing System) dengan enkripsi multi-cipher end-to-end.
                </div>
            </div>
            <div>
                <div style="font-weight: 700; color: #0b0f19; font-size: 0.85rem; margin-bottom: 0.4rem;">Kepatuhan Regulasi</div>
                <div style="color: #64748b; font-size: 0.82rem; line-height: 1.5;">
                    Undang-Undang Pelindungan Data Pribadi (UU PDP No. 27/2022)<br>
                    Standar Kriptografi Terverifikasi (AES, DES, RC4)
                </div>
            </div>
            <div>
                <div style="font-weight: 700; color: #0b0f19; font-size: 0.85rem; margin-bottom: 0.4rem;">Hak Akses & Otoritas</div>
                <div style="color: #64748b; font-size: 0.82rem; line-height: 1.5;">
                    Pemeriksaan berkas hanya dapat diakses oleh<br>
                    Tim Petugas Forensik Hukum Berwenang.
                </div>
            </div>
        </div>
        <div style="padding-top: 1.25rem; border-top: 1px solid #f1f5f9; text-align: center; color: #94a3b8; font-size: 0.78rem;">
            Hak Cipta 2026 SecureReport. Seluruh Hak Dilindungi Undang-Undang.
        </div>
    </div>
    """)
