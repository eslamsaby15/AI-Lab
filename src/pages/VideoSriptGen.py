from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
import json
from ..tasks import VideoSriptGenTask

def VideoScriptGenerationPage():
    st.subheader("📽️ Video Script Generator")

    task = None
    if "video_script" not in st.session_state:
        st.session_state.video_script = None

    if "video_json" not in st.session_state:
        st.session_state.video_json = None

    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None

    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"

    video_topic = st.text_input("Enter a video topic")
    style = st.selectbox("Choose style", [
        "Simple & Clear", "Educational", 
        "Motivational", "Storytelling", 
        "Conversational", "Beginner Friendly",  
        "Professional", "Engaging & Fun"
    ] , index = 0 ) 
    
    lang_choice = st.selectbox("🌐 Select language", ["auto", "en", "ar"], index=0)
    duration = st.number_input("⏱️ Expected duration (minutes)", min_value=1, max_value=10, value=5)

    if st.button("🚀 Generate Video Script"):
        if not video_topic.strip():
            st.warning("⚠️ Please enter a topic.")
            return

        task = VideoSriptGenTask(
            provider_name=st.session_state["generation_provider"], 
            lang=lang_choice, 
            style=style, 
            video_topic=video_topic, 
            duration=duration
        )
        
        with st.spinner("📝 Generating structured video script..."):
            response, script_json = task.run(words_per_minute=200)
            st.session_state.video_script = response
            st.session_state.video_json = script_json
            st.session_state.audio_file = None

        st.success("✅ Video script generated!")

    if st.session_state.video_json:
        res = st.session_state.video_json
        
        st.markdown(f"# 🎬 {res['title']}")
        st.markdown(f"**Style:** {res['style']}  |  **Duration:** {res['duration_minutes']} min")
        st.markdown("---")
        
        st.markdown("## 📝 Introduction")
        st.text_area("Introduction Text", res['sections']['intro'], height=100, key="intro_area")
        st.markdown("---")
        
        st.markdown("## 📖 Body") 
        st.text_area("Body Text", res['sections']['body'], height=300, key="body_area")
        st.markdown("---")
        
        st.markdown("## 🎯 Conclusion")
        st.text_area("Conclusion Text", res['sections']['conclusion'], height=100, key="conclusion_area")
        st.markdown("---")

        if st.button("🎧 Convert to Audio"):
            task = VideoSriptGenTask(
                provider_name=st.session_state["generation_provider"], 
                lang=lang_choice, 
                style=style, 
                video_topic=video_topic, 
                duration=duration
            )
            with st.spinner("🔊 Converting to audio..."):
                audio_path = task.Convert(script_text=res['narration'] ,lang = lang_choice)
                st.session_state.audio_file = audio_path
            st.success("✅ Audio generated!")

        if st.session_state.audio_file:
            st.audio(st.session_state.audio_file, format="audio/mp3")
        
        with st.sidebar:
            st.markdown("## 📂 Export Options")
            st.download_button(
                label="📄 Download Script", 
                data=res['narration'],
                file_name="video_script.txt",
                mime="text/plain"
            )
