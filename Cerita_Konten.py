import streamlit as st
import json
import re
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


st.title("Cerita Konten")


# =====================================================
# DATABASE
# =====================================================

DATA_DIR = Path("database_cerita")
DATA_DIR.mkdir(exist_ok=True)

ASSET_DIR = DATA_DIR / "assets"
ASSET_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "data_cerita.json"


def default_karakter(slot):
    return {
        "slot": slot,
        "nama_ibu": "",
        "nama_anak": "",
        "foto_ibu": "",
        "foto_anak": "",
        "foto_ruangan": "",

        "detail_ibu": "",
        "detail_anak": "",
        "detail_pakaian_ibu": "",
        "detail_pakaian_anak": "",
        "detail_aksesoris_ibu": "",
        "detail_aksesoris_anak": "",
        "detail_ruangan_lock": "",
        "catatan_larangan": ""
    }


def default_data():
    return {
        "cerita": "",
        "karakter": [
            default_karakter(i)
            for i in range(1, 6)
        ]
    }


def ensure_schema(data):
    if not isinstance(data, dict):
        data = default_data()

    if "cerita" not in data:
        data["cerita"] = ""

    if "karakter" not in data or not isinstance(data["karakter"], list):
        data["karakter"] = default_data()["karakter"]

    if len(data["karakter"]) != 5:
        data["karakter"] = default_data()["karakter"]

    for i in range(5):
        slot = i + 1
        template = default_karakter(slot)

        if not isinstance(data["karakter"][i], dict):
            data["karakter"][i] = template

        for key, value in template.items():
            if key not in data["karakter"][i]:
                data["karakter"][i][key] = value

        data["karakter"][i]["slot"] = slot

    return data


def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = default_data()
    else:
        data = default_data()

    return ensure_schema(data)


def save_data(data):
    data = ensure_schema(data)
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


# =====================================================
# GENERATE SCENE
# =====================================================

def bersihkan_teks(teks):
    teks = teks or ""
    teks = teks.replace("\r", "\n")
    teks = re.sub(r"\n+", "\n", teks)
    teks = re.sub(r"[ \t]+", " ", teks)
    return teks.strip()


def pecah_kalimat(teks):
    teks = bersihkan_teks(teks)

    if not teks:
        return []

    paragraf = [p.strip() for p in teks.split("\n") if p.strip()]

    kalimat = []
    for p in paragraf:
        bagian = re.split(r"(?<=[.!?])\s+", p)
        bagian = [b.strip() for b in bagian if b.strip()]
        kalimat.extend(bagian)

    if not kalimat:
        kalimat = paragraf

    return kalimat


def bagi_cerita_ke_scene(cerita, jumlah_scene):
    kalimat = pecah_kalimat(cerita)

    if not kalimat:
        return [""] * jumlah_scene

    hasil = []
    total = len(kalimat)

    for i in range(jumlah_scene):
        start = round(i * total / jumlah_scene)
        end = round((i + 1) * total / jumlah_scene)

        potongan = kalimat[start:end]

        if not potongan:
            potongan = [kalimat[min(i, total - 1)]]

        hasil.append(" ".join(potongan).strip())

    return hasil


def ada_kata(teks, daftar_kata):
    teks = teks.lower()
    return any(kata in teks for kata in daftar_kata)


