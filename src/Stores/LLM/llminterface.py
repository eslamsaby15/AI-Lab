from abc import abstractmethod , ABC

class LLMInterFace(ABC): 
    @abstractmethod
    def set_generation_model(self,model_id) : 
        pass

    @abstractmethod
    def set_embedded_model(self,model_id,embedding_size:int):
        pass

    @abstractmethod
    def generate_text(self,prompt , chat_history :list =  [] , max_output_tokens: int=None ,
                      temperature : float = .3) : 
        pass

    @abstractmethod
    def embedd_text(self,text :str , document_type: str = None ) :
        pass

    @abstractmethod
    def construct_prompt(Self,prompt :str , role :str):
        pass

    @abstractmethod
    def generate_text(self, prompt : str, temperature :float ) :
        pass
    