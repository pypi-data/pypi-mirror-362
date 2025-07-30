import streamlit as st
from aiyt.utils import add_punctuation, consolidate_messages, metadata, transcribe
from google.genai import Client, types
from pytubefix import YouTube
from textwrap import dedent

MODELS = ["gemini-2.0-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro"]
sess = st.session_state


def app_header(icon: str, color: str):
    icon_with_color = f":{color}[:material/{icon}:]"
    with st.container(key="app-header"):
        st.markdown(f"## {icon_with_color} &nbsp; {metadata['name']}")
        st.caption(metadata["description"])


def divider(key: int = 1):
    with st.container(key=f"divider{key}"):
        st.divider()


def input_ui() -> tuple[str, str, str]:
    """Streamlit UI for inputting API key, model, and YouTube URL"""
    with st.form(key="input-form", enter_to_submit=True, border=False):
        c1, c2 = st.columns(2)
        api_key = c1.text_input(
            "Gemini API key",
            key="gemini-api-key",
            type="password",
            help="Visit [gemini docs](https://ai.google.dev/gemini-api/docs/api-key) to get the API key",
        )
        model = c2.selectbox(
            "Select the model",
            key="model",
            options=MODELS,
            index=0,
        )

        c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
        url = c1.text_input("Youtube URL", key="url-input")

        c2.form_submit_button(
            "Submit",
            use_container_width=True,
            on_click=lambda: sess.update({"chat": None}),
        )

        submittable = api_key and model and url
        if not submittable:
            st.stop()

    return api_key, model, url


def caption_ui(yt: YouTube | None, langs: list[str], api_key: str, model: str) -> None:
    st.markdown("#### 💬 &nbsp; Extract Captions")

    st.selectbox(
        label="Select the language",
        key="caption_lang",
        options=langs,
        index=None,
        format_func=lambda x: x.split(".")[-1],
    )

    st.radio(
        label="Select the format",
        key="caption_format",
        options=["srt", "txt", "ai formatted"],
        index=0,
        horizontal=True,
        disabled=not sess.caption_lang,
    )

    transcript = ""
    if sess.caption_lang:
        if sess.caption_format == "srt":
            transcript = yt.captions[sess.caption_lang].generate_srt_captions()
        else:
            raw_transcript = yt.captions[sess.caption_lang].generate_txt_captions()
            if sess.caption_format == "txt":
                transcript = raw_transcript
            elif sess.caption_format == "ai formatted":
                transcript = add_punctuation(api_key, raw_transcript, model)

    sess.caption_output = transcript
    st.text_area(
        label="Captions",
        key="caption_output",
        height=400,
        disabled=not transcript,
    )

    return transcript


def transcribe_ui(yt: YouTube, api_key: str, model: str) -> str:
    """Streamlit UI for transcribing audio"""
    st.markdown("#### 🗣️ &nbsp; Transcribe Audio")
    if "transcribe_consent" not in sess:
        sess.transcribe_consent = dict()
    if not sess.transcribe_consent.setdefault(yt.video_id, False):
        st.info("No captions found, transcribe audio with Gemini?")
        if st.button("Transcribe"):
            sess.transcribe_consent[yt.video_id] = True
    if sess.transcribe_consent[yt.video_id]:
        st.text_area(
            label="Transcript",
            value=transcribe(yt.video_id, model, api_key),
            key="transcript_output",
            height=400,
        )
        return sess.transcript_output


def chat_ui(transcript: str, api_key: str, model: str) -> None:
    """Streamlit chat interface for interacting with the transcript"""
    divider(key=2)

    sys_prompt = dedent(f"""\
            You are a helpful assistant that can answer questions about this transcript:
            <transcript>
            {transcript}
            </transcript>
        """)

    # Initialize chat object in session state
    if sess.chat is None:
        client = Client(api_key=api_key)
        sess.chat = client.chats.create(
            model=model,
            config=types.GenerateContentConfig(system_instruction=sys_prompt),
        )

    # Display chat history with consolidated messages
    avatar = {"user": "🐒", "model": "💭"}
    consolidated_messages = consolidate_messages(sess.chat.get_history())
    for role, text in consolidated_messages:
        with st.chat_message(role, avatar=avatar[role]):
            st.markdown(text)

    # Accept user input
    if prompt := st.chat_input("chat about the transcript..."):
        # Display user message
        with st.chat_message("user", avatar=avatar["user"]):
            st.markdown(prompt)

        # Generate and display assistant response
        with st.chat_message("model", avatar=avatar["model"]):
            try:
                response = sess.chat.send_message_stream(prompt)
                st.write_stream(chunk.text for chunk in response)

            except Exception as e:
                st.error(e)
                st.stop()
