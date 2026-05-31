from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.db_models import ClaimLog
from app.utils.auth import verify_token
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/v1", tags=["admin"])

async def admin_required(token: str = Query(...)):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

@router.get("/trends")
async def get_trends(
    days: int = 7,
    admin: bool = Depends(admin_required),
    db: AsyncSession = Depends(get_db)
):
    since_date = datetime.utcnow() - timedelta(days=days)
    
    # Daily breakdown
    daily_query = select(
        func.date(ClaimLog.created_at).label('date'),
        ClaimLog.verdict,
        func.count().label('count')
    ).where(ClaimLog.created_at >= since_date).group_by('date', ClaimLog.verdict)
    
    result = await db.execute(daily_query)
    daily_data = result.all()
    
    # Top claims
    top_claims_query = select(
        ClaimLog.claim_normalised,
        func.count().label('count')
    ).where(ClaimLog.created_at >= since_date).group_by(ClaimLog.claim_normalised).order_by(func.count().desc()).limit(20)
    
    top_result = await db.execute(top_claims_query)
    top_claims = top_result.all()
    
    return {
        "daily_breakdown": [{"date": str(r[0]), "verdict": r[1], "count": r[2]} for r in daily_data],
        "top_claims": [{"claim": r[0], "count": r[1]} for r in top_claims]
    }

@router.get("/claims")
async def get_claims(
    page: int = 1,
    limit: int = 50,
    verdict: Optional[str] = None,
    admin: bool = Depends(admin_required),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * limit
    
    query = select(ClaimLog)
    if verdict:
        query = query.where(ClaimLog.verdict == verdict)
    
    query = query.offset(offset).limit(limit).order_by(ClaimLog.created_at.desc())
    
    result = await db.execute(query)
    claims = result.scalars().all()
    
    return {
        "claims": [{
            "id": str(c.id),
            "text": c.raw_text[:200],
            "verdict": c.verdict,
            "created_at": c.created_at.isoformat()
        } for c in claims],
        "page": page,
        "limit": limit
    }