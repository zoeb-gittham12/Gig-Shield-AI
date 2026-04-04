from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from app.models.worker import Platform
from app.models.claim import TriggerType, ClaimStatus


# ── Auth ──────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name: str
    mobile: str
    password: str
    city: str
    platform: Platform = Platform.zomato
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator("mobile")
    @classmethod
    def mobile_must_be_10_digits(cls, v):
        digits = v.replace("+91", "").replace(" ", "")
        if not digits.isdigit() or len(digits) < 10:
            raise ValueError("Enter a valid 10-digit mobile number")
        return digits


class LoginRequest(BaseModel):
    mobile: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    worker_id: int
    name: str


# ── Worker ────────────────────────────────────────────────────────
class WorkerProfile(BaseModel):
    id: int
    name: str
    mobile: str
    city: str
    platform: Platform
    active_plan: Optional[str]
    wallet_balance: float
    total_earnings_protected: float
    risk_score: float
    plan_end_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Plans ─────────────────────────────────────────────────────────
class PlanInfo(BaseModel):
    key: str
    name: str
    weekly_premium: int
    daily_payout: int
    max_days_per_week: int
    description: str


class PlanSelectRequest(BaseModel):
    plan_key: str  # basic / standard / premium
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class PlanSelectResponse(BaseModel):
    message: str
    plan: PlanInfo
    subscription_id: int
    end_date: datetime


# ── Claims ────────────────────────────────────────────────────────
class ClaimOut(BaseModel):
    id: int
    trigger_type: TriggerType
    trigger_value: float
    payout_amount: float
    status: ClaimStatus
    fraud_score: float
    triggered_at: datetime
    processed_at: Optional[datetime]
    weather_snapshot: Optional[dict]

    class Config:
        from_attributes = True


# ── Weather / Trigger ──────────────────────────────────────────────
class WeatherStatus(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature_c: float
    rainfall_mm: float
    aqi: Optional[float]
    triggers_active: list[str]
    is_disruption_day: bool


# ── Admin ─────────────────────────────────────────────────────────
class AdminStats(BaseModel):
    total_workers: int
    active_plans: int
    total_claims: int
    claims_paid: int
    total_payout_amount: float
    high_risk_workers: int
    risk_zones: list[dict]
