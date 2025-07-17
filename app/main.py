from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import AnalyzePartRequest, AnalyzePartResponse
from app.agent import analyze_part
import os

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

@app.get("/")
async def root():
    return {"message": "BIGPICTURE AI Agent API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "BIGPICTURE AI Agent"}

@app.post("/analyze-part/", response_model=AnalyzePartResponse)
async def analyze_part_endpoint(request: AnalyzePartRequest):
    result = await analyze_part(None, request.message)
    return AnalyzePartResponse(**result) 