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

### cards
| Column | Type | Notes |
|--------|------|-------|
| id | UUID | PK |
| user_id | UUID | FK → users |
| network | ENUM | humo, uzcard, visa |
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

## Migrations

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
