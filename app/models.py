# app/models.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
import enum

class CategoryEnum(str, enum.Enum):
    Financial = "Financial"
    Technology = "Technology"
    Health = "Health"

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
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    chapters = relationship("Chapter", back_populates="story")
    tags = relationship("StoryTag", back_populates="story")

class Chapter(Base):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP")

    story = relationship("Story", back_populates="chapters")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(255), unique=True, nullable=True)

class StoryTag(Base):
    __tablename__ = "story_tags"
    story_id = Column(Integer, ForeignKey("stories.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    story = relationship("Story", back_populates="tags")
    tag = relationship("Tag")
