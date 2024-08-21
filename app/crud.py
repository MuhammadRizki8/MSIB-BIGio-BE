# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException
from typing import Optional
from sqlalchemy import or_

def create_story(db: Session, story: schemas.StoryCreate):
    db_story = models.Story(
        title=story.title,
        author=story.author,
        synopsis=story.synopsis,
        category=story.category,
        cover_image=story.cover_image,
        status=story.status
    )
    db.add(db_story)
    db.commit()
    db.refresh(db_story)

    # Add chapters
    for chapter in story.chapters:
        db_chapter = models.Chapter(
            title=chapter.title,
            content=chapter.content,
            story_id=db_story.id
        )
        db.add(db_chapter)

    # Add tags
    for tag in story.tags:
        tag_obj = db.query(models.Tag).filter_by(tag_name=tag.tag_name).first()
        if not tag_obj:
            tag_obj = models.Tag(tag_name=tag.tag_name)
            db.add(tag_obj)
            db.commit()
            db.refresh(tag_obj)
        
        story_tag = models.StoryTag(story_id=db_story.id, tag_id=tag_obj.id)
        db.add(story_tag)

    db.commit()
    db.refresh(db_story)
    return db_story

def get_all_stories_with_tags(db: Session):
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

def get_story_details_by_id(db: Session, story_id: int):
    # Get story by ID
    story = db.query(models.Story).filter(models.Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Get related tags and chapters
    tags = db.query(models.Tag).join(models.StoryTag).filter(models.StoryTag.story_id == story.id).all()
    chapters = db.query(models.Chapter).filter(models.Chapter.story_id == story.id).all()

    # Construct story detail response
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

def search_stories(db: Session, query: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None):
    # Base query to search stories
    stories_query = db.query(models.Story)

    # Filter by title or author if query is provided
    if query:
        stories_query = stories_query.filter(
            or_(
                models.Story.title.ilike(f"%{query}%"),
                models.Story.author.ilike(f"%{query}%")
            )
        )

    # Filter by category if provided
    if category:
        stories_query = stories_query.filter(models.Story.category == category)

    # Filter by status if provided
    if status:
        stories_query = stories_query.filter(models.Story.status == status)

    # Execute the query
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


def update_story(db: Session, story_id: int, story_update: schemas.StoryUpdate):
    # Ambil data story berdasarkan ID
    db_story = db.query(models.Story).filter(models.Story.id == story_id).first()

    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Update data story
    db_story.title = story_update.title
    db_story.author = story_update.author
    db_story.synopsis = story_update.synopsis
    db_story.category = story_update.category
    db_story.cover_image = story_update.cover_image
    db_story.status = story_update.status

    # Update chapters
    db.query(models.Chapter).filter(models.Chapter.story_id == story_id).delete()
    for chapter in story_update.chapters:
        db_chapter = models.Chapter(
            title=chapter.title,
            content=chapter.content,
            story_id=db_story.id
        )
        db.add(db_chapter)

    # Update tags
    db.query(models.StoryTag).filter(models.StoryTag.story_id == story_id).delete()
    for tag in story_update.tags:
        tag_obj = db.query(models.Tag).filter_by(tag_name=tag.tag_name).first()
        if not tag_obj:
            tag_obj = models.Tag(tag_name=tag.tag_name)
            db.add(tag_obj)
            db.commit()
            db.refresh(tag_obj)

        story_tag = models.StoryTag(story_id=db_story.id, tag_id=tag_obj.id)
        db.add(story_tag)

    db.commit()
    db.refresh(db_story)
    return db_story

def delete_story(db: Session, story_id: int):
    # Fetch the story to ensure it exists
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        return None
    
    # Delete the story (will automatically delete related chapters and tags)
    db.delete(story)
    db.commit()
    return story