"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ─── HCP Schemas ─────────────────────────────────────────────────────────
class HCPBase(BaseModel):
    first_name: str
    last_name: str
    specialty: str
    institution: Optional[str] = ""
    email: Optional[str] = ""
    phone: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    tier: Optional[str] = "B"
    notes: Optional[str] = ""


class HCPCreate(HCPBase):
    pass


class HCPResponse(HCPBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Product Schemas ─────────────────────────────────────────────────────
class ProductBase(BaseModel):
    name: str
    therapeutic_area: Optional[str] = ""
    description: Optional[str] = ""


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


# ─── Interaction Schemas ─────────────────────────────────────────────────
class InteractionBase(BaseModel):
    hcp_id: int
    interaction_type: Optional[str] = "Detail Aid"
    interaction_date: Optional[datetime] = None
    duration_minutes: Optional[int] = 15
    products_discussed: Optional[str] = ""
    key_topics: Optional[str] = ""
    hcp_feedback: Optional[str] = ""
    sentiment: Optional[str] = "Neutral"
    follow_up_actions: Optional[str] = ""
    raw_notes: Optional[str] = ""


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    interaction_type: Optional[str] = None
    interaction_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    products_discussed: Optional[str] = None
    key_topics: Optional[str] = None
    hcp_feedback: Optional[str] = None
    sentiment: Optional[str] = None
    follow_up_actions: Optional[str] = None
    raw_notes: Optional[str] = None


class InteractionResponse(InteractionBase):
    id: int
    ai_summary: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
    hcp: Optional[HCPResponse] = None

    class Config:
        from_attributes = True


# ─── Chat Schemas ────────────────────────────────────────────────────────
class ChatMessage(BaseModel):
    message: str
    hcp_id: Optional[int] = None


class ChatResponse(BaseModel):
    reply: str
    interaction_data: Optional[dict] = None
    action_taken: Optional[str] = None