def analisa_scene(teks_scene, nomor_scene, jumlah_scene):
    teks = teks_scene.lower()

    emosi = "emosional, natural, dan sesuai alur cerita"
    visual = "foto medium shot ibu dan anak di ruangan yang sama, dengan ekspresi natural sesuai kejadian scene"
    posisi_ibu = "ibu berada di area utama ruangan, pose natural sesuai alur scene"
    posisi_anak = "anak berada dekat ibu atau di posisi yang sesuai dengan cerita"
    kondisi_ruangan = "ruangan tetap sama seperti foto referensi, tata letak dan dekorasi tidak berubah"
    rekomendasi_foto = "Foto utama ibu dan anak di ruangan yang sama, memperlihatkan kejadian penting pada scene ini."

    if nomor_scene == 1:
        emosi = "awal cerita, natural, memperkenalkan suasana"
        visual = "foto pembuka yang memperlihatkan ibu, anak, dan ruangan secara jelas agar penonton mengenal karakter dan lokasi"
        rekomendasi_foto = "Foto pembuka: ibu, anak, dan dekorasi ruangan terlihat jelas dalam satu frame."

    if nomor_scene == jumlah_scene:
        emosi = "penutup cerita, haru, lega, atau sedih sesuai akhir cerpen"
        visual = "foto penutup yang kuat secara emosi, fokus pada ekspresi ibu dan hubungan dengan anak"
        rekomendasi_foto = "Foto penutup emosional: close-up atau medium shot ibu dan anak dengan ekspresi yang menyimpulkan akhir cerita."

    if ada_kata(teks, ["lelah", "capek", "letih", "lesu", "mengantuk"]):
        emosi = "lelah, tertahan, dan penuh beban"
        visual = "foto ibu dengan ekspresi lelah namun tetap natural, berada di ruangan yang sama"
        posisi_ibu = "ibu duduk atau berdiri dengan postur tubuh sedikit menurun, terlihat lelah"
        rekomendasi_foto = "Foto close-up atau medium shot wajah ibu yang terlihat lelah secara natural."

    if ada_kata(teks, ["menangis", "air mata", "nangis", "sedih", "sakit hati"]):
        emosi = "sedih, terluka, dan tertahan"
        visual = "foto ibu dengan ekspresi sedih alami, mata berkaca-kaca, tanpa terlihat berlebihan"
        posisi_ibu = "ibu duduk diam atau menunduk dengan ekspresi sedih"
        rekomendasi_foto = "Foto close-up wajah ibu yang sedih, natural, dan tidak berlebihan."

    if ada_kata(teks, ["tidur", "tertidur", "kasur", "selimut", "malam"]):
        emosi = "hening, lembut, dan penuh kasih"
        visual = "foto ibu memperhatikan anak yang sedang tidur di ruangan yang sama"
        posisi_ibu = "ibu berada dekat anak, bisa duduk di samping kasur atau menatap anak"
        posisi_anak = "anak terlihat sedang tidur atau beristirahat dengan pose natural"
        rekomendasi_foto = "Foto ibu menatap anak yang sedang tidur, suasana malam tenang dan emosional."

    if ada_kata(teks, ["memeluk", "peluk", "digendong", "menggendong"]):
        emosi = "hangat, dekat, dan penuh kasih sayang"
        visual = "foto ibu memeluk atau menggendong anak secara natural"
        posisi_ibu = "ibu dekat dengan anak, tubuh mengarah ke anak"
        posisi_anak = "anak berada dalam pelukan ibu atau sangat dekat dengan ibu"
        rekomendasi_foto = "Foto ibu memeluk anak dengan ekspresi hangat dan natural."

    if ada_kata(teks, ["tersenyum", "senyum", "bahagia", "lega", "tertawa"]):
        emosi = "lega, hangat, dan bahagia sederhana"
        visual = "foto ibu dengan senyum natural, tidak berlebihan, tetap sesuai suasana cerita"
        posisi_ibu = "ibu menghadap anak atau kamera dengan ekspresi lega"
        rekomendasi_foto = "Foto ibu tersenyum lembut bersama anak di ruangan yang sama."

    if ada_kata(teks, ["marah", "kesal", "kecewa", "diam"]):
        emosi = "tegang, kecewa, dan tertahan"
        visual = "foto ibu dengan ekspresi kecewa atau diam menahan emosi"
        posisi_ibu = "ibu berdiri atau duduk dengan gestur tubuh tertahan"
        rekomendasi_foto = "Foto ibu terdiam dengan ekspresi kecewa, tetap natural dan realistis."

    if ada_kata(teks, ["dapur", "masak", "memasak", "makan", "piring"]):
        visual = "foto ibu sedang melakukan aktivitas rumah tangga secara natural, tetapi ruangan dan dekorasi utama tetap konsisten"
        rekomendasi_foto = "Foto ibu melakukan aktivitas sederhana di rumah, tetap memakai karakter dan ruangan referensi."

    return {
        "emosi": emosi,
        "visual": visual,
        "posisi_ibu": posisi_ibu,
        "posisi_anak": posisi_anak,
        "kondisi_ruangan": kondisi_ruangan,
        "rekomendasi_foto": rekomendasi_foto
    }


