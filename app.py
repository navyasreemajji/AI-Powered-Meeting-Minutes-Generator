import streamlit as st
import tempfile
import os
import soundfile as sf

from transcription import transcribe_audio
from main import meeting_minutes
from save_as_docx import save_as_docx

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Meeting Minutes Generator",
    page_icon="📝",
    layout="centered"
)

# ---------------- CUSTOM STYLING ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fb;
    }

    .main {
        background-color: #f5f7fb;
    }

    .title-box {
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }

    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        padding: 10px 18px;
        border: none;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #4338ca;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <div class="title-box">
        <h1>AI Meeting Minutes Generator</h1>
        <p>Upload meeting audio and automatically generate structured minutes</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- SECURITY CONFIG ----------------
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".m4a"}
MAX_FILE_SIZE_MB = 100

def is_safe_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        st.error("Only WAV, MP3, or M4A files are allowed.")
        return False
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        st.error("File size exceeds 25 MB.")
        return False
    return True

def validate_audio(path):
    try:
        sf.read(path)
        return True
    except Exception:
        return False

# ---------------- UPLOAD CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload meeting audio file",
    type=["wav", "mp3", "m4a"]
)

if uploaded_file and is_safe_file(uploaded_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    if not validate_audio(audio_path):
        st.error("Invalid or corrupted audio file.")
        st.stop()

    st.success("Audio file validated successfully")

    if st.button("Generate Meeting Minutes"):
        with st.spinner("Processing audio and generating minutes..."):
            transcript = transcribe_audio(audio_path)
            output = meeting_minutes(transcript)
            save_as_docx(output, "meeting_minutes.docx")

        st.success("Meeting minutes generated successfully!")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- OUTPUT CARDS ----------------
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Summary")
        st.write(output["abstract_summary"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Full Transcript")
        st.text_area("", output["transcript"], height=220)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Meeting Minutes")
        st.write(output["meeting_minutes"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Sentiment")
        st.write(output["sentiment"])
        st.markdown("</div>", unsafe_allow_html=True)

        with open("meeting_minutes.docx", "rb") as file:
            st.download_button(
                label="⬇Download Meeting Minutes (DOCX)",
                data=file,
                file_name="meeting_minutes.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

else:
    st.markdown("</div>", unsafe_allow_html=True)
