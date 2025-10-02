from langchain_text_splitters import RecursiveCharacterTextSplitter
from .BaseController import BaseController
from langchain.prompts import PromptTemplate
from ..Stores.LLM.Providers.geminiProvider import GenAIProvider
import re

class SentimentAnalysisController(BaseController):
    def __init__(self, provider: GenAIProvider = None):
        super().__init__()

        self.provider = provider

        self.prompt_template = '\n'.join([
            "You are a helpful assistant that analyzes text.",
            "Read the following text and give a simple analysis:",
            "- Determine the main sentiment (positive, negative, neutral).",
            "- List any key points or emotions mentioned.",
            "",
            "Text:",
            "{text}",
            "",
            "Output format:",
            "Sentiment: <positive/negative/neutral>",
            "Key points: <point1>, <point2>, ..."
        ])

        self.prompt = PromptTemplate(
            input_variables=["text"],
            template=self.prompt_template
        )

        self.splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)

    def analysis(self, text: str, max_length: int = 500):
        """Analyze text in chunks and return structured results."""
        if not self.provider:
            raise Exception("No provider configured for LLM analysis")

        chunks = self.splitter.split_text(text)
        if not chunks:
            raise Exception("Text is empty")

        results = []
        for chunk in chunks:
            prompt = self.prompt_template.format(text=chunk)

            output = self.provider.generate_text(
                prompt=prompt,
                max_output_tokens=max_length,
                temperature=0.3
            ).strip()

            # محاولة فصل sentiment و key points
            sentiment_match = re.search(r"Sentiment:\s*(\w+)", output, re.IGNORECASE)
            keypoints_match = re.search(r"Key points:\s*(.*)", output, re.IGNORECASE)

            sentiment = sentiment_match.group(1) if sentiment_match else "N/A"
            key_points = keypoints_match.group(1) if keypoints_match else ""

            results.append({
                "chunk": chunk,
                "sentiment": sentiment,
                "key_points": key_points
            })

        return results
