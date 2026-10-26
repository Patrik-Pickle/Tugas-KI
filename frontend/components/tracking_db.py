"""
frontend/components/tracking_db.py
Komponen Presentasi UI untuk Pelacakan Laporan dan Disposisi Kasus.
Mengonsumsi layanan basis data dan utilitas CSPRNG dari backend/disposition_service.py
dan backend/csprng_utils.py.
"""
from html import escape as html_escape

from disposition_service import (
    STATUS_PENDING,
    STATUS_INVESTIGATING,
    STATUS_NEED_EVIDENCE,
    STATUS_COMPLETED,
    STATUS_REJECTED,
    STATUS_CHOICES,
    VERDICT_PENDING,
    VERDICT_INTERNAL_SANCTION,
    VERDICT_LAW_ENFORCEMENT,
    VERDICT_DISMISSED,
    VERDICT_CHOICES,
    init_tracking_db,
    get_report_disposition,
    update_report_disposition,
    find_report_for_tracking,
)

from csprng_utils import (
    generate_csprng_ticket,
    validate_ticket_format,
)

def get_status_style(status: str) -> dict:
    """Returns background, text, and border colors for a given report status."""
    if status == STATUS_INVESTIGATING:
        return {"bg": "#fffbeb", "color": "#b45309", "border": "#fde68a"}
    elif status == STATUS_NEED_EVIDENCE:
        return {"bg": "#fff7ed", "color": "#c2410c", "border": "#fed7aa"}
    elif status == STATUS_COMPLETED:
        return {"bg": "#ecfdf5", "color": "#059669", "border": "#a7f3d0"}
    elif status == STATUS_REJECTED:
        return {"bg": "#fef2f2", "color": "#b91c1c", "border": "#fecaca"}
    else:  # STATUS_PENDING or default
        return {"bg": "#eff6ff", "color": "#1d4ed8", "border": "#bfdbfe"}

def render_status_badge(status: str) -> str:
    """Generates an HTML badge string representing the disposition status."""
    st_style = get_status_style(status)
    return (
        f'<span style="background-color: {st_style["bg"]}; color: {st_style["color"]}; '
        f'border: 1px solid {st_style["border"]}; border-radius: 9999px; '
        f'padding: 0.28rem 0.75rem; font-size: 0.76rem; font-weight: 700; display: inline-block; white-space: nowrap;">'
        f'{status}</span>'
    )

