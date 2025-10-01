from ..Stores.LLM import LLMProviderFactory ,LLMEnums ,GenAIProvider
from ..helpers import APP_Setting
from ..controllers import TransaltionController


class TranslationTask:
    def __init__(self , mode: str = "llm" ,  provider_name: LLMEnums  = None):
        
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
                
        self.Translator= TransaltionController( 
                                    mode= self.mode , 
                                    provider= self.provider)
        

    def run(self , text : str ): 
        if self.mode =='classic':
            return self.Translator.classical_Translator(text=text)
        else:
            return self.Translator.LLM_Translation(text)

            


