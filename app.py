import streamlit as st
from src.pages import (setup_page ,summarizer_page ,Diarizationr_page ,VideoScriptGenerationPage , 
                       PodcastSriptPage ,Translation_page)


# =====================
# Feature Pages
# =====================

if __name__ =="__main__" :
    setup_page()

    
    if "features" not in st.session_state:
        st.session_state["features"] = "🏡 Home"
        
    elif st.session_state["features"] == "📽️ Video Script Generator":
        VideoScriptGenerationPage()
  
    elif st.session_state["features"] == "❓ Q&A":
        st.subheader("❓ Q&A Page")
        st.write("Here goes qa_ui.render()")

    elif st.session_state["features"] == "📝 Summarize":
        st.subheader("📝 Summarize")
        summarizer_page()

    elif st.session_state["features"] == "🎧 Podcast Generator":
        PodcastSriptPage()

    elif st.session_state["features"] == "🔊 Speaker Diarization":
        Diarizationr_page()
        
      
    elif st.session_state["features"] == "🌍 Translation":
        Translation_page()

    elif st.session_state["features"] == "📊 Sentiment Analysis":
        st.subheader("📊 Sentiment Analysis Page")
        st.write("Here goes sentiment_ui.render()")
