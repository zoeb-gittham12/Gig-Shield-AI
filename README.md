# Gig-Shield-AI
AI-powered parametric insurance for delivery workers

## Inspiration

Delivery workers are crucial to India's gig economy, but they often lose income due to factors beyond their control, such as heavy rain, extreme heat, pollution, and curfews. This motivated us to create a solution that safeguards their daily earnings using AI and automation.

## What it does

GigShield AI is an AI-powered insurance platform that provides automatic compensation to delivery workers for income loss caused by environmental disruptions. Instead of going through manual claims, payouts occur automatically based on real-time data, like weather conditions and location.

## How we built it

We developed a system that includes a mix of frontend, backend, and AI-based logic:

Frontend: Mobile/Web interface for onboarding and user dashboard
Backend: API system for managing user data, claims, and payouts
AI/ML: Models for predicting risk and detecting fraud 
APIs: Weather API, location tracking, and mock payment integration 

We also set up a multi-layer anti-spoofing system that uses behavioral analysis, device data, and anomaly detection to stop GPS spoofing fraud. 

## Adversarial Defense & Anti-Spoofing Strategy

### The Differentiation
Our system goes beyond basic GPS checks by using AI-driven behavioral analysis to tell apart real delivery workers and fraudsters. Genuine users display natural movement patterns, consistent delivery activity, and varying speeds. In contrast, spoofers show unusual behaviors like sudden location jumps, staying in one place, or identical patterns between multiple users. 

We give each user a Fraud Risk Score based on their behavior in comparison to historical data and city-wide patterns.

### The Data
Instead of relying only on GPS, we gather data from various sources:

Location data (GPS and network triangulation) 
Device fingerprinting (to identify emulators or spoofing tools) 
Motion sensors (using accelerometers to confirm movement) 
App activity logs (delivery acceptance and active time) 
External APIs (for weather and traffic checks) 
Crowd comparison (to check consistency with nearby workers) 

### The UX Balance
To ensure fairness, we do not immediately reject suspicious claims: 

Low-risk claims lead to instant payouts. 
Medium-risk claims result in delayed payouts with light verification. 
High-risk claims are flagged for fraud investigation. 

This process ensures that genuine workers are not punished due to network issues or real disruptions.

### Anti-Spoofing Techniques

Detection of sudden GPS jumps (>5 km instantly)
No movement despite active delivery claims
Identical claim patterns across multiple users (syndicate detection)
Multi-sensor validation (GPS + motion + network)

### Key Innovation
Our platform moves from simple GPS-based trust to AI-driven multi-layer verification, making large-scale coordinated fraud very difficult.

## Challenges we ran into

Creating a fair system that prevents false claims while protecting honest users 
Dealing with GPS spoofing and organized fraud attacks 
Balancing automation with user trust and openness 
Developing a pricing model that can scale effectively


## Accomplishments that we're proud of

Developed a complete insurance concept tailored for gig workers 
Designed an AI-based strategy for detecting fraud and preventing spoofing 
Created a no-contact claims system with instant payouts 
Tackled real-world issues like syndicate fraud and data validation


## What we learned

How parametric insurance operates in real-life situations 
The significance of AI in detecting fraud and assessing risk 
How to design user-friendly and secure systems 
How to manage real-world issues like network failures and spoofing


## What's next for Gig-Shield AI

Build a working prototype with real API integration 
Enhance AI models using real-world data 
Collaborate with delivery platforms like Zomato and Swiggy 
Expand services to other gig workers, such as drivers and freelancers
# GigShield AI — Backend

Parametric income-protection engine for food delivery workers (Zomato / Swiggy).  
Built with **FastAPI + SQLAlchemy (async) + Open-Meteo (free weather API, no key needed)**.

---

## Architecture

```
gigshield/
├── app/
│   ├── main.py                  # FastAPI app, CORS, router registration
│   ├── core/
│   │   ├── config.py            # Thresholds, plan configs, fraud weights
│   │   ├── database.py          # Async SQLite (swap to Postgres for prod)
│   │   └── security.py         # JWT auth, password hashing
│   ├── models/
│   │   ├── worker.py            # Worker table
│   │   ├── plan.py              # PlanSubscription table
│   │   └── claim.py             # Claim table
│   ├── schemas/
│   │   └── schemas.py           # Pydantic request/response models
│   ├── services/
│   │   ├── weather_service.py   # Open-Meteo integration + trigger detection
│   │   ├── fraud_service.py     # AI fraud scoring engine
│   │   └── claim_service.py     # Parametric claim automation
│   └── api/routes/
│       ├── auth.py              # POST /register, POST /login
│       ├── workers.py           # GET /me, PATCH /me/location
│       ├── plans.py             # GET /plans, POST /subscribe, GET /premium-calculator
│       ├── claims.py            # GET /claims, POST /check-triggers, POST /simulate
│       ├── weather.py           # GET /weather/status
│       └── admin.py             # Admin dashboard stats
└── requirements.txt
```

---

## Quick Start

