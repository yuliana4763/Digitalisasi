
import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
from datetime import date
import base64

def convert_html_to_pdf(source_html):
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(source_html, dest=pdf_file)
    if pisa_status.err:
        return None
    return pdf_file

def generate_html(data):
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .page {{ page-break-after: always; }}
            .cover {{
                text-align: center;
                margin-top: 150px;
                color: #0066cc;
            }}
            .info {{
                margin-top: 40px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #333;
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>

    <!-- Page 1: Cover -->
    <div class="page cover">
        <h1>SILABUS MICROSILLABUS</h1>
        <h2>{data['judul']}</h2>
        <p>{data['penyusun']}</p>
        <p>{data['instansi']}</p>
        <p>{date.today().strftime('%d %B %Y')}</p>
    </div>

    <!-- Page 2: Informasi Umum -->
    <div class="page info">
        <h2>Informasi Pelatihan</h2>
        <table>
            <tr><td><b>Nama Pelatihan</b></td><td>{data['judul']}</td></tr>
            <tr><td><b>Durasi</b></td><td>{data['durasi']} JP</td></tr>
            <tr><td><b>Target Peserta</b></td><td>{data['peserta']}</td></tr>
            <tr><td><b>Deskripsi</b></td><td>{data['deskripsi']}</td></tr>
            <tr><td><b>Tujuan</b></td><td>{data['tujuan']}</td></tr>
            <tr><td><b>Output</b></td><td>{data['output']}</td></tr>
        </table>
    </div>

    <!-- Page 3: Materi -->
    <div class="page">
        <h2>Materi Pelatihan</h2>
        <table>
            <tr><th>No</th><th>Topik</th><th>Subtopik</th></tr>
            {"".join([f"<tr><td>{i+1}</td><td>{topik}</td><td>{sub}</td></tr>" for i, (topik, sub) in enumerate(zip(data['topik'], data['subtopik']))])}
        </table>
    </div>

    <!-- Page 4: Footer -->
    <div class="page" style="text-align: center; margin-top: 250px;">
        <h3>Pusat Pengembangan Literasi Digital</h3>
        <p>Kementerian Komunikasi dan Digital<br>Tahun 2025</p>
    </div>

    </body>
    </html>
    """

st.title("📘 Digitalisasi Silabus Micro Skill")

with st.form("silabus_form"):
    judul = st.text_input("Judul Pelatihan")
    penyusun = st.text_input("Nama Penyusun")
    instansi = st.text_input("Instansi")
    durasi = st.number_input("Durasi Pelatihan (JP)", 1, 100)
    peserta = st.text_input("Target Peserta")
    deskripsi = st.text_area("Deskripsi Pelatihan")
    tujuan = st.text_area("Tujuan Pembelajaran")
    output = st.text_area("Output Pelatihan")

    topik, subtopik = [], []
    for i in range(3):
        topik.append(st.text_input(f"Topik {i+1}", key=f"topik_{i}"))
        subtopik.append(st.text_input(f"Subtopik {i+1}", key=f"sub_{i}"))

    submitted = st.form_submit_button("Generate PDF")

if submitted:
    data = {
        "judul": judul,
        "penyusun": penyusun,
        "instansi": instansi,
        "durasi": durasi,
        "peserta": peserta,
        "deskripsi": deskripsi,
        "tujuan": tujuan,
        "output": output,
        "topik": topik,
        "subtopik": subtopik,
    }

    html_content = generate_html(data)
    pdf_file = convert_html_to_pdf(html_content)

    if pdf_file:
        st.success("✅ PDF berhasil dibuat!")
        st.download_button(
            label="📥 Download PDF Silabus",
            data=pdf_file,
            file_name="silabus_microskill.pdf",
            mime="application/pdf"
        )
    else:
        st.error("❌ Gagal membuat PDF.")
