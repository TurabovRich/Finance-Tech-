# Clarity

Educational fintech simulation — learn how company-scale mobile finance apps are structured, without handling real money.

**Market context:** Uzbekistan (PayMe, Click, PayNet as reference)  
**Stack:** Flutter · FastAPI · PostgreSQL · Docker · GitHub Actions

---

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
| `auth` | OTP (simulated), JWT, PIN setup |
| `users` | Profile, locale |
| `cards` | Linked mock cards (Humo/Uzcard/Visa) |
| `transactions` | Simulated transaction feed |
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

**Simulated OTP code:** `123456`

### 2. Mobile

```bash
./scripts/setup-mobile.sh   # requires Flutter SDK
cd mobile && flutter run
```

### 3. Tests + CI

```bash
cd backend && pytest
```

CI workflow: `.github/workflows/ci.yml` (copy from `infra/github-actions/ci.yml`)

---

## Learning mode rules

1. No real payment rails — all money data is simulated
2. Document every decision in `docs/`
3. Wire JWT auth before calling protected endpoints from mobile
4. Amounts always in **tiyin** (integer) — never float

---

## Next steps

1. Write `docs/product/PRD.md`
2. Run first Alembic migration
3. Seed fake transactions + categories
4. Wire Flutter screens to API
5. Add JWT dependency to replace `user_id` placeholders
