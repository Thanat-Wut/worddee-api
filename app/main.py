from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import words, admin

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Vocabulary management microservice for English learning",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(words.router)
app.include_router(admin.router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Service information endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
        "description": "Vocabulary management microservice",
        "endpoints": {
            "public": [
                "GET /api/random - Get random word",
                "GET /api/words - List all words",
                "GET /api/words/{id} - Get word by ID"
            ],
            "admin": [
                "POST /api/admin/words - Create word",
                "PUT /api/admin/words/{id} - Update word",
                "DELETE /api/admin/words/{id} - Delete word"
            ]
        }
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "worddee-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
