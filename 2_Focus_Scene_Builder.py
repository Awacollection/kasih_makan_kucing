import streamlit as st
from auth import check_login

check_login()
from theme import apply_black_green_theme
import json

st.set_page_config(
    page_title="Referensi Ide Konten Manual",
    layout="wide"
)

apply_black_green_theme()

st.title("Referensi Ide Konten Manual")

st.info(
    "Halaman ini dipakai untuk membuat ide konten manual tanpa memilih kategori marketplace. "
    "Cocok untuk ide bebas seperti miniatur mobil, mainan, edukasi, hiburan, animasi, stop motion, showcase produk, dan konten komersil."
)

# ===== INPUT UTAMA =====
col1, col2 = st.columns([0.35, 0.65], gap="large")

with col1:
    product_image = st.file_uploader(
        "Upload Produk / Referensi Visual",
        type=["jpg", "jpeg", "png"],
        help="Upload gambar produk atau referensi visual. Contoh: miniatur mobil, mainan, produk koleksi, scene, atau karakter."
    )

    if product_image:
        st.image(
            product_image,
            caption="Preview Produk / Referensi Visual",
            width=280
        )

with col2:
    manual_ide_prompt = st.text_area(
        "Arahan Ide Konten Manual",
        placeholder=(
            "Contoh: Berikan ide konten untuk mobil miniatur yang sedang berada "
            "di jalan sebuah kota miniatur yang sedang padat penduduk."
        ),
        height=150
    )

    tujuan_konten = st.selectbox(
        "Tujuan Konten",
        [
            "Hiburan",
            "Pendidikan",
            "Komersil",
            "Review Produk",
            "Storytelling",
            "Aesthetic / Showcase",
            "Edukasi + Soft Selling",
            "Iklan / Hard Selling",
            "Konten Viral / Fun",
            "Konten Koleksi / Hobi"
        ]
    )

    jenis_visual = st.selectbox(
        "Jenis Visual / Format Konten",
        [
            "Realistic Video",
            "Animasi 2D",
            "Animasi 3D",
            "Stop Motion",
            "Motion Graphic",
            "Miniature Realism",
            "Cinematic Realism",
            "Cartoon Style",
            "Clay Animation",
            "Anime Style",
            "Toy Photography Style"
        ]
    )

    angle_kamera = st.selectbox(
        "Tampilan / Angle Kamera",
        [
            "Eye Level / Sejajar Mata",
            "Top View / Dari Atas",
            "Low Angle / Dari Bawah",
            "Macro Close Up",
            "Street Level Miniature",
            "Tracking Shot",
            "POV Jalanan Miniatur",
            "Wide Shot Kota Miniatur",
            "Over The Shoulder",
            "Handheld Natural",
            "Slow Push In",
            "Side Tracking",
            "Bird Eye View",
            "Dolly In Cinematic"
        ]
    )

    gaya_visual = st.selectbox(
        "Gaya Visual",
        [
            "Realistic Natural",
            "Cinematic",
            "Miniature Realism",
            "UGC Natural",
            "Commercial Clean",
            "Storytelling Dramatic",
            "Aesthetic Soft",
            "Fun Playful",
            "Educational Clean",
            "Premium Product Look"
        ]
    )

    durasi_video = st.selectbox(
        "Durasi Video",
        [
            "Pendek (5-8 detik)",
            "Sedang (8-15 detik)",
            "Panjang (15-30 detik)"
        ]
    )

st.markdown("---")


