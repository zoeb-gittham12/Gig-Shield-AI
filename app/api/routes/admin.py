from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.models.worker import Worker
from app.models.claim import Claim, ClaimStatus
from app.models.plan import PlanSubscription
from app.schemas.schemas import AdminStats
from datetime import datetime

router = APIRouter()

ADMIN_SECRET = "gigshield-admin-2024"  # Replace with env var in production


def verify_admin(x_admin_key: str = Header(...)):
    if x_admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin key")


@router.get("/stats", response_model=AdminStats, dependencies=[Depends(verify_admin)])
async def admin_stats(db: AsyncSession = Depends(get_db)):
    """Overall platform statistics for the admin dashboard."""

    total_workers = (await db.execute(select(func.count(Worker.id)))).scalar_one()

    active_plans = (await db.execute(
        select(func.count(PlanSubscription.id)).where(
            PlanSubscription.is_active == True,
            PlanSubscription.end_date >= datetime.utcnow(),
        )
    )).scalar_one()

    total_claims = (await db.execute(select(func.count(Claim.id)))).scalar_one()

    claims_paid = (await db.execute(
        select(func.count(Claim.id)).where(Claim.status == ClaimStatus.paid)
    )).scalar_one()

    total_payout = (await db.execute(
        select(func.sum(Claim.payout_amount)).where(Claim.status == ClaimStatus.paid)
    )).scalar_one() or 0.0

    high_risk = (await db.execute(
        select(func.count(Worker.id)).where(Worker.risk_score >= 0.7)
    )).scalar_one()

    # Risk zones: cities with most claims
    zone_result = await db.execute(
        select(Worker.city, func.count(Claim.id).label("claim_count"))
        .join(Claim, Claim.worker_id == Worker.id)
        .group_by(Worker.city)
        .order_by(func.count(Claim.id).desc())
        .limit(5)
    )
    risk_zones = [{"city": row.city, "claim_count": row.claim_count} for row in zone_result]

    return AdminStats(
        total_workers=total_workers,
        active_plans=active_plans,
        total_claims=total_claims,
        claims_paid=claims_paid,
        total_payout_amount=total_payout,
        high_risk_workers=high_risk,
        risk_zones=risk_zones,
    )


@router.get("/workers", dependencies=[Depends(verify_admin)])
async def list_workers(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List all registered workers."""
    result = await db.execute(
        select(Worker).order_by(Worker.created_at.desc()).limit(limit).offset(offset)
    )
    workers = result.scalars().all()
    return [
        {
            "id": w.id,
            "name": w.name,
            "mobile": w.mobile,
            "city": w.city,
            "platform": w.platform,
            "active_plan": w.active_plan,
            "wallet_balance": w.wallet_balance,
            "risk_score": w.risk_score,
            "created_at": w.created_at,
        }
        for w in workers
    ]


@router.get("/claims", dependencies=[Depends(verify_admin)])
async def list_claims(
    status: str = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """List all claims, optionally filtered by status."""
    query = select(Claim).order_by(Claim.triggered_at.desc()).limit(limit)
    if status:
        try:
            query = query.where(Claim.status == ClaimStatus(status))
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

    result = await db.execute(query)
    claims = result.scalars().all()
    return [
        {
            "id": c.id,
            "worker_id": c.worker_id,
            "trigger_type": c.trigger_type,
            "trigger_value": c.trigger_value,
            "payout_amount": c.payout_amount,
            "status": c.status,
            "fraud_score": c.fraud_score,
            "triggered_at": c.triggered_at,
        }
        for c in claims
    ]
