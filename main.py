from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import gradio as gr

import models
import crud
from database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API", version="1.0")

# --- Pydantic Schemas ---
class BookBase(BaseModel):
    title: str
    author: str
    pages: int | None = None
    is_available: bool = True

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    class Config:
        from_attributes = True


# --- API ROUTES (FastAPI) ---

@app.get("/")
def root():
    return RedirectResponse(url="/ui")

@app.post("/books", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def add_new_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book_data=book.model_dump())

@app.get("/books", response_model=List[BookResponse])
def view_all_books(db: Session = Depends(get_db)):
    return crud.get_all_books(db=db)
