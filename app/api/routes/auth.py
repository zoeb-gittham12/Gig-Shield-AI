from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.worker import Worker
from app.schemas.schemas import RegisterRequest, LoginRequest, TokenResponse

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check duplicate mobile
    result = await db.execute(select(Worker).where(Worker.mobile == payload.mobile))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Mobile number already registered")

    worker = Worker(
        name=payload.name,
        mobile=payload.mobile,
        password_hash=hash_password(payload.password),
        city=payload.city,
        platform=payload.platform,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(worker)
    await db.commit()
    await db.refresh(worker)

    token = create_access_token({"sub": str(worker.id)})
    return TokenResponse(
        access_token=token,
        worker_id=worker.id,
        name=worker.name,
    )


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Worker).where(Worker.mobile == payload.mobile))
    worker = result.scalar_one_or_none()

    if not worker or not verify_password(payload.password, worker.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile or password",
        )

    token = create_access_token({"sub": str(worker.id)})
    return TokenResponse(
        access_token=token,
        worker_id=worker.id,
        name=worker.name,
    )
