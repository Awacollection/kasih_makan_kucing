import streamlit as st
from auth import check_login

check_login()
from theme import apply_black_green_theme
import json
from datetime import datetime

st.set_page_config(page_title="ACTIVITY SCENE BUILDER", layout="wide")

apply_black_green_theme()

st.markdown("""
<style>
.stApp {
    background:#030609;
    color:#ffffff;
}

.block-container {
    padding:24px;
}

h1, h2, h3, h4, h5, h6,
p, span, div, label {
    color:#ffffff !important;
}

.card {
    background:#081018;
    border:2px solid #2ED573;
    border-radius:14px;
    padding:16px;
    min-height:430px;
    box-shadow:0 0 14px rgba(46,213,115,.25);
}

.card-title {
    color:#2ED573 !important;
    font-weight:900;
    margin-bottom:12px;
    border-bottom:1px solid #2ED573;
    padding-bottom:8px;
}

.stTextInput input,
.stTextArea textarea {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
    border-radius:8px !important;
}

input::placeholder,
textarea::placeholder {
    color:#b8c0c8 !important;
}

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
}

[data-testid="stFileUploader"] {
    background:#081018 !important;
    border:2px dashed #2ED573 !important;
    border-radius:12px !important;
    padding:14px !important;
}

[data-testid="stFileUploader"] * {
    color:#ffffff !important;
}

.stButton > button {
    background:#2ED573 !important;
    color:#030609 !important;
    border:2px solid #2ED573 !important;
    border-radius:10px !important;
    font-weight:900 !important;
}

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

textarea {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
}

/* SIDEBAR HITAM */
section[data-testid="stSidebar"] {
    background:#030609 !important;
    border-right:2px solid #2ED573 !important;
}

section[data-testid="stSidebar"] * {
    color:#ffffff !important;
}

section[data-testid="stSidebar"] a {
    color:#ffffff !important;
    background:#081018 !important;
    border:1px solid #2ED573 !important;
    border-radius:8px !important;
    margin-bottom:6px !important;
}

section[data-testid="stSidebar"] a:hover {
    background:#143d2a !important;
    color:#ffffff !important;
}

section[data-testid="stSidebar"] a[aria-current="page"] {
    background:#2ED573 !important;
    color:#030609 !important;
    font-weight:900 !important;
}

img {
    border-radius:10px !important;
    border:1px solid rgba(46,213,115,.45) !important;
}
</style>
""", unsafe_allow_html=True)


def build_activity_scene_pack(
    activity,
    location,
    time_of_day,
    camera_angle,
    output_type,
    use_model,
    model_name,
    model_description,
    model_file
):
    use_model_bool = use_model == "Ya"

    if use_model_bool:
        model_data = {
            "use_model": True,
            "model_name": model_name.strip() if model_name.strip() else "Model utama",
            "model_description": model_description.strip() if model_description.strip() else "Model natural sesuai scene",
            "uploaded_model_reference": model_file is not None
        }
    else:
        model_data = {
            "use_model": False,
            "model_name": None,
            "model_description": None,
            "uploaded_model_reference": False
        }

    prompt = f"""
Create a realistic activity scene.

ACTIVITY:
{activity}

LOCATION / ENVIRONMENT:
{location}

TIME:
{time_of_day}

CAMERA ANGLE:
{camera_angle}
""".strip()

    if use_model_bool:
        prompt += f"""

MODEL RULE:
Use the selected model as the main character.
Model name / type: {model_data["model_name"]}
Model description: {model_data["model_description"]}
Uploaded model reference: {model_data["uploaded_model_reference"]}

Keep the same face, body proportion, hairstyle, outfit direction, and identity if a model reference is uploaded.
"""

    prompt += """

REALISM RULE:
Ultra realistic environment, natural lighting, realistic object interaction, realistic human posture, realistic hand position, consistent object shape, natural shadow, no distorted anatomy, no fake hands, no broken fingers.
"""

    negative_prompt = (
        "no distorted hands, no extra fingers, no broken fingers, no bad anatomy, "
        "no unrealistic object interaction, no floating object, no blurry face, "
        "no cartoon, no anime, no plastic skin, no low quality, no messy background"
    )

    data = {
        "engine": "RAW ENGINE PRO - ACTIVITY SCENE BUILDER",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scene_input": {
            "activity": activity,
            "location_environment": location,
            "time": time_of_day,
            "camera_angle": camera_angle,
            "output_type": output_type
        },
        "model": model_data,
        "copy_pack": {
            "prompt_final": prompt,
            "negative_prompt": negative_prompt
        }
    }

    return data


