"""
════════════════════════════════════════════════════════════════════
WORDDEE-API - Database Models
════════════════════════════════════════════════════════════════════
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class DifficultyLevel(enum.Enum):
    """Difficulty level enumeration"""
    Beginner = "Beginner"
    Intermediate = "Intermediate"
    Advanced = "Advanced"

class Word(Base):
    """
    Word model - stores vocabulary entries
    
    Attributes:
        id: Primary key
        word: The word itself (lowercase, unique)
        definition: Word definition
        part_of_speech: e.g., noun, verb, adjective
        pronunciation: IPA pronunciation
        difficulty_level: Beginner, Intermediate, or Advanced
        image_url: Optional image URL
        example_sentence: Usage example
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False, index=True)
    definition = Column(Text, nullable=False)
    part_of_speech = Column(String(50))
    pronunciation = Column(String(100))
    difficulty_level = Column(
        Enum(DifficultyLevel, name="difficulty_enum"),
        nullable=False,
        index=True
    )
    image_url = Column(Text)
    example_sentence = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def __repr__(self):
        return f"<Word(id={self.id}, word='{self.word}', level={self.difficulty_level.value})>"
