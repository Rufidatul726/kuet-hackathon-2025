# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models.user import User
from db.database import get_db
from services.user_service import get_user_profile, update_user_profile
from utils.token import get_current_user

router = APIRouter()

class UserProfileUpdate(BaseModel):
    username: str 
    
@router.get("/")
def get_profile(user: User = Depends(get_current_user)):
    return get_user_profile(user)

@router.put("/")
def update_profile(update_data: UserProfileUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    username = update_user_profile(update_data, db, user)
    
    return {"msg": "Profile updated successfully", "username": username}
