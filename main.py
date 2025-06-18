from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
from dotenv import load_dotenv
import secrets
import os

load_dotenv()

AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

security = HTTPBasic()

def verify_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if not AUTH_PASSWORD:
        raise HTTPException(status_code=500, detail="Пароль не встановлено")
    correct_password = secrets.compare_digest(credentials.password, AUTH_PASSWORD)
    if not correct_password:
        raise HTTPException(status_code=401, detail="Невірний пароль")
    return credentials.username

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BOOKS = [
    {"title": "Гаррі Поттер", "genre": "фентезі", "age_min": 10, "mood": "хочу пригод"},
    {"title": "Маленький принц", "genre": "філософія", "age_min": 8, "mood": "сумно"},
    {"title": "Сила підсвідомості", "genre": "мотивація", "age_min": 16, "mood": "хочу надихнутись"},
    {"title": "1984", "genre": "антиутопія", "age_min": 16, "mood": "серйозний настрій"},
    {"title": "Атлант розправив плечі", "genre": "драма", "age_min": 18, "mood": "хочу надихнутись"},
]

@app.get("/recommendations")
def recommend_books(
    genre: str = Query(..., description="Жанр книги"),
    age: int = Query(..., description="Вік користувача"),
    mood: str = Query(..., description="Настрій користувача"),
    username: str = Depends(verify_auth)
):
    results = [
        book for book in BOOKS
        if book["genre"].lower() == genre.lower()
        and book["age_min"] <= age
        and book["mood"].lower() == mood.lower()
    ]
    if not results:
        raise HTTPException(status_code=404, detail="Книги не знайдено під ці параметри")
    return {
        "користувач": username,
        "рекомендовані книги": results
    }
