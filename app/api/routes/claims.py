from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.security import get_current_worker
from app.models.worker import Worker
from app.models.claim import Claim
from app.schemas.schemas import ClaimOut
from app.services.claim_service import check_and_trigger_claims, simulate_trigger

router = APIRouter()


@router.get("/", response_model=list[ClaimOut])
async def get_claim_history(
    limit: int = 20,
    offset: int = 0,
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    """Payout history for the logged-in worker."""
    result = await db.execute(
        select(Claim)
        .where(Claim.worker_id == worker.id)
        .order_by(desc(Claim.triggered_at))
        .limit(limit)
        .offset(offset)
    )
    return result.scalars().all()


@router.post("/check-triggers", response_model=list[ClaimOut])
async def check_triggers(
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    """
    Manually force a weather trigger check for the worker's city.
    Returns any newly created claims.
    """
    claims = await check_and_trigger_claims(worker, db)
    return claims


@router.post("/simulate", response_model=ClaimOut)
async def simulate_claim(
    trigger: str = "rain",
    value: float = 5.0,
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    """
    Hackathon demo: simulate a weather trigger manually.
    trigger: rain | heat | cold | aqi
    value: the simulated sensor reading
    """
    valid_triggers = ["rain", "heat", "cold", "aqi"]
    if trigger not in valid_triggers:
        raise HTTPException(status_code=400, detail=f"trigger must be one of {valid_triggers}")

    if not worker.active_plan:
        raise HTTPException(status_code=400, detail="Worker has no active plan. Subscribe first.")

    claim = await simulate_trigger(worker, trigger, value, db)
    return claim
