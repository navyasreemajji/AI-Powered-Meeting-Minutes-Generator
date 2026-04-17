import streamlit as st
import tempfile
import os
import soundfile as sf
import time

from transcription import transcribe_audio
from main import meeting_minutes
from save_as_docx import save_as_docx

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Meeting Minutes Generator",
    page_icon="🎙️",
    layout="centered"
)

# ---------------- ADVANCED UI STYLING ----------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #020617, #020617, #0f172a);
    color: white;
}

/* Glass container */
.glass {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    backdrop-filter: blur(10px);
    margin-bottom: 25px;
}

/* Title */
.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg,#38bdf8,#a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #e5e7eb;
    margin-bottom: 25px;
    font-size: 16px;
}

/* File uploader text */
.stFileUploader label {
    color: white !important;
    font-weight: 600;
}

/* Browse files button */
button[kind="secondary"] {
    background-color: #1e293b !important;
    color: white !important;
    border-radius: 10px;
}

/* Main button */
.stButton>button {
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color: white;
    border-radius: 12px;
    padding: 12px 24px;
    border: none;
    font-size: 16px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#8b5cf6,#6366f1);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 16px;
    margin-top: 15px;
}

/* Text areas */
textarea {
    background-color: #020617 !important;
    color: white !important;
}

/* Success message */
.stAlert-success {
    background-color: #064e3b !important;
    color: #ecfdf5 !important;
}

/* Download button */
.stDownloadButton>button {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 10px;
    border: 1px solid #38bdf8;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="glass">
    <div class="title">🎙️ AI Meeting Minutes Generator</div>
    <div class="subtitle">
        Upload meeting audio and automatically generate structured meeting minutes
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- FILE UPLOAD ----------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload meeting audio file",
    type=["wav", "mp3", "m4a"]
)

st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file:
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    st.success("Audio uploaded successfully")

    if st.button("Generate Meeting Minutes"):
        progress = st.progress(0)
        status = st.empty()

        status.text("Transcribing audio...")
        progress.progress(25)
        time.sleep(1)

        transcript = transcribe_audio(audio_path)

        status.text("Analyzing and summarizing...")
        progress.progress(60)
        time.sleep(1)

        output = meeting_minutes(transcript)

        status.text("Creating document...")
        progress.progress(90)
        time.sleep(1)

        save_as_docx(output, "meeting_minutes.docx")
        progress.progress(100)
        status.text("Completed")

        st.success("Meeting minutes generated successfully")

        # ---------------- OUTPUT ----------------
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Summary")
        st.write(output["abstract_summary"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Full Transcript")
        st.text_area("Transcript", output["transcript"], height=220)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Meeting Minutes")
        st.write(output["meeting_minutes"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Sentiment")
        st.write(output["sentiment"])
        st.markdown('</div>', unsafe_allow_html=True)

        with open("meeting_minutes.docx", "rb") as file:
            st.download_button(
                label="Download Meeting Minutes (DOCX)",
                data=file,
                file_name="meeting_minutes.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )