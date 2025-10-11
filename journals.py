from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from datetime import date, datetime
from app.models.database import JournalEntry, get_session
from app.services.auth import get_current_user
from app.services.correlations import text_analyzer
from app.models.database import User
from pydantic import BaseModel

router = APIRouter()

class JournalCreate(BaseModel):
    text: str
    date: Optional[date] = None

class JournalResponse(BaseModel):
    id: int
    text: str
    date: date
    sentiment_score: Optional[float]
    created_at: datetime

@router.post("/", response_model=JournalResponse)
def create_journal_entry(
    journal_data: JournalCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    entry_date = journal_data.date or date.today()
    
    sentiment_score = text_analyzer.analyze_sentiment(journal_data.text)
    
    existing_statement = select(JournalEntry).where(
        JournalEntry.user_id == current_user.id,
        JournalEntry.date == entry_date
    )
    existing_entry = session.exec(existing_statement).first()
    
    if existing_entry:
        existing_entry.text = journal_data.text
        existing_entry.sentiment_score = sentiment_score
        session.add(existing_entry)
        session.commit()
        session.refresh(existing_entry)
        return existing_entry
    
    journal_entry = JournalEntry(
        user_id=current_user.id,
        text=journal_data.text,
        sentiment_score=sentiment_score,
        date=entry_date
    )
    
    session.add(journal_entry)
    session.commit()
    session.refresh(journal_entry)
    return journal_entry

@router.get("/", response_model=List[JournalResponse])
def get_journal_entries(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(JournalEntry).where(
        JournalEntry.user_id == current_user.id
    ).order_by(JournalEntry.date.desc())
    
    entries = session.exec(statement).all()
    return entries
