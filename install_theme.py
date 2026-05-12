from pathlib import Path
import shutil

ROOT = Path(r"C:\Users\ronald\RAW_ENGINE_WEB")
PAGES = ROOT / "pages"
BACKUP = ROOT / "_backup_before_theme"

theme_code = r'''import streamlit as st

def apply_black_green_theme():
    st.markdown("""
    <style>
    .stApp {
        background: #000000;
        color: #ffffff;
    }

    header[data-testid="stHeader"] {
        background: #000000;
        border-bottom: 1px solid #00ff99;
    }

    section[data-testid="stSidebar"] {
        background: #020406;
        border-right: 1px solid #00ff99;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    div[data-testid="stMainBlockContainer"] {
        background: #000000;
        color: #ffffff;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    p, label, span, div {
        color: #ffffff;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    div[data-baseweb="select"] > div {
        background: #04101a !important;
        color: #ffffff !important;
        border: 1px solid #00ff99 !important;
        border-radius: 8px !important;
    }

    [data-testid="stFileUploader"] {
        background: #04101a;
        border: 1px solid #00ff99;
        border-radius: 10px;
        padding: 10px;
    }

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

    .stButton > button {
        width: 100%;
        background: #2be67d !important;
        color: #ffffff !important;
        border: 1px solid #2be67d !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background: #20c96b !important;
        border-color: #20c96b !important;
    }

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

    pre, code {
        background: #04101a !important;
        color: #ffffff !important;
        border: 1px solid #00ff99 !important;
        border-radius: 8px !important;
    }

    hr {
        border-color: #00ff99 !important;
    }
    </style>
    """, unsafe_allow_html=True)
'''

def find_page_config_end(text, start_index):
    paren_start = text.find("(", start_index)
    if paren_start == -1:
        return -1

    depth = 0
    for i in range(paren_start, len(text)):
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
            if depth == 0:
                line_end = text.find("\n", i)
                return len(text) if line_end == -1 else line_end + 1
    return -1

def patch_file(path):
    text = path.read_text(encoding="utf-8")

    if "import streamlit as st" not in text:
        print(f"SKIP: {path.name}")
        return

    BACKUP.mkdir(exist_ok=True)
    backup_path = BACKUP / path.name
    if not backup_path.exists():
        shutil.copy2(path, backup_path)

    changed = False

    if "from theme import apply_black_green_theme" not in text:
        text = text.replace(
            "import streamlit as st",
            "import streamlit as st\nfrom theme import apply_black_green_theme",
            1
        )
        changed = True

    if "apply_black_green_theme()" not in text:
        idx = text.find("st.set_page_config")
        if idx != -1:
            end_idx = find_page_config_end(text, idx)
            if end_idx != -1:
                text = text[:end_idx] + "\napply_black_green_theme()\n" + text[end_idx:]
                changed = True
        else:
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
    theme_path = ROOT / "theme.py"
    theme_path.write_text(theme_code, encoding="utf-8")
    print("CREATED/UPDATED: theme.py")

    app_py = ROOT / "app.py"
    if app_py.exists():
        patch_file(app_py)

    if PAGES.exists():
        for py_file in PAGES.glob("*.py"):
            patch_file(py_file)

    print("")
    print("SELESAI.")
    print("Backup file lama ada di folder: _backup_before_theme")
    print("Sekarang refresh Streamlit.")

if __name__ == "__main__":
    main()