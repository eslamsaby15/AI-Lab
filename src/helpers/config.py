from pydantic_settings import BaseSettings

class Setting(BaseSettings) : 

    class Config:
        env_file =".env" 


def  APP_Setting() : 
    return Setting()
