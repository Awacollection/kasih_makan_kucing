import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
import base64
from openai import OpenAI
from theme import apply_black_green_theme
import json

load_dotenv()

st.set_page_config(
    page_title="Referensi Ide Konten",
    layout="wide"
)

apply_black_green_theme()

st.title("Referensi Ide Konten")

# ===== GEMINI VISION CONFIG =====
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# ===== OPENAI VISION CONFIG =====

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_PROXY_BASE_URL = os.getenv("OPENAI_PROXY_BASE_URL", "")
OPENAI_PROXY_MODEL = os.getenv("OPENAI_PROXY_MODEL", "openai/gpt-5.2-2025-12-11")

openai_client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_PROXY_BASE_URL
) if OPENAI_API_KEY and OPENAI_PROXY_BASE_URL else None

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ===== GEMINI AUTO PHOTO ANALYSIS FUNCTION =====
def analyze_image_with_gemini(uploaded_file, analysis_type="model"):
    if not GEMINI_API_KEY:
        return "GEMINI_API_KEY belum diisi di file .env."



    if uploaded_file is None:
        return "Belum ada gambar yang diupload."

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file).convert("RGB")

        model = genai.GenerativeModel("gemini-2.0-flash-lite")

        if analysis_type == "model":
            prompt = """
Analyze this uploaded mother-and-child model reference image for AI video prompt generation.

Return the analysis in Indonesian.

Focus on:
- siapa saja yang terlihat di foto
- posisi ibu
- posisi anak
- posisi tangan ibu
- posisi tangan anak
- apakah tangan ibu menyentuh pakaian anak atau tidak
- apakah tangan ibu dekat dengan area dada, kancing, kerah, atau peplum
- arah wajah ibu dan anak
- ekspresi ibu dan anak
- jarak ibu dan anak
- apakah cocok dibuat selfie front-camera atau lebih cocok direkam orang lain
- risiko gesture yang bisa membuat AI video salah, seperti ibu menunjuk kancing, menyentuh pakaian, atau kamera terasa lepas
- saran alur video yang aman mengikuti pose foto

Use concise bullet points.
"""
        else:
            prompt = """
Analyze this uploaded product reference image for AI video prompt generation.

Return the analysis in Indonesian.

Focus on:
- jenis produk
- apakah produk berupa atasan, celana, setelan, dress, rok, romper, atau lainnya
- struktur pakaian
- lengan
- kerah
- kancing
- jumlah kancing
- bentuk dan bahan kancing jika terlihat
- motif
- arah garis/motif
- warna
- ruffle/rampel
- peplum
- celana/rok/bawahan
- detail yang wajib dipertahankan
- detail yang tidak boleh berubah saat dibuat video AI

Use concise bullet points.
"""

        response = model.generate_content([prompt, image])
        return response.text.strip()

    except Exception as e:
        return f"GEMINI ANALYSIS ERROR: {e}"
# ===== OPENAI AUTO PHOTO ANALYSIS FUNCTION =====
def analyze_image_with_openai(uploaded_file, analysis_type="model"):
    if not OPENAI_API_KEY or openai_client is None:
        return "OPENAI_API_KEY belum diisi di file .env."

    if uploaded_file is None:
        return "Belum ada gambar yang diupload."

    try:
        uploaded_file.seek(0)
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        if analysis_type == "model":
            prompt = """
Analyze this uploaded mother-and-child model reference image for AI video prompt generation.

Return the analysis in Indonesian.

Focus on:
- siapa saja yang terlihat di foto
- posisi ibu
- posisi anak
- posisi tangan ibu
- posisi tangan anak
- apakah tangan ibu menyentuh pakaian anak atau tidak
- apakah tangan ibu dekat dengan area dada, kancing, kerah, atau peplum
- arah wajah ibu dan anak
- ekspresi ibu dan anak
- jarak ibu dan anak
- apakah cocok dibuat selfie front-camera atau lebih cocok direkam orang lain
- risiko gesture yang bisa membuat AI video salah
- saran alur video yang aman mengikuti pose foto

Use concise bullet points.
"""
        else:
            prompt = """
Analyze this uploaded product reference image for AI video prompt generation.

Return the analysis in Indonesian.

Focus on:
- jenis produk
- apakah produk berupa atasan, celana, setelan, dress, rok, romper, atau lainnya
- struktur pakaian
- lengan
- kerah
- kancing
- jumlah kancing
- bentuk dan bahan kancing jika terlihat
- motif
- arah garis/motif
- warna
- ruffle/rampel
- peplum
- celana/rok/bawahan
- detail yang wajib dipertahankan
- detail yang tidak boleh berubah saat dibuat video AI

Use concise bullet points.
"""

        response = openai_client.responses.create(
            model=OPENAI_PROXY_MODEL,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    ]
                }
            ]
        )

        return response.output_text.strip()

    except Exception as e:
        return f"OPENAI ANALYSIS ERROR: {e}"
