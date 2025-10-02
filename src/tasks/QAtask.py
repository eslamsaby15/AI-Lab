from ..Stores.LLM import LLMProviderFactory, LLMEnums, GenAIProvider, CohereProvider, OpenAiProvider
from ..helpers import APP_Setting
from langchain.embeddings import HuggingFaceEmbeddings
from ..controllers import QAController


class ProviderEmbeddingsWrapper:
    def __init__(self, provider):
        self.provider = provider

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self.provider.embedd_text(t, document_type='document') for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self.provider.embedd_text(text, document_type='query')


class QATask:
    def __init__(self, text: str, provider_name: LLMEnums = None, embedding_vector: LLMEnums = None):
        self.text = text

        self.config = APP_Setting()

        self.provider = None

        factory = LLMProviderFactory(self.config)

        if provider_name is None:
            default_provider = self.config.GENERATION_BACKEND_GEMINI
            provider_name = LLMEnums[default_provider]

        self.provider = factory.create(provider_name)

        if provider_name == LLMEnums.GEMINI.value:
            self.provider.set_generation_model(self.config.GENERATION_MODEL_ID_GEMINI)

        elif provider_name == LLMEnums.OPENAI.value:
            self.provider.set_generation_model(self.config.GENERATION_MODEL_ID_OPENAI)

        elif provider_name == LLMEnums.COHERE.value:
            self.provider.set_generation_model(self.config.GENERATION_MODEL_ID_COHERE_LIGHT)

        else:
            print("Unknown provider:", provider_name)

        if embedding_vector != LLMEnums.All_MiniLM_L6_v2.value:
            embedding_provider = factory.create(provider_name)

            if embedding_vector == LLMEnums.GEMINI.value:
                embedding_provider.set_embedded_model(self.config.EMBEDDING_MODEL_ID_GEMINI, 512)

            elif embedding_vector == LLMEnums.OPENAI.value:
                embedding_provider.set_embedded_model(self.config.EMBEDDING_MODEL_ID, 512)

            elif embedding_vector == LLMEnums.COHERE.value:
                embedding_provider.set_embedded_model(self.config.EMBEDDING_MODEL_ID_COHERE_MULTILINGUAL, 512)

            self.embedding = ProviderEmbeddingsWrapper(embedding_provider)

        else:
            self.embedding = HuggingFaceEmbeddings(model_name=embedding_vector, model_kwargs={"device": "cuda"})

        self.task = QAController(
            provider=self.provider,
            embedding_model=self.embedding,
            text=text
        )

    def run(self, question: str):
        return self.task.GenerateAnswer(query=question)
