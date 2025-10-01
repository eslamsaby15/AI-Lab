from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import pipeline
from .BaseController import BaseController
from langchain.prompts import PromptTemplate
from ..Stores.LLM.Providers.geminiProvider import GenAIProvider
from ..helpers.config import APP_Setting
import os
os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

class TransaltionController(BaseController):
    def __init__(self, provider: GenAIProvider = None, mode: str = "llm"):
        super().__init__()
        self.mode = mode
        self.provider = provider
        self.app_setting = APP_Setting()

        self.prompt_template = "\n\n".join([
            "You are a helpful assistant that translates text into Arabic sentences.",
            "## Rules:",
            "- Do not change, add, or remove words.",
            "- Only translate the text exactly as it is.",
            "- Keep numbers, symbols, and punctuation unchanged.",
            "## Text:",
            "{text}",
            "## Translation:",
            "translation output"
        ])

        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.prompt_template
        )

    def classical_Translator(self, text: str, max_length: int = 256, temperature: float = 0.7):
        self.Translation = pipeline(
            "translation_en_to_ar",
            model=self.app_setting.EN_AR_MODEL,
            tokenizer=self.app_setting.EN_AR_MODEL,
            device=0
        )

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=50
        )

        chunks = splitter.split_text(text)
        translations = []

        for chunk in chunks:
            output = self.Translation(
                chunk,
                max_length=512,
                do_sample=True,
                temperature=temperature
            )
            translations.append(output[0]["translation_text"])

        return "\n".join([f"- {s}" for s in translations])

    def LLM_Translation(self, text: str, max_length: int = 1024, temperature: float = 0.3):
        if not self.provider:
            raise Exception("No provider configured for LLM Translate")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=max_length,
            chunk_overlap=50
        )

        chunks = splitter.split_text(text)
        if not chunks:
            raise Exception("Text is empty")

        translations = []

        for chunk in chunks:
            prompt = self.prompt_template.format(text=chunk)
            translated_text = self.provider.generate_text(
                prompt=prompt,
                max_output_tokens=max_length,
                temperature=temperature
            )
            translations.append(translated_text.strip())

        return "\n".join([f"- {s}" for s in translations])
