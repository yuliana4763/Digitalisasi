import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
import base64
from datetime import datetime
import os

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img:
            return base64.b64encode(img.read()).decode("utf-8")
    except Exception:
        return ""

def generate_header_with_logos(micro_path, mitra_path):
    micro_logo = encode_image_to_base64(micro_path)
    mitra_logo = encode_image_to_base64(mitra_path) if mitra_path else ""
    return f"""
    <div style="width:100%; display:flex; justify-content:space-between; align-items:center; margin-top:1cm; margin-bottom:1cm;">
        <img src="data:image/png;base64,{micro_logo}" style="height:1.08cm; width:3.3cm; object-fit:contain;" />
        {'<img src="data:image/png;base64,' + mitra_logo + '" style="height:1.08cm; width:3.3cm; object-fit:contain;" />' if mitra_logo else ''}
    </div>
    """

def generate_cover_page(image_path, page_break="after"):
    encoded_image = encode_image_to_base64(image_path)
    return f"""
    <div class="page" style="page-break-{page_break}: always;">
        <img src="data:image/png;base64,{encoded_image}" style="width: 100%; height: 100vh; object-fit: cover;">
    </div>
    """

def generate_info_page(data, logo_mitra_base64=None):
    # Path logo microskill (relative path for GitHub repo)
    logo_path = os.path.join(os.path.dirname(__file__), "logo microskill.png")
    encoded_logo = encode_image_to_base64(logo_path)
    # Versi dan header tambahan
    tanggal = datetime.now().strftime("%d%m%Y")
    versi = f"Versi #Silabus-{tanggal}"
    judul = data['Nama Pelatihan']
    # Logo + header (logo microskill kiri, logo mitra kanan)
    logo_mitra_html = ""
    if logo_mitra_base64:
        logo_mitra_html = f"""
        <img src="data:image/png;base64,{logo_mitra_base64}" 
             style="height:1.08cm; width:3.3cm; object-fit:contain; display:block; margin-left:auto;"/>
        """
    header = f"""
    <div style="margin-bottom: 24px;">
        <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start; margin-top:1cm; margin-bottom:0.5cm;">
            <img src="data:image/png;base64,{encoded_logo}" 
                 style="height:1.08cm; width:3.3cm; object-fit:contain; display:block;" />
            {logo_mitra_html}
        </div>
        <div style="font-size:10pt; font-style:italic; font-family:Cambria, serif; color:#000;">
            {versi}
        </div>
        <div style="font-size:22px; font-weight:bold; margin-top:8px; font-family:Cambria, serif; color:#1a237e;">
            Silabus {judul}
        </div>
        <div style="font-size:16px; margin-top:4px; font-family:Cambria, serif; color:#1a237e;">
            Kementerian Komunikasi dan Digital Republik Indonesia
        </div>
        <div style="font-size:16px; margin-top:2px; font-family:Cambria, serif; color:#1a237e;">
            Tahun 2025
        </div>
    </div>
    """
    disclaimer = """
    <div style="background-color:#fff3cd; color:#856404; border:1px solid #ffeeba; border-radius:6px; padding:16px; margin-bottom:24px;">
        <b>Disclaimer:</b> Dokumen ini digunakan hanya untuk kebutuhan Digital Talent Scholarship Kementerian Komunikasi dan Digital Republik Indonesia. Konten ini mengandung Kekayaan Intelektual, pengguna tunduk kepada undang-undang hak cipta, merek dagang atau hak kekayaan intelektual lainnya. Dilarang untuk memproduksi, memodifikasi, menyebarluaskan, atau mengeksploitasi konten ini dengan cara atau bentuk apapun tanpa persetujuan tertulis dari Digital Talent Scholarship Kementerian Komunikasi dan Digital Republik Indonesia.
    </div>
    """
    return f"""
    <div class="page info" style="page-break-before: always; font-family: Cambria, serif;">
        <h2 style="text-align: center; color: #1a237e; font-family:Cambria, serif;">Informasi Umum Pelatihan</h2>
        {header}
        {disclaimer}
        <table style="width: 100%; border-collapse: collapse; margin-top: 30px;">
            <tr><td style="padding: 8px; width: 35%;"><b>Akademi</b></td><td style="padding: 8px;">{data['Akademi']}</td></tr>
            <tr><td style="padding: 8px;"><b>Penyelenggara Pelatihan</b></td><td style="padding: 8px;">{data['Penyelenggara Pelatihan']}</td></tr>
            <tr><td style="padding: 8px;"><b>Tema Pelatihan</b></td><td style="padding: 8px;">{data['Tema Pelatihan']}</td></tr>
            <tr><td style="padding: 8px;"><b>Nama Pelatihan</b></td><td style="padding: 8px;">{data['Nama Pelatihan']}</td></tr>
            <tr><td style="padding: 8px;"><b>Singkatan Pelatihan</b></td><td style="padding: 8px;">{data['Singkatan Pelatihan']}</td></tr>
            <tr><td style="padding: 8px;"><b>Durasi Pelatihan</b></td><td style="padding: 8px;">{data['Durasi Pelatihan']} jam</td></tr>
            <tr><td style="padding: 8px;"><b>Deskripsi Pelatihan</b></td><td style="padding: 8px;">{data['Deskripsi Pelatihan']}</td></tr>
            <tr><td style="padding: 8px;"><b>Output Pelatihan</b></td><td style="padding: 8px;">{data['Output Pelatihan']}</td></tr>
        </table>
    </div>
    """

