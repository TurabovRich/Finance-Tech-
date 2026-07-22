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
| `auth` | OTP, JWT, PIN setup |
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
alembic revision --autogenerate -m "initial"
alembic upgrade head
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs  
Health: http://localhost:8000/health

**Dev OTP code** (until SMS provider is wired): `123456`

### 2. Mobile

```bash
./scripts/setup-mobile.sh   # requires Flutter SDK
cd mobile && flutter run
```

### 3. Tests + CI

```bash
cd backend && pytest
```

CI workflow: `.github/workflows/ci.yml`

---

## Engineering rules

1. Amounts always in **tiyin** (integer) — never float
2. JWT auth on all protected endpoints; mobile uses secure token storage
3. No raw card numbers — `last_four` display only
4. Document decisions in `docs/`

---

## Current milestone

1. First Alembic migration + seed categories/transactions
2. Wire Flutter Insights home to `/api/v1/insights/monthly`
3. Real OTP flow (SMS provider integration)
4. Card linking flow end-to-end
