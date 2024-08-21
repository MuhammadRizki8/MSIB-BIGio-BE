# app/main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
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
    stories = db.query(models.Story).all()
    stories_with_tags = []
    
    for story in stories:
        tags = db.query(models.Tag).join(models.StoryTag).filter(models.StoryTag.story_id == story.id).all()
        story_with_tags = schemas.StoryList(
            id=story.id,
            title=story.title,
            author=story.author,
            synopsis=story.synopsis,
            category=story.category,
            cover_image=story.cover_image,
            status=story.status,
            tags=tags
        )
        stories_with_tags.append(story_with_tags)
    
    return stories_with_tags

@app.get("/stories/{story_id}")
def get_story_by_id(story_id: int, db: Session = Depends(get_db)):
    # Ambil story berdasarkan ID
    story = db.query(models.Story).filter(models.Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Ambil tags yang berhubungan dengan story
    tags = db.query(models.Tag).join(models.StoryTag).filter(models.StoryTag.story_id == story.id).all()
    # Ambil chapters yang berhubungan dengan story
    chapters = db.query(models.Chapter).filter(models.Chapter.story_id == story.id).all()

    # Mapping data story, tags, dan chapters ke dalam dictionary
    story_detail = {
        "id": story.id,
        "title": story.title,
        "author": story.author,
        "synopsis": story.synopsis,
        "category": story.category,
        "cover_image": story.cover_image,
        "status": story.status,
        "tags": [{"id": tag.id, "tag_name": tag.tag_name} for tag in tags],
        "chapters": [{"id": chapter.id, "title": chapter.title, "content": chapter.content} for chapter in chapters]
    }

    return story_detail

@app.get("/search/stories")
def search_stories(
    query: Optional[str] = Query(None, description="Search keyword"),
    category: Optional[str] = Query(None, description="Filter by category"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db)
):
    # Base query untuk search stories
    stories_query = db.query(models.Story)

    # Jika ada query, tambahkan filter untuk pencarian berdasarkan title atau author
    if query:
        stories_query = stories_query.filter(
            or_(
                models.Story.title.ilike(f"%{query}%"),
                models.Story.author.ilike(f"%{query}%")
            )
        )

    # Filter berdasarkan category jika diberikan
    if category:
        stories_query = stories_query.filter(models.Story.category == category)

    # Filter berdasarkan status jika diberikan
    if status:
        stories_query = stories_query.filter(models.Story.status == status)

    # Eksekusi query dan ambil hasil
    stories = stories_query.all()

    results = []
    for story in stories:
        tags = db.query(models.Tag).join(models.StoryTag).filter(models.StoryTag.story_id == story.id).all()
        chapters = db.query(models.Chapter).filter(models.Chapter.story_id == story.id).all()

        story_detail = {
            "id": story.id,
            "title": story.title,
            "author": story.author,
            "synopsis": story.synopsis,
            "category": story.category,
            "cover_image": story.cover_image,
            "status": story.status,
            "tags": tags,
            "chapters": chapters
        }

        results.append(story_detail)

    return results

@app.put("/stories/{story_id}", response_model=schemas.StoryUpdate)
def update_story(story_id: int, story: schemas.StoryUpdate, db: Session = Depends(get_db)):
    updated_story = crud.update_story(db=db, story_id=story_id, story_update=story)
    return updated_story