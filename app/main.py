# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db
from typing import List, Optional

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/stories/")
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db=db, story=story)

@app.get("/stories/", response_model=List[schemas.StoryList])
def get_stories(db: Session = Depends(get_db)):
    return crud.get_all_stories_with_tags(db)

@app.get("/stories/{story_id}")
def get_story_by_id(story_id: int, db: Session = Depends(get_db)):
    return crud.get_story_details_by_id(db, story_id)

@app.get("/search/stories")
def search_stories(
    query: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    return crud.search_stories(db=db, query=query, category=category, status=status)

@app.put("/stories/{story_id}")
def update_story(story_id: int, story_update: schemas.StoryUpdate, db: Session = Depends(get_db)):
    return crud.update_story(db=db, story_id=story_id, story_update=story_update)

@app.delete("/stories/{story_id}")
def delete_story(story_id: int, db: Session = Depends(get_db)):
    story = crud.delete_story(db=db, story_id=story_id)
    if story is None:
        raise HTTPException(status_code=404, detail="Story not found")
    return {"messege":"berhasil dihapus"}