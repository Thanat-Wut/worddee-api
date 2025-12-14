from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from fastapi import HTTPException, status
from app.db.models import Word, DifficultyLevel
from app.schemas.word import WordCreate, WordUpdate

class WordService:
    @staticmethod
    def get_random_word(db: Session, difficulty: Optional[DifficultyLevel] = None) -> Word:
        query = db.query(Word)
        
        if difficulty:
            query = query.filter(Word.difficulty_level == difficulty)
        
        # Get random word using PostgreSQL RANDOM()
        word = query.order_by(func.random()).first()
        
        if not word:
            level_msg = f" at {difficulty.value} level" if difficulty else ""
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No words found{level_msg}"
            )
        
        return word
    
    @staticmethod
    def get_words(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        difficulty: Optional[DifficultyLevel] = None,
        search: Optional[str] = None
    ) -> tuple[List[Word], int]:
        query = db.query(Word)
        
        # Apply filters
        if difficulty:
            query = query.filter(Word.difficulty_level == difficulty)
        
        if search:
            search_term = f"%{search.lower()}%"
            query = query.filter(
                (Word.word.ilike(search_term)) | 
                (Word.definition.ilike(search_term))
            )
        
        # Get total count
        total = query.count()
        
        # Get paginated results
        words = query.offset(skip).limit(limit).all()
        
        return words, total
    
    @staticmethod
    def get_word_by_id(db: Session, word_id: int) -> Word:
        
        word = db.query(Word).filter(Word.id == word_id).first()
        
        if not word:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Word with ID {word_id} not found"
            )
        
        return word
    
    @staticmethod
    def create_word(db: Session, word_data: WordCreate) -> Word:
       
        # Check if word already exists
        existing = db.query(Word).filter(Word.word == word_data.word).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Word '{word_data.word}' already exists with ID {existing.id}"
            )
        
        # Create new word
        db_word = Word(**word_data.model_dump())
        db.add(db_word)
        db.commit()
        db.refresh(db_word)
        
        return db_word
    
    @staticmethod
    def update_word(db: Session, word_id: int, word_data: WordUpdate) -> Word:
        # Get existing word
        word = WordService.get_word_by_id(db, word_id)
        
        # Check for word name conflict if word is being updated
        if word_data.word and word_data.word != word.word:
            existing = db.query(Word).filter(Word.word == word_data.word).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Word '{word_data.word}' already exists with ID {existing.id}"
                )
        
        # Update fields
        update_data = word_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(word, field, value)
        
        db.commit()
        db.refresh(word)
        
        return word
    
    @staticmethod
    def delete_word(db: Session, word_id: int) -> None:
        word = WordService.get_word_by_id(db, word_id)
        db.delete(word)
        db.commit()
