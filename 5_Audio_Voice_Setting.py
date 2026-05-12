import streamlit as st
from auth import check_login

check_login()
from theme import apply_black_green_theme

st.set_page_config(
    page_title="Pengaturan Suara & Dialog",
    layout="wide"
)

apply_black_green_theme()

st.title("🎙️ Pengaturan Suara & Dialog")

st.info(
    "Halaman ini masih mentahan. "
    "Pengaturan di sini baru disimpan sementara di session_state dan ditampilkan di halaman Referensi Ide Konten. "
    "Belum dipakai langsung untuk membuat prompt."
)

st.markdown("---")

# ===== DEFAULT VALUE =====
if "audio_mode" not in st.session_state:
    st.session_state.audio_mode = "Flow langsung dengan suara"

if "mother_voice_profile" not in st.session_state:
    st.session_state.mother_voice_profile = "Ibu Model 01"

if "child_voice_profile" not in st.session_state:
    st.session_state.child_voice_profile = "Anak Model 01"

if "dialogue_style_mode" not in st.session_state:
    st.session_state.dialogue_style_mode = "Natural Ibu & Anak"

if "speaker_lock" not in st.session_state:
    st.session_state.speaker_lock = True

if "lip_sync_lock" not in st.session_state:
    st.session_state.lip_sync_lock = True

if "gesture_ownership_lock" not in st.session_state:
    st.session_state.gesture_ownership_lock = True

if "selfie_motion_level" not in st.session_state:
    st.session_state.selfie_motion_level = "Sedikit Goyang Realistis"

if "dialogue_timeline" not in st.session_state:
    st.session_state.dialogue_timeline = ""

if "mother_voice_description" not in st.session_state:
    st.session_state.mother_voice_description = ""

if "child_voice_description" not in st.session_state:
    st.session_state.child_voice_description = ""


# ===== AUDIO MODE =====
st.markdown("## 1. Audio Mode")

audio_mode_options = [
    "Flow langsung dengan suara",
    "Silent video only",
    "Silent video + voice profile",
    "Silent video + lip-sync"
]

audio_mode = st.selectbox(
    "Pilih Audio Mode",
    audio_mode_options,
    index=audio_mode_options.index(st.session_state.audio_mode)
)

st.caption(
    "Flow langsung dengan suara = cepat tapi risiko suara berubah. "
    "Silent video + voice profile / lip-sync = lebih stabil untuk suara konsisten."
)

st.markdown("---")


# ===== VOICE PROFILE =====
st.markdown("## 2. Voice Profile Karakter")

col1, col2 = st.columns(2, gap="large")

with col1:
    mother_voice_options = [
        "Ibu Model 01",
        "Ibu Model 02",
        "Custom Voice Ibu"
    ]

    mother_voice_profile = st.selectbox(
        "Voice Profile Ibu",
        mother_voice_options,
        index=mother_voice_options.index(st.session_state.mother_voice_profile)
    )

    mother_voice_description = st.text_area(
        "Deskripsi Suara Ibu",
        value=st.session_state.mother_voice_description,
        placeholder=(
            "Contoh:\n"
            "Suara ibu muda Indonesia usia 28-32 tahun, lembut, hangat, natural, "
            "tidak formal, bukan suara iklan, ekspresi bahagia natural."
        ),
        height=140
    )

with col2:
    child_voice_options = [
        "Anak Model 01",
        "Anak Model 02",
        "Custom Voice Anak"
    ]

    child_voice_profile = st.selectbox(
        "Voice Profile Anak",
        child_voice_options,
        index=child_voice_options.index(st.session_state.child_voice_profile)
    )

    child_voice_description = st.text_area(
        "Deskripsi Suara Anak",
        value=st.session_state.child_voice_description,
        placeholder=(
            "Contoh:\n"
            "Suara anak perempuan Indonesia usia 3-4 tahun, ceria, lucu, pendek-pendek, "
            "natural toddler voice, bukan suara dewasa, tidak terlalu jelas seperti dubbing."
        ),
        height=140
    )

st.markdown("---")


# ===== DIALOGUE TIMELINE =====
st.markdown("## 3. Dialogue Timeline / Urutan Dialog")

dialogue_style_options = [
    "Natural Ibu & Anak",
    "Ceria dan Lucu",
    "Soft Selling Natural",
    "Tanpa Dialog Panjang",
    "Custom Timeline"
]