# ===== DATA KATEGORI BERTINGKAT =====
KATEGORI = {
    'Kategori A': {
        'Kesehatan': {
            'Hand Sanitizer': None,
            'Perawatan Mata': None,
            'Perawatan Telinga': None,
            'Perawatan Mulut': None,
            'Popok Dewasa': None,
            'Kewanitaan': None,
            'Alat Pijat dan Terapi': None,
            'Obat Nyamuk': None,
            'Perawatan Diri lainnya': None,
        },
        'Aksesori Fesyen': {
            'Cincin': None,
            'Anting': None,
            'Syal dan Selendang': None,
            'Sarung Tangan': None,
            'Aksesori Rambut': None,
            'Gelang Tangan dan Bangle': None,
            'Gelang Kaki': None,
            'Topi': None,
            'Kalung': None,
            'Kacamata dan Aksesori': None,
            'Ikat Pinggang': None,
            'Dasi': None,
            'Bros dan Pin': None,
            'Bordir': None,
            'Liontin': None,
            'Kancing Manset': None,
            'Tato Temporer': None,
            'Masker': None,
            'Sapu Tangan': None,
            'Aksesori Tambahan lainnya': None,
            'Set dan Paket Aksesori': None,
            'Aksesori Fesyen lainnya': None,
        },
        'Elektronik (Kelistrikan)': {
            'Stop Kontak dan Sambungan Kabel': None,
            'Pengaman Stop Kontak': None,
            'Penghemat Listrik': None,
            'Bel': None,
            'Saklar': None,
            'Alarm': None,
            'Anti Petir': None,
            'Kelistrikan lainnya': None,
        },
        'Pakaian Pria': {
            'Celana Panjang Jeans': None,
            'Hoodie dan Sweatshirt': None,
            'Sweater dan Cardigan': None,
            'Jaket': None,
            'Mantel': None,
            'dan Rompi': None,
            'Jas Formal': None,
            'Celana Panjang': None,
            'Celana Pendek': None,
            'Atasan': None,
            'Pakaian Dalam': None,
            'Pakaian Tidur': None,
            'Set Pakaian Pria': None,
            'Pakaian Tradisional': None,
            'Kostum': None,
            'Pakaian Kerja': None,
            'Kaos Kaki': None,
            'Pakaian Pria lainnya': None,
        },
        'Sepatu Pria': {
            'Boot': None,
            'Sneakers': None,
            'Slip-On dan Mules': None,
            'Loafer': None,
            'Oxford': None,
            'Sandal': None,
            'Alat Perawatan dan Pembersih Sepatu': None,
            'Parfum Sepatu': None,
            'Tali Sepatu': None,
            'Shoe Tree dan Horns': None,
            'Insole Sepatu': None,
            'Aksesori dan Perawatan Sepatu lainnya': None,
            'Sepatu Pria lainnya': None,
        },
        'Handphone dan Aksesori': {
            'Kartu Perdana': None,
            'Handphone dan Aksesori lainnya': None,
            'Smartwatch dan Fitness Tracker': None,
            'Perangkat VR': None,
            'Pelacak GPS': None,
            'Perangkat Wearable lainnya': None,
            'Tongsis': None,
            'Lazypod': None,
            'Tomsis': None,
            'Aksesori Selfie lainnya': None,
            'Lensa Tambahan Handphone': None,
            'Flash dan Lampu Selfie Handphone': None,
            'Kipas USB': None,
            'Stylus': None,
            'Phone Holder': None,
            'Tali dan Gantungan Handphone': None,
            'Pouch Handphone': None,
            'Casing': None,
            'Penggulung': None,
            'dan Pengikat Kabel': None,
            'Travel Adaptor': None,
            'Kabel dan Adaptor Handphone': None,
            'Charger': None,
            'Charger Docking': None,
            'Kabel': None,
            'Charger dan Adaptor lainnya': None,
            'Baterai': None,
            'Powerbank': None,
            'Powercase': None,
            'Powerbank dan Baterai lainnya': None,
            'Aksesori Perangkat Wearable': None,
            'Pelindung Layar Handphone': None,
            'Casing dan Skin': None,
            'Aksesori lainnya': None,
        },
        'Fesyen Muslim': {
            'Hijab': None,
            'Aksesori Hijab': None,
            'Kaos Kaki': None,
            'Handsock': None,
            'Aksesori lainnya': None,
            'Baju Olahraga Muslim': None,
            'Baju Renang Muslim': None,
            'Tunik': None,
            'Kemeja': None,
            'Blouse dan Dalaman Blouse': None,
            'Atasan Menyusui': None,
            'Atasan Muslim lainnya': None,
            'Gamis': None,
            'Abaya': None,
            'Dress Menyusui': None,
            'Kaftan': None,
            'Baju Kelelawar': None,
            'Baju Kurung': None,
            'Set Baju Muslim': None,
            'Jumpsuit': None,
            'Dress Muslim lainnya': None,
            'Rok': None,
            'Celana Panjang': None,
            'Legging': None,
            'Celana Palazzo': None,
            'Bawahan Muslim lainnya': None,
            'Pakaian Muslim Wanita lainnya': None,
            'Set Perlengkapan Sholat': None,
            'Sajadah': None,
            'Peci': None,
            'Mukena Dewasa': None,
            'Mukena Travel': None,
            'Mukena dan Perlengkapan Sholat lainnya': None,
            'Atasan': None,
            'Gamis Pria': None,
            'Celana': None,
            'Sarung': None,
            'Baju Melayu': None,
            'Pakaian Muslim Pria lainnya': None,
            'Hijab Anak': None,
            'Mukena Anak': None,
            'Pakaian dan Set Muslim Anak': None,
            'Pakaian Muslim Anak Perempuan lainnya': None,
            'Pakaian Muslim Anak Laki-Laki': None,
            'Pakaian Muslim Anak lainnya': None,
            'Rompi': None,
            'Jaket': None,
            'Mantel': None,
            'Cardigan': None,
            'Outerwear lainnya': None,
            'Set': None,
            'Fesyen Muslim lainnya': None,
        },
        'Koper dan Tas Travel': {
            'Koper': None,
            'Tas Duffel': None,
            'Tas Lipat': None,
            'Tas Serut': None,
            'Tas Travel lainnya': None,
            'Passport Cover': None,
            'Organizer Travel': None,
            'Pelindung dan Sarung Koper': None,
            'Tag Koper': None,
            'Strap Koper': None,
            'Gembok Koper': None,
            'Timbangan Koper': None,
            'Bantal Leher dan Penutup Mata': None,
            'Botol dan Wadah Isi Ulang': None,
            'Aksesori Travel lainnya': None,
            'Koper dan Tas Travel lainnya': None,
        },
        'Tas Wanita': {
            'Ransel Wanita': None,
            'Tas Laptop': None,
            'Clutch': None,
            'Tas Pinggang Wanita': None,
            'Tote Bag': None,
            'Top Handle Bag': None,
            'Tas Selempang dan Bahu Wanita': None,
            'Dompet Wanita': None,
            'Aksesori Tas': None,
            'Tas Wanita lainnya': None,
        },
        'Pakaian Wanita': {
            'Atasan': None,
            'Celana Panjang dan Legging': None,
            'Celana Pendek': None,
            'Rok': None,
            'Celana Panjang Jeans': None,
            'Dress': None,
            'Wedding Dress': None,
            'Jumpsuit': None,
            'Playsuit': None,
            'dan Overall': None,
            'Jaket': None,
            'Mantel': None,
            'dan Rompi': None,
            'Sweater dan Cardigan': None,
            'Hoodie dan Sweatshirt': None,
            'Set': None,
            'Pakaian Dalam': None,
            'Pakaian Tidur dan Piyama': None,
            'Baju Hamil': None,
            'Pakaian Tradisional': None,
            'Kostum': None,
            'Kain': None,
            'Kaos Kaki dan Stocking': None,
            'Pakaian Wanita lainnya': None,
        },
        'Sepatu Wanita': {
            'Boots': None,
            'Sneakers': None,
            'Sepatu Flat': None,
            'Heels': None,
            'Wedges': None,
            'Sandal Jepit dan Sandal lainnya': None,
            'Aksesori dan Perawatan Sepatu': None,
            'Sepatu Wanita lainnya': None,
        },
        'Tas Pria': {
            'Ransel Pria': None,
            'Tas Laptop': None,
            'Tote Bag': None,
            'Tas Kerja': None,
            'Clutch': None,
            'Tas Pinggang Pria': None,
            'Tas Selempang dan Bahu Pria': None,
            'Dompet': None,
            'Tas Pria lainnya': None,
        },
        'Jam Tangan': {
            'Jam Tangan Wanita': None,
            'Jam Tangan Pria': None,
            'Jam Tangan Couple': None,
            'Aksesori Jam Tangan': None,
            'Jam Tangan lainnya': None,
        },
        'Audio': {
            'Kabel dan Konverter Audio dan Video': None,
        },
        'Makanan dan Minuman': {
            'Biskuit': None,
            'Kue dan Wafer': None,
            'Keripik dan Kerupuk': None,
            'Biji-bijian': None,
            'Popcorn': None,
            'Rumput Laut': None,
            'Kacang': None,
            'Makanan Ringan lainnya': None,
            'Puding': None,
            'Jeli': None,
            'dan Marshmallow': None,
            'Dendeng': None,
            'Buah Kering': None,
            'Abon': None,
            'Snack Seafood': None,
            'Makanan Ringan Kering lainnya': None,
        },
        'Perawatan dan Kecantikan': {
            'Sabun Mandi': None,
            'Scrub dan Peel Tubuh': None,
            'Masker Tubuh': None,
            'Minyak Tubuh': None,
            'Body Cream': None,
            'Body Lotion dan Body Butter': None,
            'Deodoran': None,
            'Minyak Pijat': None,
            'Cream dan Wax Penghilang Bulu Rambut': None,
            'Sun Care': None,
            'Perawatan Payudara': None,
            'Perawatan Tubuh lainnya': None,
            'Perawatan Tangan': None,
            'Perawatan Kaki': None,
            'Perawatan Kuku': None,
            'Perawatan Tangan': None,
            'Kaki dan Kuku lainnya': None,
            'Shampo': None,
            'Pewarna Rambut': None,
            'Treatment Rambut': None,
            'Kondisioner Rambut dan Kulit Kepala': None,
            'Hair Styling': None,
            'Perawatan Rambut lainnya': None,
            'Perawatan Tubuh Pria': None,
            'Perawatan Wajah Pria': None,
            'Shaving dan Grooming': None,
            'Perawatan Rambut Pria': None,
            'Perawatan Pria lainnya': None,
            'Parfum dan Wewangian': None,
            'Kosmetik lainnya': None,
            'Kosmetik Wajah': None,
            'Kosmetik Mata': None,
            'Kosmetik Bibir': None,
            'Pembersih Make Up': None,
            'Aksesori Make Up': None,
            'Alat Perawatan Wajah': None,
            'Alat Pelangsing Tubuh': None,
            'Alat Penghilang Bulu Rambut': None,
            'Alat Rambut': None,
            'Alat Kecantikan lainnya': None,
            'Pembersih Wajah': None,
            'Toner': None,
            'Pelembab Wajah': None,
            'Minyak Wajah': None,
            'Facial Mist': None,
            'Serum dan Essence Wajah': None,
            'Scrub dan Peel Wajah': None,
            'Masker Wajah': None,
            'Treatment Mata': None,
            'Treatment Bibir': None,
            'Sunscreen Wajah': None,
            'Perawatan Wajah After Sun': None,
            'Kertas Minyak': None,
            'Treatment Jerawat': None,
            'Perawatan Wajah lainnya': None,
            'Paket dan Set Kecantikan': None,
            'Perawatan dan Kecantikan lainnya': None,
        },
        'Ibu dan Bayi': {
            'Perlengkapan Travelling Bayi': None,
            'Perlengkapan Makan Bayi': None,
            'Perlengkapan Mandi': None,
            'Boks dan Matras Tidur Bayi': None,
            'Ayunan Bayi': None,
            'Baby Walker': None,
            'Matras dan Sprei': None,
            'Tempat Penyimpanan': None,
            'Kamar Bayi lainnya': None,
            'Baby Monitor': None,
            'Kelambu': None,
            'Bumper': None,
            'Rail': None,
            'dan Guard': None,
            'Pelindung Sudut': None,
            'Pintu dan Pagar Bayi': None,
            'Pengaman Laci dan Lemari': None,
            'Alat Keamanan Bayi lainnya': None,
            'Perawatan Hidung dan Pernafasan': None,
            'Perawatan Kulit Bayi': None,
            'Perawatan Mulut Bayi': None,
            'Sun Care Bayi': None,
            'Kesehatan Bayi lainnya': None,
            'Perlak': None,
            'Pispot': None,
            'Popok dan Pispot lainnya': None,
            'Mainan Bayi dan Anak': None,
            'Boneka dan Mainan Boneka': None,
            'Mainan Peran': None,
            'Kendaraan Mainan': None,
            'Mainan Olahraga dan Outdoor': None,
            'Mainan Edukatif': None,
            'Mainan Robot': None,
            'Mainan lainnya': None,
            'Set dan Paket Hadiah': None,
            'Ibu dan Bayi lainnya': None,
        },
        'Fesyen Bayi dan Anak': {
    'Pakaian Bayi': None,
    'Sepatu Bayi': None,
    'Aksesori Bayi dan Anak': None,

    'Pakaian Anak Laki-Laki': {
        'Kostum': None,
        'Pakaian Dalam': None,
        'Baju Tidur': None,
        'Baju Renang': None,
        'Atasan': {
            'Kaos': None,
            'Kaos Polo': None,
            'Kemeja': None,
            'Atasan Lainnya': None,
        },
        'Outerwear': {
            'Jaket & Coat Reguler': None,
            'Outerwear Musim Dingin': None,
            'Rompi': None,
            'Sweater & Kardigan': None,
            'Blazer': None,
            'Hoodie': None,
            'Outerwear Lainnya': None,
        },
        'Bawahan': {
            'Jeans': None,
            'Celana Panjang': None,
            'Celana Pendek': None,
            'Bawahan Lainnya': None,
        },
        'Romper, Jumpsuit & Overall': None,
        'Jas & Setelan': None,
        'Pakaian Anak Laki-Laki Lainnya': None,
    },

    'Pakaian Anak Perempuan': {
        'Kostum': None,
        'Pakaian Dalam': None,
        'Baju Tidur': None,
        'Baju Renang': None,
        'Atasan': {
            'Kaos': None,
            'Kaos Polo': None,
            'Kemeja & Blouse': None,
            'Atasan Lainnya': None,
        },
        'Outerwear': {
            'Jaket & Coat Reguler': None,
            'Outerwear Musim Dingin': None,
            'Rompi': None,
            'Sweater & Kardigan': None,
            'Blazer': None,
            'Hoodie': None,
            'Outerwear Lainnya': None,
        },
        'Bawahan': {
            'Jeans': None,
            'Celana Panjang': None,
            'Celana Pendek': None,
            'Rok': None,
            'Legging': None,
            'Bawahan Lainnya': None,
        },
        'Romper, Jumpsuit & Overall': None,
        'Dress': None,
        'Jas & Setelan': None,
        'Pakaian Anak Perempuan Lainnya': None,
    },

    'Sepatu Anak Laki-Laki': None,
    'Sepatu Anak Perempuan': None,
    'Fesyen Bayi dan Anak lainnya': None,
},
        'Kamera dan Drone': {
            'Gimbal dan Stabilizer': None,
            'Lighting dan Perlengkapan Studio Foto': None,
            'Roll Film dan Kertas Foto': None,
            'Printer Foto': None,
            'Charger Baterai': None,
            'Baterai dan Battery Grip': None,
            'Tripod': None,
            'Monopod': None,
            'dan Aksesori': None,
            'Aksesori Kamera lainnya': None,
            'Dry Box dan Cabinet': None,
            'Cleaning Kit': None,
            'Silica Gel': None,
            'Blower': None,
            'Lenspen dan Brush': None,
            'Perawatan Kamera lainnya': None,
            'Kamera dan Drone lainnya': None,
        },
        'Perlengkapan Rumah': {
            'Pengharum Ruangan dan Aromaterapi': None,
            'Kloset dan Alas Dudukan Kloset': None,
            'Tempat Sikat Gigi dan Dispenser Odol': None,
            'Dispenser': None,
            'Tempat': None,
            'dan Kotak Sabun': None,
            'Rak dan Kabinet Kamar Mandi': None,
            'Bak Mandi dan Bathtub': None,
            'Handuk Mandi dan Kimono': None,
            'Kepala Shower dan Spray Bidet': None,
            'Sikat dan Spons Badan': None,
            'Tirai Shower': None,
            'Tempat Duduk Mandi dan Pispot': None,
            'Pegangan Kamar Mandi': None,
            'Shower Cap': None,
            'Kamar Mandi lainnya': None,
            'Matras Pendingin': None,
            'Pelindung Matras': None,
            'Selimut': None,
            'Bantal': None,
            'Sprei': None,
            'Sarung Bantal dan Sarung Guling': None,
            'Matras': None,
            'Kelambu': None,
            'Guling': None,
            'Kamar Tidur lainnya': None,
            'Bunga': None,
            'Furniture dan Pelindung Furniture': None,
            'Tirai dan Tirai Gulung': None,
            'Bingkai Foto dan Pajangan Dinding': None,
            'Wallpaper dan Stiker Dinding': None,
            'Jam Dinding': None,
            'Keset': None,
            'Karpet dan Tikar': None,
            'Vas dan Bejana': None,
            'Lilin dan Tempat Lilin': None,
            'Cermin': None,
            'Taplak Meja': None,
            'Dekorasi lainnya': None,
            'Penghangat Tangan dan Kantong Kompres': None,
            'Bantal Sofa': None,
            'Penahan Pintu': None,
            'Rangka dan Sandaran Tempat Tidur': None,
            'Meja dan Meja Tulis': None,
            'Lemari Pakaian': None,
            'Sofa': None,
            'Lemari dan Kabinet': None,
            'Rak dan Rak Gantung': None,
            'Furniture lainnya': None,
            'Tanaman': None,
            'Dekorasi Taman': None,
            'Tanah dan Media Tanam': None,
            'Pupuk': None,
            'Bibit dan Umbi': None,
            'Pot dan Planter': None,
            'Sistem Pengairan': None,
            'Peralatan Berkebun': None,
            'Taman lainnya': None,
            'Mesin Pemotong Rumput': None,
            'Perekat dan Tape': None,
            'Sarung Tangan': None,
            'Kacamata': None,
            'dan Masker Pelindung': None,
            'Bak Cuci Piring dan Kran Air': None,
            'Atap dan Lantai': None,
            'Cat dan Pelapis Dinding': None,
            'Perkakas': None,
            'Pompa Air dan Aksesori': None,
            'Pompa Udara dan Aksesori': None,
            'Tangga': None,
            'Troli': None,
            'Tenda dan Terpal': None,
            'Material Konstruksi': None,
            'Pintu dan Jendela': None,
            'Alat Pemeliharaan Rumah lainnya': None,
            'Tali Jemuran dan Rak Pengering': None,
            'Sikat Pembersih': None,
            'Sapu': None,
            'Kemoceng': None,
            'Kain Pel': None,
            'Basin': None,
            'Ember': None,
            'dan Gayung Air': None,
            'Spons dan Scouring Pad': None,
            'Tempat Sampah': None,
            'Kantong Plastik dan Kantong Sampah': None,
            'Lap': None,
            'Pembasmi Hama dan Gulma': None,
            'Tisu dan Tisu Kertas': None,
            'Tisu Toilet': None,
            'Pembersih': None,
            'Perawatan Pakaian': None,
            'Perawatan Rumah lainnya': None,
            'Alat dan Aksesori Pemanggang': None,
            'Alat dan Dekorasi Baking': None,
            'Penggorengan': None,
            'Panci': None,
            'Tempat Penyimpanan Makanan': None,
            'Cling Wrap': None,
            'Aluminium Foil': None,
            'Peralatan Teh': None,
            'Kopi dan Bartending': None,
            'Rak Dapur': None,
            'Celemek dan Pelindung Tangan': None,
            'Spatula dan Capitan': None,
            'Talenan': None,
            'Pisau dan Gunting Dapur': None,
            'Pengocok Telur': None,
            'Pembuka Tutup Kaleng dan Botol': None,
            'Gelas dan Sendok Takar': None,
            'Saringan': None,
            'Parutan dan Peeler': None,
            'Timbangan Dapur': None,
            'Korek Api dan Pemantik': None,
            'Perlengkapan Dapur lainnya': None,
            'Peralatan Makan': None,
            'Lampu': None,
            'Brankas': None,
            'Pemadam Api': None,
            'Perangkat Pintu dan Gembok': None,
            'Alat Pengaman lainnya': None,
            'Organizer Rumah': None,
            'Perlengkapan Pesta': None,
            'Perlengkapan Keagamaan': None,
            'Perlengkapan Rumah lainnya': None,
        },
        'Olahraga dan Outdoor': {
            'Alat Pancing': None,
            'Camping dan Hiking': None,
            'Panjat Tebing': None,
            'Skateboard dan Sepatu Roda': None,
            'Skuter dan Sepeda Roda Satu': None,
            'Segway dan Hoverboard': None,
            'Helm dan Alat Pelindung': None,
            'Boardsport lainnya': None,
            'Panahan': None,
            'Sepak Bola': None,
            'Futsal dan Sepak Takraw': None,
            'Basket': None,
            'Voli': None,
            'Bulu Tangkis': None,
            'Tenis': None,
            'Tenis Meja': None,
            'Tinju dan Bela Diri': None,
            'Golf': None,
            'Baseball dan Softball': None,
            'Squash': None,
            'Rugbi': None,
            'Billiard': None,
            'Selancar dan Wakeboard': None,
            'Ice Skating dan Olahraga Musim Dingin': None,
            'Diving dan Renang': None,
            'Boating': None,
            'Yoga dan Pilates': None,
            'Fitness': None,
            'Dart': None,
            'Alat Rekreasi Olahraga dan Aktivitas Outdoor lainnya': None,
            'Sepatu Olahraga': None,
            'Pakaian Olahraga dan Aktivitas Outdoor': None,
            'Aksesori Olahraga dan Aktivitas Outdoor': None,
            'Olahraga dan Outdoor lainnya': None,
        },
        'Buku dan Alat Tulis': {
            'Pembungkus Kado dan Kemasan': None,
            'Alat Tulis': None,
            'Perlengkapan Sekolah dan Kantor': None,
            'Perlengkapan Menggambar': None,
            'Buku Tulis dan Kertas': None,
            'Surat-Menyurat': None,
            'Buku dan Alat Tulis lainnya': None,
        },
        'Hobi dan Koleksi': {
            'Kipas Tangan': None,
            'Gantungan Kunci': None,
            'Celengan': None,
            'Magnet Kulkas': None,
            'Souvenir dan Hadiah lainnya': None,
        },
        'Mobil': {
            'Aksesori Interior Mobil': None,
            'Aksesori Eksterior Mobil': None,
            'Perkakas dan Perlengkapan Kendaraan': None,
            'Perawatan Kendaraan': None,
            'Gantungan dan Sarung Kunci Kendaraan': None,
            'Mobil lainnya': None,
        },
        'Sepeda Motor': {
            'Aksesori Sepeda Motor': None,
            'Suku Cadang Motor': None,
            'Helm dan Aksesori Pengendara Motor': None,
            'Sepeda Motor lainnya': None,
        },
        'Tiket, Voucher, dan Layanan': {
            'Tiket Event': None,
            'Makanan dan Minuman': None,
            'Belanja': None,
            'Listrik': None,
            'Gas': None,
            'dan Air': None,
            'Layanan': None,
            'Telco': None,
            'Travel dan Tour': None,
            'E-Money': None,
            'Gaming': None,
            'Streaming': None,
            'Shopee Official': None,
            'Saldo Iklan Shopee': None,
            'Shopee lainnya': None,
        },
        'Buku dan Majalah': {
            'Majalah dan Koran': None,
            'Buku Bacaan': None,
            'E-Book': None,
            'Buku dan Majalah lainnya': None,
        },
    },
    'Kategori B': {
        'Elektronik': {
            'Telepon': None,
            'Water Heater': None,
            'Penghangat Ruangan': None,
            'Barang Kebutuhan Sehari-hari (Kesehatan': None,
            'Makanan dan Minuman': None,
            'Ibu dan Bayi)': None,
            'Hewan Peliharaan': None,
            'Hobi dan Koleksi': None,
            'Aksesori Komputer': None,
        },
        'Handphone dan Aksesori': {
            'Alat Casting': None,
            'Walkie Talkie': None,
            'Kartu Memori': None,
            'USB dan Lampu Handphone': None,
            'Modem': None,
        },
        'Audio': {
            'MP3 dan MP4 Player': None,
            'CD': None,
            'DVD': None,
            'dan Blu-ray Player': None,
            'Radio dan Pemutar Kaset': None,
            'Amplifier dan Mixer': None,
            'Home Theater dan Karaoke': None,
            'Earphone': None,
            'Headphone': None,
            'dan Headset': None,
            'Voice Recorder': None,
            'Media Player lainnya': None,
            'Mikrofon dan Aksesori': None,
            'Speaker': None,
            'AV Receiver': None,
            'Perangkat Audio dan Speaker lainnya': None,
            'Audio lainnya': None,
        },
        'Gaming dan Konsol': {
            'Playstation': None,
            'Xbox': None,
            'Wii': None,
            'Nintendo 3DS dan DS': None,
            'Gameboy': None,
            'Switch': None,
            'PS Vita': None,
            'PSP': None,
            'Konsol Game lainnya': None,
     
       'Aksesori Konsol': None,
            'Video Game': None,
            'Gaming dan Konsol lainnya': None,
        },
        'Kamera dan Drone': {
            'Kamera CCTV': None,
            'Kamera Keamanan': None,
            'Lensa': None,
            'Aksesori Lensa': None,
            'Aksesori Kamera lainnya': None,
        },
        'Mobil': {
            'Mobil': None,
            'Suku Cadang Mobil': None,
            'Oli dan Pelumas Kendaraan. Sepeda Motor': None,
        },
        'Komputer dan Aksesori': {
            'Peralatan Kantor': None,
            'Printer dan Scanner': None,
            'Aksesori Desktop dan Laptop': None,
            'Modem dan Router Wireless': None,
            'Repeater': None,
            'Wireless Adapter dan Kartu Network': None,
            'Powerline Adapter': None,
            'Switch Internet dan PoE': None,
            'Kabel Network dan Konektor': None,
            'KVM Switch': None,
            'Print Server': None,
            'Komponen Network lainnya': None,
            'Software': None,
            'Peralatan Kantor lainnya': None,
            'Tinta Printer': None,
            'Printer dan Scanner lainnya': None,
            'USB HUB dan Card Reader': None,
            'Pelindung Laptop dan Skin Laptop': None,
            'Cooling Pad': None,
            'Meja dan Stand Laptop': None,
            'Pelindung Keyboard dan Trackpad': None,
            'Baterai Laptop': None,
            'Charger dan Adaptor Laptop': None,
            'Mouse Pad': None,
            'Aksesori Desktop dan Laptop lainnya': None,
            'Mouse': None,
            'Keyboard': None,
            'Drawing Tablet': None,
            'Keyboard dan Mouse lainnya': None,
            'Komputer dan Aksesori lainnya': None,
        },
        'Kesehatan': {
            'Diet dan Detoks': None,
            'Suplemen Kecantikan': None,
            'Kebugaran': None,
            'Kesejahteraan': None,
            'Suplemen Makanan lainnya': None,
            'Kesehatan lainnya': None,
            'Obat Bebas': None,
            'Obat Tradisional': None,
            'Alat Tes dan Monitor': None,
            'Timbangan dan Alat Ukur Kadar Lemak': None,
            'Perawatan Hidung dan Pernafasan': None,
            'P3K': None,
            'Stetoskop': None,
            'Obat Pereda Nyeri': None,
            'Alat Laboratorium': None,
            'Sarung Tangan dan Masker Medis': None,
            'Alat Bantu Cedera dan Disabilitas': None,
            'Alat Medis lainnya': None,
            'Kondom': None,
            'Pelumas': None,
            'Penunjang Performa': None,
            'Kesehatan Seksual lainnya': None,
        },
        'Makanan dan Minuman': {
            'Makanan Instant': None,
            'Permen': None,
            'Cokelat': None,
            'Makanan Kaleng': None,
            'Kopi': None,
            'Teh': None,
            'Minuman Coklat': None,
            'Susu': None,
            'Minuman Energi dan Isotonik': None,
            'Air Mineral': None,
            'Jus dan Sirup': None,
            'Cordial dan Sirup': None,
            'Minuman Bersoda': None,
            'Minuman Bubuk Instan': None,
            'Minuman Pencuci Mulut': None,
            'Minuman Tradisional dan Herbal': None,
            'Topping Minuman': None,
            'Susu Non-Dairy': None,
            'Minuman lainnya': None,
            'Yoghurt': None,
            'Krimer': None,
            'Mentega dan Margarin': None,
            'Keju': None,
            'Tahu': None,
            'Susu dan Olahan lainnya': None,
            'Roti dan Kue': None,
            'Minuman Alkohol': None,
            'Set Hadiah dan Hampers': None,
            'Makanan dan Minuman lainnya. Hewan Peliharaan: Makanan Hewan': None,
            'Aksesori Hewan Peliharaan': None,
            'Litter dan Toilet': None,
            'Grooming Hewan': None,
            'Pakaian dan Aksesori Hewan': None,
            'Perawatan Kesehatan Hewan': None,
            'Hewan Peliharaan lainnya': None,
        },
        'Ibu dan Bayi': {
            'Pompa ASI dan Aksesori': None,
            'Penyangga Perut': None,
            'Bantal Ibu Hamil': None,
            'Perlengkapan Ibu Hamil lainnya': None,
            'Susu Ibu Hamil': None,
            'Vitamin dan Suplemen Ibu Hamil': None,
            'Pelembab dan Cream': None,
            'Kesehatan Kehamilan lainnya': None,
            'Popok Sekali Pakai': None,
            'Popok Kain dan Aksesori': None,
            'Mainan Balok': None,
            'Puzzle': None,
            'Mainan Slime dan Squishy': None,
        },
        'Perlengkapan Rumah': {
            'Kursi Taman': None,
            'Kursi': None,
            'dan Bangku': None,
        },
        'Olahraga dan Outdoor': {
            'Sepeda': None,
            'Komponen dan Aksesori Sepeda': None,
            'Helm Sepeda': None,
            'Bersepeda lainnya': None,
        },
        'Hobi dan Koleksi': {
            'Action Figure': None,
            'Patung': None,
            'Mecha Model dan Diecast': None,
            'Vehicle Model dan Diecast': None,
            'Batu Akik dan Alam': None,
            'Koleksi Penggemar': None,
            'Koleksi Olahraga': None,
            'Koleksi Anime dan Manga': None,
            'Koin dan Uang Kertas': None,
            'Koleksi lainnya': None,
            'Mainan dan Games': None,
            'CD': None,
            'DVD dan Bluray': None,
            'Alat dan Aksesori Musik': None,
            'Piringan Hitam': None,
            'Album Foto': None,
            'Perlengkapan Menjahit': None,
            'Hobi dan Koleksi lainnya': None,
        },
    },
    'Kategori C': {
        'Aksesori Fesyen': {
            'Logam Mulia': None,
            'Perhiasan Berharga': None,
        },
        'Elektronik': {
            'TV': None,
            'Alat Elektronik Tambahan': None,
            'Aksesori Handphone': None,
            'Pointer': None,
            'Proyektor': None,
            'Layar Proyektor dan Aksesori lainnya': None,
            'Mesin Jahit dan Aksesori': None,
            'Setrika dan Mesin Uap': None,
            'Purifier': None,
            'Humidifier': None,
            'Penyedot Debu dan Peralatan Perawatan Lantai': None,
            'Mesin Cuci dan Pengering': None,
            'Mesin Cuci dan Pengering': None,
            'Pendingin Ruangan': None,
            'Dispenser dan Filter Air': None,
            'Pemanas Air': None,
            'Kulkas Wine': None,
            'Juicer': None,
            'Blender dan Mesin Kacang Kedelai': None,
            'Mesin Kopi dan Aksesori': None,
            'Mixer': None,
            'Dishwashers': None,
            'Kompor dan Regulator Gas': None,
            'Air Fryer': None,
            'Deep Fryer': None,
            'Microwave': None,
            'Oven': None,
            'Pemanggang Roti': None,
            'Food Processor dan Penggiling Daging': None,
            'Alat Masak Serbaguna': None,
            'Panci Presto': None,
            'Slow Cooker dan Mesin Sous Vide': None,
            'Penanak Nasi': None,
            'Pembuat Waffle dan Crepe': None,
            'Perebus Telur': None,
            'Pembuat Roti': None,
            'Pembuat Takoyaki': None,
            'Pembuat Dessert': None,
            'Pembuat Soda': None,
            'Kulkas': None,
            'Freezer': None,
            'Penghisap Asap Dapur': None,
            'Perangkat Dapur dan Peralatan Masak Khusus lainnya': None,
        },
        'Handphone dan Aksesori': {
            'Tablet': None,
            'Handphone': None,
        },
        'Fesyen Bayi dan Anak': {
            'Perhiasan Bayi dan Anak': None,
        },
        'Kamera dan Drone': {
            'Kamera Pocket': None,
            'Kamera Mirrorless': None,
            'Kamera Action': None,
            'Camcorder': None,
            'Kamera Instan': None,
            'Kamera Analog': None,
            'DSLR': None,
            'Kamera dan Drone lainnya Flash': None,
            'Aksesori Flash': None,
            'Drone': None,
            'Aksesori Drone': None,
        },
        'Komputer dan Aksesori': {
            'PC Desktop': None,
            'PC Mini': None,
            'Server PC': None,
            'All-in-One Desktop': None,
            'Laptop': None,
            'Desktop lainnya': None,
            'Monitor': None,
            'Fan dan Heatsink': None,
            'Processor': None,
            'Motherboard': None,
            'VGA Card': None,
            'Thermal Paste': None,
            'Power Supply': None,
            'Memory RAM': None,
            'UPS dan Stabilizer': None,
            'Casing Komputer': None,
            'Optical Drive': None,
            'Sound Card': None,
            'Komponen Desktop dan Laptop lainnya': None,
            'Hard Disk': None,
            'SSD': None,
            'Network Attached Storage (NAS)': None,
            'Flashdisk dan Flashdisk OTG': None,
            'Casing Hard Disk dan Docking': None,
            'Compact Disc (CD)': None,
            'Penyimpanan Data lainnya': None,
        },
        'Makanan dan Minuman': {
            'Makanan Kering': None,
            'Mie': None,
            'Beras': None,
            'Pasta': None,
            'Bahan Pokok lainnya': None,
            'Acar Sayuran': None,
            'Minyak': None,
            'Bumbu Masak': None,
            'Gula': None,
            'Pemanis': None,
            'Kaldu': None,
            'Saus dan Sup Instan': None,
            'Bumbu Masak Instant': None,
            'Penambah Rasa': None,
            'Tepung Bumbu': None,
            'Kebutuhan Memasak lainnya': None,
            'Penyedap Kue': None,
            'Baking Powder dan Soda Kue': None,
            'Tepung Premix Instan': None,
            'Tepung': None,
            'Pewarna Makanan': None,
            'Bahan Dekorasi Kue': None,
            'Bahan Baking lainnya': None,
            'Madu dan Olesan': None,
            'Selai dan Olesan': None,
            'Sereal': None,
            'Granola': None,
            'dan Oat': None,
            'Bar Sereal': None,
            'Menu Sarapan lainnya': None,
            'Es Krim': None,
            'Telur': None,
            'Daging': None,
            'Seafood': None,
            'Daging Vegetarian': None,
            'Makanan Segar dan Beku lainnya': None,
            'Sayuran': None,
            'Buah-buahan': None,
            'Jamur': None,
            'Makanan Beku Olahan': None,
            'Daging dan Seafood Beku': None,
        },
        'Ibu dan Bayi': {
            'Susu Formula': None,
            'Bubur dan Sereal Bayi': None,
            'Camilan Bayi': None,
            'Susu Formula dan Makanan Bayi lainnya': None,
            'Vitamin dan Suplemen Bayi': None,
        },
        'Perlengkapan Rumah': {
            'Sealer': None,
        },
    },
    'Kategori D': {
        'Elektronik': {
            'TV dan Aksesori dari kategori B menjadi C mulai 1 September 2': None,
        },
        'Komputer dan Aksesori': {
            'Penyimpanan Data: Dari kategori C menjadi D - Komponen Desktop dan Laptop: Dari kategori C - Desktop Komputer: Dari kategori C menjadi D - Laptop: Dari kategori C menjadi D - Monitor: Dari kategori C menjadi D Rekomendasi Produk - Peralatan Kantor: Dari kategori B menjadi D - Printer dan Scanner: : Dari kategori B menjadi D - Proyektor dan Aksesori: Dari kategori C menjadi D 3': None,
        },
        'Handphone dan Tablet': {
            'Handphone: Dari kategori C menjadi D 4': None,
        },
        'Fesyen Bayi dan Anak': {
            'Perhiasan Dari kategori C menjadi D 5': None,
        },
        'Aksesori Fesyen': {
            'Logam Mulia dan Perhiasan Berharga dari kategori C menjadi D': None,
        },
    },
}


