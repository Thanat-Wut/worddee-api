"""
════════════════════════════════════════════════════════════════════
WORDDEE-API - Admin Word Endpoints (Protected)
════════════════════════════════════════════════════════════════════
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import verify_api_key
from app.schemas.word import WordCreate, WordUpdate, WordResponse
from app.services.word_service import WordService

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"],
    dependencies=[Depends(verify_api_key)]
)

@router.post("/words", response_model=WordResponse, status_code=status.HTTP_201_CREATED)
async def create_word(
    word_data: WordCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Create a new word (Admin only)
    
    Requires `X-API-Key` header with valid admin API key.
    """
    word = WordService.create_word(db, word_data)
    return word

@router.put("/words/{word_id}", response_model=WordResponse)
async def update_word(
    word_id: int,
    word_data: WordUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Update an existing word (Admin only)
    
    Requires `X-API-Key` header with valid admin API key.
    """
    word = WordService.update_word(db, word_id, word_data)
    return word

@router.delete("/words/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """
    Delete a word (Admin only)
    
    Requires `X-API-Key` header with valid admin API key.
    """
    WordService.delete_word(db, word_id)
    return None