st.title("ACTIVITY SCENE BUILDER")
st.caption("Buat scene aktivitas realistis. Pilih output: Prompt Biasa, JSON, atau Prompt + JSON.")

c1, c2 = st.columns([1, 1.15], gap="medium")

with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>01 // INPUT AKTIVITAS</div>", unsafe_allow_html=True)

    activity = st.text_area(
        "AKTIVITAS",
        value="karakter sedang memegang dus paket airprayer",
        height=90
    )

    location = st.text_area(
        "LOKASI / LINGKUNGAN",
        value="ruang tamu rumah minimalis di perkotaan Bandung",
        height=90
    )

    time_of_day = st.selectbox(
        "WAKTU",
        [
            "Pagi hari",
            "Siang hari",
            "Sore hari",
            "Malam hari",
            "Golden hour",
            "Indoor bright daylight"
        ],
        index=1
    )

    camera_angle = st.selectbox(
        "ANGLE KAMERA",
        [
            "Dari atas",
            "Eye level",
            "Dari bawah",
            "Close up",
            "Wide shot",
            "Side angle",
            "Over the shoulder",
            "Top down cinematic",
            "45 degree angle",
            "Handheld realistic shot"
        ],
        index=0
    )

    output_type = st.selectbox(
        "PILIH OUTPUT",
        [
            "Prompt Biasa",
            "JSON",
            "Prompt + JSON"
        ],
        index=2
    )

    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>02 // MODEL OPSIONAL & GENERATE</div>", unsafe_allow_html=True)

    use_model = st.selectbox(
        "Gunakan Model?",
        [
            "Tidak",
            "Ya"
        ],
        index=0
    )

    model_name = ""
    model_description = ""
    model_file = None

    if use_model == "Ya":
        model_name = st.text_input(
            "Nama / Tipe Model",
            placeholder="Contoh: Female casual model"
        )

        model_description = st.text_area(
            "Deskripsi Model",
            placeholder="Contoh: wanita usia 25 tahun, outfit kasual, ekspresi natural, sedang memegang dus paket...",
            height=90
        )

        model_file = st.file_uploader(
            "Upload Foto Model (Opsional)",
            type=["jpg", "jpeg", "png"],
            key="activity_model_file"
        )

        if model_file:
            st.image(model_file, caption="Preview Model", use_container_width=True)

    if st.button("🔥 GENERATE OUTPUT", use_container_width=True):
        if not activity.strip():
            st.warning("Isi bagian AKTIVITAS dulu.")
        elif not location.strip():
            st.warning("Isi bagian LOKASI / LINGKUNGAN dulu.")
        else:
            st.session_state["activity_scene_pack"] = build_activity_scene_pack(
                activity=activity,
                location=location,
                time_of_day=time_of_day,
                camera_angle=camera_angle,
                output_type=output_type,
                use_model=use_model,
                model_name=model_name,
                model_description=model_description,
                model_file=model_file
            )
            st.success("Output berhasil dibuat.")

    st.markdown("</div>", unsafe_allow_html=True)

if "activity_scene_pack" in st.session_state:
    result = st.session_state["activity_scene_pack"]
    json_result = json.dumps(result, indent=4, ensure_ascii=False)
    selected_output = result["scene_input"]["output_type"]

    st.subheader("HASIL ACTIVITY SCENE BUILDER")

    if selected_output in ["Prompt Biasa", "Prompt + JSON"]:
        st.write("PROMPT FINAL")
        st.code(result["copy_pack"]["prompt_final"])

        st.write("COPY PROMPT")
        st.text_area(
            "Copy prompt di sini",
            result["copy_pack"]["prompt_final"],
            height=260
        )

    if selected_output in ["JSON", "Prompt + JSON"]:
        st.write("JSON FINAL")
        st.code(json_result, language="json")

        st.write("COPY JSON")
        st.text_area(
            "Tekan lama / CTRL+A lalu copy JSON",
            json_result,
            height=420
        )

    st.write("NEGATIVE PROMPT")
    st.code(result["copy_pack"]["negative_prompt"])