def render_tracking_timeline(
    status: str,
    created_at: str,
    updated_at: str,
    notes: str = "",
    decision_number: str = "",
    verdict_category: str = "",
    ticket_code: str = ""
) -> str:
    """
    Renders an HTML 3-stage progress timeline along with official investigator feedback notes
    or formal verdict document when decision is final.
    Strictly avoids emojis and em dashes.
    """
    # Stage 1
    s1_title = "1. Pengaduan Terenkripsi Masuk"
    s1_desc = f"Laporan berhasil dikirim dan dienkripsi ke basis data pada {created_at}."
    s1_badge = '<span style="background:#ecfdf5;color:#059669;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Selesai</span>'

    # Stage 2
    s2_title = "2. Penelaahan & Forensik Bukti"
    if status == STATUS_PENDING:
        s2_desc = "Menunggu antrean telaah oleh tim pemeriksa / investigator berwenang."
        s2_badge = '<span style="background:#f1f5f9;color:#64748b;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Menunggu</span>'
    elif status == STATUS_INVESTIGATING:
        s2_desc = "Tim investigator sedang memverifikasi bukti dokumen, video, dan narasi kasus."
        s2_badge = '<span style="background:#fffbeb;color:#b45309;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Sedang Berjalan</span>'
    elif status == STATUS_NEED_EVIDENCE:
        s2_desc = "Investigator memerlukan klarifikasi atau bukti pendukung tambahan dari pelapor."
        s2_badge = '<span style="background:#fff7ed;color:#c2410c;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Perlu Bukti Tambahan</span>'
    else:
        s2_desc = "Pemeriksaan bukti forensik telah rampung diselesaikan."
        s2_badge = '<span style="background:#ecfdf5;color:#059669;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Selesai Ditelaah</span>'

    # Stage 3
    is_decided = status in [STATUS_COMPLETED, STATUS_REJECTED]
    if status == STATUS_COMPLETED:
        s3_title = "3. Putusan Akhir & Tindak Lanjut"
        s3_desc = f"Penyelidikan dinyatakan selesai dan putusan resmi telah disahkan pada {updated_at}."
        s3_badge = '<span style="background:#ecfdf5;color:#059669;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:700;border:1px solid #a7f3d0;white-space:nowrap;display:inline-block;">Putusan Final Diterbitkan</span>'
    elif status == STATUS_REJECTED:
        s3_title = "3. Putusan Akhir & Tindak Lanjut"
        s3_desc = f"Laporan ditutup karena tidak memenuhi unsur atau bukti tidak memadai. Tanggal penetapan: {updated_at}."
        s3_badge = '<span style="background:#fef2f2;color:#b91c1c;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:700;border:1px solid #fecaca;white-space:nowrap;display:inline-block;">Kasus Ditutup / Ditolak</span>'
    else:
        s3_title = "3. Putusan Akhir & Tindak Lanjut"
        s3_desc = "Putusan resmi dan rekomendasi hukum akan diterbitkan setelah tahapan investigasi disahkan oleh pimpinan."
        s3_badge = '<span style="background:#f1f5f9;color:#64748b;padding:3px 10px;border-radius:12px;font-size:0.74rem;font-weight:600;white-space:nowrap;display:inline-block;">Menunggu Putusan</span>'

    notes_section = ""
    safe_notes = html_escape((notes or "").strip()).replace("\n", "<br>")

    if is_decided:
        # Tampilan Formal Lembar Putusan Resmi
        dec_num = decision_number if decision_number else (
            f"SK-INV/{ticket_code}/2026" if ticket_code else "SK-INV/WBS-OFFICIAL/2026"
        )
        verd_cat = verdict_category if verdict_category else (
            VERDICT_INTERNAL_SANCTION if status == STATUS_COMPLETED else VERDICT_DISMISSED
        )
        verd_color = "#059669" if status == STATUS_COMPLETED else "#b91c1c"
        accent_border = "#059669" if status == STATUS_COMPLETED else "#dc2626"
        notes_body = safe_notes if safe_notes else "Putusan resmi telah ditetapkan sesuai ketentuan peraturan internal dan kode etik organisasi."

        notes_section = f"""
        <div style="margin-top: 1.25rem; background-color: #f8fafc; border: 1.5px solid #cbd5e1; border-top: 4px solid {accent_border}; border-radius: 8px; padding: 1.25rem 1.35rem; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.75rem; margin-bottom: 0.85rem;">
                <div>
                    <div style="font-size: 0.72rem; text-transform: uppercase; font-weight: 700; color: #64748b; letter-spacing: 0.05em;">
                        Surat Ketetapan / Berita Acara Putusan Resmi
                    </div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.02rem; font-weight: 700; color: #0f172a; margin-top: 0.15rem;">
                        {html_escape(dec_num)}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.72rem; color: #64748b; font-weight: 600;">Tanggal Pengesahan:</div>
                    <div style="font-size: 0.82rem; font-weight: 700; color: #1e293b;">{updated_at}</div>
                </div>
            </div>

            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.75rem 0.95rem; margin-bottom: 0.75rem;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.03em;">
                    Klasifikasi Amar Putusan Kasus:
                </div>
                <div style="font-size: 0.92rem; font-weight: 700; color: {verd_color}; margin-top: 0.2rem;">
                    {html_escape(verd_cat)}
                </div>
            </div>

            <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.85rem;">
                <div style="font-size: 0.72rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.03em; margin-bottom: 0.35rem;">
                    Amar Putusan & Pertimbangan Investigator:
                </div>
                <div style="font-size: 0.88rem; color: #1e293b; line-height: 1.6;">
                    {notes_body}
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px dashed #cbd5e1; padding-top: 0.65rem; font-size: 0.76rem; color: #64748b;">
                <div>
                    Payung Regulasi: <b>UU PDP No. 27/2022</b> • Kerahasiaan Identitas Pelapor Tetap Terlindungi Mutlak.
                </div>
                <div style="font-weight: 700; color: {verd_color};">
                    Status: Sah & Mengikat
                </div>
            </div>
        </div>
        """
    elif safe_notes:
        notes_section = f"""
        <div style="margin-top: 1.15rem; background-color: #f8fafc; border: 1px solid #cbd5e1; border-left: 4px solid #1d4ed8; border-radius: 6px; padding: 0.9rem 1.1rem;">
            <div style="font-weight: 700; color: #1e293b; font-size: 0.85rem; margin-bottom: 0.35rem;">
                Catatan Resmi dari Tim Investigator (Pembaruan: {updated_at}):
            </div>
            <div style="color: #334155; font-size: 0.86rem; line-height: 1.55;">
                {safe_notes}
            </div>
        </div>
        """
    else:
        notes_section = f"""
        <div style="margin-top: 1.15rem; background-color: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 6px; padding: 0.75rem 1rem; color: #64748b; font-size: 0.82rem;">
            Belum ada catatan resmi tambahan dari investigator untuk laporan ini.
        </div>
        """

    html = f"""
    <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 1.15rem; margin-top: 0.5rem; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <div style="display: flex; flex-direction: column; gap: 0.95rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1.5rem;">
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; color: #0f172a; font-size: 0.88rem;">{s1_title}</div>
                    <div style="color: #64748b; font-size: 0.80rem; margin-top: 0.2rem;">{s1_desc}</div>
                </div>
                <div style="flex-shrink: 0; white-space: nowrap;">{s1_badge}</div>
            </div>
            <div style="border-top: 1px dashed #e2e8f0; padding-top: 0.85rem; display: flex; justify-content: space-between; align-items: flex-start; gap: 1.5rem;">
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; color: #0f172a; font-size: 0.88rem;">{s2_title}</div>
                    <div style="color: #64748b; font-size: 0.80rem; margin-top: 0.2rem;">{s2_desc}</div>
                </div>
                <div style="flex-shrink: 0; white-space: nowrap;">{s2_badge}</div>
            </div>
            <div style="border-top: 1px dashed #e2e8f0; padding-top: 0.85rem; display: flex; justify-content: space-between; align-items: flex-start; gap: 1.5rem;">
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; color: #0f172a; font-size: 0.88rem;">{s3_title}</div>
                    <div style="color: #64748b; font-size: 0.80rem; margin-top: 0.2rem;">{s3_desc}</div>
                </div>
                <div style="flex-shrink: 0; white-space: nowrap;">{s3_badge}</div>
            </div>
        </div>
        {notes_section}
    </div>
    """
    return "\n".join(line.strip() for line in html.splitlines() if line.strip())
