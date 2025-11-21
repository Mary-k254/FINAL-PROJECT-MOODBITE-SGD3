from __future__ import annotations  # ← ADD THIS
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date, datetime, timedelta
from database import MoodEntry, get_session
from auth import get_current_user
from database import User
from pydantic import BaseModel

router = APIRouter()

class MoodCreate(BaseModel):
    mood_score: int
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    date: Optional[date] = None

class MoodResponse(BaseModel):
    id: int
    mood_score: int
    tags: Optional[str]
    notes: Optional[str]
    date: date
    created_at: datetime

@router.post("/", response_model=MoodResponse)
def create_mood_entry(
    mood_data: MoodCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    entry_date = mood_data.date or date.today()
    
    existing_statement = select(MoodEntry).where(
        MoodEntry.user_id == current_user.id,
        MoodEntry.date == entry_date
    )
    existing_entry = session.exec(existing_statement).first()
    
    if existing_entry:
        existing_entry.mood_score = mood_data.mood_score
        existing_entry.tags = ",".join(mood_data.tags) if mood_data.tags else None
        existing_entry.notes = mood_data.notes
        session.add(existing_entry)
        session.commit()
        session.refresh(existing_entry)
        return existing_entry
    
    tags_str = ",".join(mood_data.tags) if mood_data.tags else None
    mood_entry = MoodEntry(
        user_id=current_user.id,
        mood_score=mood_data.mood_score,
        tags=tags_str,
        notes=mood_data.notes,
        date=entry_date
    )
    
    session.add(mood_entry)
    session.commit()
    session.refresh(mood_entry)
    return mood_entry

@router.get("/", response_model=List[MoodResponse])
def get_mood_entries(
    days_back: Optional[int] = 30,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    start_date = datetime.now().date() - timedelta(days=days_back)
    
    statement = select(MoodEntry).where(
        MoodEntry.user_id == current_user.id,
        MoodEntry.date >= start_date
    ).order_by(MoodEntry.date.desc())
    
    entries = session.exec(statement).all()
    return entries

@router.get("/stats")
def get_mood_stats(
    days_back: Optional[int] = 30,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    start_date = datetime.now().date() - timedelta(days=days_back)
    
    statement = select(MoodEntry).where(
        MoodEntry.user_id == current_user.id,
        MoodEntry.date >= start_date
    )
    
    entries = session.exec(statement).all()
    
    if not entries:
        return {
            "average_mood": 0,
            "total_entries": 0,
            "mood_trend": "insufficient_data"
        }
    
    mood_scores = [entry.mood_score for entry in entries]
    avg_mood = sum(mood_scores) / len(mood_scores)
    
    recent_entries = sorted(entries, key=lambda x: x.date)[-7:]
    if len(recent_entries) >= 2:
        recent_avg = sum(entry.mood_score for entry in recent_entries) / len(recent_entries)
        trend = "improving" if recent_avg > avg_mood else "declining" if recent_avg < avg_mood else "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "average_mood": round(avg_mood, 2),
        "total_entries": len(entries),
        "mood_trend": trend,
        "period_days": days_back
    }
