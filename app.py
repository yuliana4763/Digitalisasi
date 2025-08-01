import streamlit as st
from xhtml2pdf import pisa
from io import BytesIO
import base64
from datetime import datetime
from PIL import Image

# Fungsi untuk mengodekan gambar ke base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"Error: File gambar tidak ditemukan di '{image_path}'. Pastikan path sudah benar dan file ada di direktori yang sama dengan skrip.")
        return None
    except Exception as e:
        st.error(f"Error saat mengodekan gambar '{image_path}': {e}")
        return None

# Fungsi untuk membuat konten sampul dengan judul dinamis
def generate_cover_content_with_title(nama_pelatihan):
    return f"""
    <div style="
        width: 100%; 
        height: 100%; /* Mengisi seluruh tinggi frame yang diberikan */
        display: flex; /* Untuk memudahkan positioning teks */
        align-items: flex-start; /* Untuk menempatkan teks di bagian atas frame */
        justify-content: flex-start; /* Untuk menempatkan teks di bagian kiri frame */
    ">
       <p style="
    font-size: 45px;
    color: black;
    font-weight: 900;
    margin: 0;
    padding-top: 0.5cm;
    padding-left: 0.5cm;
    line-height: 1.2;
    font-family: Calibri, Helvetica, Arial, sans-serif;
">
    {nama_pelatihan}
</p>
    </div>
    """

def generate_info_page(data):
    tanggal = datetime.now().strftime("%d%m%Y")

    version_from_data = data.get('Versi', f"Versi #Silabus-{tanggal}")
    
    judul = data['Nama Pelatihan']
    header = f"""
    <div style="margin-bottom: 10px; ">
        <div style="font-size:16px; font-weight:bold; color:#1a237e;">{version_from_data}</div>
        <div style="font-size:22px; font-weight:bold; margin-top:8px;">Silabus {judul}</div>
        <div style="font-size:16px; margin-top:4px;">Kementerian Komunikasi dan Digital Republik Indonesia</div>
        <div style="font-size:16px; margin-top:2px;">Tahun 2025</div>
    </div>
    """
    disclaimer = """
    <div style="background-color:#fff3cd; color:#856404; border:1px solid #ffeeba; border-radius:6px; padding:16px; margin-bottom:24px;">
        <b>Disclaimer:</b> Dokumen ini digunakan hanya untuk kebutuhan Digital Talent Scholarship Kementerian Komunikasi dan Digital Republik Indonesia. Konten ini mengandung Kekayaan Intelektual, pengguna tunduk kepada undang-undang hak cipta, merek dagang atau hak kekayaan intelektual lainnya. Dilarang untuk memproduksi, memodifikasi, menyebarluaskan, atau mengeksploitasi konten ini dengan cara atau bentuk apapun tanpa persetujuan tertulis dari Digital Talent Scholarship Kementerian Komunikasi dan Digital Republik Indonesia.
    </div>
    """
    return f"""
    <div class="info-page" style="font-family: Arial, sans-serif;">
        {header}
        {disclaimer}
        <table style="width: 100%; border-collapse: collapse; margin-top: 30px;">
            <tr><td style="padding: 8px; width: 35%; border: 1px solid #ddd;"><b>Akademi</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Akademi']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Penyelenggara Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Penyelenggara Pelatihan']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Tema Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Tema Pelatihan']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Nama Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Nama Pelatihan']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Singkatan Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Singkatan Pelatihan']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Durasi Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Durasi Pelatihan']} jam</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Deskripsi Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Deskripsi Pelatihan']}</td></tr>
            <tr><td style="padding: 8px; border: 1px solid #ddd;"><b>Output Pelatihan</b></td><td style="padding: 8px; border: 1px solid #ddd;">{data['Output Pelatihan']}</td></tr>
        </table>
    </div>
    """

