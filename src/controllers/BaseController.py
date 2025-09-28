from ..helpers.config import APP_Setting
import os
import random
import string

class BaseController:
    def __init__(self):
        self.app_setting = APP_Setting()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets/Data")

    def generate_random_string(self, length: int = 6):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        