# ===== FUNGSI BANTU UNTUK MERAPIKAN KATEGORI =====
def gabungkan_dict_lama_dan_baru(target, sumber):
    """
    Menggabungkan kategori yang namanya sama tanpa menimpa data lama.
    Kalau sama-sama dictionary, isinya digabung.
    Kalau data lama kosong dan data baru punya turunan, data baru dipakai.
    """
    for nama, isi in sumber.items():
        if nama not in target:
            target[nama] = isi
        else:
            if isinstance(target[nama], dict) and isinstance(isi, dict):
                gabungkan_dict_lama_dan_baru(target[nama], isi)
            elif target[nama] is None and isinstance(isi, dict):
                target[nama] = isi
    return target


# ===== FLATTEN KATEGORI =====
# Tujuan:
# 1. Menghilangkan tampilan Kategori A/B/C/D dari dropdown.
# 2. Menampilkan langsung nama kategori marketplace, misalnya Pakaian Wanita.
# 3. Menggabungkan kategori yang sama supaya tidak saling menimpa.
# 4. Melewati Kategori D karena isinya catatan migrasi, bukan kategori jualan.
flat_kategori = {}

for nama_group, group in KATEGORI.items():
    if nama_group == "Kategori D":
        continue

    if isinstance(group, dict):
        gabungkan_dict_lama_dan_baru(flat_kategori, group)


