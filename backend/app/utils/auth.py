from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

def create_token(username: str) -> str:
    """Create JWT token for admin"""
    expire = datetime.utcnow() + timedelta(hours=24)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> bool:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("sub") == settings.ADMIN_USERNAME
    except JWTError:
        return False