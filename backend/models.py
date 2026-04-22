"""SQLAlchemy ORM models for the CRM HCP module."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import enum


class InteractionType(str, enum.Enum):
    DETAIL_AID = "Detail Aid"
    SAMPLE_DROP = "Sample Drop"
    SPEAKER_PROGRAM = "Speaker Program"
    LUNCH_AND_LEARN = "Lunch and Learn"
    VIRTUAL_MEETING = "Virtual Meeting"
    PHONE_CALL = "Phone Call"
    EMAIL = "Email"
    CONFERENCE = "Conference"
    OTHER = "Other"


class Sentiment(str, enum.Enum):
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"
    NEGATIVE = "Negative"


class HCP(Base):
    """Healthcare Professional model."""
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    specialty = Column(String(150), nullable=False)
    institution = Column(String(250), default="")
    email = Column(String(200), default="")
    phone = Column(String(50), default="")
    city = Column(String(100), default="")
    state = Column(String(100), default="")
    tier = Column(String(10), default="B")  # A, B, C
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    interactions = relationship("Interaction", back_populates="hcp", cascade="all, delete-orphan")


class Product(Base):
    """Pharmaceutical product model."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    therapeutic_area = Column(String(200), default="")
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Interaction(Base):
    """Logged interaction with an HCP."""
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"), nullable=False)
    interaction_type = Column(String(50), default="Detail Aid")
    interaction_date = Column(DateTime, default=datetime.utcnow)
    duration_minutes = Column(Integer, default=15)
    products_discussed = Column(String(500), default="")  # Comma-separated product names
    key_topics = Column(Text, default="")
    hcp_feedback = Column(Text, default="")
    sentiment = Column(String(20), default="Neutral")
    follow_up_actions = Column(Text, default="")
    ai_summary = Column(Text, default="")
    raw_notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    hcp = relationship("HCP", back_populates="interactions")
