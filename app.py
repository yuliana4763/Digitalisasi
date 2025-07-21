import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
from datetime import date

# Fungsi: Membuat HTML lengkap
def generate_full_html(data):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 40px; }}
            .cover {{
                text-align: center;
                margin-top: 100px;
            }}
            .cover h1 {{
                font-size: 32px;
                color: #1a237e;
            }}
            .cover p {{
                font-size: 18px;
                margin: 5px;
            }}
            .section {{
                margin-top: 50px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
        </style>
    </head>
    <body>
        <div class="cover">
            <h1>{data['judul']}</h1>
            <p><strong>Silabus Pelatihan Micro Skill</strong></p>
            <p>{data['nama_penyusun']}</p>
            <p>{data['instansi']}</p>
            <p><em>{date.today().strftime('%d %B %Y')}</em></p>
            <hr style="margin-top: 80px;">
        </div>

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
