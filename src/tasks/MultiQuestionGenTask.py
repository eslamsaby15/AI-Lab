
from ..Stores.LLM import LLMProviderFactory, LLMEnums
from ..helpers import APP_Setting
from ..controllers import MiniQuizController

class MiniQuizTask:
    def __init__(self, provider_name: LLMEnums = None, num_questions: int = 10):
        config = APP_Setting()
        factory = LLMProviderFactory(config)

        if provider_name is None:
            default_provider = config.GENERATION_BACKEND_GEMINI
            provider_name = LLMEnums[default_provider]

        self.provider = factory.create(provider_name)

        if provider_name == LLMEnums.GEMINI.value:
            self.provider.set_generation_model(model_id=config.GENERATION_MODEL_ID_GEMINI)

        elif provider_name == LLMEnums.OPENAI.value:
            self.provider.set_generation_model(model_id=config.GENERATION_MODEL_ID_OPENAI)

        elif provider_name == LLMEnums.COHERE.value:
            self.provider.set_generation_model(model_id=config.GENERATION_MODEL_ID_COHERE_LIGHT)

        self.quiz_controller = MiniQuizController(provider=self.provider, num_questions=num_questions)

    def run(self, transcript: str):
        return self.quiz_controller.generate_quiz(transcript)
