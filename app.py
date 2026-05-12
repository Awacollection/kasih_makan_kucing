import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Cerita Konten",
    layout="wide"
)

from auth import check_login
check_login()

st.title("Cerita Konten")

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
        except Exception:
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
        except Exception:
            pass


data = load_data()
save_data(data)

tab1, tab2 = st.tabs([
    "Karakter Dasar",
    "Cerita"
])

with tab1:
    st.subheader("Database Karakter Dasar")

    for index in range(5):
        karakter = data["karakter"][index]
        slot = karakter["slot"]

        with st.expander(f"Karakter {slot}", expanded=(slot == 1)):
            col_name1, col_name2 = st.columns(2)

            with col_name1:
                nama_ibu = st.text_input(
                    f"Nama Ibu Karakter {slot}",
                    value=karakter.get("nama_ibu", ""),
                    key=f"nama_ibu_{slot}"
                )

            with col_name2:
                nama_anak = st.text_input(
                    f"Nama Anak Karakter {slot}",
                    value=karakter.get("nama_anak", ""),
                    key=f"nama_anak_{slot}"
                )

            data["karakter"][index]["nama_ibu"] = nama_ibu
            data["karakter"][index]["nama_anak"] = nama_anak
            save_data(data)

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### Foto Ibu")

                ibu_file = st.file_uploader(
                    f"Upload foto ibu {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"ibu_upload_{slot}"
                )

                if ibu_file is not None:
                    delete_image(data["karakter"][index].get("foto_ibu", ""))
                    path = save_image(ibu_file, slot, "foto_ibu")
                    data["karakter"][index]["foto_ibu"] = path
                    save_data(data)
                    st.rerun()

                if data["karakter"][index].get("foto_ibu"):
                    st.image(data["karakter"][index]["foto_ibu"], use_container_width=True)

                    if st.button(f"Hapus Foto Ibu {slot}", key=f"hapus_ibu_{slot}"):
                        delete_image(data["karakter"][index]["foto_ibu"])
                        data["karakter"][index]["foto_ibu"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto ibu.")

            with col2:
                st.markdown("### Foto Anak")

                anak_file = st.file_uploader(
                    f"Upload foto anak {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"anak_upload_{slot}"
                )

                if anak_file is not None:
                    delete_image(data["karakter"][index].get("foto_anak", ""))
                    path = save_image(anak_file, slot, "foto_anak")
                    data["karakter"][index]["foto_anak"] = path
                    save_data(data)
                    st.rerun()

                if data["karakter"][index].get("foto_anak"):
                    st.image(data["karakter"][index]["foto_anak"], use_container_width=True)

                    if st.button(f"Hapus Foto Anak {slot}", key=f"hapus_anak_{slot}"):
                        delete_image(data["karakter"][index]["foto_anak"])
                        data["karakter"][index]["foto_anak"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto anak.")

            with col3:
                st.markdown("### Foto Dekorasi Ruangan")

                ruang_file = st.file_uploader(
                    f"Upload foto ruangan {slot}",
                    type=["png", "jpg", "jpeg"],
                    key=f"ruang_upload_{slot}"
                )

                if ruang_file is not None:
                    delete_image(data["karakter"][index].get("foto_ruangan", ""))
                    path = save_image(ruang_file, slot, "foto_ruangan")
                    data["karakter"][index]["foto_ruangan"] = path
                    save_data(data)
                    st.rerun()

                if data["karakter"][index].get("foto_ruangan"):
                    st.image(data["karakter"][index]["foto_ruangan"], use_container_width=True)

                    if st.button(f"Hapus Foto Ruangan {slot}", key=f"hapus_ruangan_{slot}"):
                        delete_image(data["karakter"][index]["foto_ruangan"])
                        data["karakter"][index]["foto_ruangan"] = ""
                        save_data(data)
                        st.rerun()
                else:
                    st.info("Belum ada foto ruangan.")

    st.success("Database karakter tersimpan otomatis.")


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
