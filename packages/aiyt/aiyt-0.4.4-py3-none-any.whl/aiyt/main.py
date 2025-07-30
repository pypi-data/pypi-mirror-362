import streamlit as st
from aiyt.ui import app_header, caption_ui, chat_ui, divider, input_ui, transcribe_ui
from pathlib import Path
from pytubefix import YouTube

root_folder = Path(__file__).parent.parent


def body():
    with st.container(border=True, key="main-container"):
        api_key, model, url = input_ui()

        try:
            yt = YouTube(url)
            yt.check_availability()
        except Exception as e:
            st.error(e)
            st.stop()

        langs = [c.code for c in yt.captions]

        divider(key=1)

        if langs or not yt:
            transcript = caption_ui(yt, langs, api_key, model)
        else:
            transcript = transcribe_ui(yt, api_key, model)

    if transcript:
        chat_ui(transcript, api_key, model)


def app():
    st.html(root_folder / "style.css")
    app_header(icon="youtube_activity", color="red")
    st.write("")
    body()


if __name__ == "__main__":
    app()
