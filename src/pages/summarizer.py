from ..helpers.config import APP_Setting
from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber,Summarizer
from ..tasks import SummarizerTask
import os

def summarizer_page(): 
    st.subheader("📝 Summarize")

    youtube_link = None 
    file_uploaded = None

    if "sum_transcript" not in st.session_state:
        st.session_state.sum_transcript = None
    if "sum_summary" not in st.session_state:
        st.session_state.sum_summary = None

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

    lang_choice = st.selectbox("🌐 Select language", ["auto", "en", "ar"], index=0)
    mode = st.radio("⚙️ Summarization Mode", ["classic", "llm"], index=1)

    if st.button("🚀 Summarize"):

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
            st.session_state.sum_transcript = transcriber.transcribe(wav_file)
            st.success("✅ Transcription done!")

        with st.spinner("📌 Summarizing..."):

            task = SummarizerTask(
                lang=lang_choice,
                mode=mode,
                provider_name=st.session_state["generation_provider"]
            )

            st.session_state.sum_summary = task.run(st.session_state.sum_transcript)
            st.success("✅ Summary generated!")


    if st.session_state.sum_transcript:
        st.subheader("Transcript")
        st.text_area("Transcript", st.session_state.sum_transcript, height=200)

    if st.session_state.sum_summary:
        st.subheader("📌 Summary")
        st.text_area(" ", st.session_state.sum_summary, height=200)

        share_text = (
            f"📝 Transcript & Summary\n\n---\n\n"
            f"📜 Transcript:\n{st.session_state.sum_transcript[:2000]}...\n\n"
            f"📌 Summary:\n{st.session_state.sum_summary}"
        )
        st.session_state["summary_output"] = share_text
