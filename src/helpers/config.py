from pydantic_settings import BaseSettings
import os 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # src
ENV_PATH = os.path.join(BASE_DIR, ".env") 

class Setting(BaseSettings) : 

    APP_NAME: str
    APP_VERSION: str
    EN_MODEL: str

    GENERATION_BACKEND_OPENAI: str
    GENERATION_BACKEND_GEMINI: str
    GENERATION_BACKEND_COHERE: str

    EMBEDDING_BACKEND_GEMINI: str
    EMBEDDING_BACKEND: str


    OPENAI_API_KEY: str = None
    COHERE_API_KEY: str = None
    GEMINI_API_KEY: str = None

    GENERATION_MODEL_ID_OPENAI: str = None
    GENERATION_MODEL_ID_GEMINI: str = None
    GENERATION_MODEL_ID_COHERE_LIGHT : str = None

    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_ID_GEMINI: str = None
    EMBEDDING_MODEL_ID_COHERE_MULTILINGUAL  : str = None
    

    OPENAI_API_URL: str = None
    INPUT_DAFAULT_MAX_CHARACTERS :  int = None
    GENERATION_DAFAULT_MAX_TOKENS:  int = None
    
    GENERATION_DAFAULT_TEMPERATURE : float = None
    

    class Config:
        env_file =ENV_PATH


def  APP_Setting() : 
    return Setting()
