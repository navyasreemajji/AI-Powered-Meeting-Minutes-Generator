from sentiment_analysis import (
    abstract_summary_extraction,
    meeting_minutes_extraction,
    sentiment_analysis
)

def meeting_minutes(transcript: str) -> dict:
    summary = abstract_summary_extraction(transcript)
    minutes_text = meeting_minutes_extraction(transcript)
    sentiment = sentiment_analysis(transcript)

    return {
        "transcript": transcript,
        "abstract_summary": summary,
        "meeting_minutes": minutes_text,
        "sentiment": sentiment
    }


if __name__ == "__main__":
    from transcription import transcribe_audio
    from save_as_docx import save_as_docx

    audio_file_path = "./audio/EarningsCall.wav"
    transcript = transcribe_audio(audio_file_path)

    output = meeting_minutes(transcript)
    print(output)

    save_as_docx(output, "meeting_minutes.docx")