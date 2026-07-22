# Clarity — Database Schema (V1)

PostgreSQL. Amounts stored as **integers in tiyin** (1 UZS = 100 tiyin).

## Entity relationship

```
users
  ├── cards (1:N)
  ├── transactions (1:N)
  └── categories (1:N custom; system categories have user_id = NULL)

transactions
  ├── → users
  ├── → cards (optional)
  └── → categories (optional)
```

## Tables

### users
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| phone | VARCHAR(20) | unique, indexed |
| pin_hash | VARCHAR(255) | nullable |
| full_name | VARCHAR(120) | nullable |
| locale | VARCHAR(10) | default `uz` |
| is_active | BOOLEAN | default true |
| created_at | TIMESTAMPTZ | |
| updated_at | TIMESTAMPTZ | |

### auth_sessions
One row per issued refresh token (i.e. per logged-in device). The refresh token
itself is never stored — only its SHA-256 hash — so a database read can't yield a
usable token.

| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK → users |
| refresh_token_hash | VARCHAR(64) | SHA-256 hex digest, unique, indexed |
| device_name | VARCHAR(120) | nullable, client-supplied at login |
| ip_address | VARCHAR(45) | nullable, captured at login |
| user_agent | VARCHAR(255) | nullable, captured at login |
| created_at | TIMESTAMPTZ | |
| last_used_at | TIMESTAMPTZ | updated on each `/auth/refresh` call |
| expires_at | TIMESTAMPTZ | `now() + REFRESH_TOKEN_EXPIRE_DAYS` at creation |
| revoked_at | TIMESTAMPTZ | nullable; NULL = still active |

The access-token JWT carries the session id as a `sid` claim so "list my sessions"
can flag which one is the current device. Refresh tokens are **not rotated** on
use in V1 — see the Threat model note in `docs/security/README.md` for why, and
the tradeoff recorded there.

### cards
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK → users |
| network | ENUM | humo, uzcard, visa (stored as the lowercase enum *value*, not the Python member name — see note below) |
| last_four | CHAR(4) | display only — no PAN |
| bank_name | VARCHAR(120) | nullable |
| nickname | VARCHAR(60) | nullable |
| is_primary | BOOLEAN | |
| created_at | TIMESTAMPTZ | |

### categories
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK, nullable for system categories |
| name | VARCHAR(80) | |
| icon | VARCHAR(40) | nullable |
| color | VARCHAR(7) | hex, nullable |
| is_system | BOOLEAN | seed data for all users |

### transactions
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK → users |
| card_id | UUID | FK, nullable |
| category_id | UUID | FK, nullable |
| type | ENUM | debit, credit, transfer, fee |
| status | ENUM | pending, completed, failed |
| amount | BIGINT | tiyin |
| fee | BIGINT | tiyin, default 0 |
| currency | CHAR(3) | default UZS |
| merchant | VARCHAR(200) | nullable |
| description | TEXT | nullable |
| occurred_at | TIMESTAMPTZ | indexed |
| created_at | TIMESTAMPTZ | |

## Insights

No table — computed from `transactions` at query time.

## Enum storage note

`CardNetwork`, `TransactionType`, and `TransactionStatus` are all `(str, enum.Enum)`
classes with `values_callable` set so Postgres stores the lowercase `.value`
(`"humo"`, `"debit"`, `"pending"`) rather than SQLAlchemy's default of the
Python member *name* (`"HUMO"`, `"DEBIT"`, `"PENDING"`). Without `values_callable`
this silently diverges from the API contract — caught and fixed before the first
migration was written, since no data existed yet to migrate.

## Migrations

The first migration (`alembic/versions/..._initial_schema.py`) creates every table
directly from `Base.metadata` rather than hand-written `op.create_table()` calls —
a deliberate one-time exception since there was no prior revision to autogenerate
a diff against. **Every migration after this one must be generated normally:**

```bash
cd backend
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```
