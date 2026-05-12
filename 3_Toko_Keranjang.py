import streamlit as st
from auth import check_login

check_login()
from theme import apply_black_green_theme
import urllib.parse
import json
import os
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="TOKO & KERANJANG", layout="wide")

apply_black_green_theme()

# ================= CONFIG =================
PRODUCT_FILE = "produk.json"
UPLOAD_DIR = "uploaded_products"
WHATSAPP_NUMBER = "628xxxxxxxxxx"  # GANTI dengan nomor WhatsApp kamu. Contoh: 6281234567890

os.makedirs(UPLOAD_DIR, exist_ok=True)

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

h1, h2, h3, h4, h5, h6,
p, span, div, label {
    color:#ffffff !important;
}

.card {
    background:#081018;
    border:2px solid #2ED573;
    border-radius:14px;
    padding:16px;
    min-height:250px;
    box-shadow:0 0 14px rgba(46,213,115,.25);
    margin-bottom:16px;
}

.card-title {
    color:#2ED573 !important;
    font-weight:900;
    margin-bottom:10px;
    border-bottom:1px solid #2ED573;
    padding-bottom:8px;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
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

textarea {
    background:#0d141c !important;
    color:#ffffff !important;
    border:2px solid #2ED573 !important;
}

/* SIDEBAR */
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

# ================= HELPERS =================
def rupiah(amount):
    return f"Rp{amount:,.0f}".replace(",", ".")


def load_products():
    if not os.path.exists(PRODUCT_FILE):
        return []

    try:
        with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_products(products):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4, ensure_ascii=False)


def save_uploaded_image(uploaded_file, product_id):
    if uploaded_file is None:
        return ""

    ext = uploaded_file.name.split(".")[-1].lower()
    filename = f"{product_id}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return filepath


