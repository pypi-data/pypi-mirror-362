import streamlit as st
from google.genai import Client
from pytubefix import YouTube
from utils import (
    add_punctuation,
    download_yt_audio,
    metadata,
    transcribe,
    upload_gemini_audio,
)


def app_header(icon: str, color: str):
    icon_with_color = f":{color}[:material/{icon}:]"
    with st.container(key="app-header"):
        st.markdown(f"## {icon_with_color} &nbsp; {metadata['name']}")
        st.caption(metadata["description"])


def divider(key: int = 1):
    with st.container(key=f"divider{key}"):
        st.divider()


def caption_ui(yt: YouTube | None, langs: list[str], api_key: str) -> None:
    st.markdown("#### 💬 &nbsp; Extract Captions")

    lang = st.selectbox(
        label="Select the language",
        key="caption-lang",
        options=langs,
        index=None,
        format_func=lambda x: x.split(".")[-1],
    )

    format = st.radio(
        label="Select the format",
        key="caption-format",
        options=["srt", "txt"],
        index=0,
        horizontal=True,
        disabled=not lang,
    )

    transcript = ""
    if lang:
        if format == "srt":
            transcript = yt.captions[lang].generate_srt_captions()
        elif format == "txt":
            raw_transcript = yt.captions[lang].generate_txt_captions()
            transcript = add_punctuation(api_key, raw_transcript)

    st.text_area(
        label="Captions",
        key="caption-output",
        value=transcript,
        height=400,
        disabled=not transcript,
    )


def transcribe_ui(yt: YouTube, api_key: str) -> str:
    """Streamlit UI for transcribing audio"""
    st.markdown("#### 🗣️ &nbsp; Transcribe Audio")
    with st.spinner("No captions found, transcribing audio with Gemini..."):
        client = Client(api_key=api_key)
        filename = yt.video_id.lower()
        buffer, mime_type = download_yt_audio(yt)
        audio_file = upload_gemini_audio(filename, buffer, mime_type, client)

        transcript = transcribe(audio_file, client)
        st.text_area(
            label="Transcript", key="transcript-output", value=transcript, height=400
        )
