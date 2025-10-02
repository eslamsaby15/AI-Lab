from ..models.ENUMS.InputENUm import InputTypes
import streamlit as st
from ..controllers import Youtube, Wav2VecTranscriber
from ..tasks import MiniQuizTask

def MiniQuiz_page():
    st.subheader("🎯 Mini Quiz - Custom Number of Questions")

    if "transcript" not in st.session_state:
        st.session_state.transcript = None
    if "quiz_result" not in st.session_state:
        st.session_state.quiz_result = None
    if "generation_provider" not in st.session_state:
        st.session_state["generation_provider"] = "Gemini"
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "show_answers" not in st.session_state:
        st.session_state.show_answers = False

    st.subheader("Quiz Settings")

    input_type = st.selectbox("Choose input type", ["Upload file", "YouTube link"])
    youtube_link = None
    file_uploaded = None

    if input_type == "Upload file":
        file_uploaded = st.file_uploader(
            '📂 Upload audio/video',
            type=[InputTypes.WAV.value, InputTypes.MKV.value, InputTypes.MP4.value, InputTypes.MP3.value]
        )
    else:
        youtube_link = st.text_input('Paste YouTube link')

    num_questions = st.number_input("Enter number of questions", min_value=1, max_value=20, value=10, step=1)
    show_questions = st.checkbox("Show Questions", value=True)

    if st.button("🚀 Generate Quiz"):
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
            st.session_state.transcript = transcriber.transcribe(wav_file)
            st.success("✅ Transcription done!")

        with st.spinner("🎯 Generating Quiz..."):
            task = MiniQuizTask(provider_name=st.session_state["generation_provider"], num_questions=num_questions)
            st.session_state.quiz_result = task.run(st.session_state.transcript)
            st.session_state.user_answers = {}
            st.session_state.show_answers = False
            st.success("✅ Quiz generated!")

    if st.session_state.quiz_result and show_questions:
        st.subheader("Quiz")
        
        for idx, q in enumerate(st.session_state.quiz_result, 1):
            st.markdown(f"**Question {idx}:** {q['question']}")
            unique_key = f"quiz_q_{idx}"
            if idx not in st.session_state.user_answers:
                st.session_state.user_answers[idx] = None

            choice = st.radio(
                f"Select an answer for Question {idx}",
                q['options'],
                key=unique_key
            )
            st.session_state.user_answers[idx] = choice
            st.markdown("---")

        if st.button("📊 Submit Answers"):
            st.session_state.show_answers = True
            score = 0
            for idx, q in enumerate(st.session_state.quiz_result, 1):
                correct_answer_index = ord(q['answer']) - ord('A')
                correct_answer_text = q['options'][correct_answer_index]
                selected = st.session_state.user_answers.get(idx)
                if selected == correct_answer_text:
                    score += 1
            st.success(f"🎉 Your Score: {score} / {len(st.session_state.quiz_result)}")

        if st.session_state.show_answers:
            for idx, q in enumerate(st.session_state.quiz_result, 1):
                correct_answer_index = ord(q['answer']) - ord('A')
                correct_answer_text = q['options'][correct_answer_index]
                selected = st.session_state.user_answers.get(idx)
                if selected == correct_answer_text:
                    st.success(f"✅ Question {idx}: Correct! Your answer: {selected}")
                else:
                    st.error(f"❌ Question {idx}: Wrong! Your answer: {selected} | Correct: {correct_answer_text}")

        # Download
        download_text = "\n\n".join(
            [f"Q{idx}: {q['question']}\nOptions:\nA) {q['options'][1]}\nB) {q['options'][1]}\nC) {q['options'][2]}\nAnswer: {q['answer']}) {q['options'][ord(q['answer']) - ord('A')]}"
             for idx, q in enumerate(st.session_state.quiz_result, 1)]
        )
        st.sidebar.subheader("📥 Download Quiz")
        st.sidebar.download_button(
            "Download Quiz",
            download_text,
            file_name="quiz.txt"
        )
