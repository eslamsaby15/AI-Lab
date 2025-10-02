import streamlit as st
from src.pages import (setup_page ,summarizer_page ,Diarizationr_page ,VideoScriptGenerationPage , 
                       PodcastSriptPage ,Translation_page ,QA_Page , SentimentAnalysis_page , TopicTagging_page , MiniQuiz_page)


# =====================
# Feature Pages
# =====================

if __name__ =="__main__" :
    setup_page()

    if "features" not in st.session_state:
        st.session_state["features"] = "🏡 Home"
        
    elif st.session_state["features"] == "📽️ Video Script Generator":
        VideoScriptGenerationPage()

    elif st.session_state["features"] == "🧩 Multi Quiz":
        MiniQuiz_page()

    elif st.session_state["features"] == "❓ Interactive Voice Quiz":
        QA_Page()
        
    elif st.session_state["features"] == "📝 Summarize":
        summarizer_page()

    elif st.session_state["features"] == "🎧 Podcast Generator":
        PodcastSriptPage()
        
    elif st.session_state["features"] == "🔊 Speaker Diarization":
        Diarizationr_page()    

    elif st.session_state["features"] == "🌍 Translation":
        Translation_page()

    elif st.session_state["features"] == "📊 Sentiment Analysis":
        SentimentAnalysis_page()

    elif st.session_state["features"] == "🏷️ Topic Tagging":
        TopicTagging_page()


        