def teks_kosong_ke_default(teks, default):
    teks = (teks or "").strip()
    return teks if teks else default


def buat_prompt_lock_global(karakter):
    nama_ibu = teks_kosong_ke_default(karakter.get("nama_ibu", ""), "ibu sesuai foto referensi")
    nama_anak = teks_kosong_ke_default(karakter.get("nama_anak", ""), "anak sesuai foto referensi")

    detail_ibu = teks_kosong_ke_default(
        karakter.get("detail_ibu", ""),
        "Pertahankan wajah, usia visual 23–30 tahun, warna kulit, bentuk tubuh, proporsi tubuh, gaya rambut, dan ciri khas wajah ibu sesuai foto referensi."
    )

    detail_anak = teks_kosong_ke_default(
        karakter.get("detail_anak", ""),
        "Pertahankan wajah, usia visual anak, warna kulit, bentuk tubuh, proporsi tubuh, gaya rambut, dan ciri khas wajah anak sesuai foto referensi."
    )

    detail_pakaian_ibu = teks_kosong_ke_default(
        karakter.get("detail_pakaian_ibu", ""),
        "Pertahankan model pakaian ibu, warna pakaian, bentuk kerah, detail lengan, detail kancing, motif kain, tekstur kain, panjang pakaian, bawahan, sepatu atau sandal jika terlihat, dan semua detail kecil pakaian sesuai foto referensi."
    )

    detail_pakaian_anak = teks_kosong_ke_default(
        karakter.get("detail_pakaian_anak", ""),
        "Pertahankan model pakaian anak, warna pakaian, bentuk kerah, detail lengan, detail kancing, motif kain, tekstur kain, panjang pakaian, bawahan, sepatu atau sandal jika terlihat, dan semua detail kecil pakaian sesuai foto referensi."
    )

    detail_aksesoris_ibu = teks_kosong_ke_default(
        karakter.get("detail_aksesoris_ibu", ""),
        "Pertahankan semua aksesoris ibu sesuai foto referensi. Jangan menghilangkan, mengganti, atau menambahkan aksesoris baru."
    )

    detail_aksesoris_anak = teks_kosong_ke_default(
        karakter.get("detail_aksesoris_anak", ""),
        "Pertahankan semua aksesoris anak sesuai foto referensi. Jangan menghilangkan, mengganti, atau menambahkan aksesoris baru."
    )

    detail_ruangan = teks_kosong_ke_default(
        karakter.get("detail_ruangan_lock", ""),
        "Pertahankan ruangan sama seperti foto referensi. Kunci warna dinding, tekstur dinding, dekorasi tembok, posisi dekorasi tembok, meja, posisi meja, kursi, sofa, kasur, lemari, rak, lampu, jendela, tirai, karpet, cermin, hiasan ruangan, dan seluruh tata letak properti utama."
    )

    catatan_larangan = teks_kosong_ke_default(
        karakter.get("catatan_larangan", ""),
        "Jangan memindahkan meja. Jangan menghilangkan dekorasi tembok. Jangan mengubah posisi furnitur besar. Jangan mengganti ruangan menjadi lokasi lain. Jangan mengubah pakaian, aksesoris, wajah, gaya rambut, bentuk tubuh, warna kulit, atau identitas karakter."
    )

    return f"""
Gunakan foto referensi sebagai dasar utama.

LOCK KARAKTER IBU:
Karakter ibu bernama {nama_ibu}. {detail_ibu}
Wajah ibu harus tetap sama. Usia visual ibu harus tetap 23–30 tahun. Jangan membuat ibu terlihat seperti orang lain. Jangan membuat ibu terlihat lebih tua atau lebih muda dari karakter referensi.

LOCK KARAKTER ANAK:
Karakter anak bernama {nama_anak}. {detail_anak}
Wajah anak harus tetap sama. Usia visual anak harus tetap sesuai foto referensi. Jangan membuat anak terlihat seperti anak lain.

LOCK PAKAIAN IBU:
{detail_pakaian_ibu}
Jangan mengganti model pakaian ibu. Jangan mengganti warna pakaian ibu. Jangan mengubah bentuk kerah, lengan, kancing, motif, tekstur kain, atau detail kecil pakaian ibu.

LOCK PAKAIAN ANAK:
{detail_pakaian_anak}
Jangan mengganti model pakaian anak. Jangan mengganti warna pakaian anak. Jangan mengubah bentuk kerah, lengan, kancing, motif, tekstur kain, atau detail kecil pakaian anak.

LOCK AKSESORIS IBU:
{detail_aksesoris_ibu}
Jumlah, bentuk, warna, jenis, dan posisi aksesoris ibu harus tetap sama.

LOCK AKSESORIS ANAK:
{detail_aksesoris_anak}
Jumlah, bentuk, warna, jenis, dan posisi aksesoris anak harus tetap sama.

LOCK RUANGAN RINCI:
{detail_ruangan}
Ruangan harus tetap sama. Jangan mengganti interior. Jangan membuat ruangan terlihat seperti rumah lain. Jangan menghilangkan dekorasi tembok. Jangan memindahkan meja. Jangan mengubah posisi furnitur utama.

GAYA FOTO NATURAL:
Buat hasil seperti foto nyata dari kamera, bukan seperti gambar AI. Gunakan gaya fotografi realistis, natural, dan manusiawi. Ekspresi harus alami, pose harus wajar, tekstur kulit realistis, tekstur kain terlihat nyata, dan ruangan terlihat benar-benar nyata. Hindari hasil yang terlihat seperti AI, CGI, anime, kartun, ilustrasi, boneka, plastik, render 3D, atau terlalu halus.

YANG BOLEH BERUBAH:
Hanya ekspresi wajah, pose tubuh, arah pandang, aktivitas, sudut kamera, jarak kamera, fokus kamera, pencahayaan, dan suasana emosional sesuai kebutuhan scene.

YANG TIDAK BOLEH BERUBAH:
Identitas tokoh, wajah, usia visual, warna kulit, bentuk tubuh, proporsi tubuh, gaya rambut, pakaian, detail pakaian, aksesoris, detail aksesoris, dekorasi tembok, posisi meja, posisi furnitur utama, dan tata letak ruangan.

LARANGAN KHUSUS:
{catatan_larangan}
""".strip()


