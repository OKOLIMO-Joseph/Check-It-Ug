import redis.asyncio as redis
import hashlib
import json
from app.config import settings
from app.models.claim import VerdictResponse

class CacheService:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    def _hash_key(self, claim: str) -> str:
        """Create hash key for claim"""
        normalized = claim.lower().strip()
        return hashlib.sha256(normalized.encode()).hexdigest()
    
    async def get(self, claim: str) -> VerdictResponse | None:
        """Get cached result"""
        key = self._hash_key(claim)
        cached = await self.redis.get(key)
        if cached:
            data = json.loads(cached)
            return VerdictResponse(**data, cached=True)
        return None
    
    async def set(self, claim: str, response: VerdictResponse):
        """Cache result"""
        key = self._hash_key(claim)
        data = response.model_dump()
        await self.redis.setex(key, settings.CACHE_TTL, json.dumps(data))

cache_service = CacheService()