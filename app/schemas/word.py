
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.db.models import DifficultyLevel

class WordCreate(BaseModel):
    """Schema for creating a new word"""
    word: str = Field(..., min_length=1, max_length=100)
    definition: str = Field(..., min_length=10)
    difficulty_level: DifficultyLevel
    
    @field_validator('word')
    @classmethod
    def word_must_be_lowercase(cls, v: str) -> str:
        return v.lower().strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "word": "serendipity",
                "definition": "The occurrence of events by chance in a happy way",
                "difficulty_level": "Advanced"
            }
        }

class WordUpdate(BaseModel):
    """Schema for updating an existing word"""
    word: Optional[str] = Field(None, min_length=1, max_length=100)
    definition: Optional[str] = Field(None, min_length=10)
    difficulty_level: Optional[DifficultyLevel] = None
    
    @field_validator('word')
    @classmethod
    def word_must_be_lowercase(cls, v: Optional[str]) -> Optional[str]:
        return v.lower().strip() if v else None

class WordResponse(BaseModel):
    """Schema for word response"""
    id: int
    word: str
    definition: str
    difficulty_level: DifficultyLevel
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "word": "apple",
                "definition": "A round fruit with red, green, or yellow skin",
                "difficulty_level": "Beginner",
                "created_at": "2025-12-12T10:00:00Z"
            }
        }

class WordList(BaseModel):
    """Schema for paginated word list"""
    total: int
    page: int
    page_size: int
    words: list[WordResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total": 30,
                "page": 1,
                "page_size": 10,
                "words": []
            }
        }
