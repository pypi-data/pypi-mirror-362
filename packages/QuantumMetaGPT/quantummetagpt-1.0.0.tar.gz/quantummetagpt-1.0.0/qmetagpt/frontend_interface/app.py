from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from ..licensing import require_license
from ..utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="QuantumMetaGPT API",
    description="REST API for autonomous quantum AI research agent",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
@require_license(features=['enterprise'])
async def startup_event():
    # Validate license on startup
    logger.info("QuantumMetaGPT API starting with valid enterprise license")
    logger.info("QuantumMetaGPT API started successfully")

@app.get("/health")
def health_check():
    return {"status": "active", "version": "1.0.0"}