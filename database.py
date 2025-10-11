from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./moodbite.db")
engine = create_engine(DATABASE_URL, echo=True)

class MoodTags(str, Enum):
    HAPPY = "happy"
    SAD = "sad"
    ANXIOUS = "anxious"
    ENERGETIC = "energetic"
    TIRED = "tired"
    STRESSED = "stressed"
    CALM = "calm"
    FOCUSED = "focused"

class FoodCategory(str, Enum):
    FRUIT = "fruit"
    VEGETABLE = "vegetable"
    PROTEIN = "protein"
    CARB = "carb"
    DAIRY = "dairy"
    FERMENTED = "fermented"
    SWEET = "sweet"
    BEVERAGE = "beverage"
    OTHER = "other"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    consent_given: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MoodEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: date = Field(default_factory=date.today)
    mood_score: int = Field(ge=0, le=10)
    tags: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: date = Field(default_factory=date.today)
    text: str
    sentiment_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FoodLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date: date = Field(default_factory=date.today)
    food_name: str
    category: FoodCategory
    amount: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Insight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    period_start: date
    period_end: date
    insight_text: str
    confidence: float = Field(ge=0, le=1)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class FoodDatabase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    category: FoodCategory
    common_names: Optional[str] = None
    mood_benefits: Optional[str] = None

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