def generate_materi_page(topik_materi):
    html = """
    <div class="page info" style="page-break-before: always; font-family: Arial, sans-serif;">
        <h2 style="text-align: center; color: #1a237e;">Materi dan Konten Pembelajaran Micro Skill</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 30px;">
            <tr style="background-color: #f0f0f0;">
                <th style="padding: 10px; text-align: left; width: 30%;">Topik</th>
                <th style="padding: 10px; text-align: left;">Materi</th>
            </tr>
    """
    for idx, topik in enumerate(topik_materi, start=1):
        html += f"""
            <tr>
                <td style="padding: 10px; vertical-align: top;">
                    <b>Topik {idx}</b><br>{topik['topik']}
                </td>
                <td style="padding: 10px;">
                    Materi:
                    <ol style="margin: 0; padding-left: 18px;">
        """
        for materi in topik["materi"]:
            html += f"<li>{materi}</li>"
        html += """
                    </ol>
                </td>
            </tr>
        """
    html += """
        </table>
    </div>
    """
    return html

def generate_page3_dynamic(materi_data):
    html = """
    <div class="page" style="page-break-before: always; font-family: Arial, sans-serif;">
        <h2 style="text-align: center; color: #1a237e;">Materi dan Konten Pembelajaran Micro Skill</h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 11pt;">
            <tr style="background-color: #007bff; color: white; text-align: center;">
                <th style="padding: 8px; width: 25%;">Topik</th>
                <th style="padding: 8px; width: 55%;">Materi</th>
                <th style="padding: 8px; width: 20%;">JP</th>
            </tr>
    """

    for topik in materi_data:
        materi_list = topik.get('materi', [])
        jp = topik.get('jp', '')
        rowspan = len(materi_list) if materi_list else 1
        # Row pertama untuk topik (pakai rowspan)
        html += f"""
        <tr>
            <td rowspan="{rowspan}" style="border: 1px solid #000; padding: 8px; vertical-align: top;">
                {topik['topik']}
            </td>
            <td style="border: 1px solid #000; padding: 8px;">{materi_list[0] if materi_list else ''}</td>
            <td rowspan="{rowspan}" style="border: 1px solid #000; text-align: center;">
                {jp}
            </td>
        </tr>
        """

        # Materi berikutnya
        for materi in materi_list[1:]:
            html += f"""
            <tr>
                <td style="border: 1px solid #000; padding: 8px;">{materi}</td>
            </tr>
            """

    html += "</table></div>"
    return html

def generate_full_html(data, topik_materi, logo_mitra_base64=None):
    cover1_path = r"Cover 1.png"
    cover2_path = r"Cover 2.png"
    cover1_base64 = encode_image_to_base64(cover1_path)
    cover2_base64 = encode_image_to_base64(cover2_path)
    return f"""
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 0;
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
            }}
            .cover {{
                width: 100vw;
                height: 100vh;
                page-break-after: always;
            }}
            .cover1 {{
                background-image: url('data:image/png;base64,{cover1_base64}');
                background-size: cover;
                background-position: center;
            }}
            .cover2 {{
                background-image: url('data:image/png;base64,{cover2_base64}');
                background-size: cover;
                background-position: center;
                page-break-before: always;
            }}
            .info {{
                margin: 40px;
            }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <!-- Cover 1 as page 1 -->
        <div class="cover cover1"></div>
        <!-- Info Page as page 2 -->
        {generate_info_page(data, logo_mitra_base64)}
        <!-- Materi Page as page 3 -->
        {generate_materi_page(topik_materi)}
        <!-- Cover 2 as page 4 -->
        <div class="cover cover2"></div>
    </body>
    </html>
    """

