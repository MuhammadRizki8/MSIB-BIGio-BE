# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException

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

def update_story(db: Session, story_id: int, story_update: schemas.StoryUpdate):
    # Fetch the existing story
    story = db.query(models.Story).filter(models.Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Update the story fields
    story.title = story_update.title
    story.author = story_update.author
    story.synopsis = story_update.synopsis
    story.category = story_update.category
    story.cover_image = story_update.cover_image
    story.status = story_update.status

    # Add new Tags without removing old ones
    for tag_data in story_update.tags:
        # Create new tag and assign it to the story
        new_tag = models.Tag(tag_name=tag_data.tag_name)
        db.add(new_tag)
        db.commit()  # Save new tag
        db.refresh(new_tag)  # Get its ID after insertion

        # Link new tag with the story
        story_tag = models.StoryTag(story_id=story.id, tag_id=new_tag.id)
        db.add(story_tag)

    # Add new Chapters without removing old ones
    for chapter_data in story_update.chapters:
        # Create new chapter
        new_chapter = models.Chapter(
            story_id=story.id,
            title=chapter_data.title,
            content=chapter_data.content
        )
        db.add(new_chapter)

    db.commit()
    return story