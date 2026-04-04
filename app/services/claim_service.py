"""
Parametric claim engine.
Checks weather triggers, scores for fraud, and auto-processes payouts.
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.worker import Worker
from app.models.claim import Claim, ClaimStatus, TriggerType
from app.models.plan import PlanSubscription
from app.services.weather_service import get_disruption_status
from app.services.fraud_service import compute_fraud_score
from app.core.config import FRAUD_BLOCK_THRESHOLD, PLANS


TRIGGER_MAP = {
    "rain": TriggerType.rain,
    "heat": TriggerType.heat,
    "cold": TriggerType.cold,
    "aqi": TriggerType.aqi,
}

TRIGGER_VALUE_KEY = {
    "rain": "rainfall_mm",
    "heat": "temperature_c",
    "cold": "temperature_c",
    "aqi": "aqi",
}

from app.core.config import RAIN_THRESHOLD_MM, TEMP_HIGH_THRESHOLD_C, TEMP_LOW_THRESHOLD_C, AQI_THRESHOLD

TRIGGER_THRESHOLD_MAP = {
    "rain": RAIN_THRESHOLD_MM,
    "heat": TEMP_HIGH_THRESHOLD_C,
    "cold": TEMP_LOW_THRESHOLD_C,
    "aqi": AQI_THRESHOLD,
}


async def check_and_trigger_claims(worker: Worker, db: AsyncSession) -> list[Claim]:
    """
    Main entry point: called on dashboard load or by cron job.
    Checks weather for the worker's city and auto-creates claims.
    Returns list of newly created claims.
    """
    if not worker.active_plan:
        return []

    # Verify plan is active
    today = datetime.utcnow()
    result = await db.execute(
        select(PlanSubscription).where(
            PlanSubscription.worker_id == worker.id,
            PlanSubscription.is_active == True,
            PlanSubscription.end_date >= today,
        )
    )
    subscription = result.scalar_one_or_none()
    if not subscription:
        return []

    # Check weekly claims cap
    week_start = today - timedelta(days=today.weekday())
    result = await db.execute(
        select(func.count(Claim.id)).where(
            Claim.worker_id == worker.id,
            Claim.triggered_at >= week_start,
            Claim.status != ClaimStatus.rejected,
        )
    )
    claims_this_week = result.scalar_one()
    if claims_this_week >= subscription.max_days_per_week:
        return []  # Cap reached

    # Check if already claimed today
    today_start = today.replace(hour=0, minute=0, second=0)
    result = await db.execute(
        select(Claim).where(
            Claim.worker_id == worker.id,
            Claim.triggered_at >= today_start,
        )
    )
    if result.scalar_one_or_none():
        return []  # Already processed today

    # Fetch live weather
    weather = await get_disruption_status(
        city=worker.city,
        lat=worker.latitude,
        lon=worker.longitude,
    )

    if not weather["is_disruption_day"]:
        return []

    created_claims = []
    for trigger_key in weather["triggers_active"]:
        trigger_type = TRIGGER_MAP.get(trigger_key)
        if not trigger_type:
            continue

        trigger_value = weather.get(TRIGGER_VALUE_KEY[trigger_key]) or 0.0
        threshold = TRIGGER_THRESHOLD_MAP[trigger_key]

        # Fraud scoring
        fraud_score, fraud_flags = await compute_fraud_score(
            worker=worker,
            weather_confirmed=True,
            db=db,
        )

        status = ClaimStatus.rejected if fraud_score >= FRAUD_BLOCK_THRESHOLD else ClaimStatus.approved

        claim = Claim(
            worker_id=worker.id,
            trigger_type=trigger_type,
            trigger_value=trigger_value,
            trigger_threshold=threshold,
            payout_amount=subscription.daily_payout if status == ClaimStatus.approved else 0.0,
            status=status,
            fraud_score=fraud_score,
            fraud_flags=fraud_flags,
            weather_snapshot=weather,
            triggered_at=today,
            processed_at=today,
            is_auto_triggered=True,
        )
        db.add(claim)

        if status == ClaimStatus.approved:
            worker.wallet_balance += subscription.daily_payout
            worker.total_earnings_protected += subscription.daily_payout
            claim.status = ClaimStatus.paid

        created_claims.append(claim)
        break  # One claim per day (primary trigger)

    await db.commit()
    for c in created_claims:
        await db.refresh(c)

    return created_claims


async def simulate_trigger(
    worker: Worker,
    trigger_key: str,
    override_value: float,
    db: AsyncSession,
) -> Claim:
    """
    Hackathon demo mode: manually simulate a weather trigger.
    """
    result = await db.execute(
        select(PlanSubscription).where(
            PlanSubscription.worker_id == worker.id,
            PlanSubscription.is_active == True,
        )
    )
    subscription = result.scalar_one_or_none()

    plan_key = worker.active_plan or "standard"
    plan_config = PLANS.get(plan_key, PLANS["standard"])
    daily_payout = subscription.daily_payout if subscription else plan_config["daily_payout"]

    fraud_score, fraud_flags = await compute_fraud_score(
        worker=worker,
        weather_confirmed=True,
        db=db,
    )

    status = ClaimStatus.rejected if fraud_score >= FRAUD_BLOCK_THRESHOLD else ClaimStatus.paid

    claim = Claim(
        worker_id=worker.id,
        trigger_type=TRIGGER_MAP.get(trigger_key, TriggerType.rain),
        trigger_value=override_value,
        trigger_threshold=TRIGGER_THRESHOLD_MAP.get(trigger_key, RAIN_THRESHOLD_MM),
        payout_amount=daily_payout if status == ClaimStatus.paid else 0.0,
        status=status,
        fraud_score=fraud_score,
        fraud_flags=fraud_flags,
        weather_snapshot={"simulated": True, "value": override_value},
        triggered_at=datetime.utcnow(),
        processed_at=datetime.utcnow(),
        is_auto_triggered=False,
    )
    db.add(claim)

    if status == ClaimStatus.paid:
        worker.wallet_balance += daily_payout
        worker.total_earnings_protected += daily_payout

    await db.commit()
    await db.refresh(claim)
    return claim
