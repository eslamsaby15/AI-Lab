from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import pipeline
from .BaseController import BaseController
from langchain.prompts import PromptTemplate
from ..Stores.LLM.Providers.geminiProvider import GenAIProvider


class Summarizer(BaseController):
    def __init__(self, lang: str = 'en', provider : GenAIProvider = None  , mode: str = "llm"):
        super().__init__()
        self.lang = lang
        self.mode = mode

        self.provider = provider
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=50
        )

        self.prompt_template = '\n\n'.join([
            "You are a helpful assistant that summarizes text in {language}.",
            "Given the following text, generate:",
            "1. A concise summary.",
            "2. Important keywords.",
            "",
            "Text:",
            "{text}",
            "",
            "Output format:",
            "Summary:\n",

            "- <summary_here>",
            "- <summary_here>",
            "",
            "Keywords:",
            "- <keyword1>, <keyword2>, ...",
            "\n"
        ])


        self.prompt = PromptTemplate(
            input_variables=["language", "text"],
            template=self.prompt_template
        )


    def classical_Summarizer(self, text: str):
        """Summarize using Classical Model"""

        self.summarizer = pipeline(
            "summarization",
            model=self.app_setting.EN_MODEL,
            tokenizer=self.app_setting.EN_MODEL,
            device=0
        )

        chunks = self.splitter.split_text(text)

        summaries = []

        for chunk in chunks:
            output = self.summarizer(
                chunk, max_length=200, min_length=50, do_sample=False
            )
            summaries.append(output[0]["summary_text"])


        return "\n".join([f"- {s}" for s in summaries])


    def LLM_Summarizer(  self, text: str, max_length: int = 500  ):
        """Summarization using LLM."""

        if not self.provider :
           raise Exception("No provider configured for LLM summarization")

        chunks , summaries = [] , []
        chunks = self.splitter.split_text(text)

        if not chunks:
            raise Exception("Text is empty")

        for  chunk in chunks : 
            prompt = self.prompt_template.format(
                language = self.lang , text = chunk
            )

            summary = self.provider.generate_Chunks(
                prompt= prompt , 
                
                temperature= .3
            )
            
            summaries.append(
                 summary.strip() )
            
        return "\n".join([f"- {s}" for s in summaries])
        
