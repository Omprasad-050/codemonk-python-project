from app.models.paragraph import Paragraph, WordFrequency
from app.schemas.paragraph import ParagraphOut
from sqlalchemy.orm import Session
from typing import List
import re

def analyze_paragraphs(text: str, db: Session, user):
    paragraphs = text.split("\n\n")
    result = []
    for p in paragraphs:
        para = Paragraph(text=p, user_id=user.id)
        db.add(para)
        db.commit()
        db.refresh(para)
        words = re.findall(r"\w+", p.lower())
        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        for word, count in freq.items():
            wf = WordFrequency(word=word, count=count, paragraph_id=para.id)
            db.add(wf)
        db.commit()
        para.word_frequencies = [dict(word=word, count=count) for word, count in freq.items()]
        result.append(para)
    return result

def search_paragraphs(word: str, db: Session, user):
    word = word.lower()
    q = db.query(Paragraph).join(WordFrequency).filter(
        Paragraph.user_id == user.id,
        WordFrequency.word == word
    ).order_by(WordFrequency.count.desc()).limit(10)
    return q.all()
