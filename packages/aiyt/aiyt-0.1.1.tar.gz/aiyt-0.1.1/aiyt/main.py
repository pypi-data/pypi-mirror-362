import streamlit as st
from aiyt.utils import youtube_obj
from ui import app_header, caption_ui, divider, transcribe_ui


def body():
    api_key = st.text_input(
        "Gemini API key",
        key="gemini-api-key",
        type="password",
        help="Visit [gemini docs](https://ai.google.dev/gemini-api/docs/api-key) to get the API key",
    )
    url = st.text_input("Youtube URL", key="url-input", disabled=not api_key)

    if not api_key or not url:
        st.stop()

    if not (yt := youtube_obj(url)):
        st.error("Invalid URL")
        st.stop()

    langs = [c.code for c in yt.captions]

    divider(key=1)

    if langs or not yt:
        caption_ui(yt, langs, api_key)
    else:
        transcribe_ui(yt, api_key)


def app():
    app_header(icon="youtube_activity", color="red")
    with st.container(border=True, key="main-container"):
        body()


if __name__ == "__main__":
    app()
