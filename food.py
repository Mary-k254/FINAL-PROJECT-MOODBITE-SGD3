from __future__ import annotations  # ← ADD THIS
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date
from database import FoodLog, FoodCategory, FoodDatabase, get_session
from auth import get_current_user
from database import User
from config import settings
from pydantic import BaseModel
import enum  # ← ADD THIS IMPORT

router = APIRouter()

# Define FoodCategory for Pydantic if it's an Enum
if hasattr(FoodCategory, '__members__'):  # It's an Enum
    class FoodCategoryStr(str, enum.Enum):
        # Copy all enum values from FoodCategory
        pass
    # Dynamically set the enum members
    for name, value in FoodCategory.__members__.items():
        setattr(FoodCategoryStr, name, value)
else:
    # If it's not an Enum, use string type
    FoodCategoryStr = str

class FoodLogCreate(BaseModel):
    food_name: str
    category: FoodCategoryStr  # ← USE THE FIXED TYPE
    amount: Optional[str] = None
    date: Optional[date] = None

@router.post("/log")
def log_food(
    food_data: FoodLogCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Convert back to the original FoodCategory for database
    food_log = FoodLog(
        user_id=current_user.id,
        food_name=food_data.food_name,
        category=FoodCategory(food_data.category),  # Convert to enum
        amount=food_data.amount,
        date=food_data.date or date.today()
    )
    
    session.add(food_log)
    session.commit()
    session.refresh(food_log)
    return {"message": "Food logged successfully", "id": food_log.id}

@router.get("/log")
def get_food_logs(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(FoodLog).where(
        FoodLog.user_id == current_user.id
    ).order_by(FoodLog.date.desc())
    
    entries = session.exec(statement).all()
    return entries

@router.get("/database")
def get_food_database(session: Session = Depends(get_session)):
    statement = select(FoodDatabase)
    foods = session.exec(statement).all()
    
    if not foods:
        for food_data in settings.DEFAULT_FOODS:
            food = FoodDatabase(**food_data)
            session.add(food)
        session.commit()
        foods = session.exec(statement).all()
    
    return foods