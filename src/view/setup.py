import streamlit as st

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

    if "features" not in st.session_state:
        st.session_state["features"] = "🏡 Home"

    # Sidebar tasks
    sidebar_tasks = [
        {"icon": "🏡", "name": "Home"},
        {"icon": "📝", "name": "Summarize"},
        {"icon": "🌍", "name": "Translation"},
        {"icon": "📊", "name": "Sentiment Analysis"},
        {"icon": "🎧", "name": "Podcast Generator"},
        {"icon": "📽️", "name": "Video Script Generator"},
        {"icon": "❓", "name": "Q&A"},
        {"icon": "🔊", "name": "Speaker Diarization"},
    ]

    # Sidebar navigation
    feature_names = [f"{f['icon']} {f['name']}" for f in sidebar_tasks]
    selected_feature = st.sidebar.selectbox(
        "Select Task", 
        feature_names, 
        index=feature_names.index(st.session_state["features"])
    )
    st.session_state["features"] = selected_feature

    openrouter_model = st.sidebar.selectbox(
        "🧠 Choose OpenRouter model",
        [
            "mistralai/mistral-7b-instruct",
            "meta-llama/llama-3-8b-instruct",
            "qwen/qwen3-next-80b-a3b-instruct",
            "openai/gpt-4-0314"
        ],
        index=0
    )
    st.session_state["openrouter_model"] = openrouter_model


    # Sidebar footer
    with st.sidebar:
        st.markdown("---")
        st.markdown("## 👨‍💻 Built by Eslam Sabry")
        st.markdown("🔗 [LinkedIn](https://www.linkedin.com/in/eslamsabryai)")
        st.markdown("🔗 [Kaggle](https://www.kaggle.com/eslamsabryelsisi)")
        st.markdown("---")

    # Main page content
    if st.session_state["features"] == "🏡 Home":
        st.title("Welcome to AI-Lab Hub 🤖")
        st.image("src/assets/images/b1.png", use_container_width=True)
        
        # Feature buttons grid
        st.markdown("##Select  a Task :")
        cols = st.columns(3)
        for i, task in enumerate(sidebar_tasks):
            with cols[i % 3]:
                if st.button(f"{task['icon']} {task['name']}", key=f"home_{task['name']}", use_container_width=True):
                    st.session_state["features"] = f"{task['icon']} {task['name']}"
                    st.rerun()
