from __future__ import annotations  # ← ADD THIS
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta, date  # ← ADD 'date' HERE
from database import Insight, get_session
from auth import get_current_user
from ai_analysis import analyzer
from database import User
from pydantic import BaseModel

router = APIRouter()

class InsightResponse(BaseModel):
    id: int
    insight_text: str
    confidence: float
    period_start: date
    period_end: date
    created_at: datetime

@router.get("/", response_model=List[InsightResponse])
def get_insights(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(Insight).where(
        Insight.user_id == current_user.id,
        Insight.is_active == True
    ).order_by(Insight.created_at.desc())
    
    insights = session.exec(statement).all()
    
    if not insights:
        insights = generate_insights_background(current_user.id, session)
    
    return insights

@router.post("/generate")
def generate_insights(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    background_tasks.add_task(generate_insights_background, current_user.id, session)
    return {"message": "Insight generation started"}

def generate_insights_background(user_id: int, session: Session):
    existing_statement = select(Insight).where(Insight.user_id == user_id)
    existing_insights = session.exec(existing_statement).all()
    for insight in existing_insights:
        insight.is_active = False
        session.add(insight)
    
    correlations = analyzer.calculate_correlations(user_id, session)
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    new_insights = []
    for correlation in correlations:
        insight = Insight(
            user_id=user_id,
            insight_text=correlation["message"],
            confidence=correlation["confidence"],
            period_start=start_date,
            period_end=end_date
        )
        session.add(insight)
        new_insights.append(insight)
    
    session.commit()
    for insight in new_insights:
        session.refresh(insight)
    
    return new_insights