# schema.py
from pydantic import BaseModel, Field
from typing import Literal

class EmailAnalysis(BaseModel):
    sender_intent: Literal["billing", "bug_report", "feature_request", "sales_inquiry", "churn_risk", "general"]
    urgency_score: int = Field(ge=1, le=5, description="1 (low) to 5 (critical)")
    tone: Literal["neutral", "frustrated", "angry", "confused", "positive"]
    action_required: str