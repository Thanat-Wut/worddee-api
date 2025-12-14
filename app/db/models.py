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
    """Word model - stores vocabulary entries"""
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, nullable=False, index=True)
    definition = Column(Text, nullable=False)
    difficulty_level = Column(
        Enum(DifficultyLevel, name="difficulty_enum"),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Word(id={self.id}, word='{self.word}', level={self.difficulty_level.value})>"