# ===== BAR PALING ATAS =====
col1, col2, col3, col4 = st.columns(4, gap="large")

# 1. Upload Produk
with col1:
    st.markdown("### Upload Produk")

    product_panel = st.container(border=True)
    with product_panel:
        product_image = st.file_uploader(
            "Pilih gambar produk",
            type=["jpg", "png", "jpeg"],
            key="upload_produk"
        )

        if product_image:
            st.markdown("**Preview Produk**")
            st.image(
                product_image,
                use_container_width=True
            )

    st.markdown("### Upload Model")

    model_panel = st.container(border=True)
    with model_panel:
        model_image = st.file_uploader(
            "Pilih gambar model opsional",
            type=["jpg", "png", "jpeg"],
            key="upload_model"
        )

        if model_image:
            st.markdown("**Preview Model**")
            st.image(
                model_image,
                use_container_width=True
            )

# 2. Kategori Produk + Sub Kategori
with col2:
    kategori = st.selectbox(
        "Kategori Produk",
        list(flat_kategori.keys())
    )

    data_sub = flat_kategori.get(kategori, {})

    sub_kategori = ""
    sub_sub_kategori = ""
    sub_sub_sub_kategori = ""

    if isinstance(data_sub, dict) and data_sub:
        sub_kategori = st.selectbox(
            "Sub Kategori",
            list(data_sub.keys())
        )

        data_sub_sub = data_sub.get(sub_kategori)

        if isinstance(data_sub_sub, dict) and data_sub_sub:
            sub_sub_kategori = st.selectbox(
                "Sub-sub Kategori",
                list(data_sub_sub.keys())
            )

            data_sub_sub_sub = data_sub_sub.get(sub_sub_kategori)

            if isinstance(data_sub_sub_sub, dict) and data_sub_sub_sub:
                sub_sub_sub_kategori = st.selectbox(
                    "Sub-sub-sub Kategori",
                    list(data_sub_sub_sub.keys())
                )

    elif not data_sub:
        st.info("Kategori ini belum memiliki rincian sub kategori.")

# 3. Deskripsi Produk
with col3:
    deskripsi = st.text_area(
        "Deskripsi Produk",
        placeholder="Contoh: bahan adem, ringan, cocok dipakai harian",
        height=120
    )

    detail_produk_visual = st.text_area(
        "Detail Visual Produk",
        value="",
        placeholder="Contoh: setelan anak 2-piece, atasan tanpa lengan, 3 kancing coklat, kerah ruffle, celana pendek ruffle, motif garis biru putih",
        height=130,
        help="Isi detail ini agar video tidak salah pakaian. Kalau dikosongkan, sistem memakai blueprint default setelan garis biru-putih."
    )

# ===== FALLBACK PRODUCT DETAIL PALING KUAT =====
# Dipakai kalau kolom Detail Visual Produk dikosongkan.
# Tujuannya supaya AI video tidak mengubah produk menjadi dress/piyama/baju generic.
if not detail_produk_visual.strip():
    detail_produk_visual = """
children toddler girl two-piece outfit set, NOT a dress, NOT pajamas, NOT romper,
blue and white thin vertical stripe pattern on every fabric panel,
sleeveless top with open arms, no inner white t-shirt, no long sleeves,
round ruffled collar around the neck,
ruffle detail around both shoulder armholes,
exactly 3 brown round front buttons centered vertically on the chest,
short top with layered peplum ruffle panel around the lower top,
matching blue-white striped shorts, elastic waist,
shorts must be visible below the top,
ruffle trim at both shorts leg openings,
keep the same stitching, same button count, same ruffle placement, same stripe direction,
use uploaded product image as absolute visual blueprint when product image is uploaded
""".strip()

konsep = st.selectbox(
    "Konsep Konten",
    [
        "Natural UGC",
        "Review Produk",
        "Storytelling",
        "Aesthetic / Fashion",
        "Soft Selling",
        "Hard Selling"
    ]
)

# 4. Target Market
with col4:
    target = st.text_area(
        "Target Penjualan",
        placeholder="Contoh: wanita 20-35 tahun, pekerja kantoran",
        height=120
    )

    hubungan = st.selectbox(
        "Hubungan Karakter",
        [
            "Ibu & Anak (Mirip)",
            "Tidak Berhubungan"
        ]
    )

    behavior_anak = st.selectbox(
        "Behavior Anak",
        [
            "Ceria Aktif",
            "Salting Lihat Kamera",
            "Suka Joget",
            "Pemalu Lucu",
            "Random Toddler"
        ]
    )

    behavior_ibu = st.selectbox(
        "Behavior Ibu",
        [
            "Ibu Lembut",
            "Ibu Santai",
            "Ibu Humoris",
            "Ibu Natural UGC"
        ]
    )
    camera_interaction = st.selectbox(
      	"Interaksi Kamera",
    	[
        "Selfie Lihat Layar HP",
        "Salting Lihat Kamera",
        "Joget Depan Kamera",
        "Tidak Sadar Direkam",
        "Direkam Ibu",
        "Vlog Natural",
        "Kamera Ayah Merekam"
        ]
    )
    lokasi_cerita = st.selectbox(
         "Lokasi Cerita",
    [
        "Ruang Tamu Rumah",
        "Kamar Anak",
        "Teras Rumah",
        "Halaman Rumah",
        "Taman Kecil",
        "Dapur Rumah",
        "Kamar Mandi",
        "Area Bermain Anak",
        "Mall / Tempat Jalan-jalan",
        "Outdoor Sore Hari"
    ]
)
    gaya = st.selectbox(
        "Gaya Penjualan",
        [
            "Soft",
            "Balanced",
            "Hard"
        ]
    )

    durasi = st.selectbox(
        "Durasi Video",
        [
            "Pendek (5-8 detik)",
            "Sedang (8-15 detik)",
            "Panjang (15-30 detik)"
        ]
    )
    format_prompt = st.selectbox(
        "Format Prompt",
        [
            "Text Cinematic",
            "JSON Cinematic"
        ]
    )

# ===== RINGKASAN AUDIO & VOICE SETTING =====
st.markdown("---")

with st.expander("🎙️ Ringkasan Pengaturan Suara & Dialog", expanded=False):
    st.write("**Status:** Pengaturan suara sudah dibuat di halaman terpisah, tetapi belum dipakai untuk membuat prompt.")

    st.write("**Audio Mode:**", st.session_state.get("audio_mode", "Belum diatur"))
    st.write("**Voice Profile Ibu:**", st.session_state.get("mother_voice_profile", "Belum diatur"))
    st.write("**Voice Profile Anak:**", st.session_state.get("child_voice_profile", "Belum diatur"))
    st.write("**Gaya Dialog:**", st.session_state.get("dialogue_style_mode", "Belum diatur"))
    st.write("**Level Goyangan Selfie:**", st.session_state.get("selfie_motion_level", "Belum diatur"))

    st.write("**Kunci Speaker:**", st.session_state.get("speaker_lock", "Belum diatur"))
    st.write("**Kunci Lip-sync:**", st.session_state.get("lip_sync_lock", "Belum diatur"))
    st.write("**Kunci Gesture Karakter:**", st.session_state.get("gesture_ownership_lock", "Belum diatur"))

    st.text_area(
        "Dialogue Timeline Aktif",
        value=st.session_state.get("dialogue_timeline", ""),
        height=120,
        disabled=True
    )

    st.caption(
        "Catatan: Ringkasan ini hanya membaca pengaturan dari halaman Pengaturan Suara & Dialog. "
        "Belum masuk ke JSON prompt."
    )

# ===== ANALISA FOTO MODEL & PRODUK =====
st.markdown("---")
st.markdown("### 🔎 Analisa Foto Model & Produk")

# ===== AUTO ANALYZE BUTTON =====
if "auto_model_analysis" not in st.session_state:
    st.session_state.auto_model_analysis = ""

if "auto_product_analysis" not in st.session_state:
    st.session_state.auto_product_analysis = ""

if st.button("🔍 Analisa Otomatis Foto dengan Gemini", use_container_width=True):

    with st.spinner("AI Vision sedang menganalisa foto model dan produk..."):

        # ANALISA MODEL
        if model_image is not None:
            st.session_state.auto_model_analysis = analyze_image_with_openai(
    model_image,
    "model"
)

        # ANALISA PRODUK
        if product_image is not None:
            st.session_state.auto_product_analysis = analyze_image_with_openai(
    product_image,
    "product"
)

    st.success("Analisa otomatis selesai.")
    
st.info(
    "Isi analisa ini berdasarkan foto model dan foto produk yang diupload. "
    "Analisa ini akan dipakai agar ide konten dan prompt tidak bertabrakan dengan pose model, posisi tangan, detail produk, dan lingkungan."
)

analisa_col1, analisa_col2 = st.columns(2, gap="large")

with analisa_col1:
    analisa_foto_model = st.text_area(
        "Analisa Foto Model",
        placeholder=(
            "Contoh:\n"
            "- Di foto ada ibu dan anak.\n"
            "- Ibu berada di belakang/samping anak.\n"
            "- Anak berdiri di depan ibu.\n"
            "- Tangan ibu tidak menyentuh bagian depan baju anak.\n"
            "- Wajah ibu dan anak menghadap kamera.\n"
            "- Ekspresi natural dan santai.\n"
            "- Scene cocok dibuat sebagai selfie natural.\n"
            "- Jangan membuat ibu menunjuk kancing atau memegang bagian depan outfit."
        ),
        value=st.session_state.auto_model_analysis,
        height=220
    )

with analisa_col2:
    analisa_foto_produk = st.text_area(
        "Analisa Foto Produk",
        placeholder=(
            "Contoh:\n"
            "- Produk adalah setelan anak perempuan 2-piece.\n"
            "- Atasan sleeveless tanpa lengan.\n"
            "- Kerah ruffle/peter pan.\n"
            "- Ada tepat 3 kancing batok kelapa warna coklat dengan 2 lubang.\n"
            "- Motif garis vertikal biru-putih.\n"
            "- Ada peplum ruffle di pinggang.\n"
            "- Celana pendek senada dengan ruffle di ujung celana.\n"
            "- Jangan ubah menjadi dress, rok, piyama, romper, atau baju generic."
        ),
        value=st.session_state.auto_product_analysis,
        height=220
    )

uploaded_photo_analysis_text = f"""
UPLOADED PHOTO ANALYSIS:

MODEL PHOTO ANALYSIS:
{analisa_foto_model if analisa_foto_model.strip() else "No manual model photo analysis provided. The AI must carefully analyze the uploaded model reference image before generating the video idea."}

PRODUCT PHOTO ANALYSIS:
{analisa_foto_produk if analisa_foto_produk.strip() else "No manual product photo analysis provided. The AI must carefully analyze the uploaded product image and preserve the exact product visual details."}

ANALYSIS USAGE RULE:
The video idea, text prompt, and JSON prompt must follow this uploaded photo analysis.
Do not create actions that conflict with the model photo analysis.
Do not create product details that conflict with the product photo analysis.
Do not force gestures, pose changes, or camera logic that contradict the uploaded model image.
""".strip()