# ===== FUNGSI BANTU =====
def get_tujuan_hint(tujuan):
    if tujuan == "Hiburan":
        return "Fokus pada konten yang menyenangkan, ringan, lucu, menarik perhatian, dan mudah dinikmati."
    elif tujuan == "Pendidikan":
        return "Fokus pada penjelasan yang mudah dipahami, informatif, dan memberi pengetahuan ringan."
    elif tujuan == "Komersil":
        return "Fokus pada menonjolkan produk secara natural agar terlihat menarik untuk dibeli."
    elif tujuan == "Review Produk":
        return "Fokus pada detail produk, bentuk, fungsi, keunggulan, dan pengalaman penggunaan."
    elif tujuan == "Storytelling":
        return "Fokus pada alur cerita yang punya awal, tengah, dan akhir."
    elif tujuan == "Aesthetic / Showcase":
        return "Fokus pada visual yang rapi, indah, detail, dan menonjolkan objek utama."
    elif tujuan == "Edukasi + Soft Selling":
        return "Fokus pada edukasi ringan sambil memperkenalkan produk secara halus."
    elif tujuan == "Iklan / Hard Selling":
        return "Fokus pada pesan promosi yang jelas, kuat, dan langsung."
    elif tujuan == "Konten Viral / Fun":
        return "Fokus pada momen yang unik, lucu, mudah dibagikan, dan cepat menarik perhatian."
    else:
        return "Fokus pada konten hobi/koleksi yang menonjolkan nilai visual, detail, dan kepuasan pemilik produk."


def get_visual_hint(jenis):
    if jenis == "Realistic Video":
        return "Gunakan tampilan video realistis seperti direkam kamera nyata."
    elif jenis == "Animasi 2D":
        return "Gunakan gaya animasi 2D yang jelas, ekspresif, dan mudah dipahami."
    elif jenis == "Animasi 3D":
        return "Gunakan gaya animasi 3D dengan objek, gerakan, dan lingkungan yang konsisten."
    elif jenis == "Stop Motion":
        return "Gunakan gaya stop motion dengan gerakan bertahap seperti objek miniatur digerakkan frame-by-frame."
    elif jenis == "Motion Graphic":
        return "Gunakan gaya motion graphic yang bersih, informatif, dan memiliki elemen visual bergerak."
    elif jenis == "Miniature Realism":
        return "Gunakan gaya realisme miniatur, membuat objek kecil terlihat seperti dunia nyata versi kecil."
    elif jenis == "Cinematic Realism":
        return "Gunakan gaya cinematic realistis dengan framing rapi dan gerakan kamera halus."
    elif jenis == "Cartoon Style":
        return "Gunakan gaya kartun yang lucu, ringan, dan ekspresif."
    elif jenis == "Clay Animation":
        return "Gunakan gaya clay animation dengan tekstur seperti plastisin dan gerakan lucu."
    elif jenis == "Anime Style":
        return "Gunakan gaya anime yang ekspresif dan menarik, namun tetap mengikuti ide utama."
    else:
        return "Gunakan gaya fotografi mainan / toy photography dengan fokus pada detail objek kecil."


def get_angle_hint(angle):
    if angle == "Eye Level / Sejajar Mata":
        return "Kamera sejajar dengan objek, membuat scene terasa natural dan mudah dipahami."
    elif angle == "Top View / Dari Atas":
        return "Kamera dari atas untuk memperlihatkan layout scene, jalan, objek, dan suasana secara menyeluruh."
    elif angle == "Low Angle / Dari Bawah":
        return "Kamera dari bawah agar objek terlihat lebih dramatis, besar, dan heroik."
    elif angle == "Macro Close Up":
        return "Kamera sangat dekat untuk menonjolkan detail tekstur, bentuk, warna, dan fitur objek."
    elif angle == "Street Level Miniature":
        return "Kamera rendah sejajar jalan miniatur agar scene terasa seperti dunia kecil yang nyata."
    elif angle == "Tracking Shot":
        return "Kamera mengikuti gerakan objek utama secara halus."
    elif angle == "POV Jalanan Miniatur":
        return "Kamera seolah berada di dalam dunia miniatur, seperti sudut pandang dari jalan kecil."
    elif angle == "Wide Shot Kota Miniatur":
        return "Kamera lebar untuk menampilkan lingkungan miniatur secara luas."
    elif angle == "Over The Shoulder":
        return "Kamera dari belakang atau samping objek/karakter untuk memberi kesan mengikuti cerita."
    elif angle == "Handheld Natural":
        return "Kamera terasa natural dengan sedikit gerakan tangan yang realistis."
    elif angle == "Slow Push In":
        return "Kamera bergerak perlahan mendekati objek utama untuk membangun fokus."
    elif angle == "Side Tracking":
        return "Kamera bergerak dari samping mengikuti objek utama."
    elif angle == "Bird Eye View":
        return "Kamera sangat tinggi dari atas seperti pemandangan peta."
    else:
        return "Kamera bergerak masuk secara cinematic untuk memperkuat fokus pada objek utama."


