"""
AI-based fraud scoring for claims.
Uses heuristics + rule engine (easily swappable for an ML model).
Score: 0.0 (clean) → 1.0 (high fraud risk)
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.worker import Worker
from app.models.claim import Claim, ClaimStatus


async def compute_fraud_score(
    worker: Worker,
    weather_confirmed: bool,
    db: AsyncSession,
) -> tuple[float, dict]:
    """
    Returns (fraud_score, flags_dict).
    Flags explain which signals contributed.
    """
    flags = {}
    score = 0.0

    # 1. Account age — new accounts filing claims are suspicious
    account_age_days = (datetime.utcnow() - worker.created_at).days
    if account_age_days < 3:
        flags["new_account"] = True
        score += 0.35
    elif account_age_days < 7:
        flags["young_account"] = True
        score += 0.15

    # 2. Claim frequency in last 7 days
    week_ago = datetime.utcnow() - timedelta(days=7)
    result = await db.execute(
        select(func.count(Claim.id)).where(
            Claim.worker_id == worker.id,
            Claim.triggered_at >= week_ago,
            Claim.status != ClaimStatus.rejected,
        )
    )
    recent_claims = result.scalar_one()

    if recent_claims >= 6:
        flags["excessive_claims"] = True
        score += 0.30
    elif recent_claims >= 4:
        flags["high_claim_frequency"] = True
        score += 0.15

    # 3. Weather not confirmed by external data
    if not weather_confirmed:
        flags["weather_unconfirmed"] = True
        score += 0.35

    # 4. No location provided — can't verify
    if worker.latitude is None or worker.longitude is None:
        flags["no_location"] = True
        score += 0.10

    return min(score, 1.0), flags
