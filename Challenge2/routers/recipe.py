# app/routers/recipes.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from services.recipe_service import create_recipe, get_recipe_by_id, get_user_recipes, recommend_recipes
from utils.token import get_current_user
from pydantic import BaseModel

router = APIRouter()

class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    instructions: str

@router.post("/")
def upload_recipe(recipe: RecipeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_recipe(db, recipe.title, recipe.ingredients, recipe.instructions, user)

@router.get("/")
def list_user_recipes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_recipes(db, user)

@router.post("/recommendations")
def recommend(ingredients: List[str], db: Session = Depends(get_db), user= Depends(get_current_user)):
    return recommend_recipes(db, ingredients, user)

@router.get("/{recipe_id}")
def get_recipe(recipe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    recipe = get_recipe_by_id(db, recipe_id)
    if recipe and recipe.owner_id == user.id:
        return recipe
    return {"error": "Recipe not found or access denied."}

@router.put("/{recipe_id}")
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_recipe(db, recipe_id, recipe.title, recipe.ingredients, recipe.instructions)

@router.delete("/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return delete_recipe(db, recipe_id)