def buat_prompt_scene(nomor_scene, durasi_per_scene, teks_scene, analisa, karakter):
    nama_ibu = teks_kosong_ke_default(karakter.get("nama_ibu", ""), "ibu")
    nama_anak = teks_kosong_ke_default(karakter.get("nama_anak", ""), "anak")

    prompt_scene = f"""
Buat foto realistis dan natural untuk scene {nomor_scene} dari video cerpen.

Bagian cerita scene ini:
{teks_scene}

Arahan visual:
{analisa["visual"]}

Emosi utama:
{analisa["emosi"]}

Posisi karakter:
- {nama_ibu}: {analisa["posisi_ibu"]}
- {nama_anak}: {analisa["posisi_anak"]}

Kondisi ruangan:
{analisa["kondisi_ruangan"]}

Durasi scene dalam video: {durasi_per_scene} detik.
Komposisi foto harus mendukung alur cerita, mudah dipahami penonton, dan terasa seperti foto kehidupan nyata.
Gunakan bahasa visual yang natural seperti arahan pemotretan, bukan tampilan buatan AI.
""".strip()

    prompt_lock = buat_prompt_lock_global(karakter)

    return f"{prompt_scene}\n\n{prompt_lock}"


def buat_output_scene(cerita, jumlah_scene, karakter):
    durasi_per_scene = 5
    total_durasi = jumlah_scene * durasi_per_scene
    potongan_scene = bagi_cerita_ke_scene(cerita, jumlah_scene)

    hasil_scene = []

    for index, teks_scene in enumerate(potongan_scene):
        nomor_scene = index + 1
        analisa = analisa_scene(teks_scene, nomor_scene, jumlah_scene)

        prompt_foto = buat_prompt_scene(
            nomor_scene=nomor_scene,
            durasi_per_scene=durasi_per_scene,
            teks_scene=teks_scene,
            analisa=analisa,
            karakter=karakter
        )

        hasil_scene.append({
            "nomor": nomor_scene,
            "durasi": durasi_per_scene,
            "total_durasi": total_durasi,
            "bagian_cerita": teks_scene,
            "emosi": analisa["emosi"],
            "visual": analisa["visual"],
            "posisi_ibu": analisa["posisi_ibu"],
            "posisi_anak": analisa["posisi_anak"],
            "kondisi_ruangan": analisa["kondisi_ruangan"],
            "rekomendasi_foto": analisa["rekomendasi_foto"],
            "prompt_foto": prompt_foto
        })

    return hasil_scene


