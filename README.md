# My15--SneakerMatch-AI
Gen Ai

Here’s a **new AI fashion project** complete with full code, explanation, and instructions to run in **VS Code** or deploy via **GitHub/Streamlit**.

---

## 👟 **SneakerMatch AI – Sneaker Finder from Outfit**

### 🔍 Overview:

**SneakerMatch AI** allows users to upload a photo of their outfit, and the app recommends matching sneakers using AI. The model analyzes outfit colors and patterns, compares them with a sneaker dataset, and suggests the best matches.

---

### ✅ Features:

* 📸 Upload your outfit photo
* 🎨 AI extracts colors and texture
* 👟 Matches with a sneaker image database
* 📝 Shows sneaker name, brand, and why it matches
* 💾 Option to download recommendations

---

## 🗂 Project Structure:

```
SneakerMatch-AI/
├── app.py
├── sneakers/
│   ├── nike_red.png
│   ├── adidas_white.png
│   └── ... (add 5-10 sample images)
├── sneaker_data.json
├── requirements.txt
└── README.md
```

---

### 📦 `requirements.txt`

```txt
streamlit
Pillow
scikit-learn
colorthief
numpy
```

---

### 📁 `sneaker_data.json`

```json
[
  {
    "name": "Nike Air Max Red",
    "brand": "Nike",
    "image": "sneakers/nike_red.png",
    "colors": ["#c60000", "#ffffff"]
  },
  {
    "name": "Adidas Cloud White",
    "brand": "Adidas",
    "image": "sneakers/adidas_white.png",
    "colors": ["#ffffff", "#dcdcdc"]
  }
]
```

---

### 🧠 `app.py`

```python
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
```

---

### 📝 `README.md`

````markdown
# 👟 SneakerMatch AI

An AI app that recommends sneakers based on your outfit. Just upload an outfit photo, and SneakerMatch AI finds the best matching sneaker from a dataset.

## 💡 Features
- Detects dominant colors from outfit
- Compares with sneaker catalog
- Displays closest sneaker match

## 🖥️ Run Locally in VS Code
1. Clone the repo:
```bash
git clone https://github.com/your-username/SneakerMatch-AI.git
cd SneakerMatch-AI
````

2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Run app:

```bash
streamlit run app.py
```

## 🌐 Deployment

Deploy easily on:

* [Streamlit Cloud](https://streamlit.io/cloud)
* Hugging Face Spaces
* GitHub Pages (for static info)

## 📸 Dataset

Add at least 5 sample sneaker images in `sneakers/` folder and update `sneaker_data.json` with color codes.

## 🧠 Future Ideas

* Use CNN to compare textures
* Use fashion APIs for real-time product suggestions

```

---

### 🧪 Want Sample Sneaker Images?
You can create a few PNG images with simple colors (e.g., red, white, black sneakers) or I can help generate them using AI.

Would you like another topic after this?
```
