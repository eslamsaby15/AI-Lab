from ..LLMEnums import LLMEnums ,OpenEnums
from ..llminterface import LLMInterFace
from openai import OpenAI
import logging

class OpenAiProvider(LLMInterFace) :
    def __init__(self , api_key :str , api_url : str , 
                   default_input_max_characters: int=1000, 
                   default_generation_max_output_tokens: int=1000 ,
                   default_generation_temperature: float=0.1
                   ) :
        
        self.api_key = api_key
        self.api_url = api_url
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens 
        self.default_generation_temperature=default_generation_temperature

        #for interface 

        self.gen_model_id = None
        self.embedd_model_id= None
        self.prompt =None , 
        self.OpenEnums= OpenEnums
        self.embedding_size =None
        self.logger = logging.getLogger(__name__)
        
        self.client= OpenAI(
            api_key=self.api_key ,
            api_url = self.api_url
        )

    def  set_generation_model(self, model_id):
        self.gen_model_id = model_id

    def set_embedded_model(self, model_id, embedding_size):
        self.embedd_model_id =  model_id
        self.embedding_size =embedding_size

    def generate_text(self, prompt : str, chat_history = [] , max_output_tokens = None, temperature = 0.3):
        
        if not self.client :
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.gen_model_id:
            self.logger.error('Generation model for OpenAI was not set')

        chat_history.append(self.construct_prompt(prompt=prompt , 
                                                  role=self.OpenEnums.USER.value))

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature =temperature if temperature else self.default_generation_temperature 

        response = self.client.chat.completions.create(
            model= self.gen_model_id,
            messages= chat_history , 
            max_tokens= max_output_tokens , 
            temperature=temperature
        )

        if response is None or not response.choices or len(response.choices) ==0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None
        
        return response.choices[0].message['content']

    def embedd_text(self, text, document_type = None):
        
        if not self.client : 
            self.logger.error("OpenAI client was not set")
            return None
        
        if not self.embedd_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        response = self.client.embeddings.create(
            model= self.embedd_model_id,
            input= text
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while generating text with OpenAI")
            return None
        
        return response.data[0].embedding
    
    def construct_prompt(self, prompt : str , role):
        return {'role' : role ,
                'content' : self.process_text(prompt)}
    

    def process_text(self, text : str ):
        return text[:self.default_input_max_characters].strip()