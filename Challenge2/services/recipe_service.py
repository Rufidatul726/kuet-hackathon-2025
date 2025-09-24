# app/services/recipe_service.py
import re
from typing import List
from sqlalchemy.orm import Session
from models.recipe import Recipe
from models.user import User
from utils.parsing import normalize, parse_ingredients

def create_recipe(db: Session, title: str, ingredients: str, instructions: str, user: User):
    recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, owner_id=user.id)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_user_recipes(db: Session, user: User):
    return db.query(Recipe).filter(Recipe.owner_id == user.id).all()
    
def recommend_recipes(db: Session, available_ingredients: List[str], user: User, top_n: int = 5):
    all_recipes = db.query(Recipe).filter(Recipe.owner_id == user.id).all()

    available_set = set([normalize(ing) for ing in available_ingredients])

    print(f"Available ingredients: {available_set}")
    scored_recipes = []

    for recipe in all_recipes:
        print(f"Checking recipe ingredients: {recipe.ingredients}")
        recipe_ings = parse_ingredients(recipe.ingredients)
        match_count = len(recipe_ings & available_set)
        print(f"Matching {recipe.title}: {match_count} matches out of {len(recipe_ings)} ingredients")
        if match_count > 0:
            score = match_count / len(recipe_ings)  # proportion match
            scored_recipes.append((score, match_count, recipe))

    # Sort by score, then by number of matched ingredients, descending
    scored_recipes.sort(key=lambda x: (x[0], x[1]), reverse=True)

    return [recipe for _, _, recipe in scored_recipes[:top_n]]

def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def update_recipe(db: Session, recipe_id: int, title: str, ingredients: str, instructions: str):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        recipe.title = title
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        db.commit()
        db.refresh(recipe)
    return recipe

def delete_recipe(db: Session, recipe_id: int):
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if recipe:
        db.delete(recipe)
        db.commit()
    return recipe