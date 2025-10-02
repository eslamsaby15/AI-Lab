from ..helpers.config import APP_Setting
from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
from ..tasks import QATask

def QA_Page(): 
    youtube_link = None 
    file_uploaded = None
    st.subheader("❓ Interactive Voice Quiz ")

    if "sum_transcript" not in st.session_state:
        st.session_state.sum_transcript = None
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    if "qa_task" not in st.session_state:
        st.session_state.qa_task = None
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

    question_input = st.text_input("🔍 Enter your question")

    if st.button("🚀 Get Answer"):
        if not youtube_link and not file_uploaded:
            st.warning("⚠️ Please enter a YouTube link or upload a file.")
            return 
        if not question_input:
            st.warning("⚠️ Please enter a question.")
            return 

        status_placeholder = st.empty()
        status_placeholder.info("⏳ Processing... Please wait")

        if st.session_state.sum_transcript is None:
            yt = Youtube()
            if youtube_link: 
                wav_file = yt.Download(youtube_link)
            else:
                wav_file = yt.save_dir(file_uploaded)
            transcriber = Wav2VecTranscriber()
            st.session_state.sum_transcript = transcriber.transcribe(wav_file)

        if st.session_state.qa_task is None:
            st.session_state.qa_task = QATask(
                text=st.session_state.sum_transcript,
                provider_name=st.session_state["generation_provider"], 
                emebdding_vector=st.session_state["embedding_provider"]
            )

        answer = st.session_state.qa_task.run(question_input)
        st.session_state.qa_history.append({"q": question_input, "a": answer})

        status_placeholder.success("✅ Answer generated!")

        st.markdown("### 📝 Conversation so far")
        for i, qa_pair in enumerate(st.session_state.qa_history, 1):
            q, a = qa_pair["q"], qa_pair["a"]
            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid #e0e0e0;
                padding:15px;
                border-radius:12px;
                margin:8px 0;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
            ">
                <p style="margin:0; color:#333;"><b>Question {i}:</b> {q}</p>
                <p style="margin-top:10px; color:#111;"><b>Answer {i}:</b> {a}</p>
            </div>
            """, unsafe_allow_html=True)
