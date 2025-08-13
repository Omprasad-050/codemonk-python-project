from fastapi import FastAPI
from app.api import auth, paragraphs

app = FastAPI(title="Text Analyzer API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(paragraphs.router, prefix="/paragraphs", tags=["paragraphs"])
