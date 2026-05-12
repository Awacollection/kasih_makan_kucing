import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Cerita Konten",
    layout="wide"
)

try:
    from theme import apply_black_green_theme
    apply_black_green_theme()
except Exception:
    pass

st.title("Cerita Konten")


# =====================================================
# SIMPLE PASSWORD LOGIN
# =====================================================

APP_PASSWORD = "ronald371011"

if "login_berhasil" not in st.session_state:
    st.session_state["login_berhasil"] = False

if not st.session_state["login_berhasil"]:
    st.subheader("Login")

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


# =====================================================
# DATABASE
# =====================================================
DATA_DIR = Path("database_cerita")
DATA_DIR.mkdir(exist_ok=True)
ASSET_DIR = DATA_DIR / "assets"
ASSET_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "data_cerita.json"
def default_data():
    return {
        "cerita": "",
        "karakter": [
            {
                "slot": i,
                "nama_ibu": "",
                "nama_anak": "",
                "foto_ibu": "",
                "foto_anak": "",
                "foto_ruangan": ""
            }
            for i in range(1, 6)
        ]
    }
def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = default_data()
    else:
        data = default_data()
    if "cerita" not in data:
        data["cerita"] = ""
    if "karakter" not in data or len(data["karakter"]) != 5:
        data["karakter"] = default_data()["karakter"]
    return data
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def save_image(uploaded_file, slot, jenis):
    folder = ASSET_DIR / f"karakter_{slot}"
    folder.mkdir(exist_ok=True)
    ext = Path(uploaded_file.name).suffix.lower()
    if ext not in [".png", ".jpg", ".jpeg"]:
        ext = ".png"
    path = folder / f"{jenis}{ext}"
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(path)
def delete_image(path_text):
    if path_text:
        try:
            Path(path_text).unlink(missing_ok=True)
        except:
            pass
data = load_data()
save_data(data)
# =====================================================
# TAB
# =====================================================
tab1, tab2 = st.tabs([
    "Karakter Dasar",
    "Cerita"
])
# =====================================================
# TAB 1 — KARAKTER DASAR
# =====================================================
