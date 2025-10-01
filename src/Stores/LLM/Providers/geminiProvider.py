from ..llminterface import LLMInterFace
from ..LLMEnums import GeminiEnums
import google.generativeai as genai
from typing import List, Union
import logging
import re


class GenAIProvider(LLMInterFace):
    def __init__(self, api_key: str,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1000,
                 default_generation_temperature: float = 0.1):

        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.gen_model_id = None
        self.embedd_model_id = None
        self.embedding_size = None
        self.enums = GeminiEnums

        genai.configure(api_key=self.api_key)
        self.logger = logging.getLogger(__name__)

    def set_embedded_model(self, model_id, embedding_size):
        self.embedd_model_id = model_id
        self.embedding_size = embedding_size

    def set_generation_model(self, model_id):
        self.gen_model_id = model_id

    def process_text(self, text: str):
        return text[: self.default_input_max_characters].strip()

    def construct_prompt(self, prompt: str, role: str):
        return {
            'role': role,
            'parts': [self.process_text(prompt)]
        }

    def embedd_text(self, text: Union[str, List[str]], document_type=None):
        if not self.embedd_model_id:
            self.logger.error("Embedding model for GenAI was not set")
            return None

        if isinstance(text, str):
            text = [text]

        input_type = GeminiEnums.DOCUMENT
        if document_type == GeminiEnums.QUERY:
            input_type = GeminiEnums.QUERY

        response = genai.embed_content(
            model=self.embedd_model_id,
            content=text,
            task_type=input_type
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return response.embedding

    def generate_text(self, prompt, chat_history=None,
                      max_output_tokens=None, temperature=None):

        if not self.gen_model_id:
            self.logger.error("gen model for GEMINI was not set")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        model = genai.GenerativeModel(self.gen_model_id)

        response = model.generate_content(
            self.process_text(prompt),
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )

        if not response or not response.text:
            self.logger.error('Error while generating text with GenAI')
            return None

        return response.text
    
    def generate_Chunks(self, prompt : str ,temperature :  float = 0.2) :
        if not self.gen_model_id:
            self.logger.error("gen model for GEMINI was not set")
            return None
        model=  genai.GenerativeModel(self.gen_model_id)

        temperature = temperature if temperature else self.default_generation_temperature

        model = genai.GenerativeModel(self.gen_model_id)

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": temperature,
            }
        )

        if not response or not response.text:
            self.logger.error('Error while generating text with GenAI')
            return None

        return response.text



        
