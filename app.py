
import os
import base64
import io
import streamlit as st
from google import genai
from PIL import Image

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="VisionMate AI",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# CLASSIC PREMIUM UI
# ==================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {
        --navy: #202B3C;
        --navy-hover: #35445C;
        --gold: #A17D42;
        --gold-light: #D5B77A;
        --ivory: #F6F5F1;
        --paper: #FFFFFF;
        --ink: #252B36;
        --muted: #687181;
        --line: #E2DED5;
    }

    .stApp {
        background: var(--ivory);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        padding-top: 2.1rem;
        padding-bottom: 2.5rem;
        max-width: 1440px;
    }

    header[data-testid="stHeader"] {
        background: rgba(246, 245, 241, 0.92);
    }

    html, body, [class*="css"], .stMarkdown, .stText,
    [data-testid="stCaptionContainer"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    h1, h2, h3, h4 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: var(--navy) !important;
        letter-spacing: -0.25px;
    }

    p, li, label, .stMarkdown p, .stMarkdown li {
        color: var(--ink);
        line-height: 1.65;
    }

    [data-testid="stCaptionContainer"] p,
    .stCaption {
        color: var(--muted) !important;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: #EEECE6;
        border-right: 1px solid #DDD8CE;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: var(--navy) !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] label {
        color: #343B46 !important;
    }

    /* Hero */

    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(120deg, #202B3C 0%, #2E3B50 72%, #3C4656 100%);
        padding: 42px 42px 39px;
        border: 1px solid rgba(213, 183, 122, 0.25);
        border-radius: 16px;
        margin-bottom: 27px;
        box-shadow: 0 12px 30px rgba(32, 43, 60, 0.13);
        transition: transform 220ms ease, box-shadow 220ms ease;
    }

    .hero:hover {
        transform: translateY(-3px);
        box-shadow: 0 17px 36px rgba(32, 43, 60, 0.19);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 230px;
        height: 230px;
        right: -75px;
        top: -105px;
        border: 1px solid rgba(213, 183, 122, 0.24);
        border-radius: 50%;
        box-shadow: 0 0 0 25px rgba(213, 183, 122, 0.035),
                    0 0 0 52px rgba(213, 183, 122, 0.025);
        pointer-events: none;
    }

    .hero-tag {
        color: var(--gold-light);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.8px;
        margin-bottom: 13px;
    }

    .hero h1 {
        color: #FFFFFF !important;
        font-size: clamp(34px, 4vw, 46px) !important;
        line-height: 1.15;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #E1E5EA !important;
        font-size: 15px;
        max-width: 680px;
        margin: 0;
    }

    /* Section labels */

    .section-label {
        color: #936F36;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 5px 0 8px;
    }

    /* Dashboard cards */

    .info-card {
        background: linear-gradient(145deg, #FFFFFF, #F9F8F4);
        border: 1px solid var(--line);
        border-radius: 13px;
        padding: 20px 16px;
        min-height: 112px;
        text-align: center;
        box-shadow: 0 4px 13px rgba(32, 43, 60, 0.045);
        transition: transform 200ms ease, box-shadow 200ms ease,
                    border-color 200ms ease;
    }

    .info-card:hover {
        transform: translateY(-5px);
        border-color: #CBB78F;
        box-shadow: 0 12px 24px rgba(32, 43, 60, 0.10);
    }

    .info-number {
        color: var(--gold);
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 29px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 7px;
    }

    .info-text {
        color: #596170;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.3px;
    }

    /* Buttons */

    .stButton > button,
    .stDownloadButton > button {
        background: var(--navy);
        color: #FFFFFF !important;
        border: 1px solid var(--navy);
        border-radius: 8px;
        min-height: 45px;
        font-weight: 600;
        letter-spacing: 0.2px;
        box-shadow: 0 4px 10px rgba(32, 43, 60, 0.10);
        transition: transform 180ms ease, background 180ms ease,
                    box-shadow 180ms ease, border-color 180ms ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background: var(--navy-hover);
        color: #FFFFFF !important;
        border-color: var(--gold-light);
        transform: translateY(-2px);
        box-shadow: 0 8px 17px rgba(32, 43, 60, 0.18);
    }

    .stButton > button:focus,
    .stDownloadButton > button:focus {
        color: #FFFFFF !important;
        border-color: var(--gold);
        box-shadow: 0 0 0 2px rgba(161, 125, 66, 0.22);
    }

    /* Inputs */

    div[data-testid="stFileUploader"] {
        background: #FFFFFF;
        border: 1px dashed #BEB6A7;
        border-radius: 12px;
        padding: 13px;
        transition: border-color 180ms ease, box-shadow 180ms ease;
    }

    div[data-testid="stFileUploader"]:hover {
        border-color: var(--gold);
        box-shadow: 0 5px 16px rgba(32, 43, 60, 0.07);
    }

    div[data-testid="stFileUploader"] *,
    div[data-testid="stCameraInput"] * {
        color: var(--ink);
    }

    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stTextInput"] input {
        background: #FFFFFF;
        color: var(--ink) !important;
        border-color: #D8D2C7;
        border-radius: 8px;
    }

    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stTextInput"] input::placeholder {
        color: #858B95 !important;
        opacity: 1;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label,
    div[data-testid="stTextArea"] label {
        color: var(--ink) !important;
        font-weight: 600;
    }

    /* Dropdown */

    [data-baseweb="popover"] ul,
    [data-baseweb="menu"] {
        background: #FFFFFF;
    }

    [data-baseweb="menu"] * {
        color: var(--ink) !important;
    }

    /* Containers */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 12px;
        box-shadow: 0 5px 16px rgba(32, 43, 60, 0.055);
        transition: box-shadow 180ms ease, border-color 180ms ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #D2C5AA;
        box-shadow: 0 9px 22px rgba(32, 43, 60, 0.09);
    }

    .result-card {
        background: #FFFFFF;
        border: 1px solid var(--line);
        border-radius: 12px;
        padding: 24px;
        margin-top: 15px;
        box-shadow: 0 5px 16px rgba(32, 43, 60, 0.055);
    }

    /* Image preview */

    [data-testid="stImage"] img {
        border-radius: 12px;
        border: 1px solid #E2DED5;
        box-shadow: 0 7px 20px rgba(32, 43, 60, 0.09);
    }

    /* Alerts */

    div[data-testid="stAlert"] {
        border-radius: 9px;
    }

    hr {
        border-color: #DED9CF !important;
    }

    footer {
        visibility: hidden;
    }

    /* Responsive */

    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.2rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 29px 23px;
            border-radius: 13px;
        }

        .hero p {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==================================================
# API CONFIGURATION
# ==================================================

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
        if key:
            return key.strip()
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY", "").strip()


api_key = get_api_key()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("## 👁️ VisionMate AI")
    st.caption("INTELLIGENT IMAGE UNDERSTANDING")
    st.divider()

    st.markdown("### About the Project")
    st.write(
        "VisionMate AI transforms images into meaningful insights "
        "using Google's Gemini AI."
    )

    st.divider()
    st.markdown("### Features")

    features = [
        "📸 Image Upload",
        "📷 Camera Capture",
        "🔍 Object Identification",
        "🌍 Scene Understanding",
        "📝 Text Extraction",
        "💬 Custom Questions",
    ]

    for feature in features:
        st.markdown(f"- {feature}")

    st.divider()
    st.markdown("### Technology")
    st.caption("PYTHON")
    st.caption("STREAMLIT")
    st.caption("GOOGLE GEMINI AI")
    st.caption("PILLOW")

    st.divider()
    st.markdown("**AI Model**")
    st.code(MODEL_NAME)

    if api_key:
        st.success("API key configured")
    else:
        st.warning("API key not configured")


# ==================================================
# HERO SECTION
# ==================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">ARTIFICIAL INTELLIGENCE • COMPUTER VISION</div>
        <h1>VisionMate AI</h1>
        <p>
            See beyond what the eyes can capture.
            Understand images through the power of artificial intelligence.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# DASHBOARD INFORMATION
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-number">01</div>
            <div class="info-text">UPLOAD IMAGE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-number">02</div>
            <div class="info-text">SELECT AI TASK</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="info-card">
            <div class="info-number">03</div>
            <div class="info-text">GET INSIGHTS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==================================================
# IMAGE INPUT
# ==================================================

st.write("")

st.markdown(
    '<div class="section-label">01 — IMAGE INPUT</div>',
    unsafe_allow_html=True,
)

st.markdown("### Bring your image to life")

upload_option = st.radio(
    "Select image source",
    ["Gallery", "Camera"],
    horizontal=True,
)

if upload_option == "Gallery":
    uploaded_image = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="Supported formats: JPG, JPEG, PNG and WEBP",
    )
