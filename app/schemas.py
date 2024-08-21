# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class CategoryEnum(str, Enum):
    Financial = "Financial"
    Technology = "Technology"
    Health = "Health"

class StatusEnum(str, Enum):
    Publish = "Publish"
    Draft = "Draft"

class ChapterCreate(BaseModel):
    title: str
    content: str

class TagCreate(BaseModel):
    tag_name: str

class StoryCreate(BaseModel):
    title: str
    author: str
    synopsis: Optional[str]
    category: CategoryEnum
    cover_image: Optional[str]
    status: StatusEnum
    chapters: Optional[List[ChapterCreate]] = []
    tags: Optional[List[TagCreate]] = []
