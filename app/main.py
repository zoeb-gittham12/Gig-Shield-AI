from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, workers, plans, claims, weather, admin
from app.core.database import init_db

app = FastAPI(
    title="GigShield AI",
    description="Parametric income protection for food delivery workers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://gigshield-ai-demo.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth.router,    prefix="/api/v1/auth",    tags=["Auth"])
app.include_router(workers.router, prefix="/api/v1/workers", tags=["Workers"])
app.include_router(plans.router,   prefix="/api/v1/plans",   tags=["Plans"])
app.include_router(claims.router,  prefix="/api/v1/claims",  tags=["Claims"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(admin.router,   prefix="/api/v1/admin",   tags=["Admin"])

@app.get("/health")
async def health():
    return {"status": "ok", "service": "GigShield AI"}
