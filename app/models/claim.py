from datetime import datetime
from sqlalchemy import String, Float, Boolean, DateTime, Integer, ForeignKey, JSON, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum


class TriggerType(str, enum.Enum):
    rain = "rain"
    heat = "heat"
    cold = "cold"
    aqi = "aqi"
    manual = "manual"


class ClaimStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey("workers.id"), index=True)

    trigger_type: Mapped[TriggerType] = mapped_column(SAEnum(TriggerType))
    trigger_value: Mapped[float] = mapped_column(Float)   # e.g., 4.2mm rain
    trigger_threshold: Mapped[float] = mapped_column(Float)

    payout_amount: Mapped[float] = mapped_column(Float)
    status: Mapped[ClaimStatus] = mapped_column(SAEnum(ClaimStatus), default=ClaimStatus.pending)

    # Fraud scoring
    fraud_score: Mapped[float] = mapped_column(Float, default=0.0)
    fraud_flags: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Weather snapshot at time of claim
    weather_snapshot: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Timestamps
    triggered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_auto_triggered: Mapped[bool] = mapped_column(Boolean, default=True)
