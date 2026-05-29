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
