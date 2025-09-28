import streamlit as st
import os
from src.controllers import Youtube

st.title("🎧 Download Audio as WAV")

url_input = st.text_input("Paste YouTube or podcast/audio link here:")

if st.button("Download and Convert"):
    if url_input:
        with st.spinner("Downloading and converting..."):
            try:
                wav_file = Youtube().Download(url_input)
                st.success("✅ Done!")
                st.audio(wav_file)
                file_name = os.path.basename(wav_file)
                st.download_button("Download WAV", wav_file, file_name=file_name)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL.")
