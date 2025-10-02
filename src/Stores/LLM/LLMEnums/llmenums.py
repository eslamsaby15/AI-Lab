from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OpenAI"
    COHERE = "Cohere"
    GEMINI ='Gemini'
    All_MiniLM_L6_v2 = "sentence-transformers/all-MiniLM-L6-v2"

class OpenEnums(Enum):
    SYSTEM= 'system' 
    USER ='user'
    ASSISTANT = "assistant"


class CoHereEnums(Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document"
    QUERY = "search_query"


class DocumentTypeEnum(Enum):
    DOCUMENT = "document"
    QUERY = "query"


class GeminiEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    MODEL = "model"   
    
    DOCUMENT = "retrieval_document"
    QUERY = "retrieval_query"