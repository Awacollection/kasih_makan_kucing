import streamlit as st
from theme import apply_black_green_theme
from auth import check_login
check_login()
import json
from pathlib import Path

st.set_page_config(page_title="Cerita Konten", layout="wide")

apply_black_green_theme()
st.title("Cerita Konten")

# =====================================================
# SIMPLE PASSWORD LOGIN
# =====================================================

APP_PASSWORD = "ronald371011"  # ganti nanti dengan password kamu sendiri

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

with tab1:
    st.subheader("Database Karakter Dasar")
    st.caption("Isi 5 karakter berbeda. Setiap karakter punya nama ibu, nama anak, foto ibu, foto anak, dan foto dekorasi ruangan.")

    for index in range(5):
        karakter = data["karakter"][index]
        slot = karakter["slot"]

        judul_expander = f"Karakter {slot}"
        if karakter.get("nama_ibu") or karakter.get("nama_anak"):
            judul_expander = f"Karakter {slot} — {karakter.get('nama_ibu', '')} & {karakter.get('nama_anak', '')}"

        with st.expander(judul_expander, expanded=(slot == 1)):

            col_name1, col_name2 = st.columns(2)

            with col_name1:
                nama_ibu = st.text_input(
                    f"Nama Ibu Karakter {slot}",
                    value=data["karakter"][index].get("nama_ibu", ""),
                    key=f"nama_ibu_{slot}"
                )

            with col_name2:
                nama_anak = st.text_input(
                    f"Nama Anak Karakter {slot}",
                    value=data["karakter"][index].get("nama_anak", ""),
                    key=f"nama_anak_{slot}"
                )

            if nama_ibu != data["karakter"][index].get("nama_ibu", ""):
                data["karakter"][index]["nama_ibu"] = nama_ibu
                save_data(data)

            if nama_anak != data["karakter"][index].get("nama_anak", ""):
                data["karakter"][index]["nama_anak"] = nama_anak
                save_data(data)

            st.divider()

            col1, col2, col3 = st.columns(3)

            # =================================================
            # FOTO IBU
            # =================================================

            with col1:
                st.markdown("### Foto Ibu")

                ibu_file = st.file_uploader(
                    f"Upload foto ibu {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"ibu_upload_{slot}"
                )

                if ibu_file is not None:
                    old_path = data["karakter"][index].get("foto_ibu", "")
                    delete_image(old_path)

                    path = save_image(ibu_file, slot, "foto_ibu")
                    data["karakter"][index]["foto_ibu"] = path
                    save_data(data)

                if data["karakter"][index].get("foto_ibu"):
                    st.image(
                        data["karakter"][index]["foto_ibu"],
                        use_container_width=True
                    )

                    if st.button(f"Hapus Foto Ibu {slot}", key=f"hapus_ibu_{slot}"):
                        delete_image(data["karakter"][index]["foto_ibu"])
                        data["karakter"][index]["foto_ibu"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto ibu.")

            # =================================================
            # FOTO ANAK
            # =================================================

            with col2:
                st.markdown("### Foto Anak")

                anak_file = st.file_uploader(
                    f"Upload foto anak {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"anak_upload_{slot}"
                )

                if anak_file is not None:
                    old_path = data["karakter"][index].get("foto_anak", "")
                    delete_image(old_path)

                    path = save_image(anak_file, slot, "foto_anak")
                    data["karakter"][index]["foto_anak"] = path
                    save_data(data)

                if data["karakter"][index].get("foto_anak"):
                    st.image(
                        data["karakter"][index]["foto_anak"],
                        use_container_width=True
                    )

                    if st.button(f"Hapus Foto Anak {slot}", key=f"hapus_anak_{slot}"):
                        delete_image(data["karakter"][index]["foto_anak"])
                        data["karakter"][index]["foto_anak"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto anak.")

            # =================================================
            # FOTO RUANGAN
            # =================================================

            with col3:
                st.markdown("### Foto Dekorasi Ruangan")

                ruang_file = st.file_uploader(
                    f"Upload foto ruangan {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"ruang_upload_{slot}"
                )

                if ruang_file is not None:
                    old_path = data["karakter"][index].get("foto_ruangan", "")
                    delete_image(old_path)

                    path = save_image(ruang_file, slot, "foto_ruangan")
                    data["karakter"][index]["foto_ruangan"] = path
                    save_data(data)

                if data["karakter"][index].get("foto_ruangan"):
                    st.image(
                        data["karakter"][index]["foto_ruangan"],
                        use_container_width=True
                    )

                    if st.button(f"Hapus Foto Ruangan {slot}", key=f"hapus_ruangan_{slot}"):
                        delete_image(data["karakter"][index]["foto_ruangan"])
                        data["karakter"][index]["foto_ruangan"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto ruangan.")

    st.success("Database karakter tersimpan otomatis.")

# =====================================================
# TAB 2 — CERITA
# =====================================================

with tab2:
    st.subheader("Kolom Cerita")

    if st.button("Hapus Cerita"):
        data["cerita"] = ""
        save_data(data)
        st.rerun()

    cerita = st.text_area(
        label="",
        value=data.get("cerita", ""),
        height=500,
        placeholder="Tulis cerpen / ide cerita di sini..."
    )

    if cerita != data.get("cerita", ""):
        data["cerita"] = cerita
        save_data(data)

    st.success("Cerita tersimpan otomatis.")
