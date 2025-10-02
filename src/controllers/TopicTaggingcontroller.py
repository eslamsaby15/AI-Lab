from langchain_text_splitters import RecursiveCharacterTextSplitter
from .BaseController import BaseController
from langchain.prompts import PromptTemplate
from ..Stores.LLM.Providers.geminiProvider import GenAIProvider
import re

class TopicTaggingController(BaseController):
    def __init__(self, provider: GenAIProvider = None):
        super().__init__()

        self.provider = provider

        self.prompt_template = '\n'.join([
            "You are a helpful assistant that analyzes text.",
            "Read the following text and generate a list of relevant topic tags or keywords.",
            "- Focus on main subjects, concepts, or recurring themes.",
            "",
            "Text:",
            "{text}",
            "",
            "Output format (comma-separated tags):"
        ])

        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.prompt_template
        )

        self.splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)

    def extract_tags(self, text: str, max_length: int = 300):
        """Analyze text in chunks and return topic tags."""
        if not self.provider:
            raise Exception("No provider configured for LLM analysis")

        chunks = self.splitter.split_text(text)
        if not chunks:
            raise Exception("Text is empty")

        all_tags = set()
        for chunk in chunks:
            prompt = self.prompt_template.format(text=chunk)

            output = self.provider.generate_text(
                prompt=prompt,
                max_output_tokens=max_length,
                temperature=0.3
            ).strip()

            tags = [tag.strip() for tag in output.split(",") if tag.strip()]
            all_tags.update(tags)

        return list(all_tags)
