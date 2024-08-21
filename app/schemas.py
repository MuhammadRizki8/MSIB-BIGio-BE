# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class CategoryEnum(str, Enum):
    Financial = "Financial"
    Technology = "Technology"
    Health = "Health"
    Fantasy = "Fantasy"
    Sport = "Sport"
    Culture = "Culture"

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


# Schema untuk menampilkan Chapter
class Chapter(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

# Schema untuk menampilkan Tag
class Tag(BaseModel):
    id: int
    tag_name: str

    class Config:
        from_attributes = True

# Schema untuk List Story dengan Tag
class StoryList(BaseModel):
    id: int
    title: str
    author: str
    synopsis: Optional[str]
    category: str
    cover_image: Optional[str]
    status: str
    tags: List[Tag]  # Sertakan tags

    class Config:
        from_attributes = True

# Schema untuk Detail Story dengan Tag dan Chapters
class StoryDetail(BaseModel):
    id: int
    title: str
    author: str
    synopsis: Optional[str]
    category: str
    cover_image: Optional[str]
    status: str
    tags: List[Tag]  # Sertakan tags
    chapters: List[Chapter]  # Sertakan chapters

    class Config:
        from_attributes = True
        
class ChapterBase(BaseModel):
    title: str
    content: str

class TagBase(BaseModel):
    tag_name: str

class ChapterUpdate(BaseModel):
    title: str
    content: str

class TagUpdate(BaseModel):
    tag_name: str

class StoryUpdate(BaseModel):
    title: str
    author: str
    synopsis: Optional[str]
    category: CategoryEnum
    cover_image: Optional[str]
    status: StatusEnum
    chapters: List[ChapterUpdate]
    tags: List[TagUpdate]