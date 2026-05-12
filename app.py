import streamlit as st
# =====================================================
# GLOBAL PASSWORD LOGIN
# =====================================================

APP_PASSWORD = "ronald371011"

if "login_berhasil" not in st.session_state:
    st.session_state["login_berhasil"] = False

if not st.session_state["login_berhasil"]:

    st.title("Login Web")

    password = st.text_input(
        "Masukkan Password",
        type="password"
    )

    if st.button("Masuk"):

        if password == APP_PASSWORD:

            st.session_state["login_berhasil"] = True

            st.rerun()

        else:

            st.error("Password salah.")

    st.stop()
try:
    from theme import apply_black_green_theme
    apply_black_green_theme()
except Exception:
    pass

# ================= STYLE =================
st.markdown("""
<style>
.stApp {
    background:#030609;
    color:#ffffff;
}

.block-container {
    padding:24px;
}

/* SEMUA TEKS DEFAULT JADI PUTIH */
h1, h2, h3, h4, h5, h6,
p, span, div, label {
    color:#ffffff !important;
}

/* SEMUA CARD OUTLINE HIJAU */
.card {
    background:#081018;
    border:2px solid #2ED573;
    border-radius:14px;
    padding:16px;
    min-height:430px;
    box-shadow:0 0 14px rgba(46,213,115,.25);
    color:#ffffff !important;
}

/* SEMUA TULISAN DALAM CARD PUTIH */
.card,
.card * {
    color:#ffffff !important;
}

/* JUDUL CARD */
.card-title {
    color:#2ED573 !important;
    font-weight:900;
    margin-bottom:12px;
    border-bottom:1px solid #2ED573;
    padding-bottom:8px;
}

/* INPUT OUTLINE HIJAU */
.stTextInput input,
.stTextArea textarea {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
    border-radius:8px !important;
}

/* PLACEHOLDER INPUT */
input::placeholder,
textarea::placeholder {
    color:#b8c0c8 !important;
}

/* LABEL INPUT, SELECTBOX, UPLOAD */
label,
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label {
    color:#ffffff !important;
}

/* SELECTBOX OUTLINE HIJAU */
div[data-baseweb="select"] > div {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
    border-radius:8px !important;
}

div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color:#ffffff !important;
}

/* DROPDOWN MENU */
div[data-baseweb="popover"],
ul[role="listbox"] {
    background:#0d141c !important;
    border:1px solid #2ED573 !important;
}

li[role="option"],
li[role="option"] * {
    background:#0d141c !important;
    color:#ffffff !important;
}

li[role="option"]:hover,
li[aria-selected="true"] {
    background:#143d2a !important;
    color:#ffffff !important;
}

/* UPLOAD BOX */
[data-testid="stFileUploader"] {
    background:#081018 !important;
    border:2px dashed #2ED573 !important;
    border-radius:12px !important;
    padding:16px !important;
    min-height:135px !important;
    text-align:center !important;
}

/* AREA DALAM UPLOADER */
[data-testid="stFileUploader"] section {
    background:transparent !important;
    border:none !important;
    min-height:90px !important;
    display:flex !important;
    align-items:center !important;
    justify-content:center !important;
    text-align:center !important;
}

/* TEKS UPLOADER PUTIH */
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div {
    color:#ffffff !important;
}

/* IKON UPLOAD PUTIH */
[data-testid="stFileUploader"] svg {
    color:#ffffff !important;
    fill:#ffffff !important;
    width:34px !important;
    height:34px !important;
}

/* TOMBOL BROWSE */
[data-testid="stFileUploader"] button {
    background:#2ED573 !important;
    color:#030609 !important;
    border:1px solid #2ED573 !important;
    border-radius:8px !important;
    font-weight:900 !important;
}

/* FRAME PREVIEW UPLOAD */
.upload-preview-frame {
    border:2px solid #2ED573;
    border-radius:12px;
    padding:8px;
    background:#05080c;
    margin-top:8px;
    margin-bottom:14px;
}

/* BUTTON HIJAU */
.stButton > button {
    background:#2ED573 !important;
    color:#030609 !important;
    border:2px solid #2ED573 !important;
    border-radius:10px !important;
    font-weight:900 !important;
}

/* CODE BOX OUTLINE HIJAU */
.stCodeBlock,
.stCodeBlock pre,
.stCodeBlock code,
pre,
code {
    background:#0b1016 !important;
    color:#2ED573 !important;
    border:1px solid #2ED573 !important;
    border-radius:8px !important;
}

/* TEXT AREA JSON OUTLINE HIJAU */
textarea {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
}

/* INFO / ALERT */
.stAlert {
    border:1px solid #2ED573 !important;
    border-radius:8px !important;
}

.stAlert div {
    color:#ffffff !important;
}

/* IMAGE PREVIEW */
img {
    border-radius:10px !important;
    border:1px solid rgba(46,213,115,.45) !important;
}

</style>
""", unsafe_allow_html=True)

