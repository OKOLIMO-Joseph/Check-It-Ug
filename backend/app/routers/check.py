from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.claim import ClaimRequest, VerdictResponse
from app.services.pipeline import pipeline
from app.services.cache import cache_service
from app.database import get_db
from app.models.db_models import ClaimLog
import uuid

router = APIRouter(prefix="/api/v1", tags=["check"])

@router.post("/check", response_model=VerdictResponse)
async def check_claim(
    request: ClaimRequest,
    db: AsyncSession = Depends(get_db)
):
    # Check cache first
    cached = await cache_service.get(request.text)
    if cached:
        return cached
    
    # Run pipeline
    result = await pipeline.run_pipeline(request.text, request.lang)
    
    # Store in database asynchronously
    claim_log = ClaimLog(
        id=uuid.uuid4(),
        raw_text=request.text,
        claim_normalised=result.claim_normalised,
        verdict=result.verdict.value,
        confidence=result.confidence,
        explanation=result.explanation,
        sources=result.sources,
        lang=result.lang.value,
        source_channel=request.source.value
    )
    db.add(claim_log)
    await db.commit()
    
    # Cache result
    await cache_service.set(request.text, result)
    
    return result