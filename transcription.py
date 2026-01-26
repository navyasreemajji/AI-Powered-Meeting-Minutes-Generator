import whisper
import streamlit as st

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def transcribe_audio(audio_file_path, _unused=None):
    model = load_whisper_model()
    result = model.transcribe(audio_file_path)
    return result["text"]