# ================= DATA =================
DATABASE_KATEGORI = {
    "👗 PAKAIAN WANITA": ["Atasan", "Bawahan", "Dress", "Setelan", "Outer", "Hijab"],
    "👕 PAKAIAN PRIA": ["Kaos", "Kemeja", "Celana", "Jaket"],
    "🧒 PAKAIAN ANAK": ["Oneset Anak", "Kaos Anak", "Celana Anak", "Dress Anak"],
    "💄 KECANTIKAN": ["Skincare", "Makeup", "Body Care"],
    "🏠 RUMAH TANGGA": ["Dapur", "Dekorasi", "Kamar Mandi"],
    "🎮 GAMING": ["Console", "Aksesoris", "Top Up"]
}

CHARACTER_STYLE = [
    "Realistic Human Proportion",
    "Semirealistic Beauty Character",
    "Stylized Cartoon Iconic Character",
    "Western Style",
    "Eastern Anime / Manga / Manhwa",
    "Indie / Artisanal Style",
    "Cyberpunk / Futuristic",
    "Y2K / Retro",
    "Dark / Gothic / Grunge",
    "Cottagecore",
    "High-Street / Hypebeast",
    "Kawaii / Chibi",
    "Minimalist / Line Art",
    "Korean Look Female Model",
    "Streetwear Fashion Model",
    "Luxury Brand Model",
    "UGC TikTok Creator",
    "Other / Custom Style"
]

# ================= LOGIC =================
def clean_product_name(product):
    product = product.strip()
    if not product:
        return "produk ini"
    if len(product) > 45:
        return "produk ini"
    return product


def optimize_voice_for_lipsync(text, duration):
    text = text.strip()

    replacements = {
        "produk ini": "ini",
        "celana ini": "ini",
        "tanpa effort": "tanpa ribet",
        "sebelum kehabisan": "sekarang"
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    max_chars = 55

    if "5" in duration:
        max_chars = 38
    elif "8" in duration:
        max_chars = 52
    elif "10" in duration:
        max_chars = 65
    elif "15" in duration:
        max_chars = 90
    elif "20" in duration:
        max_chars = 120
    elif "30" in duration:
        max_chars = 160

    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0]

    return text


def extract_keywords(note):
    text = note.lower()
    keywords = []

    mapping = {
        "jenjang": "kaki terlihat lebih jenjang",
        "timeless": "desain timeless",
        "slim": "siluet lebih ramping",
        "straight": "potongan straight leg",
        "drapey": "bahan jatuh natural",
        "ringan": "bahan ringan",
        "flowy": "gerakan kain flowy",
        "premium": "look premium",
        "nyaman": "nyaman dipakai"
    }

    for k, v in mapping.items():
        if k in text:
            keywords.append(v)

    return keywords[:5] if keywords else ["nyaman dipakai", "look premium"]


def make_ideas(product, note):
    p = clean_product_name(product)
    keys = extract_keywords(note)
    k1 = keys[0]

    return [
        {
            "name": "HOOK",
            "story": "Model muncul dengan close-up outfit, lalu kamera bergerak pelan menampilkan detail produk.",
            "voice": f"{p} bikin look kamu rapi tanpa effort."
        },
        {
            "name": "MASALAH",
            "story": "Model terlihat bingung memilih outfit yang nyaman tapi tetap stylish.",
            "voice": "Sering cari celana yang nyaman tapi tetap bikin kaki terlihat jenjang?"
        },
        {
            "name": "SOLUSI",
            "story": f"Model memakai produk, berjalan natural, dan memperlihatkan {k1}.",
            "voice": f"{p} bikin kaki terlihat jenjang dan tetap nyaman."
        },
        {
            "name": "PENUTUP",
            "story": "Model berhenti, tersenyum natural, lalu memperlihatkan full outfit.",
            "voice": f"{p}, simple dipakai dan tetap stylish."
        },
        {
            "name": "HARD SELLING",
            "story": "Produk tampil jelas, model menunjukkan detail bahan dan fit, lalu CTA kuat.",
            "voice": f"Checkout {p} sekarang sebelum kehabisan."
        }
    ]


def build_pack(product, category, sub, note, character, voice_style, tone, camera, ratio, duration, idea, has_product, has_model):
    short_product = clean_product_name(product)
    keywords = extract_keywords(note)
    voice_script = optimize_voice_for_lipsync(idea["voice"], duration)

    ref_rules = ""
    if has_model:
        ref_rules += "Use uploaded model image as the main character reference. Keep same face, body, hairstyle, and identity.\\n"
    if has_product:
        ref_rules += "Use uploaded product image as the main product reference. Keep same product shape, color, fabric, texture, and details.\\n"

    idea_name = idea["name"]
    idea_story = idea["story"]

    video_prompt = f"""
Create an ultra realistic vertical fashion ads video.

Reference rules:
{ref_rules}

Product:
{short_product}

Category:
{category} / {sub}

Character style:
{character}

Format:
{ratio}

Duration:
{duration}

Camera:
{camera}

Scene:
{idea_name}

Story:
{idea_story}

Spoken line:
"{voice_script}"

Audio rules:
No music.
No background sound.
No external narrator.
Only the model speaks directly to camera.
Voice style: {voice_style}
Tone: {tone}

Lip sync rules:
The voice must come from the model mouth.
Mouth movement must match every word clearly.
Use natural Indonesian speaking rhythm.
Use short, clear speech.
No robotic tone.
No delayed lip movement.

Motion rules:
Natural walking.
Natural hand movement.
Natural breathing.
Natural eye movement.
Natural facial expression.
Realistic fabric movement.

Consistency rules:
Same face across all frames.
Same body proportion.
Same hairstyle.
Same outfit direction.
Same product detail.
No face morphing.
No product morphing.
No frozen mouth.
No robotic movement.

Visual quality:
Ultra realistic skin texture.
Premium cinematic lighting.
Realistic camera movement.
Soft realistic shadow.
Natural cloth physics.
High-end fashion advertising style.
"""

    return {
        "engine": "RAW ENGINE PRO - FLOW PROMPT ENGINE",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product": {
            "name": product,
            "short_name": short_product,
            "category": category,
            "sub_category": sub,
            "keywords": keywords,
            "uploaded_product_reference": has_product
        },
        "character": {
            "style": character,
            "uploaded_model_reference": has_model
        },
        "video_setting": {
            "voice": voice_style,
            "tone": tone,
            "camera": camera,
            "ratio": ratio,
            "duration": duration
        },
        "selected_idea": {
            "name": idea_name,
            "story": idea_story,
            "original_voice": idea["voice"],
            "optimized_voice": voice_script
        },
        "flow_ai_copy_pack": {
            "video_prompt": video_prompt.strip(),
            "voice_script": voice_script,
            "negative_prompt": "no music, no bad lip sync, no robotic movement, no changing face, no distorted mouth, no fake walking, no blurry face, no cartoon, no anime, no frozen mouth"
        }
    }


# ================= UI =================
st.title("RAW ENGINE PRO")
st.caption("Ultra realistic Flow AI prompt generator — tanpa API, tanpa billing, siap copy paste.")

if "ideas" in st.session_state:
    st.subheader("5 Ide Video")
    for i, idea in enumerate(st.session_state["ideas"], start=1):
        with st.expander(f"{i}. {idea['name']}"):
            st.write("Cerita")
            st.code(idea["story"])
            st.write("Voice Script")
            st.code(idea["voice"])

# ================= REFERENSI IDE KONTEN =================
st.markdown("### Ide Referensi Konten")

content_idea = st.text_area(
    "Tulis referensi ide konten",
    placeholder="Contoh: model berjalan pelan, menunjukkan detail bahan, lalu full outfit...",
    height=90
)

if not content_idea.strip():
    content_idea = "Produk dipakai model secara natural, menampilkan detail produk dengan jelas."

