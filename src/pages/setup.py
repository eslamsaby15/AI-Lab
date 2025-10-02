import streamlit as st
from ..helpers.config import APP_Setting


def setup_page():
    # Page Config
    st.set_page_config(
        page_title="AI-Lab 📃",
        layout="wide",
        page_icon="🤖"
    )
    
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem; max-width: 1100px;}
        .stMetric .stMetricDelta {direction:ltr}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Defaults
    if "features" not in st.session_state:
        st.session_state["features"] = "🏡 Home"

    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"

    if "embedding_provider" not in st.session_state:
        st.session_state["embedding_provider"] = "Cohere"

    # Sidebar tasks
    sidebar_tasks = [
    {"icon": "🏡", "name": "Home"},
    {"icon": "📝", "name": "Summarize"},
    {"icon": "🌍", "name": "Translation"},
    {"icon": "📊", "name": "Sentiment Analysis"},
    {"icon": "🎧", "name": "Podcast Generator"},
    {"icon": "📽️", "name": "Video Script Generator"},
    {"icon": "❓", "name": "Interactive Voice Quiz"},
    {"icon": "🔊", "name": "Speaker Diarization"},
    {"icon": "🏷️", "name": "Topic Tagging"},
    {"icon": "🧩", "name": "Multi Quiz"} ]

    # Sidebar navigation
    feature_names = [f"{f['icon']} {f['name']}" for f in sidebar_tasks]
    selected_feature = st.sidebar.selectbox(
        "Select Task", 
        feature_names, 
        index=feature_names.index(st.session_state["features"])
    )
    st.session_state["features"] = selected_feature

    # Sidebar provider selection
    st.sidebar.markdown("### ⚙️ Providers Setup")
    st.session_state["generation_provider"] = st.sidebar.selectbox(
        "Select Generation Provider",
        ["OpenAI", "Gemini", "Cohere"],
        index=["OpenAI", "Gemini", "Cohere"].index(st.session_state["generation_provider"])
    )

    st.session_state["embedding_provider"] = st.sidebar.selectbox(
        "Select Embedding Provider",
        ["Cohere", "OpenAI", "Gemini", "sentence-transformers/all-MiniLM-L6-v2"],
        index=["Cohere", "OpenAI", "Gemini" , 
               "sentence-transformers/all-MiniLM-L6-v2" ].index(st.session_state["embedding_provider"])
    )

    with st.sidebar:
        st.markdown("---")
        st.markdown("## 👨‍💻 Built by :")
        st.markdown("**Eslam Sabry** \n\n _ML Engineer_")
        st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/eslamsabryai) 🔗 [Kaggle](https://www.kaggle.com/eslamsabryelsisi)")
        st.markdown("---")


    # Main page content
    if st.session_state["features"] == "🏡 Home":
        st.title("Welcome to AI-Lab Hub 🤖")
        st.image("src/assets/images/b1.png", use_container_width=True)
        
        # Feature buttons grid
        st.markdown("Select  a Task :")
        cols = st.columns(3)
        for i, task in enumerate(sidebar_tasks):
            with cols[i % 3]:
                if st.button(f"{task['icon']} {task['name']}", key=f"home_{task['name']}", use_container_width=True):
                    st.session_state["features"] = f"{task['icon']} {task['name']}"
                    st.rerun()
