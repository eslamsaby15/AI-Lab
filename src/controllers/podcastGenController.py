from .BaseController import BaseController
import re
from .BaseController import BaseController
from ..Stores.LLM import GenAIProvider
from ..models.prompts import PodCastPromptEnum
import os
from gtts import gTTS


class PodcastGenController(BaseController): 
    def __init__(self, provider : GenAIProvider , lang: str = "en",  
                 topic : str = None  , style : str ='Simple & Clear', 
                  duration: int = 3)  : 
        super().__init__()
        
        self.lang = lang if lang != 'auto' else 'en'
        self.provider = provider
        self.video_topic = topic  
        self.style = style 
        self.duration  = duration
        self.prompt= None
        self.template= None
        self.temp_dir = os.path.join(self.base_dir, "assets/temp")


        if self.lang.lower().strip() == "ar":
            self.template = PodCastPromptEnum.AR.value
        else:
            self.template = PodCastPromptEnum.EN.value

        self.prompt= None


    def calculate_words(self, words_per_minute=130):
        total_words = self.duration * words_per_minute
        intro_words = int(total_words * 0.2)  
        conclusion_words = int(total_words * 0.2)  
        main_words = total_words - intro_words - conclusion_words 
        return total_words, intro_words, main_words, conclusion_words
    
    def GenerateScript(self, words_per_minute: int = 130):
        total_words, intro_words, main_words, conclusion_words = self.calculate_words(words_per_minute)

        self.prompt = self.template.format(
            topic=self.video_topic,
            style=self.style,
            total_minutes=self.duration,
            intro_words=intro_words,
            main_words=main_words,
            conclusion_words=conclusion_words
        )
        
        response = self.provider.generate_Chunks(self.prompt, temperature=.4) 
        
        json_output = self.script_to_json(response)
        return response, json_output
    

    def script_to_json(self, raw_script : str ) :
        cleaned_script = re.sub(r'\*\*|\*', '', raw_script)
        sections =[ ]
        current_section = None 

        lines = cleaned_script.split('\n')

        for line in lines : 
            line = line.strip()
            if not line :
                continue

            if line.startswith('[INTRO]') or line.startswith('[Q&A SESSION]') or line.startswith('[OUTRO]'):

                if current_section : 
                    sections.append(current_section)
                
                current_section = { 
                    "title" : line.strip("[]") , 
                    "parts" : []
                }

                continue

            if line.startswith('[host]:'): 
                if current_section :
                    current_section['parts'].append(
                        {
                        "type": "host",
                        "text": line.replace('[host]:', '').strip() } 
                    )

            elif  line.startswith("[speaker_a]:"): 
                if current_section : 
                    current_section['parts'].append(
                        {"type": "speaker_a",
                        "text": line.replace('[speaker_a]:', '').strip()}
                    )

            if current_section:
                sections.append(current_section)

        return {
            "topic": self.video_topic,
            "style": self.style,
            "duration": self.duration,
            "sections": sections
        }



    def script_to_audio(self, script_text: str, lang="en"):
            """Convert video script narration into one MP3 file."""
            os.makedirs(self.temp_dir, exist_ok=True)
            random_name = self.generate_random_string(8)
            filename = f"{self.temp_dir}/{random_name}_video_script.mp3"
            if lang =='ar' : 
                tts = gTTS(text=script_text, lang=lang)
            else : 
                tts = gTTS(text=script_text, lang=lang, tld="com")
            tts.save(filename)
            return filename