from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.core.security import get_current_worker
from app.models.worker import Worker
from app.schemas.schemas import WeatherStatus
from app.services.weather_service import get_disruption_status

router = APIRouter()


@router.get("/status", response_model=WeatherStatus)
async def weather_status(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    worker: Worker = Depends(get_current_worker),
):
    """
    Returns live weather + active disruption triggers for a city.
    Uses worker's registered city/location if not specified.
    """
    target_city = city or worker.city
    target_lat = lat or worker.latitude
    target_lon = lon or worker.longitude

    result = await get_disruption_status(
        city=target_city,
        lat=target_lat,
        lon=target_lon,
    )
    return WeatherStatus(**{k: v for k, v in result.items() if k != "raw"})


@router.get("/status/public")
async def weather_status_public(
    city: str = Query(..., description="City name e.g. Mumbai"),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    """
    Public endpoint (no auth) for checking weather triggers.
    Useful for the onboarding screen before login.
    """
    result = await get_disruption_status(city=city, lat=lat, lon=lon)
    return {
        "city": result["city"],
        "temperature_c": result["temperature_c"],
        "rainfall_mm": result["rainfall_mm"],
        "aqi": result["aqi"],
        "triggers_active": result["triggers_active"],
        "is_disruption_day": result["is_disruption_day"],
    }
