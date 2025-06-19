import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.novelai.net')
    
    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise ValueError("API_KEY not found in .env file")
        return True