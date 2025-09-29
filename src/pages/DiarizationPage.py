from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
from ..tasks import DiarizationTask
import json

def Diarizationr_page(): 
    st.subheader("🔊 Speaker Diarization")

    youtube_link = None 
    file_uploaded = None

    if "sum_transcript" not in st.session_state:
        st.session_state.sum_transcript = None

    if "diarization_result" not in st.session_state:
        st.session_state.diarization_result = None

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

    lang_choice = st.selectbox("🌐 Select language", ["auto", "en", "ar"], index=0)

    if st.button("🚀 Diarize"):
        if not youtube_link and not file_uploaded:
            st.warning("⚠️ Please enter a YouTube link or upload a file.")
            return 

        try:
            yt = Youtube()
            if youtube_link: 
                wav_file = yt.Download(youtube_link)
            else:
                wav_file = yt.save_dir(file_uploaded)

            with st.spinner("📝 Transcribing..."):
                transcriber = Wav2VecTranscriber()
                transcription_result = transcriber.transcribe(wav_file)
                st.session_state.sum_transcript = transcription_result
                st.success("✅ Transcription done!")

            with st.spinner("📌 Diarizating..."):
                task = DiarizationTask(provider_name=st.session_state["generation_provider"], lang=lang_choice)
                st.session_state.diarization_result = task.run(st.session_state.sum_transcript)
                st.success("✅ Diarization completed!")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return

    if st.session_state.sum_transcript:
        st.subheader("Transcript")
        st.text_area("Transcript", st.session_state.sum_transcript, height=200)

    if st.session_state.diarization_result and st.session_state.diarization_result.segments:
        segments = st.session_state.diarization_result.segments
        
        st.markdown("### 🎤 Conversation")

        if lang_choice == 'ar':
            speaker_map = {
                "A": "🧑 المتحدث 1 :",
                "B": "👩 المتحدث 2 :"
            }
        else:
            speaker_map = {
                "A": "🧑 Speaker 1 :",
                "B": "👩 Speaker 2 :"
            }

        for i, seg in enumerate(segments):
            speaker_label = speaker_map.get(seg.speaker, seg.speaker)
            text = seg.text
            bg = "#4678aa" if i % 2 == 0 else "#2A5E62"
            direction = "rtl" if lang_choice == 'ar' else 'ltr'
            
            st.markdown(f"""
            <div style="background:{bg};padding:10px;border-radius:10px;margin:5px 0;direction:{direction};color:white">
                <b>{speaker_label}</b> {text}
            </div>
            """, unsafe_allow_html=True)

        segments_data = [{"speaker": s.speaker, "text": s.text} for s in segments]
        diarized_json = json.dumps(segments_data, ensure_ascii=False, indent=2)
        
        st.download_button(
            "💾 Download JSON",
            data=diarized_json,
            file_name="diarization.json",
            mime="application/json"
        )
        
    elif st.session_state.diarization_result:
        st.info("No segments found in the diarization result.")