else:
    uploaded_image = st.camera_input("Capture an image")


# ==================================================
# IMAGE PROCESSING
# ==================================================

if uploaded_image:

    try:
        image = Image.open(uploaded_image).convert("RGB")

    except Exception:
        st.error("Unable to read this image. Please try another file.")
        st.stop()

    st.write("")

    left, right = st.columns([1.1, 0.9], gap="large")

    # IMAGE PREVIEW

    with left:

        st.markdown(
            '<div class="section-label">IMAGE PREVIEW</div>',
            unsafe_allow_html=True,
        )

        st.image(image, width="stretch")

        st.caption(
            f"Image dimensions: {image.width} × {image.height} pixels"
        )

    # TASK SELECTION

    with right:

        st.markdown(
            '<div class="section-label">02 — AI ANALYSIS</div>',
            unsafe_allow_html=True,
        )

        st.markdown("### What should VisionMate do?")

        analysis_type = st.selectbox(
            "Choose your task",
            [
                "Describe this image",
                "Identify objects",
                "Explain the scene",
                "Extract visible text (OCR)",
                "Analyze this image in detail",
                "Ask a custom question",
            ],
        )

        prompts = {
            "Describe this image": (
                "Describe this image clearly and naturally. "
                "Explain its main subject and important details."
            ),

            "Identify objects": (
                "Identify the important objects in this image. "
                "Explain their appearance and positions."
            ),

            "Explain the scene": (
                "Explain the scene shown in this image. "
                "Describe the environment, activities and context."
            ),

            "Extract visible text (OCR)": (
                "Extract all clearly visible text from this image. "
                "Preserve the original wording and layout where possible."
            ),

            "Analyze this image in detail": (
                "Provide a comprehensive analysis of this image, "
                "including objects, colors, environment, composition "
                "and relevant context."
            ),
        }

        custom_question = ""

        if analysis_type == "Ask a custom question":

            custom_question = st.text_area(
                "Enter your question",
                placeholder="What objects are visible in this image?",
                height=120,
            )

        st.write("")

        analyze_button = st.button(
        "✦  Analyze Image",
         width="stretch",
        type="primary",
        help="Click to analyze the image using Gemini AI",
        )

    # ==================================================
    # GEMINI AI ANALYSIS - UPDATED INTERACTIONS API
    # ==================================================

    if analyze_button:

        if not api_key:

            st.error(
                "Gemini API key is missing. "
                "Configure it in .streamlit/secrets.toml."
            )

        elif (
            analysis_type == "Ask a custom question"
            and not custom_question.strip()
        ):

            st.warning("Please enter a question first.")

        else:

            prompt = (
                custom_question.strip()
                if analysis_type == "Ask a custom question"
                else prompts[analysis_type]
            )

            try:

                with st.spinner(
                    "VisionMate is analyzing your image..."
                ):

                    # Initialize Gemini client with timeout
                    client = genai.Client(
                        api_key=api_key,
                        http_options={
                            "timeout": 120000
                        },
                    )

                    # Convert PIL image to JPEG bytes
                    image_buffer = io.BytesIO()

                    image.save(
                        image_buffer,
                        format="JPEG",
                        quality=90,
                    )

                    image_bytes = image_buffer.getvalue()

                    # Convert image bytes to Base64
                    image_base64 = base64.b64encode(
                        image_bytes
                    ).decode("utf-8")

                    # Call Gemini Interactions API
                    interaction = client.interactions.create(
                        model=MODEL_NAME,
                        input=[
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image",
                                "data": image_base64,
                                "mime_type": "image/jpeg",
                            },
                        ],
                    )

                    # Extract AI response
                    result = (
                        interaction.output_text or ""
                    ).strip()

                if result:

                    st.session_state["vision_result"] = result

                    st.session_state["vision_task"] = analysis_type

                    st.success(
                        "Analysis completed successfully!"
                    )

                else:

                    st.warning(
                        "The AI returned an empty response. "
                        "Please try again."
                    )

            except Exception as e:

                st.error(
                    "Unable to analyze the image."
                )

                with st.expander(
                    "View technical error details"
                ):

                    st.code(
                        f"{type(e).__name__}: {str(e)}"
                    )

                st.info(
                    "Check your API key, model access, "
                    "internet connection and SDK version."
                )