# ===== LOGIC MODEL & ANAK =====
is_kategori_anak = "Anak" in kategori

if model_image:
    model_info = "Gunakan model sesuai referensi gambar yang diupload."
else:
    model_info = "Gunakan model wanita dewasa natural."

if is_kategori_anak:
    if hubungan == "Ibu & Anak (Mirip)":
        child_info = "Tambahkan anak dengan wajah mirip ibu (genetik konsisten)."
    else:
        child_info = "Tambahkan anak dengan karakter bebas (tidak harus mirip)."
else:
    child_info = "Tidak perlu anak dalam scene."

hasil_kategori = kategori

if sub_kategori:
    hasil_kategori += f" > {sub_kategori}"

if sub_sub_kategori:
    hasil_kategori += f" > {sub_sub_kategori}"

if sub_sub_sub_kategori:
    hasil_kategori += f" > {sub_sub_sub_kategori}"

st.markdown("---")
st.write(f"**Dipilih:** {hasil_kategori}")

# ===== GENERATE 5 IDE KONTEN =====
st.markdown("### Generate Ide Konten")

# ===== STYLE GLOBAL =====
if konsep == "Natural UGC":
    style_hint = "Video terasa seperti rekaman selfie asli dari kamera depan HP ibu, natural, spontan, dan tidak dibuat-buat."
elif konsep == "Review Produk":
    style_hint = "Fokus menjelaskan produk dengan jelas dan informatif."
elif konsep == "Storytelling":
    style_hint = "Ada alur cerita yang mengalir dari awal sampai akhir."
elif konsep == "Aesthetic / Fashion":
    style_hint = "Visual lebih rapi, menarik, dan fokus ke tampilan."
elif konsep == "Soft Selling":
    style_hint = "Tidak terasa jualan, lebih ke experience."
else:
    style_hint = "Langsung fokus jualan dan keunggulan produk."

# Gaya jualan
if gaya == "Soft":
    selling_hint = "Tidak ada ajakan beli langsung."
elif gaya == "Balanced":
    selling_hint = "Ada sedikit ajakan beli di akhir."
else:
    selling_hint = "Gunakan call to action yang jelas dan kuat."

# ===== BEHAVIOR ANAK =====
if behavior_anak == "Ceria Aktif":
    behavior_anak_hint = """
- cheerful but controlled child expression
- small natural toddler micro movement only
- subtle blinking
- soft smile
- tiny head tilt
- relaxed curious eyes
- minimal body movement
- no active hand movement
- no jumping
- no dancing
- no fast head movement
- no large playful motion
"""
elif behavior_anak == "Salting Lihat Kamera":
    behavior_anak_hint = """
- child is aware of front camera
- reacts naturally while seeing own reflection
- cute shy smile
- playful posing like modern children
- excited expression while looking at screen
"""

elif behavior_anak == "Suka Joget":
    behavior_anak_hint = """
- child enjoys moving to camera
- spontaneous dancing movement
- playful body movement
- happy energetic expression
"""

elif behavior_anak == "Pemalu Lucu":
    behavior_anak_hint = """
- shy but cute child behavior
- sometimes hiding expression
- awkward natural smile
- realistic timid toddler behavior
"""

else:
    behavior_anak_hint = """
- random toddler behavior
- unpredictable child movement
- natural child chaos
- spontaneous expression changes
"""

# ===== BEHAVIOR IBU =====
if behavior_ibu == "Ibu Lembut":
    behavior_ibu_hint = """
- soft mother energy
- gentle voice and expression
- warm loving interaction
"""

elif behavior_ibu == "Ibu Santai":
    behavior_ibu_hint = """
- relaxed casual mother behavior
- natural everyday interaction
- comfortable body language
"""

elif behavior_ibu == "Ibu Humoris":
    behavior_ibu_hint = """
- playful mother interaction
- laughing naturally with child
- expressive fun energy
"""

else:
    behavior_ibu_hint = """
- natural UGC mother behavior
- casual smartphone video feeling
- realistic everyday interaction
"""

# ===== STORY FLOW =====
story_flow_hint = """
- video must feel like a real spontaneous family moment
- interaction should feel accidental and organic
- avoid scripted commercial feeling
- child behavior should drive the scene naturally
- emotional flow must feel believable
- no dramatic acting
- no overacting
- create slice of life feeling
"""

# ===== EMOTION LOCK =====
emotion_lock_hint = """
- mother facial expression must match her voice emotion
- if mother sounds happy, face must also look happy
- if mother laughs, body language must reflect joy
- avoid emotional mismatch
- avoid blank facial expression
"""

# ===== PRODUCT LOCK =====
product_lock_hint = """
- outfit details MUST remain identical across all clips
- maintain same buttons
- maintain same stitching
- maintain same fabric texture
- maintain same clothing color
- maintain same accessory details
- do not randomly redesign outfit
"""

# ===== REALISTIC TODDLER LOGIC =====
toddler_logic_hint = """
- modern toddlers understand smartphone cameras
- child may react to seeing themselves on front camera
- child may pose naturally
- child may dance or smile at camera
- child may become excited seeing outfit
- child may call mother naturally
- child movement should feel unpredictable but realistic
- avoid robotic toddler movement
"""
# ===== SELFIE POV LOCK BARU =====
selfie_pov_lock_text = """
ABSOLUTE SELFIE POV LOCK:
The viewer is the mother's smartphone front-camera lens itself.
The recording device must remain invisible because it is the camera.
Do not show any visible phone body.
Do not show any visible phone screen.
Do not show any mirrorless camera.
Do not show any DSLR camera.
Do not show any external camera.

The mother records directly from her own front-facing smartphone camera using ONE HAND ONLY.
One of the mother's arms must be visibly extended toward the front-camera lens and cropped near the edge of the frame, like a real selfie arm.
The extended recording arm may show forearm, wrist, or partial hand near the frame edge, but the phone itself must stay invisible.
The recording arm must NOT hold or hug the child.
The mother must NOT use both hands to hug or hold the child.
The mother's other hand may gently steady the child at the waist or back.

Only the mother and the child appear in the video.
No third person.
No cameraman.
No second camera.
No mirror reflection.
No tripod shot.
No external filming angle.
No third-person cinematic perspective.
The video must never look like someone else filming a mother who is holding a camera.
The framing must look like a true front-camera selfie: close-medium framing, both faces visible, front outfit visible, slight natural one-handed handheld movement.
""".strip()


# ===== CHILD EXPRESSION LOCK BARU =====
child_natural_expression_lock_text = """
CHILD NATURAL EXPRESSION LOCK:
The child must look cute, relaxed, playful, and naturally curious on camera.
Avoid tense, stiff, scared, blank, or frozen facial expression.
When the mother is speaking, the child is NOT frozen.
The child should react with small natural toddler micro-expressions:
soft smile, tiny shy grin, blinking, slight cheek movement, small head tilt, curious eyes, and relaxed mouth.
The child may glance at the mother, then back to the front-camera lens.
The child may make a cute shy face, tiny pout, or playful expression for a moment.
The child should feel like a real toddler enjoying being recorded, not like an AI character posing.
No stiff staring.
No emotionless face.
No robotic expression.
No tense mouth.
No frightened eyes.
No adult-like acting.
Keep the child innocent, cute, spontaneous, and natural.
""".strip()


# ===== SPEAKER & LIPSYNC LOCK BARU =====
speaker_lipsync_lock_text = """
SPEAKER AND LIP-SYNC LOCK:
There are only two speakers: mother and child.
When the mother speaks, only the mother's mouth moves.
When the child speaks, only the child's mouth moves.
The child dialogue must be spoken by the child's voice, not the mother.
The mother must not speak the child's line.
The child must not speak the mother's line.
Non-speaking character must keep mouth closed or naturally relaxed.
No overlapping voices.
No ventriloquist effect.
No wrong speaker voice.
No mismatched lip-sync.
""".strip()

# ===== AUDIO CLEAN LOCK BARU =====
audio_clean_lock_text = """
AUDIO CLEAN LOCK:
No background music.
No instrumental music.
No cinematic music.
No jingles.
No sound effects.
No whoosh sound.
No pop sound.
No transition sound.
No ambient noise.
No crowd noise.
No room noise.
No wind noise.
No birds, vehicles, TV, radio, or unrelated background sounds.
Only the active speaking character voice is allowed.
When mother speaks, only mother's voice is heard.
When child speaks, only child's voice is heard.
When nobody speaks, the audio must be silent.
No extra narrator voice.
No extra AI voice.
No off-screen voice.
No overlapping voices.
""".strip()

# ===== SELFIE HAND & OUTFIT TOUCH LOCK BARU =====
selfie_hand_outfit_lock_text = """
HAND AND OUTFIT SAFETY LOCK:
Do not force the mother to visibly hold a phone if it conflicts with the uploaded model reference pose.
Follow the uploaded model pose, hand position, and interaction logic first.
Camera must remain stable with minimal movement.

The mother's hands must stay natural and physically believable.
If the mother supports or interacts with the child, the hand may stay only at:
side waist, lower back, side torso, shoulder side, or gentle natural support area.

The mother's hand must NEVER touch the front chest area of the outfit.
The mother's hand must NEVER touch the buttons.
The mother's hand must NEVER touch the collar.
The mother's hand must NEVER touch the peplum ruffle.
The mother's hand must NEVER point at, adjust, pull, pinch, hold, or cover the front outfit.
Do not let the mother hold or pinch the child's front buttons.
Do not let the mother adjust the collar.
Do not let the mother touch the peplum.
Do not let the mother block any of the 3 buttons.

Keep all 3 front buttons clearly visible without being touched.
Keep the front outfit visible.
Keep the hand motion minimal, slow, and natural.
No aggressive fabric pulling.
No sudden hand movement toward chest, collar, buttons, or peplum.
""".strip()


# ===== MODEL / PRODUCT / ENVIRONMENT ANALYSIS LOCK =====
scene_analysis_lock_text = """
SCENE ANALYSIS LOCK:
Before generating the video story, first analyze the uploaded model reference image, uploaded product image, environment context, and all selected dropdown options.

The AI must understand:
- who is present in the image
- mother position
- child position
- hand positions
- body orientation
- face direction
- distance between mother and child
- interaction logic between mother and child
- whether the pose already looks selfie-like or not
- whether the current pose supports selfie recording or not
- current emotional tone of the uploaded model image
- room/environment appearance
- product appearance and structure
- product detail placement
- all dropdown selections chosen by the user

The generated story must ADAPT to the uploaded images instead of forcing a conflicting action.

Do not generate actions that conflict with the uploaded model pose.
Do not suddenly create pointing gestures.
Do not suddenly move the mother hand toward the outfit buttons.
Do not suddenly create product-presenting gestures.
Do not force unnatural hand movement just to show product details.

If the uploaded mother hand position does not touch the outfit:
- keep the hand away from the outfit

If the uploaded product already has visible details:
- do not force hand gestures to explain the product

The generated video must feel like a natural continuation of the uploaded photo, not a newly invented unrelated scene.
""".strip()

# ===== SELFIE & VOICE NEGATIVE RULES BARU =====
selfie_negative_rules = [
    "visible phone",
    "visible smartphone",
    "phone in hand",
    "phone as main object",
    "visible phone screen",
    "visible phone back",
    "visible recording device",
    "mirrorless camera",
    "DSLR camera",
    "camcorder",
    "external camera",
    "tripod",
    "cameraman",
    "third person",
    "outside observer shot",
    "third-person selfie shot",
    "external filming angle",
    "mirror selfie",
    "mother holding visible device",
    "visible camera in hand",
    "mother using both hands to hug child",
    "both mother hands holding child",
    "no extended selfie arm",
    "missing selfie arm",
    "recording hand blocking outfit",
    "recording hand covering face",
    "external camera perspective"
]

voice_negative_rules = [
    "child voice spoken by mother",
    "mother speaking child dialogue",
    "wrong speaker",
    "wrong lip-sync",
    "mismatched mouth movement",
    "ventriloquist effect",
    "child mouth closed while child voice speaks",
    "mother mouth moving during child dialogue",
    "overlapping voices"
]

audio_negative_rules = [
    "background music",
    "instrumental music",
    "cinematic music",
    "jingle",
    "sound effects",
    "whoosh sound",
    "pop sound",
    "transition sound",
    "ambient noise",
    "crowd noise",
    "room noise",
    "wind noise",
    "birds sound",
    "vehicle noise",
    "TV sound",
    "radio sound",
    "unrelated background sounds",
    "extra narrator voice",
    "extra AI voice",
    "off-screen voice",
    "overlapping voices",
    "music under dialogue"
]
hand_outfit_negative_rules = [
    "mother holding phone then releasing it",
    "recording hand switching roles",
    "recording hand touching child outfit",
    "recording hand touching buttons",
    "recording hand touching collar",
    "recording hand touching peplum",
    "mother hand touching buttons",
    "mother hand touching collar",
    "mother hand touching peplum",
    "mother pointing at buttons",
    "mother adjusting buttons",
    "mother pinching buttons",
    "mother pulling collar",
    "mother adjusting collar",
    "mother holding front outfit",
    "mother covering buttons",
    "mother covering collar",
    "mother covering peplum",
    "buttons covered by hand",
    "front outfit covered by hand"
]