def add_product(name, price, description, category, marketplace_link, uploaded_file):
    products = load_products()

    product_id = f"produk_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
    image_path = save_uploaded_image(uploaded_file, product_id)

    product = {
        "id": product_id,
        "name": name,
        "price": int(price),
        "description": description,
        "category": category,
        "marketplace_link": marketplace_link,
        "image_path": image_path,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    products.append(product)
    save_products(products)


def delete_product(product_id):
    products = load_products()
    remaining = []

    for p in products:
        if p["id"] == product_id:
            image_path = p.get("image_path", "")
            if image_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
        else:
            remaining.append(p)

    save_products(remaining)


if "cart" not in st.session_state:
    st.session_state["cart"] = []


def add_to_cart(product):
    for item in st.session_state["cart"]:
        if item["id"] == product["id"]:
            item["qty"] += 1
            return

    st.session_state["cart"].append({
        "id": product["id"],
        "name": product["name"],
        "price": product["price"],
        "qty": 1
    })


def remove_from_cart(product_id):
    st.session_state["cart"] = [
        item for item in st.session_state["cart"]
        if item["id"] != product_id
    ]


def clear_cart():
    st.session_state["cart"] = []


def cart_total():
    return sum(item["price"] * item["qty"] for item in st.session_state["cart"])


def build_whatsapp_link(customer_name, customer_note):
    lines = []
    lines.append("Halo, saya mau order:")
    lines.append("")

    for i, item in enumerate(st.session_state["cart"], start=1):
        subtotal = item["price"] * item["qty"]
        lines.append(f"{i}. {item['name']}")
        lines.append(f"   Qty: {item['qty']}")
        lines.append(f"   Harga: {rupiah(item['price'])}")
        lines.append(f"   Subtotal: {rupiah(subtotal)}")
        lines.append("")

    lines.append(f"TOTAL: {rupiah(cart_total())}")
    lines.append("")

    if customer_name.strip():
        lines.append(f"Nama: {customer_name}")

    if customer_note.strip():
        lines.append(f"Catatan: {customer_note}")

    message = "\n".join(lines)
    encoded = urllib.parse.quote(message)

    return f"https://wa.me/{WHATSAPP_NUMBER}?text={encoded}"


# ================= UI =================
st.title("TOKO & KERANJANG")
st.caption("Upload produk, simpan katalog, tambah ke keranjang, dan checkout via WhatsApp.")

tab1, tab2 = st.tabs(["🛒 Katalog & Keranjang", "➕ Tambah Produk"])

# ================= TAB 1 =================
with tab1:
    products = load_products()

    c1, c2 = st.columns([1.35, 1], gap="medium")

    with c1:
        st.subheader("Katalog Produk")

        if not products:
            st.info("Belum ada produk. Buka tab Tambah Produk untuk menambahkan produk.")
        else:
            for idx, product in enumerate(products):
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='card-title'>{product['name']}</div>", unsafe_allow_html=True)

                if product.get("image_path") and os.path.exists(product["image_path"]):
                    st.image(product["image_path"], use_container_width=True)

                st.write(f"Kategori: {product.get('category', '-')}")
                st.write(product.get("description", ""))
                st.write(f"**Harga: {rupiah(product['price'])}**")

                col_a, col_b, col_c = st.columns([1, 1, 1])

                with col_a:
                    if st.button("Tambah", key=f"add_{product['id']}_{idx}", use_container_width=True):
                        add_to_cart(product)
                        st.success("Masuk keranjang.")

                with col_b:
                    link = product.get("marketplace_link", "")
                    if link:
                        st.link_button("Marketplace", link, use_container_width=True)
                    else:
                        st.info("No link")

                with col_c:
                    if st.button("Hapus Produk", key=f"delete_{product['id']}_{idx}", use_container_width=True):
                        delete_product(product["id"])
                        st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.subheader("Keranjang")

        if not st.session_state["cart"]:
            st.info("Keranjang masih kosong.")
        else:
            for item in st.session_state["cart"]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='card-title'>{item['name']}</div>", unsafe_allow_html=True)

                st.write(f"Qty: {item['qty']}")
                st.write(f"Harga: {rupiah(item['price'])}")
                st.write(f"Subtotal: {rupiah(item['price'] * item['qty'])}")

                if st.button("Hapus", key=f"remove_{item['id']}", use_container_width=True):
                    remove_from_cart(item["id"])
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("### Total")
            st.subheader(rupiah(cart_total()))

            customer_name = st.text_input("Nama Pembeli", placeholder="Contoh: Ronald")
            customer_note = st.text_area("Catatan Order", placeholder="Contoh: Saya mau order produk ini...", height=90)

            if WHATSAPP_NUMBER == "628xxxxxxxxxx":
                st.warning("Nomor WhatsApp belum diganti di kode.")
            else:
                whatsapp_link = build_whatsapp_link(customer_name, customer_note)
                st.link_button("Checkout via WhatsApp", whatsapp_link, use_container_width=True)

            if st.button("Kosongkan Keranjang", use_container_width=True):
                clear_cart()
                st.rerun()

# ================= TAB 2 =================
with tab2:
    st.subheader("Tambah Produk Baru")

    c1, c2 = st.columns([1, 1], gap="medium")

    with c1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>DATA PRODUK</div>", unsafe_allow_html=True)

        new_name = st.text_input("Nama Produk")
        new_price = st.number_input("Harga", min_value=0, step=1000)
        new_category = st.text_input("Kategori", placeholder="Contoh: Digital Tools / Fashion / Jasa")
        new_desc = st.text_area("Deskripsi Produk", height=120)
        new_link = st.text_input("Link Marketplace / Link Produk", placeholder="https://...")

        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='card-title'>FOTO PRODUK</div>", unsafe_allow_html=True)

        new_image = st.file_uploader("Upload Foto Produk", type=["jpg", "jpeg", "png"], key="new_product_image")

        if new_image:
            st.image(new_image, caption="Preview Foto Produk", use_container_width=True)

        if st.button("Simpan Produk", use_container_width=True):
            if not new_name.strip():
                st.warning("Nama produk wajib diisi.")
            elif new_price <= 0:
                st.warning("Harga harus lebih dari 0.")
            else:
                add_product(
                    name=new_name,
                    price=new_price,
                    description=new_desc,
                    category=new_category,
                    marketplace_link=new_link,
                    uploaded_file=new_image
                )
                st.success("Produk berhasil disimpan.")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Produk tersimpan di produk.json dan gambar tersimpan di folder uploaded_products.")