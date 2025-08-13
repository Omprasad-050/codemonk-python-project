from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.paragraph import ParagraphCreate, ParagraphOut
from app.models.paragraph import Paragraph, WordFrequency
from app.database import SessionLocal
from app.core.dependencies import get_current_user
from app.services.paragraph_service import analyze_paragraphs, search_paragraphs
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=List[ParagraphOut])
def submit_paragraphs(paragraph: ParagraphCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return analyze_paragraphs(paragraph.text, db, user)

@router.get("/search")
def search(word: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return search_paragraphs(word, db, user)

@router.get("/", response_model=List[ParagraphOut])
def get_paragraphs(db: Session = Depends(get_db), user=Depends(get_current_user), skip: int = 0, limit: int = 10):
    paragraphs = db.query(Paragraph).filter(Paragraph.user_id == user.id).offset(skip).limit(limit).all()
    return paragraphs
