from datetime import datetime
from sqlalchemy import String, Float, Boolean, DateTime, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
import enum


class Platform(str, enum.Enum):
    zomato = "zomato"
    swiggy = "swiggy"
    both = "both"


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    mobile: Mapped[str] = mapped_column(String(15), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    platform: Mapped[Platform] = mapped_column(SAEnum(Platform), default=Platform.zomato)

    # Plan
    active_plan: Mapped[str | None] = mapped_column(String(20), nullable=True)  # basic/standard/premium
    plan_start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    plan_end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Financials
    wallet_balance: Mapped[float] = mapped_column(Float, default=0.0)
    total_earnings_protected: Mapped[float] = mapped_column(Float, default=0.0)

    # Risk
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1

    # Metadata
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
