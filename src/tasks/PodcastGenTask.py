from ..Stores.LLM import LLMProviderFactory, LLMEnums, GenAIProvider
from ..helpers import APP_Setting
from ..controllers import PodcastGenController



class PoadcastGenTask:
    def __init__(self, lang: str = "en", provider_name: LLMEnums = None, 
                 topic : str = None  , style : str ='Casual & Fu', 
                  duration: int = 3):

        self.lang = lang if lang != 'auto' else 'en'
        self.duration = duration
        self.style = style
        self.topic = topic
        self.config= APP_Setting()
        self.provider : GenAIProvider =None
        self.duration = duration
         
        factory = LLMProviderFactory(self.config) 

        if provider_name is None : 
            default_provider = self.config.GENERATION_BACKEND_GEMINI
            provider_name = LLMEnums[default_provider]

        self.provider = factory.create(provider_name)

        if provider_name == LLMEnums.GEMINI.value:
            self.provider.set_generation_model(model_id = self.config.GENERATION_MODEL_ID_GEMINI)
        elif provider_name == LLMEnums.OPENAI.value:
            self.provider.set_generation_model(model_id = self.config.GENERATION_MODEL_ID_OPENAI)
        elif provider_name == LLMEnums.COHERE.value:
            self.provider.set_generation_model(model_id = self.config.GENERATION_MODEL_ID_COHERE_LIGHT)
        else : 
            print(provider_name)

        self.podGen = PodcastGenController(
            lang=self.lang , 
            topic=self.topic , 
            style=self.style , 
            provider= self.provider , 
            duration= self.duration
        )

    def run(self, words_per_minute : int = 100 ):
        return self.podGen.GenerateScript( words_per_minute )

    def Convert(self , script_text : str ,lang= "en" ) :
        return self.podGen.script_to_audio(script_text=script_text ,lang=lang) 
    
    