scene_conflict_negative_rules = [
    "action conflicting with uploaded pose",
    "unnatural pose transition",
    "forced product presentation gesture",
    "mother suddenly pointing at buttons",
    "mother suddenly touching outfit",
    "mother suddenly changing hand role",
    "interaction not matching uploaded model image",
    "scene not matching uploaded environment",
    "unrelated movement",
    "unnatural interaction change",
    "forced marketing gesture",
    "unnatural hand transition",
    "mother releasing recording phone",
    "mother changing from selfie recording to product pointing",
    "AI-invented gesture unrelated to uploaded reference"
]

child_expression_negative_rules = [
    "tense child expression",
    "stiff child face",
    "scared child face",
    "blank stare",
    "emotionless toddler",
    "frozen child expression",
    "robotic toddler",
    "adult-like child acting",
    "unnatural smile",
    "dead eyes",
    "frightened eyes",
    "tense mouth",
    "AI-looking face",
    "waxy face"
]
# ===== SAFETY MOTION =====
safety_motion_hint = """
- realistic physical movement only
- no clipping through furniture
- no broken body movement
- no impossible walking path
- characters must interact naturally with environment
"""

# ===== CAMERA INTERACTION =====
if camera_interaction == "Selfie Lihat Layar HP":
    camera_interaction_hint = """
- child sees themselves using front smartphone camera
- child reacts naturally to own appearance
- cute surprised reaction while seeing outfit
- child becomes excited seeing themselves on screen
- selfie interaction feels modern and realistic
"""

elif camera_interaction == "Salting Lihat Kamera":
    camera_interaction_hint = """
- child becomes shy while noticing camera
- playful smiling reaction
- awkward cute posing
- natural modern child camera awareness
"""

elif camera_interaction == "Joget Depan Kamera":
    camera_interaction_hint = """
- child naturally dances in front of camera
- playful body movement
- spontaneous happy energy
- movement feels random and realistic
"""

elif camera_interaction == "Tidak Sadar Direkam":
    camera_interaction_hint = """
- characters behave naturally without looking at camera
- candid family moment feeling
- realistic hidden camera atmosphere
"""

elif camera_interaction == "Direkam Ibu":
    camera_interaction_hint = """
- camera behaves like mother recording child
- warm family recording feeling
- natural handheld smartphone movement
"""

elif camera_interaction == "Vlog Natural":
    camera_interaction_hint = """
- natural casual vlog feeling
- spontaneous smartphone interaction
- realistic daily life recording
"""

else:
    camera_interaction_hint = """
- stable realistic camera feeling
- almost static framing
- minimal natural micro movement only
- no fast camera movement
- no camera dip
- no sudden reframing
- no zoom in or zoom out
- keep mother and child in the same frame
- keep child's front outfit visible without changing camera angle
"""

# ===== RECORDING POV LOCK DINAMIS =====
# Tujuan:
# Kalau pilih "Kamera Ayah Merekam", prompt TIDAK boleh memakai selfie lock.
# Kalau selain itu, prompt tetap memakai aturan selfie/rekaman kamera depan ibu.
if camera_interaction == "Kamera Ayah Merekam":
    recording_pov_lock_text = """
FATHER RECORDING POV LOCK:
This video is recorded by the father using a handheld smartphone camera.
The father is behind the camera and must NOT appear in the video.
Only the mother and the child appear in the video.
The mother is NOT holding any phone.
The mother is NOT recording herself.
The mother is NOT taking a selfie.
Do not show the mother holding a phone, mirrorless camera, DSLR, or any recording device.
Do not show any mirror reflection.
Do not show any selfie angle.
Do not show a front-camera selfie perspective.
Do not show the video as if the mother is filming herself.
The camera perspective must feel like a real father naturally recording his wife and child at home.
Use a simple handheld smartphone camera feeling from father's eye level.
No tripod.
No cameraman visible.
No third person visible.
No mirror shot.
No reflection shot.
Mother uses both hands naturally to interact with or gently hold the child.
The child's outfit must stay clearly visible.
""".strip()
else:
    recording_pov_lock_text = """
SELFIE RECORDING LOCK:
This video must be recorded only from the mother's own smartphone front camera in true selfie POV.
The mother holds the phone with ONE HAND ONLY.
The hand holding the phone should be partially visible or mostly out of frame because it is being used to hold the recording phone.
Do not show any second camera.
Do not show any cameraman.
Do not show any third person.
Only the mother and the child are present in the recording.
No tripod shot.
No external filming angle.
No cinematic third-person camera.
No security camera angle.
No mirror shot.
No other people in the room.
The framing must feel like a real handheld front-camera selfie video recorded directly by the mother.
The phone itself should remain mostly invisible, because it is the recording device.
Natural slight handheld shake from one-handed recording is allowed.
""".strip()


# ===== DIALOGUE 2 TURN LOCK =====
dialogue_2_turn_lock_text = """
DIALOGUE RULE:
Only 2 speaking turns in this clip.
Turn 1: Mother speaks.
Turn 2: Child speaks.
No third speaking turn.
No extra dialogue after the child speaks.
No repeated dialogue.
No overlapping voices.
When mother speaks, only mother's mouth moves.
When child speaks, only child's mouth moves.
The child dialogue must be spoken by the child's voice, not the mother.
The mother must not speak the child's line.
""".strip()

# ===== VISUAL SAFETY LOCK =====
visual_safety_hint = """
- do not generate extra fingers
- do not generate extra hands
- do not generate extra limbs
- maintain realistic human anatomy
- keep normal body proportions
- no duplicated body parts
- no mutated hands
- no distorted face
- no floating objects

- do not add random buttons
- do not add extra outfit details
- keep original outfit design exactly
- preserve same stitching and accessories

- avoid cinematic light effects
- avoid glow effects
- avoid lens flare
- avoid floating particles
- avoid random visual effects
- avoid fantasy atmosphere

- realistic smartphone video only
- simple natural lighting only
"""

auto_safety_rules = """
STRICT CONTINUITY AND CAMERA SAFETY RULES:
- Do not change clothing structure.
- Do not change button count.
- Do not change stripe direction.
- Do not move hands toward collar or chest.
- Avoid aggressive fabric pulling.
- Avoid large body movement.
- Avoid sudden camera movement.
- Avoid finger deformation.
- Avoid face distortion.
- Preserve mother-child distance consistency.

NO REFRAMING RULE:
- Do not zoom in.
- Do not zoom out.
- Do not reframe the camera.
- Do not crop the child's front outfit.
- Do not crop the chest buttons.
- Do not crop the shorts.
- Keep chest, peplum, and shorts visible in the same stable frame.
- Keep the same camera angle throughout the clip.
- Use almost static framing with only minimal natural micro movement.

BUTTON STRUCTURE LOCK:
- Exactly 3 buttons only.
- Keep the buttons vertically aligned in the center front.
- Keep equal spacing between all buttons.
- Keep the same button size in all frames.
- Keep the same brown coconut-shell look.
- Keep the same two-hole button detail.
- Never blur the buttons.
- Never merge the buttons.
- Never remove any button.
- Never replace the buttons with plastic-looking buttons.

STRIPE CONTINUITY LOCK:
- Preserve exact vertical stripe direction.
- Preserve stripe thickness.
- Preserve stripe spacing.
- Keep blue-white stripes consistent in every frame.
- Do not bend stripes unnaturally.
- Do not turn vertical stripes into diagonal stripes.
- Do not turn stripes into wrinkles.
- Do not blur the stripe pattern.
- Do not remove stripes on ruffle, peplum, collar, or shorts.
- Keep stripe alignment stable during micro movement.

BOTTOM STRUCTURE LOCK:
- Shorts must remain visible in every scene.
- Preserve clear separation between top and shorts.
- Peplum must remain a short flared top detail, not a dress silhouette.
- Peplum must not extend downward into skirt or dress shape.
- Preserve shorts leg openings.
- Preserve ruffle hem on both shorts legs.
- Keep the shorts loose-fit and elastic-waist.
- Do not merge peplum and shorts into one garment.
- Do not transform shorts into skirt, dress, romper, or long pants.

FACE STABILITY LOCK:
- Preserve exact mother face identity from uploaded model reference.
- Preserve exact child face identity from uploaded model reference.
- Preserve face proportions.
- Preserve eye spacing.
- Preserve cheek structure.
- Preserve nose and mouth shape.
- Avoid exaggerated expression.
- Avoid mouth over-opening during dialogue.
- Avoid face stretching.
- Avoid face melting.
- Avoid eye distortion.
- Avoid changing the child's age impression.
- Keep facial motion subtle and natural.
"""

pose_aware_camera_rule = """
POSE-AWARE CAMERA RULE:
- Follow the uploaded model reference pose first.
- Do not force selfie recording if the uploaded model pose looks more suitable for stable/static camera.
- Do not force the mother to hold a phone if it conflicts with the uploaded model image.
- Use stable smartphone-style framing that preserves the original pose logic.
- Camera movement must be minimal, slow, and natural.
- Do not change character positions just to create a selfie angle.
- Do not invent a new camera angle that contradicts the uploaded model reference.
- Keep mother and child position consistent with the uploaded model reference.
- Keep the child's outfit visible without forcing hand gestures or camera dipping.
"""

# ===== PRODUCT REFERENCE LOCK UNTUK VIDEO =====
product_reference_status = (
    "Uploaded product image is available. Use it as the ABSOLUTE VISUAL BLUEPRINT for the outfit."
    if product_image
    else "No product image uploaded. Use Detail Visual Produk text as the strict outfit blueprint."
)

product_blueprint_lines = [
    line.strip(" -")
    for line in detail_produk_visual.splitlines()
    if line.strip()
]

product_strict_rules = [
    "The product outfit must match the uploaded product reference image, not only the general marketplace category.",
    "Preserve exact garment type: top + shorts two-piece set.",
    "Preserve exact silhouette, stripe direction, fabric texture, stitching, ruffle position, and button count.",
    "Exactly 3 brown round buttons on the center front chest; never add or remove buttons.",
    "The top is sleeveless; do not add inner t-shirt sleeves or long sleeves.",
    "The shorts must remain visible below the top with ruffle trim at both leg openings.",
    "Do not redesign the product into a dress, skirt, pajamas, romper, blouse, or generic striped outfit.",
    "Maintain the same outfit design consistently across clip 1 and clip 2."
    "FREEZE GARMENT STRUCTURE: do not reinterpret garment structure; preserve exact sewing layout, peplum cut, collar geometry, stripe spacing, button spacing, shorts length, and ruffle volume.",
]

product_negative_rules = [
    "no dress",
    "no skirt",
    "no pajamas",
    "no romper",
    "no generic clothing",
    "no white inner t-shirt",
    "no sleeves under the sleeveless top",
    "no random buttons",
    "no missing buttons",
    "no changed stripe pattern",
    "no diagonal stripes",
    "no different color",
    "no outfit morphing between clips"
]

product_prompt_lock_text = f"""
PRODUCT REFERENCE LOCK:
{product_reference_status}

CATEGORY PATH:
{hasil_kategori}

EXACT PRODUCT VISUAL DETAILS:
{detail_produk_visual}

STRICT PRODUCT RULES:
- """ + "\n- ".join(product_strict_rules) + """

NEGATIVE PRODUCT RULES:
- """ + "\n- ".join(product_negative_rules)

# ===== DURASI =====
if "Pendek" in durasi:
    durasi_hint = "Gunakan 2-3 scene cepat."
elif "Sedang" in durasi:
    durasi_hint = "Gunakan 3-4 scene dengan ritme natural."
else:
    durasi_hint = "Gunakan 4-5 scene dengan detail lebih jelas."

if st.button("Generate 5 Ide Konten", use_container_width=True):

    # ===== STYLE LOGIC =====
    if konsep == "Natural UGC":
        style_hint = "Video terasa seperti rekaman selfie asli dari kamera depan HP ibu, natural, spontan, dan tidak dibuat-buat."
    elif konsep == "Review Produk":
        style_hint = "Fokus menjelaskan produk dengan jelas dan informatif."
    elif konsep == "Storytelling":
        style_hint = "Ada alur cerita yang mengalir dari awal sampai akhir."
    elif konsep == "Aesthetic / Fashion":
        style_hint = "Visual lebih rapi, menarik, dan fokus ke tampilan."
    elif konsep == "Soft Selling":
        style_hint = "Tidak terasa jualan, lebih ke experience."
    else:
        style_hint = "Langsung fokus jualan dan keunggulan produk."

    # Gaya jualan
    if gaya == "Soft":
        selling_hint = "Tidak ada ajakan beli langsung."
    elif gaya == "Balanced":
        selling_hint = "Ada sedikit ajakan beli di akhir."
    else:
        selling_hint = "Gunakan call to action yang jelas dan kuat."

    # Durasi
    if "Pendek" in durasi:
        durasi_hint = "Gunakan 2-3 scene cepat."
    elif "Sedang" in durasi:
        durasi_hint = "Gunakan 3-4 scene dengan ritme natural."
    else:
        durasi_hint = "Gunakan 4-5 scene dengan detail lebih jelas."

    ide_konten = [
        {
            "judul": "1. Natural Product Showcase",
            "alur": f"{style_hint} {selling_hint} {durasi_hint} Produk ditampilkan sesuai kategori {hasil_kategori}. {model_info} {child_info}",
            "kamera": "Handheld natural, seperti direkam orang lain.",
            "tujuan": "Membuat produk terlihat nyata dan relatable."
        },
        {
            "judul": "2. Detail Produk & Benefit",
            "alur": f"{style_hint} Fokus pada detail produk: {deskripsi}. {selling_hint}",
            "kamera": "Close up detail lalu pindah ke full view.",
            "tujuan": "Menjelaskan keunggulan produk."
        },
        {
            "judul": "3. Lifestyle Usage",
            "alur": f"{style_hint} Produk digunakan oleh target: {target}. {durasi_hint}",
            "kamera": "Follow activity, natural movement.",
            "tujuan": "Membuat pembeli membayangkan penggunaan nyata."
        },
        {
            "judul": "4. Story Scene",
            "alur": f"{style_hint} {model_info} {child_info} {selling_hint}",
            "kamera": "UGC natural, seperti video sehari-hari.",
            "tujuan": "Bangun emosi dan koneksi."
        },
        {
            "judul": "5. Closing CTA",
            "alur": f"{selling_hint} Produk ditampilkan jelas dengan fokus pada keunggulan utama.",
            "kamera": "Full → close up.",
            "tujuan": "Dorong pembelian."
        }
    ]

    st.session_state["ide_konten"] = ide_konten

