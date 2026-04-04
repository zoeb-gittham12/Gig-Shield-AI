from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import get_current_worker
from app.models.worker import Worker
from app.schemas.schemas import WorkerProfile
from app.services.claim_service import check_and_trigger_claims

router = APIRouter()


@router.get("/me", response_model=WorkerProfile)
async def get_profile(
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    """Get current worker profile. Also auto-checks for weather triggers."""
    # Auto-trigger check on each dashboard load
    await check_and_trigger_claims(worker, db)
    await db.refresh(worker)
    return worker


@router.patch("/me/location")
async def update_location(
    latitude: float,
    longitude: float,
    worker: Worker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    """Update worker's GPS coordinates for accurate weather checks."""
    worker.latitude = latitude
    worker.longitude = longitude
    await db.commit()
    return {"message": "Location updated", "latitude": latitude, "longitude": longitude}
