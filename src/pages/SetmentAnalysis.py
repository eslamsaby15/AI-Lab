from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
from ..tasks import SentimentAnalysisTask  

def SentimentAnalysis_page(): 
    st.subheader("📊 Sentiment Analysis")

    youtube_link = None 
    file_uploaded = None

    if "sum_transcript" not in st.session_state:
        st.session_state.sum_transcript = None

    if "sentiment_result" not in st.session_state:
        st.session_state.sentiment_result = None

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
            st.session_state.sum_transcript = transcription_result
            st.success("✅ Transcription done!")

        with st.spinner("📊 Analyzing Sentiment..."):
            task = SentimentAnalysisTask(provider_name=st.session_state["generation_provider"])
            st.session_state.sentiment_result = task.run(st.session_state.sum_transcript)
            st.success("✅ Sentiment analysis completed!")

        st.subheader("Sentiment Analysis Output")

        download_text = ""
        for i, chunk_result in enumerate(st.session_state.sentiment_result, 1):
            sentiment = chunk_result.get("sentiment", "N/A")
            key_points = chunk_result.get("key_points", "")

            download_text += f"Paragraph {i}\nSentiment: {sentiment}\nKey points: {key_points}\n\n"

            st.markdown(f"""
            <div style="
                background:#ffffff;
                border:1px solid #e0e0e0;
                padding:15px;
                border-radius:12px;
                margin:8px 0;
                box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
            ">
                <p style="margin:0; color:#333;"><b>Paragraph {i}</b></p>
                <p style="margin-top:5px; color:#555;"><b>Sentiment:</b> {sentiment}</p>
                <p style="margin-top:5px; color:#111;"><b>Key points:</b> {key_points}</p>
            </div>
            """, unsafe_allow_html=True)

        st.sidebar.subheader("📥 Download")
        st.sidebar.download_button(
            "Download Sentiment Analysis",
            download_text,
            file_name="sentiment_analysis.txt"
        )