def gabungkan_semua_scene(hasil_scene):
    blok = []

    for scene in hasil_scene:
        teks = f"""
SCENE {scene["nomor"]}
Durasi: {scene["durasi"]} detik

Bagian cerita:
{scene["bagian_cerita"]}

Emosi:
{scene["emosi"]}

Visual utama:
{scene["visual"]}

Posisi karakter:
- Ibu: {scene["posisi_ibu"]}
- Anak: {scene["posisi_anak"]}

Kondisi ruangan:
{scene["kondisi_ruangan"]}

Rekomendasi foto:
1. {scene["rekomendasi_foto"]}

Prompt foto:
{scene["prompt_foto"]}
""".strip()

        blok.append(teks)

    return ("\n\n" + "=" * 80 + "\n\n").join(blok)


# =====================================================
# LOAD DATA
# =====================================================

data = load_data()
save_data(data)


# =====================================================
# TAB UTAMA
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "Karakter Dasar",
    "Cerita",
    "Generate Scene"
])


# =====================================================
# TAB 1 - KARAKTER DASAR
# =====================================================

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
                    st.success("Foto ibu berhasil diupload.")

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
                    st.success("Foto anak berhasil diupload.")

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
                st.success("Foto ruangan berhasil diupload.")

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


# =====================================================
# TAB 2 - CERITA
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
        placeholder="Tulis cerpen / ide cerita di sini...",
        key="cerita_utama"
    )

    if cerita != data.get("cerita", ""):
        data["cerita"] = cerita
        save_data(data)

    st.success("Cerita tersimpan otomatis.")


# =====================================================
# TAB 3 - GENERATE SCENE
# =====================================================

