from pydantic import BaseModel
from typing import List

class ParagraphCreate(BaseModel):
    text: str

class ParagraphOut(BaseModel):
    id: int
    text: str
    word_frequencies: List[dict]

    class Config:
        orm_mode = True
