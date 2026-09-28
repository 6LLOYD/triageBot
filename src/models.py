from enum import Enum
from pydantic import BaseModel, Field

class TicketCategory(str, Enum):
    BUG = "bug"
    PAYMENT = "payment"
    ACCOUNT = "account"
    SUGGESTION = "suggestion"
    TOXICITY = "toxicity"
    OTHER = "autre"

class TicketSentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"

class TicketAnalysis(BaseModel):
    category: TicketCategory
    severity: int = Field(ge=1, le=5)
    sentiment: TicketSentiment
    summary: str