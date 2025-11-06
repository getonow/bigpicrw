from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AnalyzePartRequest, AnalyzePartResponse
from app.agent import analyze_part
from app.config import OPENAI_API_KEY
from app.supabase_client import SUPABASE_URL, SUPABASE_ANON_KEY
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="BIGPICTURE AI Agent")

# Add CORS middleware for frontend integration
# In production, you should specify your actual frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Log configuration status on startup"""
    logger.info("Starting BIGPICTURE AI Agent...")
    logger.info(f"OpenAI API Key configured: {bool(OPENAI_API_KEY)}")
    logger.info(f"Supabase URL configured: {bool(SUPABASE_URL)}")
    logger.info(f"Supabase Key configured: {bool(SUPABASE_ANON_KEY)}")
    port = os.getenv("PORT", "8000")
    logger.info(f"Server will listen on port: {port}")

@app.get("/")
async def root():
    return {"message": "BIGPICTURE AI Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint - should always return 200 if service is running"""
    try:
        # Check if critical services are configured
        config_status = {
            "openai_configured": bool(OPENAI_API_KEY),
            "supabase_configured": bool(SUPABASE_URL and SUPABASE_ANON_KEY)
        }
        
        return {
            "status": "healthy",
            "service": "BIGPICTURE AI Agent",
            "config": config_status
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        # Still return 200 to indicate service is running
        return {
            "status": "healthy",
            "service": "BIGPICTURE AI Agent",
            "error": str(e)
        }

@app.post("/analyze-part/", response_model=AnalyzePartResponse)
async def analyze_part_endpoint(request: AnalyzePartRequest):
    try:
        result = await analyze_part(None, request.message)
        return AnalyzePartResponse(**result)
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 