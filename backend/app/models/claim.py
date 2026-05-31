from pydantic import BaseModel
from enum import Enum
from typing import List, Optional

class Lang(str, Enum):
    en = "en"
    lg = "lg"
    nyn = "nyn"

class Source(str, Enum):
    web = "web"
    whatsapp = "whatsapp"
    sms = "sms"

class Verdict(str, Enum):
    true = "true"
    false = "false"
    misleading = "misleading"
    unverifiable = "unverifiable"

class ClaimRequest(BaseModel):
    text: str
    lang: Lang = Lang.en
    source: Source = Source.web

class VerdictResponse(BaseModel):
    verdict: Verdict
    confidence: float
    explanation: str
    sources: List[str]
    claim_normalised: str
    lang: Lang
    cached: bool = False