def save_pdf(html_content):
    result = BytesIO()
    pisa.CreatePDF(src=html_content, dest=result)
    result.seek(0)
    return result

# STREAMLIT APP
if "topik_count" not in st.session_state:
    st.session_state.topik_count = 1

st.title("Digitalisasi Silabus Micro Skill")
st.markdown("Isi data berikut untuk membuat silabus pelatihan secara otomatis dalam format PDF.")

# Tombol tambah/hapus topik di luar form
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Tambah Topik"):
        st.session_state.topik_count += 1
with col2:
    if st.session_state.topik_count > 1:
        if st.button("➖ Hapus Topik"):
            st.session_state.topik_count -= 1

# Upload logo mitra di sidebar kanan atas
st.sidebar.markdown("### Upload Logo Mitra")
logo_mitra_file = st.sidebar.file_uploader("Logo Mitra (PNG/JPG)", type=["png", "jpg", "jpeg"])
logo_mitra_base64 = None
if logo_mitra_file is not None:
    logo_mitra_base64 = base64.b64encode(logo_mitra_file.read()).decode("utf-8")

with st.form("form_silabus"):
    st.subheader("Informasi Umum")
    akademi = st.text_input("Akademi", value="Micro Skill")
    penyelenggara_pelatihan = st.text_input("Penyelenggara Pelatihan")
    
    tema_options = [
        "Kewirausahaan Digital",
        "ElevAIte",
        "Konten Digital",
        "Cakap Digital",
        "Data Analisis",
        "Kecerdasan Artifisial",
        "Keamanan Informasi",
        "Komunikasi",
        "Pemrograman",
        "Sistem Manajemen Keamanan Informasi",
        "Mindset Digital",
        "Teknologi Informasi",
        "Pengantar SPBE",
        "Etika dan Budaya Digital",
        "Generative AI untuk Pendidikan",
        "Ekonomi Digital",
        "Bisnis Digital",
        "Literasi Digital"
    ]
    tema_pelatihan = st.selectbox(
        "Tema Pelatihan (pilih atau ketik manual)", 
        options=tema_options + ["Lainnya (isi manual)"]
    )
    if tema_pelatihan == "Lainnya (isi manual)":
        tema_pelatihan = st.text_input("Tema Pelatihan (isi manual)")

    nama_pelatihan = st.text_input("Nama Pelatihan")
    singkatan_pelatihan = st.text_input("Singkatan Pelatihan")
    durasi = st.number_input("Durasi (jam)", min_value=1)
    deskripsi_pelatihan = st.text_area("Deskripsi Pelatihan")
    output_pelatihan = st.text_area("Output Pelatihan")

    st.subheader("Materi Pelatihan")
    topik_materi = []
    for i in range(st.session_state.topik_count):
        topik = st.text_input(f"Topik {i+1}", key=f"topik_{i}")
        materi = st.text_area(
            f"Materi untuk Topik {i+1}", key=f"materi_{i}"
        )
        if topik and materi:
            materi_list = [m.strip() for m in materi.split(",") if m.strip()]
            topik_materi.append({"topik": topik, "materi": materi_list})

    submit = st.form_submit_button("🚀 Buat PDF Silabus")

if submit:
    data = {
        "Akademi": akademi,
        "Penyelenggara Pelatihan": penyelenggara_pelatihan,
        "Tema Pelatihan": tema_pelatihan,
        "Nama Pelatihan": nama_pelatihan,
        "Singkatan Pelatihan": singkatan_pelatihan,
        "Durasi Pelatihan": durasi,
        "Deskripsi Pelatihan": deskripsi_pelatihan,
        "Output Pelatihan": output_pelatihan
    }

    html_result = generate_full_html(data, topik_materi, logo_mitra_base64)
    pdf_file = save_pdf(html_result)

    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📥 Download Silabus PDF",
        data=pdf_file,
        file_name="Silabus_MicroSkill.pdf",
        mime="application/pdf"
    )
