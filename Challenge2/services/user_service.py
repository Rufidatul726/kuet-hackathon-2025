from fastapi import Depends, HTTPException
from pydantic import BaseModel
from requests import Session
from db.database import get_db
from models.user import User
from utils.token import get_current_user

class UserProfile(BaseModel):
    id: int
    email: str
    username: str

class UserProfileUpdate(BaseModel):
    username: str | None = None


def get_user_profile(user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = {
        "id": user.id,
        "email": user.email,
        "username": user.username
    }
    return user_data

def update_user_profile(update_data: UserProfileUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if update_data.username is not None:
        user.username = update_data.username
    db.commit()
    db.refresh(user)
    return user.username

