import streamlit as st
from transformers import pipeline

@st.cache_resource
def load_nlp_models():
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    sentiment_model = pipeline("sentiment-analysis")
    return summarizer, sentiment_model


def abstract_summary_extraction(text: str) -> str:
    summarizer, _ = load_nlp_models()
    summary = summarizer(text, max_length=150, min_length=60, do_sample=False)
    return summary[0]["summary_text"]


def meeting_minutes_extraction(text: str):
    summarizer, _ = load_nlp_models()
    summary = summarizer(text, max_length=300, min_length=150, do_sample=False)
    paragraph = summary[0]["summary_text"]

    # Convert paragraph into clean bullet points
    points = [
        p.strip()
        for p in paragraph.replace("•", ".").split(".")
        if len(p.strip()) > 20
    ]

    return points

def sentiment_analysis(text: str) -> str:
    _, sentiment_model = load_nlp_models()
    result = sentiment_model(text[:512])
    return result[0]["label"]
