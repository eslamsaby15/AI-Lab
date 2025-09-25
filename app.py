import streamlit as st
from src.view import setup_page


# =====================
# Feature Pages
# =====================

if __name__ =="__main__" :
    setup_page()

    if "features" not in st.session_state:
        st.session_state["features"] = "🏡 Home"

    elif st.session_state["features"] == "🔊 Speaker Diarization":
        st.subheader("🔊 Speaker Diarization Page")
        st.write("Here goes diarization_ui.render()")
    
    elif st.session_state["features"] == "🎧 Podcast Generator":
        st.subheader("🎧 Podcast Generator Page")
        st.write("Here goes podcast_generator_ui.render()")

    elif st.session_state["features"] == "📽️ Video Script Generator":
        st.subheader("📽️ Video Script Generator Page")
        st.write("Here goes video_script_generator_ui.render()")
  
    elif st.session_state["features"] == "❓ Q&A":
        st.subheader("❓ Q&A Page")
        st.write("Here goes qa_ui.render()")

    elif st.session_state["features"] == "📝 Summarize":
        st.subheader("📝 Summarize Page")
        st.write("Here goes summarizer_ui.render()")

    elif st.session_state["features"] == "🌍 Translation":
        st.subheader("🌍 Translation Page")
        st.write("Here goes translation_ui.render()")

    elif st.session_state["features"] == "📊 Sentiment Analysis":
        st.subheader("📊 Sentiment Analysis Page")
        st.write("Here goes sentiment_ui.render()")
