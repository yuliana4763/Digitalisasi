import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")

def generate_cover_page(image_path, page_break="after"):
    encoded_image = encode_image_to_base64(image_path)
    return f"""
    <div class="page" style="page-break-{page_break}: always;">
        <img src="data:image/png;base64,{encoded_image}" style="width: 100%; height: 100vh; object-fit: cover;">
    </div>
    """

def generate_info_page(data):
    return f"""
    <div class="page info" style="page-break-before: always; font-family: Arial, sans-serif;">
        <h2 style="text-align: center; color: #1a237e;">Informasi Umum Pelatihan</h2>
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
                <th style="padding: 10px; text-align: left;">Topik</th>
                <th style="padding: 10px; text-align: left;">Materi</th>
            </tr>
    """
    for topik in topik_materi:
        html += f"""
            <tr>
                <td style="padding: 10px; vertical-align: top;"><b>{topik['topik']}</b></td>
                <td style="padding: 10px;">
                    <ul style="margin: 0; padding-left: 18px;">
        """
        for materi in topik["materi"]:
            html += f"<li>{materi}</li>"
        html += """
                    </ul>
                </td>
            </tr>
        """
    html += """
        </table>
    </div>
    """
    return html

def generate_full_html(data, topik_materi):
    cover1_path = r"C:\Data Backup\KOMDIGI RI\digitalisasi silabus\silabus_microskill_app\Cover 1.png"
    cover2_path = r"C:\Data Backup\KOMDIGI RI\digitalisasi silabus\silabus_microskill_app\Cover 2.png"
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .page {{ page-break-after: always; }}
            .cover {{ text-align: center; margin-top: 150px; color: #0066cc; }}
            .info {{ margin-top: 40px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #333; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        {generate_cover_page(cover1_path, "after")}
        {generate_info_page(data)}
        {generate_materi_page(topik_materi)}
        {generate_cover_page(cover2_path, "before")}
    </body>
    </html>
    """

def save_pdf(html_content):
    result = BytesIO()
    pisa.CreatePDF(src=html_content, dest=result)
    result.seek(0)
    return result

# STREAMLIT APP
st.title("Digitalisasi Silabus Micro Skill")
st.markdown("Isi data berikut untuk membuat silabus pelatihan secara otomatis dalam format PDF.")

with st.form("form_silabus"):
    st.subheader("Informasi Umum")
    akademi =  st.text_input("Akademi")
    penyelenggara_pelatihan = st.text_input("Penyelenggara Pelatihan")
    tema_pelatihan = st.text_input("Tema Pelatihan")
    nama_pelatihan = st.text_input("Nama Pelatihan")
    singkatan_pelatihan = st.text_input("Singkatan Pelatihan")
    durasi = st.number_input("Durasi (jam)", min_value=1)
    deskripsi_pelatihan = st.text_area("Deskripsi Pelatihan")
    output_pelatihan = st.text_area("Output Pelatihan")

    st.subheader("Materi Pelatihan")
    topik_materi = []
    for i in range(1, 4):
        topik = st.text_input(f"Topik {i}", key=f"topik_{i}")
        materi = st.text_area(f"Materi untuk Topik {i} (pisahkan dengan koma)", key=f"materi_{i}")
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

    html_result = generate_full_html(data, topik_materi)
    pdf_file = save_pdf(html_result)

    st.success("✅ PDF berhasil dibuat!")
    st.download_button(
        label="📥 Download Silabus PDF",
        data=pdf_file,
        file_name="Silabus_MicroSkill.pdf",
        mime="application/pdf"
    )
