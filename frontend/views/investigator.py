import os
import streamlit as st
import database
import crypto_utils
from components.header import render_sovereign_header
from components.previewers import render_ktp_preview, render_pdf_preview, render_video_preview
from components.icons import (
    icon,
    ICON_ACTIVITY,
    ICON_SEARCH,
    ICON_USER,
    ICON_LOCK,
    ICON_UNLOCK,
    ICON_FILE_TEXT,
    ICON_ID_CARD,
    ICON_CHECK_CIRCLE
)
from components.utils import clean_html
from components.layout import stat_card, callout
from components.footer import render_footer
from components.tracking_db import (
    get_report_disposition,
    update_report_disposition,
    render_status_badge,
    STATUS_CHOICES,
    VERDICT_CHOICES
)

STORAGE_DIR = os.path.join("storage", "encrypted_files")

def render_investigator_view():
    """
    Renders the Forensic Investigator Portal structured into clean sidebar sections:
    1. Workspace Kasus & Dekripsi
    2. Dossier & Telemetri Forensik
    """
    user = st.session_state.get("user")
    if not user or user.get("role") != "investigator":
        st.error("Otorisasi Ditolak: Anda harus login sebagai petugas pemeriksa resmi.")
        return

    # Header in main content area with top-left profile popover
    render_sovereign_header(
        title="SecureReport : Workspace Investigator",
        subtitle="Portal Verifikasi Forensik Kriptografi & Dekripsi Dossier Bukti Hukum"
    )

    all_reports = database.get_all_reports()

    # Tab-based structure to organize the forensic workflow
    tab_workspace, tab_telemetry = st.tabs([
        "Workspace Dekripsi & Telaah Kasus",
        "Ringkasan Dossier & Telemetri Sistem"
    ])

    with tab_telemetry:
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        total_count = len(all_reports)
        cipher_counts = {"AES": 0, "DES": 0, "RC4": 0}
        for r in all_reports:
            c = r["cipher_used"].upper()
            if c in cipher_counts:
                cipher_counts[c] += 1

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(stat_card("Total Laporan Masuk", str(total_count), color="#1d4ed8"), unsafe_allow_html=True)
        with col_m2:
            st.markdown(stat_card("AES Protected (128-bit)", str(cipher_counts['AES']), color="#1d4ed8"), unsafe_allow_html=True)
        with col_m3:
            st.markdown(stat_card("DES Protected (64-bit)", str(cipher_counts['DES']), color="#d97706"), unsafe_allow_html=True)
        with col_m4:
            st.markdown(stat_card("RC4 Stream Cipher", str(cipher_counts['RC4']), color="#2563eb"), unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        if all_reports:
            st.markdown(
                clean_html(f"""
                <div style="font-weight: 700; font-size: 0.95rem; color: #0b0f19; margin-bottom: 0.75rem;">
                    Daftar Dossier Terdaftar dalam Sistem:
                </div>
                """),
                unsafe_allow_html=True
            )
            for r in all_reports:
                disp_r = get_report_disposition(r['id'])
                ticket_code_r = disp_r.get("tracking_token", f"WBS-{r['id']:05d}")
                st.markdown(
                    clean_html(f"""
                    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 0.88rem; font-weight: 600; color: #0b0f19;">
                            {ticket_code_r} : {r['title']}
                        </span>
                        <div style="display: flex; gap: 0.75rem; align-items: center; font-size: 0.8rem; color: #64748b;">
                            <span>Pelapor: <b>{r['reporter']}</b></span>
                            <span>{r['created_at']}</span>
                            <span class="sovereign-badge badge-primary">{r['cipher_used']}</span>
                            {render_status_badge(disp_r['status'])}
                        </div>
                    </div>
                    """),
                    unsafe_allow_html=True
                )

    with tab_workspace:
        st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
        if not all_reports:
            st.info("Saat ini belum ada pengaduan yang masuk ke dalam sistem.")
            return

        # 1. Selector Dossier
        st.markdown(
            clean_html(f"""
            <div style="font-weight: 700; font-size: 0.95rem; color: #0b0f19; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.4rem;">
                {icon(ICON_SEARCH, size=16, color="#1d4ed8")}
                <span>Pilih Dossier Kasus untuk Diperiksa</span>
            </div>
            """),
            unsafe_allow_html=True
        )
        
        report_options = {}
        for r in all_reports:
            r_disp = get_report_disposition(r["id"])
            t_code = r_disp.get("tracking_token", f"WBS-{r['id']:05d}")
            report_options[f"{t_code} : {r['title']} [{r_disp['status']}] ({r['cipher_used']})"] = r["id"]
        
        selected_label = st.selectbox("Daftar Dossier Terdaftar:", list(report_options.keys()), label_visibility="collapsed")
        selected_id = report_options[selected_label]
        
        report = database.get_report_by_id(selected_id)
        if not report:
            st.error("Dossier tidak ditemukan.")
            return

        curr_disp = get_report_disposition(report["id"])
        ticket_code = curr_disp.get("tracking_token", f"WBS-{report['id']:05d}")

        # 2. Case Workspace Card
        st.markdown(
            clean_html(f"""
            <div style="background: #ffffff; border: 1.5px solid #e2e8f0; border-radius: 12px; padding: 1.35rem 1.6rem; margin: 1rem 0 1.5rem 0; box-shadow: 0 1px 3px rgba(11,15,25,0.04);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.65rem; margin-bottom: 0.85rem;">
                    <div>
                        <span style="font-size: 0.72rem; color: #64748b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.04em;">Nomor Tiket Investigasi Resmi (CSPRNG)</span>
                        <h3 style="font-family: 'Merriweather', serif; font-size: 1.25rem; font-weight: 700; color: #0b0f19; margin: 0.15rem 0 0 0;">
                            {ticket_code} : {report['title']}
                        </h3>
                    </div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <span class="sovereign-badge badge-primary" style="font-size: 0.82rem; font-weight: 700;">
                            Cipher: {report['cipher_used']}
                        </span>
                        {render_status_badge(curr_disp['status'])}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; font-size: 0.84rem; color: #475569;">
                    <div>{icon(ICON_USER, size=14, color="#1d4ed8")} <b>Pelapor:</b> {report['reporter']}</div>
                    <div>{icon(ICON_ACTIVITY, size=14, color="#1d4ed8")} <b>Waktu Submit:</b> {report['created_at']}</div>
                    <div>{icon(ICON_LOCK, size=14, color="#059669")} <b>Integritas Payload:</b> Terproteksi BLOB</div>
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

        # 3. Dekripsi Kronologi
        st.markdown(
            clean_html(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.65rem;">
                <span style="width: 26px; height: 26px; border-radius: 50%; background-color: #eff6ff; border: 1.5px solid #bfdbfe; color: #1d4ed8; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.82rem; display: flex; align-items: center; justify-content: center;">
                    1
                </span>
                <span style="font-family: 'Merriweather', serif; font-size: 1.05rem; font-weight: 700; color: #0b0f19;">
                    Verifikasi Narasi Kronologi Peristiwa
                </span>
            </div>
            """),
            unsafe_allow_html=True
        )

        col_c1, col_c2 = st.columns([1, 1])
        with col_c1:
            st.caption("Cuplikan Sandi Kriptografis (Ciphertext Hex BLOB):")
            raw_blob = report["chronology_encrypted"]
            hex_preview = raw_blob[:64].hex() + ("..." if len(raw_blob) > 64 else "")
            st.markdown(f"<div class='cipher-telemetry-box'>{hex_preview}\n(Total Ukuran Cipher: {len(raw_blob)} bytes)</div>", unsafe_allow_html=True)
            
        with col_c2:
            st.caption("Aksi Dekripsi Investigator:")
            if st.button("Dekripsi Kronologi Teks", key=f"btn_dec_text_{report['id']}", use_container_width=True):
                try:
                    decrypted_bytes, dec_time = crypto_utils.decrypt_data(report["chronology_encrypted"], report["cipher_used"])
                    st.session_state[f"dec_text_{report['id']}"] = {
                        "text": decrypted_bytes.decode("utf-8", errors="replace"),
                        "time": dec_time
                    }
                except Exception as e:
                    st.error(f"Gagal mendekripsi kronologi: {str(e)}")

            if f"dec_text_{report['id']}" in st.session_state:
                res = st.session_state[f"dec_text_{report['id']}"]
                st.markdown(
                    clean_html(f"""
                    <div class="cipher-plaintext-box">
                        <div style="font-size: 0.75rem; color: #059669; font-weight: 700; margin-bottom: 0.4rem; display: flex; align-items: center; gap: 0.35rem;">
                            {icon(ICON_CHECK_CIRCLE, size=14, color="#059669")}
                            <span>Berhasil didekripsi dalam {res['time'] * 1000:.3f} ms</span>
                        </div>
                        {res['text']}
                    </div>
                    """),
                    unsafe_allow_html=True
                )

        st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 1.75rem 0;'>", unsafe_allow_html=True)

        # 4. Dekripsi Berkas Bukti
        st.markdown(
            clean_html(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
                <span style="width: 26px; height: 26px; border-radius: 50%; background-color: #eff6ff; border: 1.5px solid #bfdbfe; color: #1d4ed8; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.82rem; display: flex; align-items: center; justify-content: center;">
                    2
                </span>
                <span style="font-family: 'Merriweather', serif; font-size: 1.05rem; font-weight: 700; color: #0b0f19;">
                    Dekripsi & Pratinjau Berkas Bukti Terlampir
                </span>
            </div>
            <p style="font-size: 0.84rem; color: #64748b; margin-bottom: 1rem;">
                Berkas bukti fisik dienkripsi di media penyimpanan server. Klik tombol di bawah untuk mendekripsi berkas secara aman ke memory buffer forensik.
            </p>
            """),
            unsafe_allow_html=True
        )

        ktp_path = os.path.join(STORAGE_DIR, report["ktp_filename"])
        doc_path = os.path.join(STORAGE_DIR, report["doc_filename"])
        vid_path = os.path.join(STORAGE_DIR, report["video_filename"])

        if st.button("Dekripsi Seluruh Berkas Bukti (KTP, PDF, MP4)", key=f"btn_dec_all_files_{report['id']}", use_container_width=True):
            with st.spinner("Mendekripsi berkas bukti forensik..."):
                decrypted_files = {}
                for file_key, file_path, label in [
                    ("ktp", ktp_path, "KTP"),
                    ("doc", doc_path, "Dokumen PDF"),
                    ("vid", vid_path, "Video MP4")
                ]:
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, "rb") as f:
                                enc_content = f.read()
                            dec_content, dec_time = crypto_utils.decrypt_data(enc_content, report["cipher_used"])
                            decrypted_files[file_key] = {
                                "bytes": dec_content,
                                "time": dec_time,
                                "filename": os.path.basename(file_path).replace(".enc", "")
                            }
                        except Exception as e:
                            st.error(f"Gagal mendekripsi berkas {label}: {str(e)}")
                    else:
                        st.warning(f"File terenkripsi {label} tidak ditemukan di server: <code>{file_path}</code>")

                st.session_state[f"dec_files_{report['id']}"] = decrypted_files

        # Menampilkan Hasil Dekripsi Berkas
        if f"dec_files_{report['id']}" in st.session_state:
            files = st.session_state[f"dec_files_{report['id']}"]
            
            # A. KTP Previewer
            if "ktp" in files:
                clean_name = files["ktp"]["filename"]
                render_ktp_preview(files["ktp"]["bytes"], clean_name)

            # B. PDF Previewer
            if "doc" in files:
                clean_name = files["doc"]["filename"]
                render_pdf_preview(files["doc"]["bytes"], clean_name)

            # C. Video Previewer
            if "vid" in files:
                clean_name = files["vid"]["filename"]
                render_video_preview(files["vid"]["bytes"], clean_name)

        st.markdown("<hr style='border: 0; border-top: 1px solid #e2e8f0; margin: 1.75rem 0;'>", unsafe_allow_html=True)

        # 5. Form Disposisi & Penyampaian Hasil Pemeriksaan Kasus
        st.markdown(
            clean_html(f"""
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem;">
                <span style="width: 26px; height: 26px; border-radius: 50%; background-color: #eff6ff; border: 1.5px solid #bfdbfe; color: #1d4ed8; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.82rem; display: flex; align-items: center; justify-content: center;">
                    3
                </span>
                <span style="font-family: 'Merriweather', serif; font-size: 1.05rem; font-weight: 700; color: #0b0f19;">
                    Disposisi Status & Hasil Pemeriksaan Kasus
                </span>
            </div>
            <p style="font-size: 0.84rem; color: #64748b; margin-bottom: 1rem;">
                Perbarui status penanganan dan berikan catatan temuan resmi untuk dipantau secara langsung oleh pihak pelapor.
            </p>
            """),
            unsafe_allow_html=True
        )

        curr_disp = get_report_disposition(report["id"])
        curr_status = curr_disp.get("status", "Menunggu Penelaahan")
        try:
            status_idx = STATUS_CHOICES.index(curr_status)
        except ValueError:
            status_idx = 0

        curr_verdict = curr_disp.get("verdict_category", VERDICT_CHOICES[0])
        try:
            verdict_idx = VERDICT_CHOICES.index(curr_verdict)
        except ValueError:
            verdict_idx = 0

        with st.form(key=f"form_disp_{report['id']}"):
            sel_status = st.selectbox(
                "Status Perkembangan Penanganan Kasus:",
                options=STATUS_CHOICES,
                index=status_idx,
                key=f"sel_status_widget_{report['id']}"
            )

            col_v1, col_v2 = st.columns(2)
            with col_v1:
                default_dec_num = curr_disp.get("decision_number") or f"SK-INV/{ticket_code}/2026"
                input_decision_number = st.text_input(
                    "Nomor Registrasi Surat Putusan (SK/BAP):",
                    value=default_dec_num,
                    key=f"text_decision_number_{report['id']}",
                    help="Nomor resmi penetapan berkas hasil investigasi"
                )
            with col_v2:
                sel_verdict = st.selectbox(
                    "Klasifikasi Amar Putusan Kasus:",
                    options=VERDICT_CHOICES,
                    index=verdict_idx,
                    key=f"sel_verdict_widget_{report['id']}",
                    help="Kategori putusan akhir penanganan kasus"
                )

            input_notes = st.text_area(
                "Amar Putusan & Pertimbangan Investigator untuk Pelapor:",
                value=curr_disp.get("notes", ""),
                height=130,
                placeholder="Tuliskan temuan investigasi, alasan tindak lanjut, amar putusan (terbukti/tidak terbukti), atau instruksi langkah hukum bagi pelapor...",
                key=f"text_notes_widget_{report['id']}"
            )
            submitted = st.form_submit_button("Sahkan Putusan & Kirim Hasil Penanganan", type="primary", use_container_width=True)
            if submitted:
                update_report_disposition(
                    report["id"],
                    status=sel_status,
                    notes=input_notes,
                    decision_number=input_decision_number,
                    verdict_category=sel_verdict
                )
                st.success("Putusan resmi dan disposisi investigasi berhasil disahkan dan disalurkan ke portal pelapor!")
                st.rerun()

    # Footer
    st.markdown(render_footer(), unsafe_allow_html=True)
