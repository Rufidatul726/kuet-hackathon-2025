# routers/chatbot.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import get_db
from utils.token import get_current_user
from utils.llm_client import generate_recipe_response
from models.recipe import Recipe

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_with_bot(request: ChatRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    recipes = db.query(Recipe).filter(Recipe.owner_id == user.id).all()
    ingredients = ", ".join([r.ingredients for r in recipes])
    
    response = generate_recipe_response(request.message, ingredients)
    return {"reply": response}
