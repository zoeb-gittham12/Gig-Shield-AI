import os

# Weather API (Open-Meteo is free, no key required)
OPEN_METEO_BASE = "https://api.open-meteo.com/v1/forecast"
# For Air Quality we use Open-Meteo AQI endpoint
OPEN_METEO_AQI_BASE = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Parametric trigger thresholds
RAIN_THRESHOLD_MM = 2.5        # mm/hr — heavy rain disruption
TEMP_HIGH_THRESHOLD_C = 42.0   # °C — extreme heat
TEMP_LOW_THRESHOLD_C = 5.0     # °C — extreme cold
AQI_THRESHOLD = 200            # AQI index — hazardous air

# Premium plans (weekly)
PLANS = {
    "basic": {
        "name": "Basic Shield",
        "weekly_premium": 29,
        "daily_payout": 250,
        "max_days_per_week": 3,
        "description": "Essential protection for occasional disruptions",
    },
    "standard": {
        "name": "Standard Shield",
        "weekly_premium": 35,
        "daily_payout": 300,
        "max_days_per_week": 5,
        "description": "Balanced protection for regular workers",
    },
    "premium": {
        "name": "Premium Shield",
        "weekly_premium": 49,
        "daily_payout": 500,
        "max_days_per_week": 7,
        "description": "Full protection for daily delivery professionals",
    },
}

# Fraud scoring weights
FRAUD_SCORE_WEIGHTS = {
    "account_age_days": 0.2,
    "claim_frequency": 0.3,
    "weather_confirmation": 0.4,
    "location_consistency": 0.1,
}
FRAUD_BLOCK_THRESHOLD = 0.75  # Block claims above this score
