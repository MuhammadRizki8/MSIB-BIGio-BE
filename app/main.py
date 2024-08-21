# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, Base, get_db

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/stories/")
def create_story(story: schemas.StoryCreate, db: Session = Depends(get_db)):
    return crud.create_story(db=db, story=story)
