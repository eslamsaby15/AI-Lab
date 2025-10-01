from ..helpers.config import APP_Setting
from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
import os
from ..tasks import TranslationTask

def Translation_page(): 
    st.subheader("🌍 Translation Page")
    youtube_link = None 
    file_uploaded = None

    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "translation" not in st.session_state:
        st.session_state.translation = None

    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"

    if "embedding_provider" not in st.session_state:
        st.session_state["embedding_provider"] = "Cohere"

    input_type = st.selectbox("Choose input type", ["Upload file", "YouTube link"])

    if input_type == "Upload file":
        file_uploaded = st.file_uploader(
            '📂 Upload audio/video', 
            type=[InputTypes.WAV.value, InputTypes.MKV.value, InputTypes.MP4.value, InputTypes.MP3.value]
        )
    elif input_type == "YouTube link":
        youtube_link = st.text_input('Paste YouTube link')

    mode = st.radio("⚙️ Translation Mode", ["classic", "llm"], index=1)

    if st.button("🚀 Translate"):

        if not youtube_link and not file_uploaded:
            st.warning("⚠️ Please enter a YouTube link or upload a file.")
            return 

        yt = Youtube()
        if youtube_link: 
            wav_file = yt.Download(youtube_link)
        else:
            wav_file = yt.save_dir(file_uploaded)

        with st.spinner("📝 Transcribing..."):
            transcriber = Wav2VecTranscriber()
            st.session_state.transcript = transcriber.transcribe(wav_file)
            st.success("✅ Transcription done!")

        with st.spinner("🌍 Translating..."):
            task = TranslationTask(
                mode=mode,
                provider_name=st.session_state["generation_provider"]
            )
            st.session_state.translation = task.run(st.session_state.transcript)
            st.success("✅ Translation generated!")

    if st.session_state.transcript:
        st.subheader("Transcript")
        st.text_area("Transcript", st.session_state.transcript, height=200)

    if st.session_state.translation:
        st.subheader("🌍 Translation")
        st.text_area(" ", st.session_state.translation, height=200)

        st.sidebar.subheader("📥 Download")
        st.sidebar.download_button(
            "Download Translation",
            st.session_state.translation,
            file_name="translation.txt"
        )
