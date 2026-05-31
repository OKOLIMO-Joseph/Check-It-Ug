from sqlalchemy import Column, String, DateTime, Float, JSON, Integer, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class ClaimLog(Base):
    __tablename__ = "claim_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_text = Column(String, nullable=False)
    claim_normalised = Column(String, nullable=False)
    verdict = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(String, nullable=False)
    sources = Column(JSON, nullable=False)
    lang = Column(String, nullable=False)
    source_channel = Column(String, nullable=False)
    phone_hash = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)