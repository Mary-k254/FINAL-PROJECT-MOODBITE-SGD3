import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "MoodBite"
    VERSION: str = "1.0.0"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./moodbite.db")
    
    SENTIMENT_MODEL: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    SPACY_MODEL: str = "en_core_web_sm"
    
    DEFAULT_FOODS: list = [
        {"name": "ugali", "category": "carb", "common_names": "cornmeal,posho"},
        {"name": "sukuma wiki", "category": "vegetable", "common_names": "kale,collard greens"},
        {"name": "chapati", "category": "carb", "common_names": "flatbread"},
        {"name": "rice", "category": "carb", "common_names": ""},
        {"name": "beans", "category": "protein", "common_names": ""},
        {"name": "chicken", "category": "protein", "common_names": ""},
        {"name": "fish", "category": "protein", "common_names": "tilapia,omena"},
        {"name": "eggs", "category": "protein", "common_names": ""},
        {"name": "yogurt", "category": "fermented", "common_names": "maziwa mala"},
        {"name": "banana", "category": "fruit", "common_names": "ndizi"},
        {"name": "avocado", "category": "fruit", "common_names": "parachichi"},
        {"name": "orange", "category": "fruit", "common_names": "chungwa"},
        {"name": "apple", "category": "fruit", "common_names": "tufaa"},
        {"name": "water", "category": "beverage", "common_names": "maji"},
        {"name": "tea", "category": "beverage", "common_names": "chai"},
        {"name": "coffee", "category": "beverage", "common_names": "kahawa"},
    ]

settings = Settings()
