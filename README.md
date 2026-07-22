# Clarity

Personal finance clarity for Uzbekistan — see where your money goes, built to scale.

**Market:** Uzbekistan (PayMe, Click, PayNet as context — we compete on understanding, not just paying)  
**Stack:** Flutter · FastAPI · PostgreSQL · Docker · GitHub Actions

---

## What Clarity is

A real fintech product: link your cards, track spending by category, and open the app to **insights first** — not another payment button.

Product vision: [`docs/product/VISION.md`](docs/product/VISION.md)

## Project structure

```
FinanceApp/
├── docs/              # Product, design, architecture, security, business
├── backend/           # FastAPI modular monolith
├── mobile/            # Flutter app (feature-first)
├── infra/             # Docker, CI, nginx, terraform placeholders
├── scripts/           # Setup helpers
└── docker-compose.yml
```

## Backend modules (V1)

| Module | Responsibility |
|--------|----------------|
| `auth` | OTP, JWT access + refresh tokens, sessions, PIN setup |
| `users` | Profile, locale |
| `cards` | Linked cards (Humo/Uzcard/Visa) |
| `transactions` | Transaction feed |
| `categories` | System + user spending categories |
| `insights` | Monthly aggregates (computed) |

Each module: `router` → `service` → `repository` → `models`

## Quick start

### 1. Database + API

```bash
docker compose up -d db
cp backend/.env.example backend/.env
./scripts/setup-backend.sh
cd backend && source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  
Health: http://localhost:8000/health

**Dev OTP code** (until SMS provider is wired): `123456`

**Auth flow:** `POST /auth/otp/request` → `POST /auth/otp/verify` (returns
`access_token` + `refresh_token`) → `POST /auth/refresh` to renew the access token
→ `POST /auth/logout` or `POST /auth/sessions/{id}/revoke` to end a session.
`GET /auth/sessions` lists a user's active sessions/devices.

### 2. Mobile

```bash
./scripts/setup-mobile.sh   # requires Flutter SDK
cd mobile && flutter run
```

### 3. Tests + CI

Tests run against a real Postgres — `docker-compose.yml` provisions a separate
`clarity_test` database (via `infra/docker/init-test-db.sql`) so `pytest` never
touches dev data.

```bash
docker compose up -d db
cd backend && pytest
```

CI workflow: `.github/workflows/ci.yml` (spins up its own ephemeral Postgres service)

---

## Engineering rules

1. Amounts always in **tiyin** (integer) — never float
2. JWT auth on all protected endpoints; mobile uses secure token storage
3. No raw card numbers — `last_four` display only
4. Document decisions in `docs/`

---

## Current milestone

1. Seed system categories via migration data (schema exists; seed data doesn't yet)
2. Wire Flutter Insights home to `/api/v1/insights/monthly`
3. Real OTP flow (SMS provider integration)
4. Card linking flow end-to-end
5. Rate limiting on `/auth/otp/*` (brute-force protection — tracked, not yet implemented)
