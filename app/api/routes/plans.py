from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_worker
from app.core.config import PLANS
from app.models.worker import Worker
from app.models.plan import PlanSubscription
from app.schemas.schemas import PlanInfo, PlanSelectRequest, PlanSelectResponse

router = APIRouter()


@router.get("/", response_model=list[PlanInfo])
async def list_plans():
    """Return all available protection plans."""
    return [
        PlanInfo(key=k, **v)
        for k, v in PLANS.items()
    ]


@router.post("/subscribe", response_model=PlanSelectResponse)
async def subscribe_plan(
    payload: PlanSelectRequest,
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    plan_config = PLANS.get(payload.plan_key)
    if not plan_config:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {payload.plan_key}")

    # Deactivate any existing plan
    result = await db.execute(
        select(PlanSubscription).where(
            PlanSubscription.worker_id == worker.id,
            PlanSubscription.is_active == True,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.is_active = False

    # Update location if provided
    if payload.latitude:
        worker.latitude = payload.latitude
    if payload.longitude:
        worker.longitude = payload.longitude

    start = datetime.utcnow()
    end = start + timedelta(weeks=1)

    subscription = PlanSubscription(
        worker_id=worker.id,
        plan_key=payload.plan_key,
        weekly_premium=plan_config["weekly_premium"],
        daily_payout=plan_config["daily_payout"],
        max_days_per_week=plan_config["max_days_per_week"],
        start_date=start,
        end_date=end,
        is_active=True,
        premium_paid=True,  # Simulate payment success for hackathon
    )
    db.add(subscription)

    worker.active_plan = payload.plan_key
    worker.plan_start_date = start
    worker.plan_end_date = end

    await db.commit()
    await db.refresh(subscription)

    return PlanSelectResponse(
        message=f"Successfully subscribed to {plan_config['name']}",
        plan=PlanInfo(key=payload.plan_key, **plan_config),
        subscription_id=subscription.id,
        end_date=end,
    )


@router.get("/premium-calculator")
async def premium_calculator(
    weekly_income: float,
    city: str,
    platform: str = "zomato",
):
    """
    Recommends the best plan based on estimated weekly income.
    Higher earners benefit more from premium plans.
    """
    if weekly_income >= 3000:
        recommended = "premium"
    elif weekly_income >= 1500:
        recommended = "standard"
    else:
        recommended = "basic"

    plan = PLANS[recommended]
    coverage_ratio = (plan["daily_payout"] * plan["max_days_per_week"]) / max(weekly_income, 1)

    return {
        "weekly_income": weekly_income,
        "recommended_plan": recommended,
        "plan_details": plan,
        "estimated_coverage_ratio": round(coverage_ratio, 2),
        "break_even_days": round(plan["weekly_premium"] / plan["daily_payout"], 2),
        "city": city,
        "platform": platform,
    }
