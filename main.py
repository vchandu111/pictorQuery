import streamlit as st
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

# 🔑 Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 📌 Page configuration
st.set_page_config(page_title="GPT-4o Vision App", layout="centered")

# 🖼️ Title and description
st.title("🧠 GPT-4o Vision: Text + Image Q&A")
st.markdown("Upload an image and ask GPT-4o a question about it. The model will respond using its vision + language capabilities.")

# 📤 Image upload
uploaded_image = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])

# ✏️ Text prompt input
user_text_prompt = st.text_input("💬 What do you want to ask about this image?")

# 🧬 Function to encode image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

# 🚀 Run only if all inputs are available
if uploaded_image and user_text_prompt and api_key:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔄 Analyzing image and generating response..."):
        base64_image = encode_image(uploaded_image)

        client = OpenAI(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful tutor."},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_text_prompt},
                        {"type": "image_url", "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }}
                    ]}
                ],
                temperature=0
            )

            st.subheader("📝 GPT-4o Response")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.error(f"❌ Error: {e}")

# 🔁 Friendly user guidance
elif not uploaded_image:
    st.info("📎 Please upload an image to continue.")
elif not user_text_prompt:
    st.info("✏️ Please enter a question related to the image.")
elif not api_key:
    st.warning("🔐 API key not found. Please add it to your `.env` file.")
