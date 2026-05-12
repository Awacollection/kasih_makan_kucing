from pathlib import Path
from auth import check_login

check_login()
import shutil

ROOT = Path(r"C:\Users\ronald\RAW_ENGINE_WEB")
PAGES = ROOT / "pages"
BACKUP = ROOT / "_backup_before_theme"

theme_code = r'''import streamlit as st

def apply_black_green_theme():
    st.markdown("""
    <style>
    /* ===== GLOBAL ===== */
    .stApp {
        background: #000000;
        color: #ffffff;
    }

    html, body, [class*="css"] {
        color: #ffffff;
        font-family: Arial, sans-serif;
    }

    /* ===== HEADER ===== */
    header[data-testid="stHeader"] {
        background: #000000;
        border-bottom: 1px solid #00ff99;
    }

    div[data-testid="stToolbar"] {
        background: #000000;
    }

    section[data-testid="stMain"] {
        background: #000000;
    }

    div[data-testid="stMainBlockContainer"] {
        background: #000000;
        color: #ffffff;
        padding-top: 1.2rem;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: #020406;
        border-right: 1px solid #00ff99;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* ===== TITLE / TEXT ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    p, label, span, div {
        color: #ffffff;
    }

    /* ===== INPUT ===== */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    div[data-baseweb="select"] > div,
    .stDateInput input,
    .stTimeInput input {
        background: #04101a !important;
        color: #ffffff !important;
        border: 1px solid #00ff99 !important;
        border-radius: 8px !important;
    }

    /* ===== FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        background: #04101a;
        border: 1px solid #00ff99;
        border-radius: 10px;
        padding: 10px;
    }

    /* ===== SELECTBOX ===== */
    div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    ul[role="listbox"] {
        background: #04101a !important;
        border: 1px solid #00ff99 !important;
    }

    ul[role="listbox"] li {
        background: #04101a !important;
        color: #ffffff !important;
    }

    ul[role="listbox"] li:hover {
        background: #0a1d2b !important;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        width: 100%;
        background: #2be67d !important;
        color: #ffffff !important;
        border: 1px solid #2be67d !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.6rem 1rem !important;
    }

    .stButton > button:hover {
        background: #20c96b !important;
        border-color: #20c96b !important;
        color: #ffffff !important;
    }

    /* ===== RADIO ===== */
    div[role="radiogroup"] label {
        background: #04101a;
        border: 1px solid #00ff99;
        border-radius: 8px;
        padding: 6px 10px;
        margin-right: 8px;
    }

    /* ===== CHECKBOX ===== */
    .stCheckbox label {
        color: #ffffff !important;
    }

    /* ===== EXPANDER ===== */
    details {
        background: #04101a !important;
        border: 1px solid #00ff99 !important;
        border-radius: 10px !important;
        padding: 4px 10px !important;
        margin-bottom: 10px !important;
    }

    details summary {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ===== TABS ===== */
    button[data-baseweb="tab"] {
        background: #04101a !important;
        color: #ffffff !important;
        border: 1px solid #00ff99 !important;
        border-radius: 8px 8px 0 0 !important;
    }

    button[aria-selected="true"] {
        background: #0a1d2b !important;
        color: #00ff99 !important;
    }

    /* ===== CODE BLOCK ===== */
    pre, code {
        background: #04101a !important;
        color: #ffffff !important;
        border: 1px solid #00ff99 !important;
        border-radius: 8px !important;
    }

    /* ===== TABLE ===== */
    table {
        background: #04101a !important;
        color: #ffffff !important;
        border-collapse: collapse !important;
    }

    table th, table td {
        border: 1px solid #00ff99 !important;
        color: #ffffff !important;
    }

    /* ===== HR ===== */
    hr {
        border-color: #00ff99 !important;
    }

    /* ===== CAPTION ===== */
    .stCaption {
        color: #8df5c0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
'''

def find_set_page_config_end(text: str, start_index: int) -> int:
    paren_start = text.find("(", start_index)
    if paren_start == -1:
        return -1

    depth = 0
    for i in range(paren_start, len(text)):
        char = text[i]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                line_end = text.find("\n", i)
                return len(text) if line_end == -1 else line_end + 1
    return -1

def patch_file(path: Path):
    text = path.read_text(encoding="utf-8")

    if "import streamlit as st" not in text:
        print(f"SKIP tidak ada streamlit: {path.name}")
        return

    # Backup
    BACKUP.mkdir(exist_ok=True)
    backup_path = BACKUP / path.name
    if not backup_path.exists():
        shutil.copy2(path, backup_path)

    changed = False

    # Tambah import theme
    if "from theme import apply_black_green_theme" not in text:
        text = text.replace(
            "import streamlit as st",
            "import streamlit as st\nfrom theme import apply_black_green_theme",
            1
        )
        changed = True

    # Tambah apply_black_green_theme setelah st.set_page_config
    if "apply_black_green_theme()" not in text:
        idx = text.find("st.set_page_config")
        if idx != -1:
            end_idx = find_set_page_config_end(text, idx)
            if end_idx != -1:
                text = text[:end_idx] + "\napply_black_green_theme()\n" + text[end_idx:]
                changed = True
            else:
                print(f"GAGAL cari akhir st.set_page_config: {path.name}")
        else:
            # Kalau tidak ada st.set_page_config, taruh setelah import theme
            marker = "from theme import apply_black_green_theme\n"
            pos = text.find(marker)
            if pos != -1:
                insert_pos = pos + len(marker)
                text = text[:insert_pos] + "\napply_black_green_theme()\n" + text[insert_pos:]
                changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"UPDATED: {path.name}")
    else:
        print(f"SUDAH ADA THEME: {path.name}")

def main():
    if not ROOT.exists():
        raise FileNotFoundError(f"Folder tidak ditemukan: {ROOT}")

    # Buat theme.py
    theme_path = ROOT / "theme.py"
    theme_path.write_text(theme_code, encoding="utf-8")
    print("CREATED/UPDATED: theme.py")

    # Patch app.py kalau ada
    app_py = ROOT / "app.py"
    if app_py.exists():
        patch_file(app_py)

    # Patch semua pages/*.py
    if PAGES.exists():
        for py_file in PAGES.glob("*.py"):
            if py_file.name == "theme.py":
                continue
            patch_file(py_file)

    print("\nSELESAI.")
    print("Backup file lama ada di folder: _backup_before_theme")
    print("Sekarang refresh Streamlit.")

if __name__ == "__main__":
    main()