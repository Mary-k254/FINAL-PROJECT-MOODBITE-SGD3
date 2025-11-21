from __future__ import annotations  # ← Add this line at the VERY TOP
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from database import User, get_session
from security import verify_token, verify_password, get_password_hash

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    payload = verify_token(credentials.credentials)
    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user

def authenticate_user(session: Session, email: str, password: str):
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
