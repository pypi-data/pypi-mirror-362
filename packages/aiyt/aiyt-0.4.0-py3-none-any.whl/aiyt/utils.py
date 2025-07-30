import streamlit as st
import tomllib
from google.genai import Client, types
from io import BytesIO
from pathlib import Path
from pytubefix import Buffer, YouTube

sess = st.session_state


def pyproject_data() -> dict:
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        return tomllib.load(f)


metadata = pyproject_data()["project"]


@st.cache_data(show_spinner=False)
def add_punctuation(api_key: str, transcript: str, model: str) -> str:
    """Add punctuation to a transcript using Gemini's LLM."""
    sys_prompt = "add punctuations and appropiate paragraphs to the following text, do not add any comments"
    client = Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=sys_prompt),
        contents=transcript,
    )
    return response.text


def download_audio_from_yt(id: str) -> tuple[Buffer, str]:
    """download the lowest quality audio stream to a pytubefix Buffer object"""
    yt = YouTube(f"https://youtu.be/{id}")
    audio_streams = yt.streams.filter(only_audio=True, audio_codec="opus")
    lowest_quality_stream = audio_streams.order_by("abr").first()
    if not lowest_quality_stream:
        st.error("No audio stream found")
        st.stop()
    buffer = Buffer()
    buffer.download_in_buffer(lowest_quality_stream)
    mime_type = lowest_quality_stream.mime_type
    return buffer, mime_type


# reserve for one-off upload use cases
# def get_audio_part(mime_type: str, buffer: Buffer) -> types.Part:
#     """convert the pytubefix Buffer object to a Gemini types.Part object"""
#     return types.Part.from_bytes(data=buffer.read(), mime_type=mime_type)


def remove_duplicate_gemini_audio(name: str, client: Client):
    """adding audio with the same name to Gemini cloud storage will raise an error, so remove the existing one"""
    audio_files = [f.name for f in client.files.list()]
    for file_name in audio_files:
        if name in file_name:
            client.files.delete(name=file_name)


def upload_audio_to_gemini(
    name: str, buffer: Buffer, mime_type: str, client: Client
) -> types.File:
    """upload the audio to Gemini cloud storage"""
    io_obj: BytesIO = buffer.buffer
    io_obj.seek(0)
    upload_config = types.UploadFileConfig(mime_type=mime_type, name=name)
    remove_duplicate_gemini_audio(name, client)
    return client.files.upload(file=io_obj, config=upload_config)


@st.cache_data(show_spinner=False)
def transcribe(
    id: str,
    model: str,
    api_key: str,
    system_prompt: str = "You are a professional transcriber. You output only transcript, no other text.",
    user_prompt: str = "Generate a transcript of the speech",
) -> str:
    """transcribe the audio using Gemini"""
    filename = id.lower()
    buffer, mime_type = download_audio_from_yt(id)
    client = Client(api_key=api_key)
    audio_file = upload_audio_to_gemini(filename, buffer, mime_type, client)

    response = client.models.generate_content(
        model=model,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
        contents=[user_prompt, audio_file],
    )
    return response.text


def consolidate_messages(messages: list) -> list:
    """Consolidate consecutive messages with the same role into single messages"""
    if not messages:
        return []

    consolidated = []
    current_role = None
    current_text = ""

    for message in messages:
        if current_role is None:
            current_role = message.role
            current_text = message.parts[0].text
        elif message.role == current_role:
            # Same role, concatenate text
            current_text += message.parts[0].text
        else:
            # Different role, save current and start new
            consolidated.append((current_role, current_text))
            current_role = message.role
            current_text = message.parts[0].text

    # Don't forget the last message
    if current_role is not None:
        consolidated.append((current_role, current_text))

    return consolidated
