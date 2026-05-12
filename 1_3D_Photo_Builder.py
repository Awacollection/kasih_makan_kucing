import os
import time
import requests
import streamlit as st
from auth import check_login

check_login()
from theme import apply_black_green_theme
from dotenv import load_dotenv
import replicate

load_dotenv()

st.set_page_config(
    page_title="CHARACTER PHOTO BUILDER",
    layout="wide"
)

apply_black_green_theme()

API_KEY = os.getenv("FREEPIK_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

CREATE_URL = "https://api.magnific.com/v1/ai/text-to-image/imagen4-ultra"


def check_task(task_id):
    status_url = f"https://api.magnific.com/v1/ai/text-to-image/imagen4-ultra/{task_id}"

    headers = {
        "Content-Type": "application/json",
        "x-magnific-api-key": API_KEY
    }

    for i in range(30):
        response = requests.get(status_url, headers=headers, timeout=60)

        if response.status_code not in [200, 201, 202]:
            st.error(response.text)
            return None

        data = response.json()
        status = data.get("data", {}).get("status")
        generated = data.get("data", {}).get("generated", [])

        if generated:
            return generated[0]

        st.info(f"Menunggu gambar... status: {status}")
        time.sleep(3)

    st.warning("Gambar belum selesai setelah menunggu.")
    return None


def generate_image(prompt, image_file=None):
    # Kalau ada upload gambar, pakai Replicate image-to-image
    if image_file:
        if not REPLICATE_API_TOKEN:
            st.error("REPLICATE_API_TOKEN belum ada di file .env")
            return None

        try:
            image_file.seek(0)

            output = replicate.run(
                "stability-ai/sdxl:c221b2b8ef527988fb59bf24a8b97c4561f1c671f73bd389f866bfb27c061316",
                input={
                    "prompt": prompt,
                    "image": image_file,
                    "prompt_strength": 0.65,
                    "num_outputs": 1
                }
            )

            if isinstance(output, list) and len(output) > 0:
                return output[0]

            return output

        except Exception as e:
            st.error(str(e))
            return None

    # Kalau tidak upload gambar, tetap pakai Freepik text-to-image
    if not API_KEY:
        st.error("FREEPIK_API_KEY belum ada di file .env")
        return None

    headers = {
        "Content-Type": "application/json",
        "x-magnific-api-key": API_KEY
    }

    payload = {
        "prompt": prompt,
        "aspect_ratio": "social_story_9_16",
        "enhance_prompt": True,
        "num_images": 1
    }

    response = requests.post(CREATE_URL, headers=headers, json=payload, timeout=60)

    if response.status_code not in [200, 201, 202]:
        st.error(response.text)
        return None

    data = response.json()
    generated = data.get("data", {}).get("generated", [])

    if generated:
        return generated[0]

    task_id = data.get("data", {}).get("task_id")

    if task_id:
        st.info(f"Task dibuat: {task_id}")
        return check_task(task_id)

    st.warning("API belum mengirim gambar.")
    st.json(data)
    return None


st.title("CHARACTER PHOTO BUILDER (SIMPLE PRO)")

st.markdown("### 🧩 Product / Concept")
product_name = st.text_input(
    "Nama Produk / Ide",
    placeholder="Contoh: Gamis wanita putih"
)

st.markdown("### 🎯 Style Preset")
preset = st.selectbox("Pilih Style", [
    "Shopee Seller",
    "TikTok UGC",
    "Brand Catalog",
    "Instagram Lifestyle"
])

st.markdown("### 👤 Character")

gender = st.selectbox("Gender", ["Female", "Male"], key="gender_select")

st.markdown("### 🖼 Upload Reference (Opsional)")

uploaded_image = st.file_uploader(
    "Upload gambar model / referensi",
    type=["jpg", "png", "jpeg"]
)
if uploaded_image:
    st.image(uploaded_image, caption="Preview Image", width=260)

    st.caption(f"Nama file: {uploaded_image.name}")
    st.caption(f"Tipe file: {uploaded_image.type}")

st.markdown("### 🚀 Generate")

if st.button("🔥 Generate Prompt + Image"):

    st.write("Test Replicate:", REPLICATE_API_TOKEN)

    if preset == "Shopee Seller":
        style_prompt = (
            "marketplace seller photo, simple background, product clearly visible, "
            "natural lighting, slightly imperfect composition, real ecommerce photo"
        )
    elif preset == "TikTok UGC":
        style_prompt = (
            "tiktok shop content style, vertical framing, dynamic pose, "
            "engaging lifestyle content, realistic social media look"
        )
    elif preset == "Brand Catalog":
        style_prompt = (
            "clean studio photography, minimal background, sharp focus, "
            "premium catalog look, professional lighting"
        )
    else:
        style_prompt = (
            "instagram lifestyle photo, aesthetic composition, natural lighting, "
            "casual modern fashion look"
        )
    product_lower = product_name.lower()

    if "anak" in product_lower or "kids" in product_lower or "child" in product_lower:
        product_display = (
            f"{product_name}, displayed for ecommerce product reference, "
            "not worn by a child, presented safely by an adult model or as a product display"
        )
    else:
        product_display = product_name
    prompt = f"""
A realistic full body photo of an Indonesian {gender.lower()} aged 25-30, showing the outfit clearly.

Focus on the clothing product: {product_display}, fully visible from head to toe.

The model is standing casually like a real seller, slightly imperfect pose, relaxed body language.

Framing: full body, slightly off-center, like a real marketplace photo.

Lighting: natural daylight from window, slightly uneven, not studio lighting.

Camera: smartphone camera, slight blur, slight noise, handheld feel, real imperfections.

Background: simple real home environment (room, wall, curtain, floor), not studio, slightly messy but clean.

Photo style: real marketplace seller photo, not professional, not studio, natural casual look.

The image must look like a real seller photo taken casually, not a professional photoshoot, not aesthetic, not overly clean, not AI generated, no beauty filter.
"""

    st.code(prompt)
    st.success("✅ Prompt siap digunakan")

    with st.spinner("Generating image..."):
        if uploaded_image:
            image_url = generate_image(prompt, uploaded_image)
        else:
            image_url = generate_image(prompt)

    if image_url:
        st.image(image_url, caption="Generated Image", use_container_width=True)