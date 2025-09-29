from ..Stores.LLM import LLMProviderFactory, LLMEnums, GenAIProvider
from ..helpers import APP_Setting
from ..controllers import Diarization


class DiarizationTask:
    def __init__(self, lang: str = "en", provider_name: LLMEnums = None, chunk_size: int = 3000):

        self.lang = lang if lang != 'auto' else 'en'
        self.chunk_size = chunk_size
        self.config= APP_Setting()

        self.provider : GenAIProvider =None
         
        factory = LLMProviderFactory(self.config) 

        if provider_name is None : 
            default_provider = self.config.GENERATION_BACKEND_GEMINI
            provider_name = LLMEnums[default_provider]

        self.provider = factory.create(provider_name)

        if provider_name == LLMEnums.GEMINI.value:
            self.provider.set_generation_model(model_id = self.config.GENERATION_MODEL_ID_GEMINI)
        elif provider_name == LLMEnums.OPENAI.value:
            self.provider.set_generation_model(model_id = self.config.GENERATION_MODEL_ID_OPENAI)

        else : 
            print(provider_name)
                

        self.diarization = Diarization(
            lang=self.lang,
            provider=self.provider,
            chunk_size=self.chunk_size
        )

    def run(self, transcript: str):
        return self.diarization.run_diarization(transcript)
