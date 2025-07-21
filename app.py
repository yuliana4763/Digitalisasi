import streamlit as st
import pdfkit
import os
from datetime import date

# Konfigurasi pdfkit untuk Linux (Google Colab)
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")

def generate_html(data):
    html_template = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #1a237e; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            td, th {{ padding: 10px; border: 1px solid #999; }}
        </style>
    </head>
    <body>
        <h1>Silabus Pelatihan Micro Skill</h1>
        <p><strong>Judul Pelatihan:</strong> {data['judul']}</p>
        <p><strong>Deskripsi:</strong> {data['deskripsi']}</p>
        <p><strong>Durasi:</strong> {data['durasi']} jam</p>
        <p><strong>Target Peserta:</strong> {data['peserta']}</p>
        <p><strong>Tujuan Pembelajaran:</strong> {data['tujuan']}</p>

        <h3>Materi:</h3>
        <table>
            <tr>
                <th>No</th><th>Topik</th><th>Subtopik</th>
            </tr>
    """
    for idx, (topik, subtopik) in enumerate(zip(data['topik'], data['subtopik']), 1):
        html_template += f"""
            <tr>
                <td>{idx}</td><td>{topik}</td><td>{subtopik}</td>
            </tr>
        """
    html_template += """
        </table>
        <br><p><em>Dibuat pada tanggal {}</em></p>
    </body>
    </html>
    """.format(date.today().strftime("%d %B %Y"))

    return html_template

def save_pdf(html, filename):
    pdfkit.from_string(html, filename, configuration=PDFKIT_CONFIG)

# Streamlit App
st.title("Generator Silabus Micro Skill (PDF)")

with st.form("silabus_form"):
    judul = st.text_input("Judul Pelatihan")
    deskripsi = st.text_area("Deskripsi")
    durasi = st.number_input("Durasi (jam)", min_value=1)
    peserta = st.text_input("Target Peserta")
    tujuan = st.text_area("Tujuan Pembelajaran")

    topik = []
    subtopik = []
    for i in range(1, 4):
        topik.append(st.text_input(f"Topik {i}", key=f"topik_{i}"))
        subtopik.append(st.text_input(f"Subtopik {i}", key=f"subtopik_{i}"))

    submitted = st.form_submit_button("Buat PDF")

if submitted:
    data = {
        "judul": judul,
        "deskripsi": deskripsi,
        "durasi": durasi,
        "peserta": peserta,
        "tujuan": tujuan,
        "topik": topik,
        "subtopik": subtopik
    }

    html = generate_html(data)
    filename = "/content/Silabus_MicroSkill.pdf"
    save_pdf(html, filename)

    with open(filename, "rb") as file:
        st.success("✅ PDF berhasil dibuat!")
        st.download_button(
            label="📥 Download Silabus PDF",
            data=file,
            file_name="Silabus_MicroSkill.pdf",
            mime="application/pdf"
        )
