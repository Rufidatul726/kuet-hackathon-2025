# app/main.py
from fastapi import FastAPI
from routers import auth, recipe, chat, user
from db.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kitchen Buddy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(recipe.router, prefix="/recipe", tags=["Recipe"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])