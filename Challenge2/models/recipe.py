# app/models/recipe.py
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from db.database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(Text)
    instructions = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