# ===== GENERATE IDE =====
st.markdown("### Generate Ide Konten Manual")

if st.button("Generate 5 Ide Konten Manual", use_container_width=True):

    if not manual_ide_prompt.strip():
        st.warning("Isi dulu Arahan Ide Konten Manual.")
    else:
        tujuan_hint = get_tujuan_hint(tujuan_konten)
        visual_hint = get_visual_hint(jenis_visual)
        angle_hint = get_angle_hint(angle_kamera)

        ide_konten_manual = [
            {
                "judul": "1. Opening Scene yang Menarik",
                "alur": (
                    f"Buat pembuka konten berdasarkan arahan: {manual_ide_prompt}. "
                    f"Scene dimulai dengan pengenalan objek utama dan suasana. "
                    f"Tujuan konten: {tujuan_konten}. {tujuan_hint} "
                    f"Gunakan jenis visual: {jenis_visual}. {visual_hint} "
                    f"Gunakan angle kamera: {angle_kamera}. {angle_hint}"
                ),
                "kamera": angle_kamera,
                "tujuan": "Membuat penonton langsung memahami konsep utama konten."
            },
            {
                "judul": "2. Detail Produk dan Lingkungan",
                "alur": (
                    f"Tampilkan detail produk atau objek utama secara rinci berdasarkan arahan: {manual_ide_prompt}. "
                    f"Fokus pada bentuk, ukuran, tekstur, warna, suasana sekitar, dan elemen pendukung scene. "
                    f"Gaya visual: {gaya_visual}. Jenis visual: {jenis_visual}."
                ),
                "kamera": f"Kombinasi {angle_kamera} dengan close up detail.",
                "tujuan": "Menonjolkan detail produk dan membangun dunia visual yang jelas."
            },
            {
                "judul": "3. Storytelling Scene",
                "alur": (
                    f"Buat alur cerita pendek dari ide: {manual_ide_prompt}. "
                    f"Scene harus terasa hidup, punya awal, tengah, dan akhir. "
                    f"Jika objek utama adalah produk, produk harus menjadi bagian penting dari cerita."
                ),
                "kamera": angle_kamera,
                "tujuan": "Membuat konten terasa punya cerita, bukan hanya tampilan produk."
            },
            {
                "judul": "4. Nilai Konten Sesuai Tujuan",
                "alur": (
                    f"Sesuaikan ide dengan tujuan konten: {tujuan_konten}. {tujuan_hint} "
                    f"Konten harus tetap mengikuti arahan utama: {manual_ide_prompt}. "
                    f"Jangan membuat objek atau cerita yang keluar dari ide utama."
                ),
                "kamera": "Kamera mengikuti objek utama secara natural.",
                "tujuan": "Menyesuaikan pesan konten dengan tujuan yang dipilih."
            },
            {
                "judul": "5. Closing Scene yang Berkesan",
                "alur": (
                    f"Tutup video dengan shot yang memperkuat ide utama: {manual_ide_prompt}. "
                    f"Objek utama tetap menjadi fokus akhir. "
                    f"Gunakan gaya visual {gaya_visual} dan format {jenis_visual}."
                ),
                "kamera": "Closing shot yang jelas, rapi, dan mudah diingat.",
                "tujuan": "Memberi penutup konten yang kuat dan mudah dipahami."
            }
        ]

        st.session_state["ide_konten_manual"] = ide_konten_manual