# ==================================================
# DISPLAY AI RESULT
# ==================================================

if "vision_result" in st.session_state:

    st.divider()

    st.markdown(
        '<div class="section-label">03 — AI INSIGHTS</div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ✦ VisionMate Analysis")

    with st.container(border=True):

        st.caption(
            f"Task: {st.session_state['vision_task']}"
        )

        st.markdown(
            st.session_state["vision_result"]
        )

    st.download_button(
        label="↓ Download Analysis",
        data=st.session_state["vision_result"],
        file_name="visionmate_analysis.txt",
        mime="text/plain",
    )


# ==================================================
# EMPTY STATE
# ==================================================

elif not uploaded_image:

    st.write("")

    with st.container(border=True):

        st.markdown(
            "### Your next discovery starts here"
        )

        st.write(
            "Upload an image or capture a photo to let "
            "VisionMate AI understand what's inside."
        )

        st.caption(
            "SUPPORTED FORMATS: JPG · JPEG · PNG · WEBP"
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:18px 12px;
        color:#687181;
        font-size:12px;
        line-height:1.8;
    ">
        <strong style="
            color:#202B3C;
            letter-spacing:1.5px;
        ">VISIONMATE AI</strong>
        <br>
        Intelligent Image Understanding
        <br><br>
        Built with Python, Streamlit &amp; Google Gemini AI
        <br>
        © 2026 VisionMate AI
    </div>
    """,
    unsafe_allow_html=True,
)

