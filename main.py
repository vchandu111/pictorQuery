import streamlit as st
import base64
from openai import OpenAI

# 🗝️ Load API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Page setup
st.set_page_config(page_title="GPT-4o Vision App", layout="centered")
st.title("🧠 GPT-4o Vision: Text + Image Q&A")
st.markdown("Upload an image and ask GPT-4o a question about it.")

# Upload and prompt
uploaded_image = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])
user_text_prompt = st.text_input("💬 Your question about the image")

# Convert image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

if uploaded_image and user_text_prompt:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔄 Analyzing..."):
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
