# app/models.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base
import enum

class CategoryEnum(str, enum.Enum):
    Financial = "Financial"
    Technology = "Technology"
    Health = "Health"
    Fantasy = "Fantasy"
    Sport = "Sport"
    Culture = "Culture"

class StatusEnum(str, enum.Enum):
    Publish = "Publish"
    Draft = "Draft"

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    synopsis = Column(Text)
    category = Column(Enum(CategoryEnum), nullable=False)
    cover_image = Column(String(255), nullable=True)
    status = Column(Enum(StatusEnum), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    chapters = relationship("Chapter", back_populates="story", cascade="all, delete-orphan")
    story_tags = relationship("StoryTag", back_populates="story", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    story = relationship("Story", back_populates="chapters")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(255), unique=True, nullable=True)

    story_tags = relationship("StoryTag", back_populates="tag")

class StoryTag(Base):
    __tablename__ = "story_tags"

    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
    
    story = relationship("Story", back_populates="story_tags")
    tag = relationship("Tag", back_populates="story_tags")