if "ide_konten" in st.session_state:

    if st.button("🔄 Reset & Generate Ulang", use_container_width=True):
        if "ide_konten" in st.session_state:
            del st.session_state["ide_konten"]
        if "semua_prompt_video" in st.session_state:
            del st.session_state["semua_prompt_video"]

        st.rerun()

    st.markdown("### Hasil 5 Ide Konten")

    selected_replace = []

    for i, ide in enumerate(st.session_state["ide_konten"]):
        col_a, col_b = st.columns([0.1, 0.9])

        with col_a:
            if st.checkbox("", key=f"pilih_{i}"):
                selected_replace.append(i)

        with col_b:
            with st.expander(ide["judul"]):
                st.write("**Alur Cerita:**")
                st.write(ide["alur"])
                st.write("**Cara Kamera:**")
                st.write(ide["kamera"])
                st.write("**Tujuan Konten:**")
                st.write(ide["tujuan"])

    if st.button("Refresh Ide Terpilih"):
        for idx in selected_replace:
            new_ide = {
                "judul": f"{idx+1}. Ide Baru",
                "alur": f"{style_hint} {selling_hint} {durasi_hint} Ide baru untuk kategori {hasil_kategori}. {model_info} {child_info}",
                "kamera": "Natural handheld atau sesuai konsep.",
                "tujuan": "Memberikan variasi ide konten baru."
            }

            st.session_state["ide_konten"][idx] = new_ide

        st.rerun()

    st.markdown("### Jadikan Semua Ide Menjadi Prompt")

    if st.button("Jadikan Semua Ide Prompt"):
        semua_prompt = []

        for ide in st.session_state["ide_konten"]:

            # ===== TEXT CINEMATIC SELALU DIBUAT =====

            text_clip1 = f"""
Create ultra realistic vertical 9:16 smartphone selfie video (0-8s).
Style: {style_hint}. {selling_hint}. {durasi_hint}.
Scene: Hook + Mother & Child interaction at {lokasi_cerita}.

SELFIE RECORDING LOCK:
This video must be recorded only from the mother's own smartphone front camera in true selfie POV.
The mother holds the phone with ONE HAND ONLY.
The hand holding the phone should be partially visible or mostly out of frame because it is being used to hold the recording phone.
Do not show any second camera.
Do not show any cameraman.
Do not show any third person.
Only the mother and the child are present in the recording.
No tripod shot.
No external filming angle.
No cinematic third-person camera.
No security camera angle.
No mirror shot.
No other people in the room.
The framing must feel like a real handheld front-camera selfie video recorded directly by the mother.
The phone itself should remain mostly invisible, because it is the recording device.
Natural slight handheld shake from one-handed recording is allowed.

{child_natural_expression_lock_text}

{speaker_lipsync_lock_text}

{audio_clean_lock_text}

{selfie_hand_outfit_lock_text}

{scene_analysis_lock_text}

{uploaded_photo_analysis_text}

{auto_safety_rules}

{pose_aware_camera_rule}

{product_prompt_lock_text}

Mother behavior:
{behavior_ibu_hint}

Child behavior:
{behavior_anak_hint}

Camera:
{camera_interaction_hint}
Handheld smartphone movement, natural indoor daylight, slight real-camera imperfection.

Important action:
- Only 2 speaking turns in this clip.
- Turn 1: mother speaks.
- Turn 2: child speaks.
- No third dialogue.
- Show the front of the child's outfit clearly.
- Show the ruffled collar, sleeveless shoulder ruffles, exactly 3 brown coconut-shell buttons with 2 holes each, peplum ruffle, and matching shorts.
- Do not cover the buttons with hand/body.
- When mother speaks, only mother's mouth moves.
- When child speaks, only child's mouth moves.
- The child dialogue must be spoken by the child's voice, not the mother.

{visual_safety_hint}
"""

            text_clip2 = f"""
Create continuation ultra realistic vertical 9:16 smartphone selfie video (0-8s).
SAME mother, SAME child, SAME outfit as clip 1.
No product morphing between clips.

SELFIE RECORDING LOCK:
This video must be recorded only from the mother's own smartphone front camera in true selfie POV.
The mother holds the phone with ONE HAND ONLY.
The hand holding the phone should be partially visible or mostly out of frame because it is being used to hold the recording phone.
Do not show any second camera.
Do not show any cameraman.
Do not show any third person.
Only the mother and the child are present in the recording.
No tripod shot.
No external filming angle.
No cinematic third-person camera.
No security camera angle.
No mirror shot.
No other people in the room.
The framing must feel like a real handheld front-camera selfie video recorded directly by the mother.
The phone itself should remain mostly invisible, because it is the recording device.
Natural slight handheld shake from one-handed recording is allowed.

{child_natural_expression_lock_text}

{speaker_lipsync_lock_text}

{audio_clean_lock_text}

{selfie_hand_outfit_lock_text}

{scene_analysis_lock_text}

{uploaded_photo_analysis_text}

{auto_safety_rules}

{pose_aware_camera_rule}

{product_prompt_lock_text}
Action: Detail focus + natural closing.
- Only 2 speaking turns in this clip.
- Turn 1: mother speaks.
- Turn 2: child speaks.
- No third dialogue.
- Keep the same 3 brown coconut-shell front buttons with exactly 2 visible sewing holes each.
- Keep the same vertical blue-white stripes.
- Keep the same sleeveless ruffle top.
- Keep matching shorts visible with ruffle trim.
- Do not turn the outfit into dress, skirt, pajamas, romper, or generic clothing.
- When mother speaks, only mother's mouth moves.
- When child speaks, only child's mouth moves.
- The child dialogue must be spoken by the child's voice, not the mother.

Camera:
{camera_interaction_hint}
Natural handheld smartphone movement, realistic home video look.

{visual_safety_hint}
"""

            if True:

                # JSON dibuat memakai dict + json.dumps supaya tidak rusak kurung kurawal.
                # Fokus utama: pakaian anak harus mengikuti upload produk / Detail Visual Produk.

                base_camera = {
                    "style": "STABLE NATURAL SMARTPHONE VIDEO POV",
                    "pov_lock": [
                        "the viewer sees a stable natural smartphone recording with almost static framing",
                        "this must be a true selfie recording made directly by the mother",
                        "do not depict an outside observer filming the mother and child",
                        "camera movement must stay minimal, stable, and realistic",
                        "do not force visible phone-holding arm if it conflicts with the uploaded model pose",
                        "do not show the full smartphone body as a prominent visible object",
                        "if any part of the phone, hand, or wrist appears, it must be only a tiny edge near the frame border",
                        "the mother's OTHER HAND supports, holds, or steadies the child",
                        "only mother and child are present",
                        "do not show any third person",
                        "do not show any cameraman",
                        "do not show any second camera",
                        "do not show any mirror reflection",
                        "do not show any tripod shot",
                        "do not show any external filming angle",
                        "do not show any third-person cinematic perspective",
                        "framing must feel like a natural close-medium front-camera selfie",
                        "the first seconds must clearly show both faces and the child's front outfit",
                        "the recording hand must not block the outfit",
                        "subtle natural one-handed handheld motion only",
                        "realistic indoor daylight, no cinematic glow"
                    ],
                    "interaction": camera_interaction_hint.strip(),
                    "location": lokasi_cerita
                }

                selfie_negative_rules = [
                    "outside observer shot",
                    "third-person selfie shot",
                    "external filming angle",
                    "visible full smartphone body",
                    "phone as main object",
                    "mirror selfie",
                    "tripod shot",
                    "cameraman visible",
                    "third person visible",
                    "mother holding phone with two hands",
                    "recording hand blocking outfit",
                    "recording hand covering face",
                    "external camera perspective"
                ]

                product_lock_json = {
                    "category_path": hasil_kategori,
                    "uploaded_reference_status": product_reference_status,
                    "absolute_blueprint_instruction": "Use the uploaded product photo / product collage as the exact outfit blueprint. Match garment structure, not just color.",
                    "exact_visual_details_from_ui": product_blueprint_lines,
                    "must_keep": product_strict_rules,
                    "must_avoid": product_negative_rules,
                    "continuity_lock": "Same outfit design must remain identical in every clip: same 3 buttons, same ruffles, same stripes, same shorts."
                }

                model_reference_status = (
                    "Uploaded mother-and-child model reference image is available. Use it as the ABSOLUTE CHARACTER IDENTITY BLUEPRINT for both mother and child."
                    if model_image
                    else "No mother-and-child model reference image uploaded. Use natural Indonesian mother and toddler child identity."
                )

                character_identity_lock_json = {
                    "reference_status": model_reference_status,
                    "absolute_identity_instruction": "If a model reference image is uploaded, the mother and child must match the exact identity from that reference image, not a newly generated generic mother and child.",
                    "mother_identity_lock": [
                        "mother face must match the uploaded mother reference",
                        "same facial structure",
                        "same skin tone",
                        "same eye shape",
                        "same nose shape",
                        "same mouth and smile style",
                        "same hairstyle impression",
                        "same hair color",
                        "same overall visual identity",
                        "do not redesign the mother face",
                        "do not generate a different mother"
                    ],
                    "child_identity_lock": [
                        "child face must match the uploaded child reference",
                        "same toddler face identity",
                        "same cheek shape",
                        "same eye shape",
                        "same nose shape",
                        "same mouth shape",
                        "same bangs or fringe style if present in reference",
                        "same hairstyle impression",
                        "same hair color",
                        "same overall child visual identity",
                        "do not redesign the child face",
                        "do not generate a different child",
                        "do not change the child's age impression"
                    ],
                    "continuity_rules": [
                        "same mother identity across clip 1 and clip 2",
                        "same child identity across clip 1 and clip 2",
                        "no face identity drift",
                        "no hairstyle drift",
                        "no age drift",
                        "no different people between clips"
                    ]
                }

                voice_ownership_lock_json = {
                    "speaker_count": 2,
                    "speakers": ["mother", "child"],
                    "mother_voice_owner": "Only the mother uses the mother voice. Mother's voice must be adult female voice.",
                    "child_voice_owner": "Only the child uses the child voice. Child's voice must be toddler/young child voice.",
                    "strict_rules": [
                        "mother must never speak the child's dialogue",
                        "child must never speak the mother's dialogue",
                        "when speaker is mother_only, only mother mouth moves and only adult female mother voice is heard",
                        "when speaker is child_only, only child mouth moves and only toddler child voice is heard",
                        "non-speaking character mouth stays closed or naturally relaxed",
                        "no swapped voices",
                        "no mother voice for child dialogue",
                        "no child voice for mother dialogue",
                        "no overlapping voices",
                        "no ventriloquist effect",
                        "no mismatched lip-sync"
                    ]
                }

                common_characters = {
                    "mother": {
                        "identity": "MUST MATCH uploaded mother model reference image exactly when model image is uploaded; not a generic Indonesian mother.",
                        "reference_lock": "use uploaded model image as mother face and hairstyle identity blueprint",
                        "behavior": behavior_ibu_hint.strip(),
                        "anatomy_lock": "normal realistic body, exactly two arms and two hands only",
                        "mouth_rule": "mouth moves only when mother is speaking",
                        "voice_rule": "adult female mother voice only; never speak child dialogue"
                    },
                    "child": {
                        "identity": "MUST MATCH uploaded child model reference image exactly when model image is uploaded; not a generic toddler.",
                        "reference_lock": "use uploaded model image as child face, hairstyle, age, and expression identity blueprint",
                        "wearing_product": "child wears the exact product outfit from product_lock, not a different recommended outfit",
                        "behavior": behavior_anak_hint.strip(),
                        "anatomy_lock": "normal toddler anatomy, exactly two arms and two hands only",
                        "mouth_rule": "mouth moves only when child is speaking",
                        "voice_rule": "toddler child voice only; never speak mother dialogue"
                    }
                }

                clip1_dict = {
                    "clip": 1,
                    "ratio": "9:16",
                    "duration": "0-8 seconds",
                    "video_type": "ultra realistic vertical smartphone selfie video",
                    "content_idea": ide["judul"],
                    "story_context": ide["alur"],
                    "product_lock": product_lock_json,
                    "character_identity_lock": character_identity_lock_json,
                    "voice_ownership_lock": voice_ownership_lock_json,
                    "characters": common_characters,
                    "camera": base_camera,
                    "scene": {
                        "concept": konsep,
                        "style_hint": style_hint,
                        "selling_hint": selling_hint,
                        "story_flow": story_flow_hint.strip(),
                        "emotion_lock": emotion_lock_hint.strip(),
                        "safety_motion": safety_motion_hint.strip(),
                        "visual_safety": visual_safety_hint.strip()
                    },
                    "child_expression_lock": child_natural_expression_lock_text,
                    "speaker_and_lipsync_lock": speaker_lipsync_lock_text,
                    "audio_clean_lock": audio_clean_lock_text,
                    "selfie_hand_outfit_lock": selfie_hand_outfit_lock_text,
                    "scene_analysis_lock": scene_analysis_lock_text,
	            "uploaded_photo_analysis": uploaded_photo_analysis_text,
		    "auto_safety_rules": auto_safety_rules,
		    "pose_aware_camera_rule": pose_aware_camera_rule,
		    "dialogue_rule": {
                        "total_speaking_turns": 2,
                        "turn_1": "mother speaks only",
                        "turn_2": "child speaks only",
                        "no_third_dialogue": True,
                        "no_extra_dialogue_after_child": True,
                        "no_repeated_dialogue": True,
                        "no_overlapping_voices": True,
                        "when_mother_speaks": "only mother's mouth moves",
                        "when_child_speaks": "only child's mouth moves",
                        "child_dialogue_must_be_spoken_by_child_voice": True,
                        "mother_must_not_speak_child_line": True
                    },

                    "action_timeline": [
                        {
                            "time": "0-3s",
                            "speaker": "mother_only",
                            "dialogue": "Wah, baju barunya lucu banget ya!",
                            "action": "Mother and child stay in a stable natural smartphone-style frame. Do not force visible phone holding. The camera remains almost static with minimal micro movement. Both faces and the child's front outfit stay clearly visible.",
                            "product_visibility": "front top visible: ruffled collar, sleeveless shoulders, exactly 3 brown coconut-shell buttons with 2 visible sewing holes each",
                            "mother_mouth_state": "active_speaking",
                            "child_mouth_state": "closed_no_lipsync"
                        },
                        {
                            "time": "3-6s",
                            "speaker": "child_only",
                            "dialogue": "Iya Bunda, lucu ya!",
                            "action": "Child gives a small natural reaction with soft smile, subtle blinking, and tiny head tilt. Mother's hands stay natural and must not cover the child's front outfit, buttons, collar, peplum, or shorts.",
                            "product_visibility": "vertical blue-white stripes remain straight; peplum ruffle visible",
                            "mother_mouth_state": "closed_no_lipsync",
                            "child_mouth_state": "active_speaking"
                        },
                        {
                            "time": "6-8s",
                            "speaker": "none",
                            "dialogue": "",
                            "action": "Camera remains almost static with stable framing. The child makes a tiny natural posture shift so the matching striped shorts with ruffle trim stay visible without changing camera angle.",
                            "product_visibility": "shorts visible, not a skirt, not a dress"
                        }
                    ],
              "negative_prompt": (
               product_negative_rules
               + selfie_negative_rules
               + voice_negative_rules
               + audio_negative_rules
               + hand_outfit_negative_rules
               + scene_conflict_negative_rules
               + [
                        "anime face",
                        "CGI skin",
                        "plastic skin",
                        "over-smoothed face",
                        "extra fingers",
                        "extra hands",
                        "distorted toddler body",
                        "floating objects"
    ]
)
}

                clip2_dict = {
                    "clip": 2,
                    "ratio": "9:16",
                    "duration": "0-8 seconds",
                    "video_type": "ultra realistic continuation smartphone selfie video",
                    "continuity": {
    "continue_from_clip_1": True,
    "same_mother": True,
    "same_child": True,
    "same_outfit": True,
    "preserve_face_identity": True,
    "preserve_clothing_identity": True,
    "no_product_morphing": True,

    "same_selfie_recording_logic": True,
    "same_phone_holding_hand": True,
    "same_hand_roles": True,
    "same_camera_behavior": True,
    "same_room_environment": True,
    "same_character_positions": True,
    "same_interaction_style": True,
    "same_emotional_tone": True,

    "do_not_restart_scene_from_new_angle": True,
    "do_not_generate_new_camera_setup": True,
    "do_not_change_pose_logic": True,
    "do_not_change_mother_child_distance": True,
    "do_not_create_new_unrelated_action": True,

    "clip_2_must_feel_like_natural_continuation_of_clip_1": True
},
                    "content_idea": ide["judul"],
                    "product_lock": product_lock_json,
                    "character_identity_lock": character_identity_lock_json,
                    "voice_ownership_lock": voice_ownership_lock_json,
                    "characters": common_characters,
                    "camera": base_camera,
                    "child_expression_lock": child_natural_expression_lock_text,
                    "speaker_and_lipsync_lock": speaker_lipsync_lock_text,
                    "audio_clean_lock": audio_clean_lock_text,
                    "selfie_hand_outfit_lock": selfie_hand_outfit_lock_text,
                    "scene_analysis_lock": scene_analysis_lock_text,
		    "uploaded_photo_analysis": uploaded_photo_analysis_text,
		    "auto_safety_rules": auto_safety_rules,
		    "pose_aware_camera_rule": pose_aware_camera_rule,
		    "dialogue_rule": {
                        "total_speaking_turns": 2,
                        "turn_1": "mother speaks only",
                        "turn_2": "child speaks only",
                        "no_third_dialogue": True,
                        "no_extra_dialogue_after_child": True,
                        "no_repeated_dialogue": True,
                        "no_overlapping_voices": True,
                        "when_mother_speaks": "only mother's mouth moves",
                        "when_child_speaks": "only child's mouth moves",
                        "child_dialogue_must_be_spoken_by_child_voice": True,
                        "mother_must_not_speak_child_line": True
                    },

                         "action_timeline": [
                        {
                            "time": "0-4s",
                            "speaker": "mother_only",
                            "dialogue": "Bahannya adem, dipakai main juga tetap nyaman.",
                            "action": "Mother and child continue in the same stable frame and same pose logic from clip 1. Camera stays almost static with no zoom, no dip, and no sudden reframing. The child stays cute, relaxed, and naturally reacts without speaking yet.",
                            "product_visibility": "full two-piece set visible: sleeveless ruffle top, ruffled collar, exactly 3 brown coconut-shell buttons with 2 visible sewing holes each, peplum ruffle, and matching ruffle shorts",
                            "mother_mouth_state": "active_speaking",
                            "child_mouth_state": "closed_no_lipsync"
                        },
                        {
                            "time": "4-8s",
                            "speaker": "child_only",
                            "dialogue": "Aku suka, Bunda!",
                            "action": "Child looks forward naturally with a cute shy-but-happy toddler expression, soft smile, subtle blinking, and tiny head tilt only. Mother smiles warmly but does not speak again. No third dialogue after the child.",
                            "product_visibility": "same vertical blue-white stripes, same ruffled collar, same peplum, same matching shorts, same 3 brown coconut-shell buttons with 2 visible holes each",
                            "mother_mouth_state": "closed_no_lipsync",
                            "child_mouth_state": "active_speaking"
                        }
                    ],

             "negative_prompt": (
               product_negative_rules
               + selfie_negative_rules
               + voice_negative_rules
               + audio_negative_rules
               + hand_outfit_negative_rules
               + scene_conflict_negative_rules
               + [     
                        "outfit changes from clip 1",
                        "extra buttons",
                        "missing buttons",
                        "changed collar",
                        "changed shorts",
                        "wrong garment type",
                        "anime face",
                        "CGI skin",
                        "extra limbs"
    ]
)
}

                clip1 = json.dumps(clip1_dict, ensure_ascii=False, indent=2)
                clip2 = json.dumps(clip2_dict, ensure_ascii=False, indent=2)

            else:
                # --- FORMAT TEXT CINEMATIC LEBIH KUAT UNTUK LOCK PRODUK ---

                clip1 = f"""
Create ultra realistic vertical 9:16 smartphone selfie video (0-8s).
Create ultra realistic vertical 9:16 smartphone selfie video (0-8s).
Style: {style_hint}. {selling_hint}. {durasi_hint}.
Scene: Hook + Mother & Child selfie interaction at {lokasi_cerita}.

SELFIE RECORDING LOCK:
This video should feel like a stable natural smartphone recording, using almost static framing and minimal camera movement.
The mother holds the phone with ONE HAND ONLY.
The hand holding the phone should be partially visible or mostly out of frame because it is being used to hold the recording phone.
Do not show any second camera.
Do not show any cameraman.
Do not show any third person.
Only the mother and the child are present in the recording.
No tripod shot.
No external filming angle.
No cinematic third-person camera.
No security camera angle.
No mirror shot.
No other people in the room.
The framing must feel like a real handheld front-camera selfie video recorded directly by the mother.
The phone itself should remain mostly invisible, because it is the recording device.
Natural slight handheld shake from one-handed recording is allowed.

{child_natural_expression_lock_text}

{speaker_lipsync_lock_text}

{audio_clean_lock_text}

{selfie_hand_outfit_lock_text}

{scene_analysis_lock_text}

{product_prompt_lock_text}

{product_prompt_lock_text}

Mother behavior:
{behavior_ibu_hint}

Child behavior:
{behavior_anak_hint}

Camera:
{camera_interaction_hint}
Handheld smartphone movement, natural indoor daylight, slight real-camera imperfection.

Important action:
- Show the front of the child's outfit clearly.
- Show the ruffled collar, sleeveless shoulder ruffles, exactly 3 brown buttons, peplum ruffle, and matching shorts.
- Do not cover the buttons with hand/body.

{visual_safety_hint}
"""

                clip2 = f"""
Create continuation ultra realistic vertical 9:16 smartphone selfie video (0-8s).
SAME mother, SAME child, SAME outfit as clip 1.
No product morphing between clips.

SELFIE RECORDING LOCK:
This video should feel like a stable natural smartphone recording, using almost static framing and minimal camera movement.
The mother holds the phone with ONE HAND ONLY.
The hand holding the phone should be partially visible or mostly out of frame because it is being used to hold the recording phone.
Do not show any second camera.
Do not show any cameraman.
Do not show any third person.
Only the mother and the child are present in the recording.
No tripod shot.
No external filming angle.
No cinematic third-person camera.
No security camera angle.
No mirror shot.
No other people in the room.
The framing must feel like a real handheld front-camera selfie video recorded directly by the mother.
The phone itself should remain mostly invisible, because it is the recording device.
Natural slight handheld shake from one-handed recording is allowed.

{child_natural_expression_lock_text}

{speaker_lipsync_lock_text}

{product_prompt_lock_text}

Action: Detail focus + natural closing.
Action: Detail focus + natural closing.
- Keep the same 3 brown front buttons.
- Keep the same vertical blue-white stripes.
- Keep the same sleeveless ruffle top.
- Keep matching shorts visible with ruffle trim.
- Do not turn the outfit into dress, skirt, pajamas, romper, or generic clothing.

Camera:
{camera_interaction_hint}
Natural handheld smartphone movement, realistic home video look.

{visual_safety_hint}
"""

            # ===== SIMPAN TEXT DAN JSON =====
            # Text Cinematic sudah selalu dibuat di atas sebagai text_clip1 dan text_clip2.
            # JSON Cinematic juga sudah selalu dibuat di atas sebagai clip1 dan clip2.
            # Jadi dua-duanya selalu disimpan agar bisa dicopy bebas.
            json_clip1 = clip1.strip()
            json_clip2 = clip2.strip()

            semua_prompt.append({
                "clip1": clip1.strip(),
                "clip2": clip2.strip(),
                "text_clip1": text_clip1,
                "text_clip2": text_clip2,
                "json_clip1": json_clip1,
                "json_clip2": json_clip2,
                "format_utama": format_prompt
            })

        st.session_state["semua_prompt_video"] = semua_prompt    
    if "semua_prompt_video" in st.session_state:
        for i, item in enumerate(st.session_state["semua_prompt_video"], start=1):

            st.markdown(f"## 🎬 Ide {i}")

            if item.get("format_utama") == "JSON Cinematic":
                st.markdown("### JSON Cinematic")

                with st.expander("JSON CLIP 1 (0–8 detik)", expanded=True):
                    st.text_area(
                        "JSON Prompt Clip 1",
                        item.get("json_clip1", item.get("clip1", "")),
                        height=300,
                        key=f"json_clip1_{i}"
                    )

                with st.expander("JSON CLIP 2 (0–8 detik lanjutan)"):
                    st.text_area(
                        "JSON Prompt Clip 2",
                        item.get("json_clip2", item.get("clip2", "")),
                        height=300,
                        key=f"json_clip2_{i}"
                    )

                st.markdown("### Text Cinematic")

                with st.expander("TEXT CLIP 1 (0–8 detik)"):
                    st.text_area(
                        "Text Prompt Clip 1",
                        item.get("text_clip1", ""),
                        height=300,
                        key=f"text_clip1_{i}"
                    )

                with st.expander("TEXT CLIP 2 (0–8 detik lanjutan)"):
                    st.text_area(
                        "Text Prompt Clip 2",
                        item.get("text_clip2", ""),
                        height=300,
                        key=f"text_clip2_{i}"
                    )

            else:
                st.markdown("### Text Cinematic")

                with st.expander("TEXT CLIP 1 (0–8 detik)", expanded=True):
                    st.text_area(
                        "Text Prompt Clip 1",
                        item.get("text_clip1", item.get("clip1", "")),
                        height=300,
                        key=f"text_clip1_{i}"
                    )

                with st.expander("TEXT CLIP 2 (0–8 detik lanjutan)"):
                    st.text_area(
                        "Text Prompt Clip 2",
                        item.get("text_clip2", item.get("clip2", "")),
                        height=300,
                        key=f"text_clip2_{i}"
                    )

                st.markdown("### JSON Cinematic")

                with st.expander("JSON CLIP 1 (0–8 detik)"):
                    st.text_area(
                        "JSON Prompt Clip 1",
                        item.get("json_clip1", ""),
                        height=300,
                        key=f"json_clip1_{i}"
                    )

                with st.expander("JSON CLIP 2 (0–8 detik lanjutan)"):
                    st.text_area(
                        "JSON Prompt Clip 2",
                        item.get("json_clip2", ""),
                        height=300,
                        key=f"json_clip2_{i}"
                    )

  