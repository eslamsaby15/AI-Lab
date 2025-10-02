from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
from ..tasks import TopicTaggingTask  


def TopicTagging_page(): 
    st.subheader("🏷️ Topic Tagging")

    youtube_link = None 
    file_uploaded = None

    if "transcript" not in st.session_state:
        st.session_state.transcript = None

    if "tagging_result" not in st.session_state:
        st.session_state.tagging_result = None

    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"

    input_type = st.selectbox("Choose input type", ["Upload file", "YouTube link"])

    if input_type == "Upload file":
        file_uploaded = st.file_uploader(
            '📂 Upload audio/video', 
            type=[InputTypes.WAV.value, InputTypes.MKV.value, InputTypes.MP4.value, InputTypes.MP3.value]
        )
    elif input_type == "YouTube link":
        youtube_link = st.text_input('Paste YouTube link')

    if st.button("🚀 Process"):
        if not youtube_link and not file_uploaded:
            st.warning("⚠️ Please enter a YouTube link or upload a file.")
            return 

        try:
            yt = Youtube()
            if youtube_link: 
                wav_file = yt.Download(youtube_link)
            else:
                wav_file = yt.save_dir(file_uploaded)
        except Exception as e:
            st.error(f"❌ Error downloading file: {str(e)}")
            return 

        with st.spinner("📝 Transcribing..."):
            transcriber = Wav2VecTranscriber()
            transcription_result = transcriber.transcribe(wav_file)
            st.session_state.transcript = transcription_result
            st.success("✅ Transcription done!")

        with st.spinner("🏷️ Extracting Topics..."):
            task = TopicTaggingTask(provider_name=st.session_state["generation_provider"])
            st.session_state.tagging_result = task.run(st.session_state.transcript)
            st.success("✅ Topic tagging completed!")

        st.subheader("Topic Tags Output")

        download_text = "Topic Tags:\n\n"
        for i, tag in enumerate(st.session_state.tagging_result, 1):
            download_text += f"{i}. {tag}\n"
            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid #e0e0e0;
                padding:12px;
                border-radius:12px;
                margin:6px 0;
                box-shadow: 0px 1px 4px rgba(0,0,0,0.05);
            ">
                <p style="margin:0; color:#333;"><b>Tag {i}:</b> {tag}</p>
            </div>
            """, unsafe_allow_html=True)

        st.sidebar.subheader("📥 Download")
        st.sidebar.download_button(
            "Download Topic Tags",
            download_text,
            file_name="topic_tags.txt"
        )
