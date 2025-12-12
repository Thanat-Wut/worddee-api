"""
════════════════════════════════════════════════════════════════════
WORDDEE-API - Main Application
════════════════════════════════════════════════════════════════════
Vocabulary management microservice for Worddee.ai platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Create FastAPI application
app = FastAPI(
   title="Worddee API",
   description="Vocabulary management microservice for English learning",
   version="1.0.0",
   docs_url="/docs",
   redoc_url="/redoc"
)
# CORS Configuration
app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],  # TODO: Configure from environment
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
# Root endpoint
@app.get("/")
async def root():
   """Service information endpoint"""
   return {
       "service": "Worddee API",
       "version": "1.0.0",
       "status": "running",
       "docs": "/docs",
       "description": "Vocabulary management microservice"
   }
# Health check endpoint
@app.get("/health")
async def health_check():
   """Health check endpoint for monitoring"""
   return {
       "status": "healthy",
       "service": "worddee-api"
   }
if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
