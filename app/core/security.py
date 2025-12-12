"""
════════════════════════════════════════════════════════════════════
WORDDEE-API - Security & Authentication
════════════════════════════════════════════════════════════════════
"""
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings

# API Key Header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Verify admin API key for protected endpoints
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        str: Verified API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required. Please provide X-API-Key header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key. Access denied.",
        )
    
    return api_key
