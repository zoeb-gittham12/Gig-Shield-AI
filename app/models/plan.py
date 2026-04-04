from datetime import datetime
from sqlalchemy import String, Float, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class PlanSubscription(Base):
    __tablename__ = "plan_subscriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    worker_id: Mapped[int] = mapped_column(Integer, ForeignKey("workers.id"), index=True)
    plan_key: Mapped[str] = mapped_column(String(20))   # basic/standard/premium
    weekly_premium: Mapped[float] = mapped_column(Float)
    daily_payout: Mapped[float] = mapped_column(Float)
    max_days_per_week: Mapped[int] = mapped_column(Integer)

    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    premium_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
