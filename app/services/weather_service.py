"""
Weather & AQI service using Open-Meteo (free, no API key required).
Resolves city → lat/lon via Open-Meteo geocoding.
"""
import httpx
from typing import Optional
from app.core.config import (
    OPEN_METEO_BASE, OPEN_METEO_AQI_BASE,
    RAIN_THRESHOLD_MM, TEMP_HIGH_THRESHOLD_C,
    TEMP_LOW_THRESHOLD_C, AQI_THRESHOLD,
)

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Known Indian city coordinates as fallback
CITY_COORDS = {
    "mumbai":    (19.0760, 72.8777),
    "delhi":     (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "chennai":   (13.0827, 80.2707),
    "kolkata":   (22.5726, 88.3639),
    "pune":      (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur":    (26.9124, 75.7873),
    "surat":     (21.1702, 72.8311),
    "vadodara":  (22.3072, 73.1812),
    "lucknow":   (26.8467, 80.9462),
}


async def resolve_coordinates(city: str) -> tuple[float, float]:
    """Get lat/lon for a city name."""
    city_key = city.lower().strip()
    if city_key in CITY_COORDS:
        return CITY_COORDS[city_key]
    
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.get(GEOCODE_URL, params={"name": city, "count": 1, "language": "en"})
            data = r.json()
            if data.get("results"):
                loc = data["results"][0]
                return loc["latitude"], loc["longitude"]
    except Exception:
        pass
    
    # Default to Mumbai if unresolvable
    return 19.0760, 72.8777


async def fetch_weather(lat: float, lon: float) -> dict:
    """Fetch current weather from Open-Meteo."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,rain,weathercode",
        "timezone": "Asia/Kolkata",
        "forecast_days": 1,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(OPEN_METEO_BASE, params=params)
        r.raise_for_status()
        return r.json()


async def fetch_aqi(lat: float, lon: float) -> Optional[float]:
    """Fetch current AQI from Open-Meteo Air Quality API."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "european_aqi",
        "timezone": "Asia/Kolkata",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(OPEN_METEO_AQI_BASE, params=params)
            r.raise_for_status()
            data = r.json()
            return data.get("current", {}).get("european_aqi")
    except Exception:
        return None


async def get_disruption_status(
    city: str,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> dict:
    """
    Master method: returns weather conditions + which parametric
    triggers are currently active for a given location.
    """
    if lat is None or lon is None:
        lat, lon = await resolve_coordinates(city)

    weather_data = await fetch_weather(lat, lon)
    current = weather_data.get("current", {})

    temperature = current.get("temperature_2m", 30.0)
    rainfall = current.get("rain", 0.0) or current.get("precipitation", 0.0)

    aqi = await fetch_aqi(lat, lon)

    triggers = []
    if rainfall >= RAIN_THRESHOLD_MM:
        triggers.append("rain")
    if temperature >= TEMP_HIGH_THRESHOLD_C:
        triggers.append("heat")
    if temperature <= TEMP_LOW_THRESHOLD_C:
        triggers.append("cold")
    if aqi and aqi >= AQI_THRESHOLD:
        triggers.append("aqi")

    return {
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "temperature_c": temperature,
        "rainfall_mm": rainfall,
        "aqi": aqi,
        "triggers_active": triggers,
        "is_disruption_day": len(triggers) > 0,
        "raw": current,
    }
