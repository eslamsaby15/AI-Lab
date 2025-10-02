from .BaseController import BaseController

from langchain.prompts import ChatPromptTemplate
from .BaseController import BaseController
from ..Stores.LLM import GenAIProvider
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import InMemoryVectorStore



class QAController(BaseController): 
    def __init__(self, provider : GenAIProvider ,  embedding_model  , text : str)  : 
        super().__init__()
        
        self.provider = provider
        self.embedding_model = embedding_model

        self.template= "\n".join([
        "You are an assistant for question-answering tasks. ",
        "Use the following pieces of retrieved context to answer the question.  ",
        "If you don't know the answer, just say that you don't know. ",
        "Use three sentences maximum and keep the answer concise.\n",
        "Question: {question} \n",
        "Context: {context}"])
        self.text= text 

        self.vector_db= self.process_documents(text = self.text)

 
    def get_chunks(self , text: str, chunk_size: int = 400, chunk_overlap: int = 50):
        splitter = RecursiveCharacterTextSplitter( chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
        return chunks

    def get_vectordb(self, chunks):
        vectordb = InMemoryVectorStore.from_texts(chunks, self.embedding_model)
        return vectordb

    def process_documents(self , text : str ):
        chunks = self.get_chunks(text=text)
        vectordb = self.get_vectordb(chunks=chunks)
        return vectordb

    def GenerateAnswer(self, query: str, top_k: int = 3):
        if not self.vector_db:
            raise ValueError("❌ Vector store not built")

        results = self.vector_db.similarity_search(query, k=top_k)

        context = "\n".join([doc.page_content for doc in results])

        prompt = self.template.format(question=query, context=context)
      
        answer = self.provider.generate_text(prompt,temperature = .3)

        return answer