c1, c2, c3 = st.columns([1, 1, 1.1], gap="medium")

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>01 // PRODUCT</div>", unsafe_allow_html=True)

    product_ref = st.file_uploader("Upload Produk", type=["jpg", "jpeg", "png"], key="product_ref")

    if product_ref:
        st.markdown("<div class='upload-preview-frame'>", unsafe_allow_html=True)
        st.image(product_ref, caption="Produk", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    product = st.text_input("Nama Produk Singkat", placeholder="Contoh: Joybasic Loose Casual Sweatpants")
    category = st.selectbox("Kategori", list(DATABASE_KATEGORI.keys()))
    sub = st.selectbox("Sub Kategori", DATABASE_KATEGORI[category])
    note = st.text_area("Deskripsi / Benefit Produk", placeholder="Masukkan bahan, benefit, target market, style, promo...", height=120)

    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>02 // CHARACTER & VIDEO</div>", unsafe_allow_html=True)

    model_ref = st.file_uploader("Upload Karakter", type=["jpg", "jpeg", "png"], key="model_ref")

    if model_ref:
        st.markdown("<div class='upload-preview-frame'>", unsafe_allow_html=True)
        st.image(model_ref, caption="Model", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    selected_character = st.selectbox("Character Style", CHARACTER_STYLE)

    if selected_character == "Other / Custom Style":
        custom_character = st.text_input("Masukkan custom character style")
        character = custom_character if custom_character.strip() else "Custom Character"
    else:
        character = selected_character

    voice_style = st.selectbox("Voice", [
        "Female Indonesia - Soft",
        "Female Indonesia - Energetic",
        "Female Indonesia - Luxury",
        "Male Indonesia - Deep",
        "Narrator Indonesia - Clean"
    ])

    tone = st.selectbox("Tone", ["Natural", "Soft", "Energetic", "Luxury", "Urgent"])

    camera = st.selectbox("Angle Kamera", [
        "1. Eye-Level",
        "2. Selfie Angle",
        "3. Low Angle",
        "4. High Angle",
        "5. Side Profile",
        "6. 45-Degree Angle",
        "7. POV",
        "8. Close-Up",
        "9. Extreme Close-Up",
        "10. Over the Shoulder",
        "11. Dutch Angle",
        "12. Wide Shot",
        "13. Top-Down / Flat Lay",
        "14. Worm's Eye View",
        "15. Handheld Shake",
        "16. Fish Eye"
    ])

    ratio = st.selectbox("Format", [
        "9:16 TikTok/Reels",
        "1:1 Marketplace",
        "16:9 YouTube",
        "4:5 Ads"
    ])

    duration = st.selectbox("Durasi", [
        "5 seconds",
        "8 seconds",
        "10 seconds",
        "15 seconds",
        "20 seconds",
        "30 seconds"
    ])

    if st.button("✨ BUAT 5 IDE VIDEO", use_container_width=True):
        if not product:
            st.warning("Isi nama produk dulu.")
        else:
            st.session_state["ideas"] = make_ideas(product, note)
            st.success("5 ide video berhasil dibuat.")

    st.markdown("</div>", unsafe_allow_html=True)

with c3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>03 // GENERATE PACK</div>", unsafe_allow_html=True)

    if "ideas" in st.session_state:
        selected_index = st.selectbox("Pilih Ide", list(range(1, 6))) - 1
        selected_idea = st.session_state["ideas"][selected_index]

        preview_voice = optimize_voice_for_lipsync(selected_idea["voice"], duration)

        st.write("Preview Voice Optimized")
        st.code(preview_voice)

        if st.button("⚡ GENERATE FLOW AI COPY PACK", use_container_width=True):
            st.session_state["pack"] = build_pack(
                product=product,
                category=category,
                sub=sub,
                note=note,
                character=character,
                voice_style=voice_style,
                tone=tone,
                camera=camera,
                ratio=ratio,
                duration=duration,
                idea=selected_idea,
                has_product=product_ref is not None,
                has_model=model_ref is not None
            )
            st.success("Pack berhasil dibuat.")
    else:
        st.info("Klik BUAT 5 IDE VIDEO dulu.")

    st.markdown("</div>", unsafe_allow_html=True)

if "pack" in st.session_state:
    pack = st.session_state["pack"]

    st.subheader("FLOW AI COPY PACK FINAL")

    st.write("VIDEO PROMPT")
    st.code(pack["flow_ai_copy_pack"]["video_prompt"])

    st.write("VOICE SCRIPT")
    st.code(pack["flow_ai_copy_pack"]["voice_script"])

    st.write("NEGATIVE PROMPT")
    st.code(pack["flow_ai_copy_pack"]["negative_prompt"])

    json_data = json.dumps(pack, indent=4, ensure_ascii=False)

    st.subheader("JSON FINAL — SIAP COPY HP")
    st.text_area("Tekan lama → Pilih Semua → Salin", json_data, height=420)
    st.info("Android: tekan lama teks → pilih semua → salin → paste ke Flow AI")