def generate_materi_page(topik_materi):
    html = """
    <div class="materi-page" style="font-family: Arial, sans-serif;">
        <h2 style="text-align: center; color: #1a237e;">Informasi Pelatihan Micro Skill</h2>
        <h3 style="text-align: center; color: #1a237e;">Materi dan Konten Pembelajaran</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 30px;">
            <tr style="background-color: #f0f0f0;">
                <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Topik</th>
                <th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Materi</th>
            </tr>
    """
    for topik in topik_materi:
        html += f"""
            <tr>
                <td style="padding: 10px; vertical-align: top; border: 1px solid #ddd;"><b>{topik['topik']}</b></td>
                <td style="padding: 10px; border: 1px solid #ddd;">
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
    encoded_cover_first = encode_image_to_base64("cover1.png") 
    encoded_cover_main = encode_image_to_base64("white.png") 
    encoded_cover_last = encode_image_to_base64("cover2.png") 

    cover_first_bg_url = f"url('data:image/png;base64,{encoded_cover_first}')" if encoded_cover_first else "none"
    cover_main_bg_url = f"url('data:image/png;base64,{encoded_cover_main}')" if encoded_cover_main else "none"
    cover_last_bg_url = f"url('data:image/png;base64,{encoded_cover_last}')" if encoded_cover_last else "none"

    return f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: white; 
            }}

            /* --- DEFAULT PAGE TEMPLATE (Digunakan sebagai dasar untuk mendefinisikan @frame) --- */
            @page {{
                size: A4 portrait;
                margin: 1cm; /* Margin default untuk halaman yang tidak spesifik */

                /* Default frame untuk konten utama - bisa di-override oleh template lain */
                @frame content_frame {{
                    top: 1cm;
                    left: 1cm;
                    width: 19cm; /* 21cm (A4 lebar) - 2cm (margin kiri+kanan) */
                    height: 27.7cm; /* 29.7cm (A4 tinggi) - 2cm (margin atas+bawah) */
                }}

                /* Frame untuk footer - akan diisi oleh elemen dengan id "footerContent" */
                @frame footer_frame {{
                    -pdf-frame-content: footerContent;
                    bottom: 1cm;
                    left: 1cm;
                    width: 19cm; /* Sama dengan lebar content_frame */
                    height: 1cm;
                }}
            }}

            /* --- TEMPLATE HALAMAN SAMPUL PERTAMA --- */
            @page cover_first_template {{
                size: A4 portrait;
                margin: 0; /* Penting: margin 0 untuk halaman sampul agar gambar mengisi penuh */
                background-image: {cover_first_bg_url};
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover; 

                /* DEFINE FRAME FOR TITLE CONTENT ON COVER PAGE */
                @frame cover_title_frame {{
                    top: 15cm; 
                    left: 0.1cm; 
                    width: 15cm; 
                    height: 10cm; 
                    -pdf-frame-content: coverTitleContent; 
                }}
            }}

            /* --- TEMPLATE HALAMAN SAMPUL UTAMA (MAIN COVER) --- */
            @page main_cover_template {{
                size: A4 portrait;
                margin: 0; /* Penting: margin 0 untuk halaman sampul agar gambar mengisi penuh */
                background-image: {cover_main_bg_url};
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
                /* No specific content frame here, as it's meant to be a blank page */
            }}

            /* --- TEMPLATE HALAMAN SAMPUL TERAKHIR --- */
            @page cover_last_template {{
                size: A4 portrait;
                margin: 0; 
                background-image: {cover_last_bg_url};
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }}

            /* --- TEMPLATE HALAMAN KONTEN ISI (misal: Informasi Umum, Materi) --- */
            @page content_page_template {{
                size: A4 portrait;
                /* Adjust margins to give space for the header content (logo + text) */
                margin: 3cm 1cm 2.5cm 1cm; /* Increased top margin */
                background-color: white; /* Pastikan background putih untuk halaman konten */
                background-image: none; /* Pastikan tidak ada gambar di background halaman konten */

                @frame content_frame {{
                    top: 3cm; /* Start content frame below the new header area */
                    left: 1cm;
                    width: 19cm;
                    height: 23.7cm; /* Height adjusted: 29.7 - 3 (top) - 2.5 (bottom) = 24.2 */
                }}
            }}

            /* Styling tabel untuk halaman konten */
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f0f0f0;
            }}
        </style>
    </head>
    <body>
        <pdf:nexttemplate name="cover_first_template" />
        <div id="coverTitleContent">
            {generate_cover_content_with_title(data['Nama Pelatihan'])}
        </div>
        <pdf:nextpage /> 
        
        <pdf:nexttemplate name="main_cover_template" />
        <pdf:nextpage /> 
        
        <pdf:nexttemplate name="content_page_template" />
        {generate_info_page(data, encoded_logo)} <pdf:nextpage />
        {generate_materi_page(topik_materi)}

        <pdf:nexttemplate name="cover_last_template" /> 
        <pdf:nextpage /> 
        
        <div id="footerContent">
            <table style="width:100%; border:none; border-collapse:collapse;">
                <tr>
                    <td style="text-align:left; border:none; padding:0;">Customer No. 417</td>
                    <td style="text-align:right; border:none; padding:0;">Halaman <pdf:pagenumber /> dari <pdf:pagecount /></td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
def save_pdf(html_content, file_name="Silabus_MicroSkill.pdf"):
    result = BytesIO()
    try:
        # --- Tambahan untuk debugging: simpan HTML ke file ---
        try:
            with open("debug_output.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            st.info("HTML mentah disimpan ke 'debug_output.html' untuk debugging.")
        except Exception as e:
            st.warning(f"Gagal menyimpan HTML debug: {e}")
        # --- Akhir tambahan debugging ---

        pisa_status = pisa.CreatePDF(src=html_content, dest=result, encoding='UTF-8')
        result.seek(0)
        if pisa_status.err:
            st.error(f"Error saat membuat PDF: {pisa_status.err}")
            if hasattr(pisa_status, 'log') and pisa_status.log:
                st.error("Pisa Error Log Details:")
                for entry in pisa_status.log:
                    st.error(f"- {entry}")
            return None
        return result
    except Exception as e:
        st.error(f"Terjadi kesalahan tak terduga saat membuat PDF: {e}")
        return None

# --- Pre-defined Syllabus Data ---
syllabus_data = {
    "Mengamankan Diri dari Kejahatan Siber": {
        "data": {
            "Versi": "#Silabus-17012025",
            "Akademi": "Micro Skill (Default)",
            "Penyelenggara Pelatihan": "Pusat Pengembangan Literasi Digital",
            "Tema Pelatihan": "Keamanan Informasi",
            "Nama Pelatihan": "Mengamankan Diri dari Kejahatan Siber",
            "Singkatan Pelatihan": "C02002",
            "Durasi Pelatihan": 1, 
            "Deskripsi Pelatihan": "Kejahatan siber sering terjadi karena adanya celah atau kerentanan dalam sistem keamanan. Untuk itu pelatihan ini menekankan pentingnya mempelajari cara melindungi diri dari kejahatan siber penting untuk mencegah kerugian seperti seperti phishing, malware, ransomware, dan peretasan.",
            "Output Pelatihan": "Setelah mengikuti pelatihan ini, peserta diharapkan dapat:\n1. Memahami tentang Kejahatan Siber\n2. Pengintaian Siber dan Pencegahannya\n3. Memahami informasi yang boleh dibagikan\n4. Pentingnya Menjaga Privasi dan Keamanan di Media Sosial\n5. Etika dalam keamanan data dan informasi di Era Digital\n6. Prinsip Dasar Etika dalam Pengamanan Data\n7. Pentingnya Selektif dalam Berbagi Informasi Pribadi di Era Digital."
        },
        "topik_materi": [
            {"topik": "Memahami Kejahatan Siber", "materi": ["Definisi dan Jenis Kejahatan Siber", "Dampak Kejahatan Siber"]},
            {"topik": "Pengintaian Siber dan Pencegahannya", "materi": ["Teknik Pengintaian Siber (Phishing, Malware, Ransomware)", "Strategi Pencegahan dan Mitigasi Resiko"]},
            {"topik": "Manajemen Informasi Digital", "materi": ["Memahami Informasi yang Boleh Dibagikan", "Pentingnya Menjaga Privasi dan Keamanan di Media Sosial"]},
            {"topik": "Etika dan Hukum dalam Keamanan Data", "materi": ["Etika dalam Keamanan Data dan Informasi di Era Digital", "Prinsip Dasar Etika dalam Pengamanan Data", "Hukum Terkait Keamanan Siber"]},
            {"topik": "Berbagi Informasi Pribadi Secara Aman", "materi": ["Pentingnya Selektif dalam Berbagi Informasi Pribadi di Era Digital", "Tips dan Trik Keamanan Digital"]}
        ]
    },
    "Dasar-dasar Kecerdasan Buatan": {
        "data": {
            "Versi": "#Silabus-30072025",
            "Akademi": "Micro Skill",
            "Penyelenggara Pelatihan": "Kementerian Komunikasi dan Digital",
            "Tema Pelatihan": "Kewirausahaan Digital", # This was "Kewirausahaan Digital" in the image, not "Kecerdasan Artifisial"
            "Nama Pelatihan": "Dasar-dasar Kecerdasan Buatan",
            "Singkatan Pelatihan": "DAI",
            "Durasi Pelatihan": 40,
            "Deskripsi Pelatihan": "Pelatihan ini memperkenalkan konsep dasar Kecerdasan Buatan, algoritma pembelajaran mesin, dan aplikasinya di berbagai bidang.",
            "Output Pelatihan": "Peserta mampu memahami konsep dasar AI, mengimplementasikan algoritma sederhana, dan mengidentifikasi potensi penerapan AI."
        },
        "topik_materi": [
            {"topik": "Pengantar Kecerdasan Buatan", "materi": ["Definisi dan Sejarah AI", "Jenis-jenis AI (ANI, AGI, ASI)", "Peran AI dalam Kehidupan Modern"]},
            {"topik": "Konsep Pembelajaran Mesin", "materi": ["Apa itu Machine Learning?", "Pembelajaran Terawasi (Supervised Learning)", "Pembelajaran Tak Terawasi (Unsupervised Learning)", "Pembelajaran Penguatan (Reinforcement Learning)"]},
            {"topik": "Algoritma Dasar ML", "materi": ["Regresi Linear", "Klasifikasi (Decision Trees, KNN)", "Clustering (K-Means)"]},
            {"topik": "Penerapan AI dalam Berbagai Bidang", "materi": ["AI di Bidang Kesehatan", "AI di Keuangan", "AI di Transportasi", "AI di Pendidikan"]},
            {"topik": "Etika dan Tantangan AI", "materi": ["Bias dalam AI", "Privasi Data", "Keamanan AI", "Masa Depan AI"]}
        ]
    }
}

# STREAMLIT APP
st.set_page_config(layout="centered", page_title="Digitalisasi Silabus Micro Skill")
st.title("Digitalisasi Silabus Micro Skill")
st.markdown("Pilih silabus yang ingin dibuat atau isi data secara manual.")

syllabus_options = list(syllabus_data.keys())
syllabus_options.insert(0, "Buat Silabus Baru (Isi Manual)") # Option to create new

selected_syllabus = st.selectbox("Pilih Silabus", syllabus_options)

current_data = {}
current_topik_materi = []

if selected_syllabus != "Buat Silabus Baru (Isi Manual)":
    current_data = syllabus_data[selected_syllabus]["data"]
    current_topik_materi = syllabus_data[selected_syllabus]["topik_materi"]
    st.session_state.topik_count = len(current_topik_materi) if current_topik_materi else 1
else:
    if "topik_count" not in st.session_state:
        st.session_state.topik_count = 1


with st.form("form_silabus"):
    st.subheader("Informasi Umum")
    akademi = st.text_input("Akademi", value=current_data.get("Akademi", "Micro Skill"))
    penyelenggara_pelatihan = st.text_input("Penyelenggara Pelatihan", value=current_data.get("Penyelenggara Pelatihan", "Kementerian Komunikasi dan Digital"))
    
    tema_options = [
        "Kewirausahaan Digital", "ElevAIte", "Konten Digital", "Cakap Digital",
        "Data Analisis", "Kecerdasan Artifisial", "Keamanan Informasi", "Komunikasi",
        "Pemrograman", "Sistem Manajemen Keamanan Informasi", "Mindset Digital",
        "Teknologi Informasi", "Pengantar SPBE", "Etika dan Budaya Digital",
        "Generative AI untuk Pendidikan", "Ekonomi Digital", "Bisnis Digital",
        "Literasi Digital"
    ]
    # Handle the selected theme based on pre-filled data or default
    initial_tema = current_data.get("Tema Pelatihan", "Kecerdasan Artifisial")
    if initial_tema not in tema_options:
        tema_options.append(initial_tema) # Add it to options if it's a new one
    tema_options.sort() # Keep it sorted if you add new ones
    
    tema_pelatihan = st.selectbox(
        "Tema Pelatihan (pilih atau ketik manual)", 
        options=tema_options + ["Lainnya (isi manual)"],
        index=tema_options.index(initial_tema) if initial_tema in tema_options else (len(tema_options)) # Select if present, or "Lainnya"
    )
    if tema_pelatihan == "Lainnya (isi manual)":
        tema_pelatihan = st.text_input("Tema Pelatihan (isi manual)", value=initial_tema if initial_tema not in tema_options else "")

    nama_pelatihan = st.text_input("Nama Pelatihan", value=current_data.get("Nama Pelatihan", "Dasar-dasar Kecerdasan Buatan"))
    singkatan_pelatihan = st.text_input("Singkatan Pelatihan", value=current_data.get("Singkatan Pelatihan", "DAI"))
    durasi = st.number_input("Durasi (jam)", min_value=1, value=current_data.get("Durasi Pelatihan", 40))
    deskripsi_pelatihan = st.text_area("Deskripsi Pelatihan", value=current_data.get("Deskripsi Pelatihan", "Pelatihan ini memperkenalkan konsep dasar Kecerdasan Buatan, algoritma pembelajaran mesin, dan aplikasinya di berbagai bidang."))
    output_pelatihan = st.text_area("Output Pelatihan", value=current_data.get("Output Pelatihan", "Peserta mampu memahami konsep dasar AI, mengimplementasikan algoritma sederhana, dan mengidentifikasi potensi penerapan AI."))

    st.subheader("Materi Pelatihan")
    # Adjust topik_count based on loaded data or user additions/removals
    display_topik_materi = []
    for i in range(st.session_state.topik_count):
        st.write(f"--- Topik {i+1} ---")
        default_topik = current_topik_materi[i]['topik'] if i < len(current_topik_materi) else ""
        default_materi = ", ".join(current_topik_materi[i]['materi']) if i < len(current_topik_materi) else ""
        
        topik = st.text_input(f"Nama Topik {i+1}", value=default_topik, key=f"topik_{selected_syllabus}_{i}")
        materi = st.text_area(
            f"Materi untuk Topik {i+1} (pisahkan dengan koma)", value=default_materi, key=f"materi_{selected_syllabus}_{i}"
        )
        if topik and materi:
            materi_list = [m.strip() for m in materi.split(",") if m.strip()]
            display_topik_materi.append({"topik": topik, "materi": materi_list})
        elif st.session_state.topik_count > 1 and (not topik or not materi):
            st.warning(f"Topik {i+1} atau Materinya kosong, tidak akan disertakan dalam PDF.")

    col1, col2 = st.columns(2)
    with col1:
        add_topik_button = st.form_submit_button("➕ Tambah Topik Baru", on_click=lambda: st.session_state.update(topik_count=st.session_state.topik_count + 1))
    with col2:
        remove_topik_button = st.form_submit_button("➖ Hapus Topik Terakhir", on_click=lambda: st.session_state.update(topik_count=max(1, st.session_state.topik_count - 1)))

    submit = st.form_submit_button("🚀 Buat PDF Silabus")

if submit:
    # Use the form's current values, which are either pre-filled or manually entered
    final_data = {
        "Akademi": akademi,
        "Penyelenggara Pelatihan": penyelenggara_pelatihan,
        "Tema Pelatihan": tema_pelatihan,
        "Nama Pelatihan": nama_pelatihan,
        "Singkatan Pelatihan": singkatan_pelatihan,
        "Durasi Pelatihan": durasi,
        "Deskripsi Pelatihan": deskripsi_pelatihan,
        "Output Pelatihan": output_pelatihan,
        "Versi": current_data.get('Versi', datetime.now().strftime("Versi #Silabus-%d%m%Y")) # Keep existing version or generate new
    }

    filtered_topik_materi = [t for t in display_topik_materi if t['topik'] and t['materi']]

    html_result = generate_full_html(final_data, filtered_topik_materi)
    
    # Determine filename based on selected syllabus or custom name
    if selected_syllabus == "Buat Silabus Baru (Isi Manual)":
        file_name = f"Silabus_{final_data['Nama Pelatihan'].replace(' ', '_')}.pdf"
    else:
        file_name = f"Silabus_{selected_syllabus.replace(' ', '_')}.pdf"

    pdf_file = save_pdf(html_result, file_name=file_name)

    if pdf_file:
        st.success("✅ PDF berhasil dibuat!")
        st.download_button(
            label="📥 Unduh Silabus PDF",
            data=pdf_file,
            file_name=file_name,
            mime="application/pdf"
        )
    else:
        st.error("❌ Gagal membuat PDF. Periksa kembali log untuk detailnya.")