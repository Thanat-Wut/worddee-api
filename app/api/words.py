from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.database import get_db
from app.db.models import DifficultyLevel
from app.schemas.word import WordResponse, WordList
from app.services.word_service import WordService

router = APIRouter(prefix="/api", tags=["Words"])

@router.get("/random", response_model=WordResponse)
async def get_random_word(
    difficulty: Optional[DifficultyLevel] = Query(
        None,
        description="Filter by difficulty level"
    ),
    db: Session = Depends(get_db)
):
    word = WordService.get_random_word(db, difficulty)
    return word

@router.get("/words", response_model=WordList)
async def list_words(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search in word or definition"),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    words, total = WordService.get_words(db, skip, page_size, difficulty, search)
    
    return WordList(
        total=total,
        page=page,
        page_size=page_size,
        words=words
    )
@router.get("/words/{word_id}", response_model=WordResponse)
async def get_word(
    word_id: int,
    db: Session = Depends(get_db)
):
    word = WordService.get_word_by_id(db, word_id)
    return word
