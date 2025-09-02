# app.py
import streamlit as st
from PIL import Image
from utils.vision import extract_tags
from utils.openai_caption import generate_caption
import io

st.set_page_config(page_title="AI Image Caption Generator")
st.title("🖼️ AI Image Caption Generator")

st.markdown("Upload an image, and we'll generate a caption using Azure Vision and GPT-4o.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width="stretch")

    with st.spinner("Analyzing image and generating caption..."):
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        image_bytes = image_bytes.getvalue()

        tags = extract_tags(image_bytes)
        caption = generate_caption(tags)

    st.markdown("### 🧠 Generated Caption")
    st.success(caption)
