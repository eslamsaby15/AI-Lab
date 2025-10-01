from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
import json
from ..tasks import PoadcastGenTask

def PodcastSriptPage():
    st.subheader("🎧 Podcast Generator")

    if "podcast_data" not in st.session_state:
        st.session_state.podcast_data = None
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None
    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"

    poadcast_topic = st.text_input("Enter a topic")
    style = st.selectbox("Choose style", [
        "Conversational","Storytelling", "Interview", 
        "Motivational", "Analytical", "Casual & Fun"
    ], index=5)
    lang_choice = st.selectbox("🌐 Select language", ["auto", "en", "ar"], index=0)
    duration = st.number_input("⏱️ Expected duration (minutes)", min_value=1, max_value=15, value=5)

    if st.button("🚀 Generate podcast Script"):
        if not poadcast_topic.strip():
            st.warning("⚠️ Please enter a topic.")
            return
        
        task = PoadcastGenTask(
            provider_name=st.session_state["generation_provider"], 
            lang=lang_choice, 
            style=style, 
            topic=poadcast_topic, 
            duration=duration
        )
        
        with st.spinner("📝 Generating Podcast script..."):
            response, script_json = task.run(words_per_minute=200)
            st.session_state.podcast_data = {
                "script": response,
                "json": script_json,
                "topic": poadcast_topic,
                "style": style,
                "duration": duration
            }
            st.session_state.audio_file = None

        st.success("✅ Podcast script generated!")

    if st.session_state.podcast_data:
        podcast_data = st.session_state.podcast_data
        
        st.markdown("---")
        st.markdown("## 🎤 Podcast Conversation")
        
        if lang_choice == 'ar' :
            host_label = "🎤 المضيف"
            speaker_label = "👤 المتحدث"
        else:
            host_label = "🎤 Host"
            speaker_label = "👤 Speaker"
        
        # Display each section only once
        json_data = podcast_data['json']
        if 'sections' in json_data:
            seen_sections = set()
            for section in json_data['sections']:
                if section['title'] in seen_sections:
                    continue
                seen_sections.add(section['title'])

                st.markdown(f"### 🎯 {section['title']}")
                
                for part in section['parts']:
                    if part['type'] == 'host':
                        bg_color = "#4678aa"
                        label = host_label
                    else:
                        bg_color = "#2A5E62"
                        label = speaker_label
                    
                    direction = "rtl" if (lang_choice == 'ar' or 
                                          (lang_choice == 'auto' and any(char in part['text'] for char in 'اأإآ'))) else "ltr"
                    
                    st.markdown(f"""
                    <div style="background:{bg_color}; padding:15px; border-radius:10px; margin:10px 0; 
                                direction:{direction}; color:white; text-align:{'right' if direction == 'rtl' else 'left'};">
                        <b>{label}:</b> {part['text']}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 🎵 Audio Generation")
        
        if st.button("🎧 Convert to Audio"):
            task = PoadcastGenTask(
                provider_name=st.session_state["generation_provider"], 
                lang=lang_choice, 
                style=podcast_data['style'], 
                topic=podcast_data['topic'], 
                duration=podcast_data['duration']
            )
            with st.spinner("🔊 Converting to audio..."):
                audio_path = task.Convert(script_text=podcast_data['script'] , lang=lang_choice)
                st.session_state.audio_file = audio_path
            st.success("✅ Audio generated!")

        if st.session_state.audio_file:
            st.audio(st.session_state.audio_file, format="audio/mp3")
            st.download_button(
                "📥 Download Audio",
                data=st.session_state.audio_file,
                file_name="podcast_audio.mp3",
                mime="audio/mp3"
            )

        # Sidebar for downloads only
        with st.sidebar:
            st.markdown("## 📂 Export Options")
            
            if 'json' in podcast_data:
                podcast_json_str = json.dumps(podcast_data['json'], ensure_ascii=False, indent=2)
                st.download_button(
                    "💾 Download JSON",
                    data=podcast_json_str,
                    file_name="podcast_script.json",
                    mime="application/json"
                )
            
            st.download_button(
                "📄 Download Text Script",
                data=podcast_data['script'],
                file_name="podcast_script.txt",
                mime="text/plain"
            )