dialogue_style_mode = st.selectbox(
    "Gaya Dialog",
    dialogue_style_options,
    index=dialogue_style_options.index(st.session_state.dialogue_style_mode)
)

dialogue_timeline = st.text_area(
    "Tulis urutan dialog dan aksi",
    value=st.session_state.dialogue_timeline,
    placeholder=(
        "Contoh:\n"
        "0-2s: Ibu memegang HP dengan tangan kanan, tangan kiri merangkul pundak anak.\n"
        "2-4s: Anak menunjuk baju dan berkata: 'Bajunya bagus, Bu. Aku suka!'\n"
        "4-6s: Ibu mendekatkan kepala ke anak dan berkata: 'Ade lucu ih, ade suka bajunya ya?'\n"
        "6-8s: Anak bergaya lucu dan berkata: 'Iya, aku suka, Bunda!'"
    ),
    height=220
)

st.markdown("---")


# ===== LOCK SETTINGS =====
st.markdown("## 4. Speaker, Lip-sync, dan Gesture Lock")

lock_col1, lock_col2, lock_col3 = st.columns(3, gap="large")

with lock_col1:
    speaker_lock = st.checkbox(
        "Kunci Speaker",
        value=st.session_state.speaker_lock
    )
    st.caption("Mencegah suara ibu keluar dari anak, atau suara anak keluar dari ibu.")

with lock_col2:
    lip_sync_lock = st.checkbox(
        "Kunci Lip-sync",
        value=st.session_state.lip_sync_lock
    )
    st.caption("Saat ibu bicara, hanya bibir ibu bergerak. Saat anak bicara, hanya bibir anak bergerak.")

with lock_col3:
    gesture_ownership_lock = st.checkbox(
        "Kunci Gesture Karakter",
        value=st.session_state.gesture_ownership_lock
    )
    st.caption("Mencegah ibu dan anak melakukan gesture yang sama secara bersamaan tanpa aturan.")

st.markdown("---")


# ===== SELFIE MOTION =====
st.markdown("## 5. Selfie Motion Realism")

selfie_motion_options = [
    "Halus Natural",
    "Sedikit Goyang Realistis",
    "UGC Goyang Natural"
]

selfie_motion_level = st.selectbox(
    "Level Goyangan Kamera Selfie",
    selfie_motion_options,
    index=selfie_motion_options.index(st.session_state.selfie_motion_level)
)

st.caption(
    "Catatan: HP mahal tetap punya sedikit gerakan tangan saat selfie. "
    "Jangan terlalu stabil seperti tripod atau gimbal."
)

st.markdown("---")


# ===== SAVE =====
if st.button("💾 Simpan Pengaturan Suara", use_container_width=True):
    st.session_state.audio_mode = audio_mode
    st.session_state.mother_voice_profile = mother_voice_profile
    st.session_state.child_voice_profile = child_voice_profile
    st.session_state.mother_voice_description = mother_voice_description
    st.session_state.child_voice_description = child_voice_description
    st.session_state.dialogue_style_mode = dialogue_style_mode
    st.session_state.dialogue_timeline = dialogue_timeline
    st.session_state.speaker_lock = speaker_lock
    st.session_state.lip_sync_lock = lip_sync_lock
    st.session_state.gesture_ownership_lock = gesture_ownership_lock
    st.session_state.selfie_motion_level = selfie_motion_level

    st.success("Pengaturan suara disimpan sementara di session_state.")


# ===== PREVIEW =====
st.markdown("## 6. Preview Pengaturan Aktif")

preview_data = {
    "audio_mode": audio_mode,
    "mother_voice_profile": mother_voice_profile,
    "mother_voice_description": mother_voice_description,
    "child_voice_profile": child_voice_profile,
    "child_voice_description": child_voice_description,
    "dialogue_style_mode": dialogue_style_mode,
    "dialogue_timeline": dialogue_timeline,
    "speaker_lock": speaker_lock,
    "lip_sync_lock": lip_sync_lock,
    "gesture_ownership_lock": gesture_ownership_lock,
    "selfie_motion_level": selfie_motion_level
}

st.json(preview_data)

st.warning(
    "Status: halaman ini sudah nyambung secara session_state, "
    "tetapi belum digunakan untuk mengubah prompt di halaman Referensi Ide Konten."
)