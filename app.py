
import streamlit as st
from google import genai
from PIL import Image
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="VisionMate AI",
    page_icon="👁️",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #17152b);
    color: white;
}
h1 {
    color: #8B9CFF;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #B8BDD6;
    font-size: 16px;
}
.stButton button {
    background: linear-gradient(90deg, #6558E8, #3988E8);
    color: white;
    border: none;
    border-radius: 10px;
    width: 100%;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("👁️ VisionMate AI")

st.markdown(
    '<p class="subtitle">See Beyond Images with Artificial Intelligence</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- API CONFIGURATION ----------------
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))

# ---------------- IMAGE UPLOAD ----------------
st.markdown("### 📸 Upload or Capture an Image")

upload_option = st.radio(
    "Choose image source",
    ["Gallery", "Camera"],
    horizontal=True
)

if upload_option == "Gallery":
    uploaded_image = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png", "webp"]
    )
else:
    uploaded_image = st.camera_input("Take a photo")

# ---------------- IMAGE ANALYSIS ----------------
if uploaded_image:

    image = Image.open(uploaded_image).convert("RGB")

    st.image(
        image,
        caption="Your uploaded image",
        use_container_width=True
    )

    st.divider()

    st.markdown("### 🤖 Ask VisionMate")

    analysis_type = st.selectbox(
        "Choose an AI task",
        [
            "Describe this image",
            "Identify objects",
            "Explain the scene",
            "Extract visible text (OCR)",
            "Analyze this image in detail",
            "Ask a custom question"
        ]
    )

    custom_question = ""

    if analysis_type == "Ask a custom question":
        custom_question = st.text_area(
            "What would you like to know?",
            placeholder="Example: What objects are visible?"
        )

    prompts = {
        "Describe this image":
            "Describe this image clearly and naturally.",

        "Identify objects":
            "Identify the main objects visible in this image.",

        "Explain the scene":
            "Explain what is happening in this image.",

        "Extract visible text (OCR)":
            "Read and extract all clearly visible text from this image.",

        "Analyze this image in detail":
            "Provide a detailed analysis of this image, including objects, colors, environment and context."
    }

    if st.button("✨ Analyze Image"):

        if analysis_type == "Ask a custom question" and not custom_question.strip():
            st.warning("Please enter your question.")

        elif not api_key:
            st.error(
                "Gemini API key is missing. "
                "Please configure GEMINI_API_KEY in Streamlit Secrets."
            )

        else:
            try:
                prompt = (
                    custom_question.strip()
                    if analysis_type == "Ask a custom question"
                    else prompts[analysis_type]
                )

                with st.spinner("🧠 VisionMate is analyzing your image..."):

                    client = genai.Client(api_key=api_key)

                    response = client.models.generate_content(
                        model=os.getenv(
                            "GEMINI_MODEL",
                            "gemini-2.5-flash"
                        ),
                        contents=[prompt, image]
                    )

                if response.text:
                    st.markdown("### 💡 AI Analysis")
                    st.markdown(response.text)
                else:
                    st.warning("The AI returned an empty response.")

            except Exception:
                st.error(
                    "Unable to analyze the image. "
                    "Please check your API key, model availability "
                    "and internet connection, then try again."
                )

else:
    st.info("👆 Upload an image or capture a photo to get started.")

# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    """
    <p style='text-align:center;color:#9298B5;'>
    Built with ❤️ using Python, Streamlit & Gemini AI
    </p>
    """,
    unsafe_allow_html=True
)
