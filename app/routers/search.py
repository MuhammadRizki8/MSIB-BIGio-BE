# app/routers/search.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/search/stories", response_model=List[schemas.StoryList])
def search_stories(query: str, db: Session = Depends(get_db)):
    stories = db.query(models.Story).filter(
        or_(
            models.Story.title.ilike(f"%{query}%"),
            models.Story.author.ilike(f"%{query}%")
        )
    ).all()
    return stories
