# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

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