with tab3:
    st.subheader("Generate Scene Cerpen")

    st.info(
        "Tab ini membuat 5–6 scene dari cerpen, rekomendasi foto per scene, "
        "dan prompt foto dengan lock karakter, pakaian, aksesoris, serta ruangan."
    )

    col_setting1, col_setting2 = st.columns(2)

    with col_setting1:
        slot_pilihan = st.selectbox(
            "Pilih karakter",
            options=[1, 2, 3, 4, 5],
            index=0,
            key="slot_generate_scene"
        )

    with col_setting2:
        durasi_video = st.radio(
            "Durasi video",
            options=[25, 30],
            index=0,
            horizontal=True,
            format_func=lambda x: f"{x} detik",
            key="durasi_generate_scene"
        )

    jumlah_scene = 5 if durasi_video == 25 else 6
    index_karakter = slot_pilihan - 1
    karakter = data["karakter"][index_karakter]

    st.caption(
        f"Durasi {durasi_video} detik akan dibuat menjadi {jumlah_scene} scene. "
        "Setiap scene berdurasi 5 detik."
    )

    st.divider()

    st.markdown(f"### Preview Karakter {slot_pilihan}")

    col_preview1, col_preview2, col_preview3 = st.columns(3)

    with col_preview1:
        st.markdown("#### Foto Ibu")
        foto_ibu = karakter.get("foto_ibu", "")
        if foto_ibu and Path(foto_ibu).exists():
            st.image(foto_ibu, use_container_width=True)
        else:
            st.info("Foto ibu belum tersedia.")

    with col_preview2:
        st.markdown("#### Foto Anak")
        foto_anak = karakter.get("foto_anak", "")
        if foto_anak and Path(foto_anak).exists():
            st.image(foto_anak, use_container_width=True)
        else:
            st.info("Foto anak belum tersedia.")

    with col_preview3:
        st.markdown("#### Foto Ruangan")
        foto_ruangan = karakter.get("foto_ruangan", "")
        if foto_ruangan and Path(foto_ruangan).exists():
            st.image(foto_ruangan, use_container_width=True)
        else:
            st.info("Foto ruangan belum tersedia.")

    st.divider()

    st.markdown("### Detail Lock Karakter, Pakaian, Aksesoris, dan Ruangan")

    st.warning(
        "Isi bagian ini dengan rinci supaya prompt tidak mengubah wajah, pakaian, aksesoris, meja, dekorasi tembok, dan tata ruang."
    )

    col_lock1, col_lock2 = st.columns(2)

    with col_lock1:
        nama_ibu_lock = st.text_input(
            "Nama ibu",
            value=karakter.get("nama_ibu", ""),
            key=f"nama_ibu_lock_{slot_pilihan}"
        )

        detail_ibu = st.text_area(
            "Detail wajah / tubuh / rambut ibu yang harus dikunci",
            value=karakter.get("detail_ibu", ""),
            height=120,
            placeholder="Contoh: ibu usia visual 25 tahun, wajah oval, kulit sawo matang, rambut hitam sebahu, tubuh proporsional...",
            key=f"detail_ibu_lock_{slot_pilihan}"
        )

        detail_pakaian_ibu = st.text_area(
            "Detail pakaian ibu yang tidak boleh berubah",
            value=karakter.get("detail_pakaian_ibu", ""),
            height=130,
            placeholder="Contoh: blouse krem lengan panjang, kerah bulat, motif floral kecil, bahan katun, rok coklat...",
            key=f"detail_pakaian_ibu_lock_{slot_pilihan}"
        )

        detail_aksesoris_ibu = st.text_area(
            "Detail aksesoris ibu yang tidak boleh berubah",
            value=karakter.get("detail_aksesoris_ibu", ""),
            height=100,
            placeholder="Contoh: gelang tipis warna emas, cincin di tangan kanan, tidak memakai kalung...",
            key=f"detail_aksesoris_ibu_lock_{slot_pilihan}"
        )

    with col_lock2:
        nama_anak_lock = st.text_input(
            "Nama anak",
            value=karakter.get("nama_anak", ""),
            key=f"nama_anak_lock_{slot_pilihan}"
        )

        detail_anak = st.text_area(
            "Detail wajah / tubuh / rambut anak yang harus dikunci",
            value=karakter.get("detail_anak", ""),
            height=120,
            placeholder="Contoh: anak perempuan usia visual 4 tahun, wajah bulat, rambut hitam pendek, tubuh kecil natural...",
            key=f"detail_anak_lock_{slot_pilihan}"
        )

        detail_pakaian_anak = st.text_area(
            "Detail pakaian anak yang tidak boleh berubah",
            value=karakter.get("detail_pakaian_anak", ""),
            height=130,
            placeholder="Contoh: dress putih, lengan ruffle, kancing batok coklat dua lubang di dada depan...",
            key=f"detail_pakaian_anak_lock_{slot_pilihan}"
        )

        detail_aksesoris_anak = st.text_area(
            "Detail aksesoris anak yang tidak boleh berubah",
            value=karakter.get("detail_aksesoris_anak", ""),
            height=100,
            placeholder="Contoh: bando pink kecil, tidak memakai kalung, tidak memakai tas...",
            key=f"detail_aksesoris_anak_lock_{slot_pilihan}"
        )

    detail_ruangan_lock = st.text_area(
        "Detail ruangan yang harus dikunci secara rinci",
        value=karakter.get("detail_ruangan_lock", ""),
        height=160,
        placeholder=(
            "Contoh: ruang keluarga dengan dinding krem, meja kayu kecil di tengah depan sofa, "
            "2 dekorasi frame foto di tembok belakang sofa, lampu berdiri di sisi kanan, tirai putih di kiri, "
            "karpet abu-abu. Posisi meja, dekorasi tembok, sofa, lampu, dan tirai tidak boleh berubah."
        ),
        key=f"detail_ruangan_lock_{slot_pilihan}"
    )

    catatan_larangan = st.text_area(
        "Catatan larangan khusus",
        value=karakter.get("catatan_larangan", ""),
        height=120,
        placeholder=(
            "Contoh: jangan memindahkan meja, jangan menghilangkan dekorasi tembok, jangan mengganti warna dinding, "
            "jangan mengubah kancing pakaian anak, jangan menambah aksesoris baru."
        ),
        key=f"catatan_larangan_lock_{slot_pilihan}"
    )

    def simpan_detail_lock():
        data["karakter"][index_karakter]["nama_ibu"] = nama_ibu_lock
        data["karakter"][index_karakter]["nama_anak"] = nama_anak_lock
        data["karakter"][index_karakter]["detail_ibu"] = detail_ibu
        data["karakter"][index_karakter]["detail_anak"] = detail_anak
        data["karakter"][index_karakter]["detail_pakaian_ibu"] = detail_pakaian_ibu
        data["karakter"][index_karakter]["detail_pakaian_anak"] = detail_pakaian_anak
        data["karakter"][index_karakter]["detail_aksesoris_ibu"] = detail_aksesoris_ibu
        data["karakter"][index_karakter]["detail_aksesoris_anak"] = detail_aksesoris_anak
        data["karakter"][index_karakter]["detail_ruangan_lock"] = detail_ruangan_lock
        data["karakter"][index_karakter]["catatan_larangan"] = catatan_larangan
        save_data(data)

    if st.button("Simpan Detail Lock", type="secondary"):
        simpan_detail_lock()
        st.success("Detail lock berhasil disimpan.")

    st.divider()

    st.markdown("### Cerpen yang Akan Digenerate")

    cerita_generate = st.text_area(
        "Cerita",
        value=data.get("cerita", ""),
        height=250,
        placeholder="Cerpen dari tab Cerita akan muncul di sini. Bisa juga diedit langsung dari sini.",
        key="cerita_generate"
    )

    if cerita_generate != data.get("cerita", ""):
        data["cerita"] = cerita_generate
        save_data(data)

    col_generate1, col_generate2 = st.columns([1, 2])

    with col_generate1:
        tombol_generate = st.button(
            "Buat Scene Cerpen",
            type="primary",
            use_container_width=True
        )

    with col_generate2:
        st.info(
            f"Sistem akan membuat {jumlah_scene} scene untuk video {durasi_video} detik. "
            "Setiap scene otomatis memiliki rekomendasi foto dan prompt lock lengkap."
        )

    if tombol_generate:
        simpan_detail_lock()

        cerita_bersih = bersihkan_teks(cerita_generate)

        if not cerita_bersih:
            st.error("Cerita masih kosong. Isi cerpen terlebih dahulu.")
            st.stop()

        hasil_scene = buat_output_scene(
            cerita=cerita_bersih,
            jumlah_scene=jumlah_scene,
            karakter=data["karakter"][index_karakter]
        )

        st.session_state["hasil_scene_cerpen"] = hasil_scene
        st.session_state["hasil_scene_text"] = gabungkan_semua_scene(hasil_scene)

        st.success("Scene, rekomendasi foto, dan prompt foto berhasil dibuat.")

    if "hasil_scene_cerpen" in st.session_state:
        hasil_scene = st.session_state["hasil_scene_cerpen"]
        hasil_scene_text = st.session_state.get("hasil_scene_text", gabungkan_semua_scene(hasil_scene))

        st.divider()
        st.markdown("### Hasil Scene Cerpen")

        st.download_button(
            label="Download Semua Prompt TXT",
            data=hasil_scene_text,
            file_name="scene_cerpen_prompt_lock.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.text_area(
            "Copy semua hasil scene dari sini",
            value=hasil_scene_text,
            height=350
        )

        for scene in hasil_scene:
            with st.expander(f"SCENE {scene['nomor']} - Durasi {scene['durasi']} detik", expanded=(scene["nomor"] == 1)):
                st.markdown("#### Bagian Cerita")
                st.write(scene["bagian_cerita"])

                st.markdown("#### Emosi")
                st.write(scene["emosi"])

                st.markdown("#### Visual Utama")
                st.write(scene["visual"])

                st.markdown("#### Posisi Karakter")
                st.write(f"**Ibu:** {scene['posisi_ibu']}")
                st.write(f"**Anak:** {scene['posisi_anak']}")

                st.markdown("#### Kondisi Ruangan")
                st.write(scene["kondisi_ruangan"])

                st.markdown("#### Rekomendasi Foto")
                st.write(f"1. {scene['rekomendasi_foto']}")

                st.markdown("#### Prompt Foto")
                st.code(scene["prompt_foto"], language="text")
    else:
        st.info("Klik tombol 'Buat Scene Cerpen' untuk membuat scene dan prompt foto.")
