from ..Stores.LLM import LLMProviderFactory ,LLMEnums ,GenAIProvider
from ..helpers import APP_Setting
from ..controllers import Summarizer


class SummarizerTask:
    def __init__(self , lang: str = "en", mode: str = "llm" ,  provider_name: LLMEnums  = None):
        
        self.lang = lang if lang != 'auto' else 'en'
        self.mode = mode
        self.config= APP_Setting()

        self.provider : GenAIProvider =None
        if self.mode == 'llm' : 
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
                
        self.summarizer= Summarizer(lang= self.lang , 
                                    mode= self.mode , 
                                    provider= self.provider)
        

    def run(self , text : str ): 
        if self.mode =='classic':
            return self.summarizer.classical_Summarizer(text=text)
        else:
            return self.summarizer.LLM_Summarizer(text)

            