if "ide_konten_manual" in st.session_state:

    if st.button("🔄 Reset Ide Manual", use_container_width=True):
        del st.session_state["ide_konten_manual"]
        if "prompt_manual" in st.session_state:
            del st.session_state["prompt_manual"]
        st.rerun()

    st.markdown("### Hasil 5 Ide Konten Manual")

    for i, ide in enumerate(st.session_state["ide_konten_manual"], start=1):
        with st.expander(ide["judul"]):
            st.write("**Alur Cerita:**")
            st.write(ide["alur"])
            st.write("**Cara Kamera:**")
            st.write(ide["kamera"])
            st.write("**Tujuan Konten:**")
            st.write(ide["tujuan"])

    st.markdown("### Jadikan Semua Ide Menjadi Prompt")

    if st.button("Jadikan Semua Ide Prompt Manual", use_container_width=True):
        semua_prompt = []

        product_status = (
            "Uploaded product/reference image is available. Use it as the absolute visual reference for the main product/object."
            if product_image
            else "No product/reference image uploaded. Use the manual idea text as the main visual guide."
        )

        tujuan_hint = get_tujuan_hint(tujuan_konten)
        visual_hint = get_visual_hint(jenis_visual)
        angle_hint = get_angle_hint(angle_kamera)

        for ide in st.session_state["ide_konten_manual"]:

            text_clip1 = f"""
Create ultra realistic vertical 9:16 video based on this manual content idea.

MANUAL IDEA:
{manual_ide_prompt}

CONTENT PURPOSE:
{tujuan_konten}
{tujuan_hint}

VISUAL FORMAT:
{jenis_visual}
{visual_hint}

CAMERA ANGLE:
{angle_kamera}
{angle_hint}

VISUAL STYLE:
{gaya_visual}

DURATION:
{durasi_video}

PRODUCT / VISUAL REFERENCE:
{product_status}

CONTENT IDEA:
{ide["judul"]}

STORY FLOW:
{ide["alur"]}

CAMERA DIRECTION:
{ide["kamera"]}

CLIP 1 PURPOSE:
Open the scene, introduce the main object/product, show the environment clearly, and make the viewer understand the concept.

IMPORTANT RULES:
- Follow the uploaded product/reference image if available.
- Do not randomly redesign the main product/object.
- Keep the product/object identity consistent.
- Keep the scene consistent with the manual idea.
- Use the selected visual format: {jenis_visual}.
- Use the selected camera angle: {angle_kamera}.
- Make the video visually clear and easy to understand.
- Keep realistic motion and natural camera movement when using realistic style.
- If using animation style, keep object shape and scene logic consistent.
- Avoid random objects that are not related to the idea.
- Avoid changing the main product/object into another object.
""".strip()

            text_clip2 = f"""
Create continuation vertical 9:16 video for the same manual content idea.

CONTINUITY:
Continue from Clip 1.
Use the same product/object.
Use the same visual world and same scene logic.
Do not change the main object design.
Do not introduce unrelated new objects.

MANUAL IDEA:
{manual_ide_prompt}

CONTENT PURPOSE:
{tujuan_konten}
{tujuan_hint}

VISUAL FORMAT:
{jenis_visual}
{visual_hint}

CAMERA ANGLE:
{angle_kamera}
{angle_hint}

VISUAL STYLE:
{gaya_visual}

CONTINUATION STORY:
{ide["alur"]}

CLIP 2 PURPOSE:
Continue the story, show more detail, strengthen the selected purpose, and create a natural closing or continuation.

IMPORTANT RULES:
- Keep product/object identity consistent.
- Keep the same environment style.
- Keep the same visual format: {jenis_visual}.
- Keep the same camera direction logic: {angle_kamera}.
- Do not create unrelated new objects.
- Do not change the main product/object design.
- Make the continuation or closing feel natural.
""".strip()

            json_clip1_dict = {
                "clip": 1,
                "ratio": "9:16",
                "duration": durasi_video,
                "video_type": "manual idea cinematic video",
                "manual_idea": manual_ide_prompt,
                "content_purpose": {
                    "selected": tujuan_konten,
                    "instruction": tujuan_hint
                },
                "visual_format": {
                    "selected": jenis_visual,
                    "instruction": visual_hint
                },
                "camera_angle": {
                    "selected": angle_kamera,
                    "instruction": angle_hint
                },
                "visual_style": gaya_visual,
                "product_reference_status": product_status,
                "content_idea": ide["judul"],
                "story_flow": ide["alur"],
                "camera_direction": ide["kamera"],
                "clip_purpose": "Open the scene, introduce the main object/product, show the environment clearly, and make the viewer understand the concept.",
                "rules": [
                    "Follow uploaded product/reference image if available.",
                    "Do not randomly redesign the main product or object.",
                    "Keep the product/object identity consistent.",
                    "Keep the scene consistent with the manual idea.",
                    f"Use the selected visual format: {jenis_visual}.",
                    f"Use the selected camera angle: {angle_kamera}.",
                    "Make the video visually clear and easy to understand.",
                    "Avoid unrelated random objects.",
                    "Avoid changing the main product/object into another object."
                ]
            }

            json_clip2_dict = {
                "clip": 2,
                "ratio": "9:16",
                "duration": durasi_video,
                "video_type": "manual idea continuation video",
                "continuity": {
                    "continue_from_clip_1": True,
                    "same_product_or_object": True,
                    "same_visual_world": True,
                    "same_visual_format": jenis_visual,
                    "same_camera_logic": angle_kamera,
                    "no_random_redesign": True
                },
                "manual_idea": manual_ide_prompt,
                "content_purpose": {
                    "selected": tujuan_konten,
                    "instruction": tujuan_hint
                },
                "visual_format": {
                    "selected": jenis_visual,
                    "instruction": visual_hint
                },
                "camera_angle": {
                    "selected": angle_kamera,
                    "instruction": angle_hint
                },
                "visual_style": gaya_visual,
                "product_reference_status": product_status,
                "content_idea": ide["judul"],
                "continuation_story": ide["alur"],
                "clip_purpose": "Continue the story, show more detail, strengthen the selected purpose, and create a natural closing or continuation.",
                "rules": [
                    "Keep product/object identity consistent.",
                    "Keep the same environment style.",
                    f"Keep the same visual format: {jenis_visual}.",
                    f"Keep the same camera direction logic: {angle_kamera}.",
                    "Do not create unrelated new objects.",
                    "Do not change the main product/object design.",
                    "Make the continuation or closing feel natural."
                ]
            }

            json_clip1 = json.dumps(json_clip1_dict, ensure_ascii=False, indent=2)
            json_clip2 = json.dumps(json_clip2_dict, ensure_ascii=False, indent=2)

            semua_prompt.append({
                "judul": ide["judul"],
                "text_clip1": text_clip1,
                "text_clip2": text_clip2,
                "json_clip1": json_clip1,
                "json_clip2": json_clip2
            })

        st.session_state["prompt_manual"] = semua_prompt

if "prompt_manual" in st.session_state:
    st.markdown("### Hasil Prompt Manual")

    for i, item in enumerate(st.session_state["prompt_manual"], start=1):
        st.markdown(f"## 🎬 Ide Manual {i}: {item['judul']}")

        st.markdown("### Text Cinematic")

        with st.expander("TEXT CLIP 1", expanded=True):
            st.text_area(
                "Text Prompt Clip 1",
                item["text_clip1"],
                height=320,
                key=f"manual_text_clip1_{i}"
            )

        with st.expander("TEXT CLIP 2"):
            st.text_area(
                "Text Prompt Clip 2",
                item["text_clip2"],
                height=320,
                key=f"manual_text_clip2_{i}"
            )

        st.markdown("### JSON Cinematic")

        with st.expander("JSON CLIP 1"):
            st.text_area(
                "JSON Prompt Clip 1",
                item["json_clip1"],
                height=320,
                key=f"manual_json_clip1_{i}"
            )

        with st.expander("JSON CLIP 2"):
            st.text_area(
                "JSON Prompt Clip 2",
                item["json_clip2"],
                height=320,
                key=f"manual_json_clip2_{i}"
            )