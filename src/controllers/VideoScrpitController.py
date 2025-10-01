from .BaseController import BaseController
import re
from langchain.prompts import ChatPromptTemplate
from .BaseController import BaseController
from ..Stores.LLM import GenAIProvider
from ..models.prompts import VideoScriptTemplate
import os
from gtts import gTTS


class VideoSriptGenController(BaseController): 
    def __init__(self, provider : GenAIProvider , lang: str = "en",  
                 video_topic : str = None  , style : str ='Simple & Clear', 
                  duration: int = 3)  : 
        super().__init__()
        
        self.lang = lang if lang != 'auto' else 'en'
        self.provider = provider
        self.video_topic = video_topic 
        self.style = style 
        self.duration  = duration
        self.prompt= None
        self.template= None
        self.temp_dir = os.path.join(self.base_dir, "assets/temp")


        if self.lang.lower().strip() == "ar":
            self.template = VideoScriptTemplate.AR.value
        else:
            self.template = VideoScriptTemplate.EN.value

        self.prompt= None


    def script_to_json(self , raw_script: str) -> dict:
        sections = []
        current_section = None
        script_text = ""
        script_chunks = []

        cleaned_script = re.sub(r'\*\*|\*', '', raw_script)
        
        lines = cleaned_script.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith('---'):
                continue
                
            if line.startswith('[INTRO]') or line.startswith('[MAIN]') or line.startswith('[CONCLUSION]'):
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "title": line.strip('[]'),
                    "parts": []
                }
                continue
                
            if line.startswith('NARRATOR:'):
                narrator_text = line.replace('NARRATOR:', '').strip()
                if current_section:
                    current_section["parts"].append({
                        "type": "narrator",
                        "text": narrator_text
                    })
                script_text += narrator_text + "\n\n"
                script_chunks.append(narrator_text)
                    
            elif line.startswith('VISUALS:'):
                if current_section:
                    current_section["parts"].append({
                        "type": "visuals",
                        "text": line.replace('VISUALS:', '').strip()
                    })
                    
            elif line.startswith('TEXT:'):
                if current_section:
                    current_section["parts"].append({
                        "type": "text", 
                        "text": line.replace('TEXT:', '').strip()
                    })
        
        if current_section:
            sections.append(current_section)
        
        intro_text = ""
        body_text = ""
        conclusion_text = ""
        
        for section in sections:
            if section["title"] == "INTRO":
                for part in section["parts"]:
                    if part["type"] == "narrator":
                        intro_text += part["text"] + "\n\n"

            elif section["title"] == "MAIN":
                for part in section["parts"]:
                    if part["type"] == "narrator":
                        body_text += part["text"] + "\n\n"

                        
            elif section["title"] == "CONCLUSION":
                for part in section["parts"]:
                    if part["type"] == "narrator":
                        conclusion_text += part["text"] + "\n\n"
        
        script_json = {
            "title": self.video_topic,
            "style": self.style,
            "duration_minutes": self.duration,
            "sections": {
                "intro": intro_text.strip(),
                "body": body_text.strip(),
                "conclusion": conclusion_text.strip()
            },
            "narration": script_text.strip(),
            "chunks": script_chunks
        }
        
        return script_json


    def calculate_words(self, words_per_minute : int =200):
        total_words = self.duration * words_per_minute
        intro_words = int(total_words * 0.2)  
        conclusion_words = int(total_words * 0.2)  
        main_words = total_words - intro_words - conclusion_words 
        
        return total_words, intro_words, main_words, conclusion_words
    

    def GenerateScript(self, words_per_minute: int = 200):
        total_words, intro_words, main_words, conclusion_words = self.calculate_words(words_per_minute)

        self.prompt = self.template.format(
            topic=self.video_topic,
            style=self.style,
            total_minutes=self.duration,
            intro_words=intro_words,
            main_words=main_words,
            conclusion_words=conclusion_words
        )
        
        response = self.provider.generate_Chunks(self.prompt, temperature=.5) 
        
        json_output = self.script_to_json(response)
        return response, json_output
    

    def video_to_audio(self, script_text: str, lang="en"):
        """Convert video script narration into one MP3 file."""
        os.makedirs(self.temp_dir, exist_ok=True)
        random_name = self.generate_random_string(8)
        filename = f"{self.temp_dir}/{random_name}_video_script.mp3"
        if lang == 'ar' : 
            tts = gTTS(text=script_text, lang=lang)
        else : 
            tts = gTTS(text=script_text, lang=lang, tld="com")
        tts.save(filename)
        return filename
    

