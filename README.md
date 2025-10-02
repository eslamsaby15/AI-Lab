# 🎙️ AIVox Lab

A simple **AI-Powered Voice & Text Processing Lab** built with **Streamlit**.  
It provides multiple tools for working with **speech, text, and audio intelligence**, all in one place.  

![AIVox Workflow](/src/assets/images/b1.png)

This app is built using [**Streamlit**](https://streamlit.io/) and state-of-the-art **AI models** for speech and text.

------
## 🚀 AIVox Features 

- **Summarization** → Summarize long texts or transcripts into concise insights.  
- **Translation** → Translate text between different languages.  
- **Sentiment Analysis** → Detect emotions and polarity (positive, negative, neutral).  
- **Podcast Generator** → Generate podcast-style audio from written text.  
- **Video Script Generator** → Automatically generate scripts for videos.  
- **Interactive Voice Quiz** → Voice-based quiz system for interactive learning.  
- **Multi Quiz** → Generate and play multi-question quizzes with AI.  
- **Speaker Diarization** → Detect and separate different speakers in an audio file.  
- **Topic Tagging** → Tag texts or transcripts with relevant topics.  

------
## 🔹 Workflow

### 1. Input Processing 🎤
- Accept audio, text, or transcripts.  
- Normalize and clean the input.  

### 2. Model Processing ⚙️
- Pass input through summarization, translation, or classification models.  
- For audio, run diarization or topic tagging modules.  

### 3. Output Generation ✨
- Generate text summaries, translations, or structured analysis.  
- Produce podcasts or scripts with natural-sounding narration.  

### 4. User Interaction 🖥️
- Display results in a **Streamlit interface** with download support.  
- Allow quizzes and interactive Q&A with AI.  


------
## 📂 AIVox Lab - Structure

```bash
│   app.py
│   LICENCE
│   README.md
│
\---src
    │   requirements.txt
    │
    +---controllers
    │   │   BaseController.py
    │   │   DiarizationController.py
    │   │   GenQuestionController.py
    │   │   podcastGenController.py
    │   │   ProjectController.py
    │   │   QaController.py
    │   │   sentimentanalysisController.py
    │   │   SummarizeController.py
    │   │   TopicTaggingcontroller.py
    │   │   TranslationController.py
    │   │   VideoScrpitController.py
    │   │   Wav2vecTranscriber.py
    │   │   Youtube.py
    │
    +---helpers
    │   │   config.py
    │
    +---models
    │   +---ENUMS
    │   │   diarizationenum.py
    │   │   InputENUm.py
    │   │   SementModels.py
    │   │
    │   +---prompts
    │   │   PodcatPrompt.py
    │   │   VideoGenPrompts.py
    │
    +---pages
    │   DiarizationPage.py
    │   miniQuiz_page.py
    │   PodcastGenPage.py
    │   QApage.py
    │   SetmentAnalysis.py
    │   setup.py
    │   summarizer.py
    │   topic_page.py
    │   TranslationPage.py
    │   VideoSriptGen.py
    │
    +---Stores
    │   +---LLM
    │   │   LLMFactory.py
    │   │   llminterface.py
    │   │
    │   │   +---LLMEnums
    │   │   │   llmenums.py
    │   │
    │   │   +---Providers
    │   │   │   cohereProvider.py
    │   │   │   geminiProvider.py
    │   │   │   openAiProvider.py
    │
    +---tasks
    │   Diarizationtask.py
    │   MultiQuestionGenTask.py
    │   PodcastGenTask.py
    │   QAtask.py
    │   sentimentanalysisTask.py
    │   Summarizer.py
    │   TopicTagging.py
    │   Translationtask.py
    │   VideoGenTask.py

```

------
## 📦 Installation

### Requirements
- Python 3.11  

### Install Python using MiniConda

1) Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)  

2) Create a new environment:
```bash
conda create -n aivox python=3.11
```

3) Activate the environment:
```bash
$ conda activate aivox
```

4) Install the required packages:
```bash
$ pip install -r requirements.txt
```

5) Setup the environment variables:
```bash
$ cp .env.example .env
```

6) Run streamlit app:
```bash
$ streamlit run app.py
```
---------
## 🔹 Conclusion  

**AIVox Lab** 

AIVox Lab unifies multiple speech and text AI tasks in a single app.  
You can summarize long texts or transcripts, translate between languages, analyze sentiment, generate podcasts and video scripts, run interactive quizzes, and perform speaker diarization and topic tagging—all within a simple, user-friendly interface.


Built with **Streamlit** for an interactive and user-friendly interface.  

---------
## 👨‍💻 Built by Eslam Sabry

concat  
🔗 [LinkedIn](https://www.linkedin.com/in/eslamsabryai)  
🔗 [Kaggle](https://www.kaggle.com/eslamsabryelsisi)  
