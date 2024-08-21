# app/routers/story.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ... import models, schemas, crud
from ..database import get_db

router = APIRouter()

@router.post("/stories/")
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db=db, story=story)

@router.get("/stories/", response_model=List[schemas.StoryList])
def get_stories(db: Session = Depends(get_db)):
    stories = crud.get_all_stories(db)
    return stories

@router.get("/stories/{story_id}", response_model=schemas.StoryDetail)
def get_story_by_id(story_id: int, db: Session = Depends(get_db)):
    story = crud.get_story_by_id(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story
