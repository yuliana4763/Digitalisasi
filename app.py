import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
from datetime import date

# Fungsi: Membuat HTML lengkap
# Halaman 1
def generate_full_html(data):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Cover Silabus MicroSkill</title>
        <style>
            @page {
                size: A4;
                margin: 0;
            }
            body {
                margin: 0;
                font-family: 'Arial', sans-serif;
                position: relative;
                height: 100vh;
            }
            .container {
                padding: 80px 60px 30px 60px;
                height: 100%;
                background-color: #ffffff;
                position: relative;
            }
            .logo-container {
                display: flex;
                justify-content: flex-start;
                align-items: center;
                gap: 20px;
            }
            .logo-container img {
                height: 50px;
            }
            .title {
                margin-top: 100px;
                font-size: 38px;
                font-weight: bold;
                color: #0D47A1;
                text-transform: uppercase;
            }
            .subtitle {
                font-size: 36px;
                color: #00B0FF;
                font-weight: bold;
                margin-top: -10px;
            }
            .course-title {
                font-size: 24px;
                margin-top: 50px;
                color: #444;
                font-weight: bold;
            }
            .footer {
                position: absolute;
                bottom: 0;
                left: 0;
                background-color: #00B0FF;
                width: 100%;
                color: white;
                font-size: 16px;
                padding: 18px 60px;
                box-sizing: border-box;
            }
            .pattern {
                position: absolute;
                right: 40px;
                top: 150px;
                height: 450px;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo-container">
                <img src="https://images.app.goo.gl/zT2mwAAkMoU7pWyTA" alt="Logo Komdigi">
                <img src="https://drive.google.com/file/d/1W221LoZbrSdUIxjtFBSmXwweeUD7um14/view?usp=sharing" alt="Logo MicroSkill">
            </div>

            <div class="title">SILABUS</div>
            <div class="subtitle">MICROSKILL</div>
            <div class="course-title">Nama Judul Pelatihan</div>

            <img class="pattern" src="https://i.imgur.com/28rACRA.png" alt="Pattern">

            <div class="footer">
                Pusat Pengembangan Literasi Digital<br>
                Kementerian Komunikasi dan Digital<br>
                Tahun 2025
            </div>
        </div>
    </body>
    </html>

    <div style="page-break-after: always;"></div>
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Halaman 2 Silabus</title>
        <style>
            @page {
                size: A4;
                margin: 50px;
            }

            body {
                font-family: 'Arial', sans-serif;
                font-size: 12pt;
                position: relative;
            }

            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .header-left img {
                height: 40px;
            }

            .header-right img {
                height: 40px;
            }

            .title {
                margin-top: 20px;
                color: #1976d2;
                font-size: 18pt;
                font-weight: bold;
            }

            .sub-title {
                color: #0d47a1;
                font-size: 14pt;
                font-weight: bold;
            }

            .year {
                color: #d32f2f;
                font-weight: bold;
                font-size: 12pt;
            }

            .disclaimer {
                font-size: 9pt;
                color: #444;
                margin-top: 10px;
                font-style: italic;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }

            th {
                background-color: #1565c0;
                color: white;
                padding: 8px;
                text-align: left;
            }

            td {
                padding: 8px;
                border: 1px solid #ccc;
            }

            .footer {
                position: absolute;
                bottom: -40px;
                right: 0;
                font-size: 10pt;
                color: #888;
            }
        </style>
    </head>
    <body>

        <!-- HEADER -->
        <div class="header">
            <div class="header-left">
                <img src="https://i.imgur.com/r2avSda.png" alt="Logo MicroSkill">
            </div>
            <div class="header-right">
                <img src="data:image/png;base64,{logo_mitra_base64}" alt="Logo Mitra">
            </div>
        </div>

        <!-- JUDUL -->
        <div class="title">Silabus {judul_pelatihan}</div>
        <div class="sub-title">Kementerian Komunikasi dan Digital Republik Indonesia</div>
        <div class="year">Tahun 2025</div>

        <!-- DISCLAMER -->
        <div class="disclaimer">
            Disclaimer: Silabus ini merupakan bagian dari Program Digital Talent Scholarship Kementerian Kominfo dan digunakan untuk tujuan pelatihan. Konten disesuaikan dengan tema pelatihan dan kebutuhan peserta Micro Skill.
        </div>

        <!-- TABEL INFORMASI -->
        <table>
            <tr><th colspan="2">Informasi Pelatihan Micro Skill</th></tr>
            <tr><td>Akademi</td><td>Micro Skill (Default)</td></tr>
            <tr><td>Penyelenggara Pelatihan</td><td>{penyelenggara}</td></tr>
            <tr><td>Tema Pelatihan</td><td>{tema}</td></tr>
            <tr><td>Nama Pelatihan</td><td>{judul_pelatihan}</td></tr>
            <tr><td>Singkatan Pelatihan</td><td>{singkatan}</td></tr>
            <tr><td>Durasi Pelatihan</td><td>{durasi}</td></tr>
            <tr><td>Deskripsi Pelatihan</td><td>{deskripsi}</td></tr>
            <tr><td>Output Pelatihan</td><td>{output}</td></tr>
        </table>

        <!-- FOOTER -->
        <div class="footer">1</div>

    </body>
    </html>

    <div style="page-break-after: always;"></div>


    <div style="page-break-after: always;"></div>

        <div class="section">
            <h2>Deskripsi Pelatihan</h2>
            <p>{data['deskripsi']}</p>
            <h2>Durasi</h2>
            <p>{data['durasi']} jam</p>
            <h2>Target Peserta</h2>
            <p>{data['peserta']}</p>
            <h2>Tujuan Pembelajaran</h2>
            <p>{data['tujuan']}</p>
            <h2>Materi Pelatihan</h2>
            <table>
                <tr><th>No</th><th>Topik</th><th>Subtopik</th></tr>"""
    for i, (topik, subtopik) in enumerate(zip(data['topik'], data['subtopik']), 1):
        html += f"<tr><td>{i}</td><td>{topik}</td><td>{subtopik}</td></tr>"
    html += f"""
            </table>
            <br>
            <p><em>Disusun pada tanggal {date.today().strftime('%d %B %Y')}</em></p>
        </div>
    </body>
    </html>
    """
    return html

# Fungsi: Simpan PDF dari HTML (xhtml2pdf)
def save_pdf(html_content):
    result = BytesIO()
    pisa.CreatePDF(src=html_content, dest=result)
    return result

# STREAMLIT APP
st.title("📄 Digitalisasi Silabus Micro Skill")
st.markdown("Isi data berikut untuk membuat silabus pelatihan secara otomatis dalam format PDF.")

with st.form("form_silabus"):
    st.subheader("📘 Informasi Cover")
    judul = st.text_input("Judul Pelatihan")
    nama_penyusun = st.text_input("Nama Penyusun")
    instansi = st.text_input("Nama Instansi")

    st.subheader("📚 Informasi Umum")
    deskripsi = st.text_area("Deskripsi Pelatihan")
    durasi = st.number_input("Durasi (jam)", min_value=1)
    peserta = st.text_input("Target Peserta")
    tujuan = st.text_area("Tujuan Pembelajaran")

    st.subheader("🧩 Materi Pelatihan")
    topik = []
    subtopik = []
    for i in range(1, 4):
        topik.append(st.text_input(f"Topik {i}", key=f"topik_{i}"))
        subtopik.append(st.text_input(f"Subtopik {i}", key=f"subtopik_{i}"))

    submit = st.form_submit_button("🚀 Buat PDF Silabus")

if submit:
    data = {
        "judul": judul,
        "nama_penyusun": nama_penyusun,
        "instansi": instansi,
        "deskripsi": deskripsi,
        "durasi": durasi,
        "peserta": peserta,
        "tujuan": tujuan,
        "topik": topik,
        "subtopik": subtopik
    }

    html_result = generate_full_html(data)
    pdf_file = save_pdf(html_result)

    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📥 Download Silabus PDF",
        data=pdf_file,
        file_name="Silabus_MicroSkill.pdf",
        mime="application/pdf"
    )