```bash
# 1. Create virtualenv
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app.main:app --reload --port 8000
```

Interactive API docs: **http://localhost:8000/docs**

---

## API Reference

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | Register a new worker |
| POST | `/api/v1/auth/login` | Login, get JWT token |

**Register body:**
```json
{
  "name": "Ravi Kumar",
  "mobile": "9876543210",
  "password": "securepass",
  "city": "Mumbai",
  "platform": "zomato",
  "latitude": 19.076,
  "longitude": 72.8777
}
```

---

### Worker
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/workers/me` | Profile + auto weather trigger check |
| PATCH | `/api/v1/workers/me/location` | Update GPS location |

All protected routes require: `Authorization: Bearer <token>`

---

### Plans
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/plans/` | List all plans |
| POST | `/api/v1/plans/subscribe` | Subscribe to a plan |
| GET | `/api/v1/plans/premium-calculator` | Get plan recommendation by income |

**Plans available:**
| Plan | Weekly Premium | Daily Payout | Max Days/Week |
|------|---------------|--------------|---------------|
| basic | ₹29 | ₹250 | 3 |
| standard | ₹35 | ₹300 | 5 |
| premium | ₹49 | ₹500 | 7 |

---

### Claims
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/claims/` | Payout history |
| POST | `/api/v1/claims/check-triggers` | Force weather check + auto-claim |
| POST | `/api/v1/claims/simulate?trigger=rain&value=5.0` | Demo: simulate a trigger |

---

### Weather
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/weather/status` | Live weather + active triggers (auth) |
| GET | `/api/v1/weather/status/public?city=Mumbai` | Public weather check (no auth) |

---

### Admin Dashboard
Pass header `X-Admin-Key: gigshield-admin-2024`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/admin/stats` | Platform-wide stats |
| GET | `/api/v1/admin/workers` | All registered workers |
| GET | `/api/v1/admin/claims` | All claims (filter by status) |

---

## Parametric Trigger Thresholds

| Trigger | Condition | Source |
|---------|-----------|--------|
| 🌧 Rain | ≥ 2.5 mm/hr | Open-Meteo |
| 🔥 Heat | ≥ 42°C | Open-Meteo |
| 🥶 Cold | ≤ 5°C | Open-Meteo |
| 💨 AQI | ≥ 200 (European AQI) | Open-Meteo Air Quality |

All thresholds are configurable in `app/core/config.py`.

---

## Fraud Detection Logic

Each auto-claim runs through a scoring engine before payout:

| Signal | Weight | Description |
|--------|--------|-------------|
| New account (< 3 days) | +0.35 | High-risk new signups |
| Young account (< 7 days) | +0.15 | Slightly elevated risk |
| ≥ 6 claims in 7 days | +0.30 | Excessive claim rate |
| ≥ 4 claims in 7 days | +0.15 | High claim frequency |
| Weather unconfirmed | +0.35 | No external verification |
| No GPS location | +0.10 | Can't verify presence |

**Score ≥ 0.75 → Claim auto-rejected**

---

## Zero-Touch Claim Flow

```
Worker opens dashboard
        │
        ▼
GET /workers/me
        │
        ▼
check_and_trigger_claims()
        │
        ├── No active plan? → Skip
        ├── Weekly cap reached? → Skip
        ├── Already claimed today? → Skip
        │
        ▼
fetch_weather(city/lat/lon)   ← Open-Meteo API
        │
        ├── No triggers active? → Skip
        │
        ▼
compute_fraud_score()
        │
        ├── Score ≥ 0.75? → Claim REJECTED
        │
        ▼
Claim APPROVED → Payout credited to wallet_balance
```

---

## Production Checklist

- [ ] Change `SECRET_KEY` in `core/security.py` to a strong env variable
- [ ] Change `ADMIN_SECRET` in `api/routes/admin.py`
- [ ] Switch `DATABASE_URL` from SQLite → PostgreSQL (`asyncpg`)
- [ ] Add rate limiting (e.g., `slowapi`)
- [ ] Add a cron job to call `/claims/check-triggers` for all active workers daily
- [ ] Integrate a real payment gateway (Razorpay) for premium collection and payout
- [ ] Add SMS notifications via Twilio/MSG91 when claims are paid

---

## Demo (Hackathon Flow)

```bash
# 1. Register a worker
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Ravi","mobile":"9876543210","password":"test123","city":"Mumbai","platform":"zomato"}'

# 2. Subscribe to premium plan
curl -X POST http://localhost:8000/api/v1/plans/subscribe \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"plan_key":"premium"}'

# 3. Simulate a heavy rain trigger
curl -X POST "http://localhost:8000/api/v1/claims/simulate?trigger=rain&value=8.5" \
  -H "Authorization: Bearer <token>"

# 4. Check payout history
curl http://localhost:8000/api/v1/claims/ \
  -H "Authorization: Bearer <token>"

# 5. Admin stats
curl http://localhost:8000/api/v1/admin/stats \
  -H "X-Admin-Key: gigshield-admin-2024"
```