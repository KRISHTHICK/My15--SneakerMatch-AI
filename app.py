import streamlit as st
from PIL import Image
import os, json
from colorthief import ColorThief
from io import BytesIO
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="👟 SneakerMatch AI", layout="centered")
st.title("👟 SneakerMatch AI – Sneaker Finder from Outfit")

# Load sneaker data
with open("sneaker_data.json", "r") as f:
    sneakers = json.load(f)

def get_dominant_colors(image):
    img_bytes = BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    ct = ColorThief(img_bytes)
    palette = ct.get_palette(color_count=2)
    return palette

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def match_sneakers(palette_rgb):
    outfit_vec = np.array(palette_rgb).flatten().reshape(1, -1)
    best_score, best_match = -1, None

    for s in sneakers:
        sneaker_vec = np.array([hex_to_rgb(c) for c in s["colors"]]).flatten().reshape(1, -1)
        score = cosine_similarity(outfit_vec, sneaker_vec)[0][0]
        if score > best_score:
            best_score = score
            best_match = s
    return best_match

uploaded = st.file_uploader("📸 Upload your outfit image", type=["png", "jpg", "jpeg"])
if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Your Outfit", use_column_width=True)

    palette = get_dominant_colors(image)
    palette_hex = [rgb_to_hex(c) for c in palette]
    st.markdown("### 🎨 Detected Dominant Colors")
    st.markdown(", ".join(palette_hex))

    sneaker = match_sneakers(palette)
    st.markdown("### 👟 Best Match Found:")
    st.image(sneaker["image"], width=250)
    st.success(f"**{sneaker['name']}** by {sneaker['brand']}")
    st.info("✅ Matched based on color similarity to your outfit.")
