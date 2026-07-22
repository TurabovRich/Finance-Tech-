# Clarity — Architecture

## Stack

| Layer | Technology |
|-------|------------|
| Mobile | Flutter + Riverpod + go_router |
| API | FastAPI (modular monolith) |
| Database | PostgreSQL |
| Migrations | Alembic |
| Containers | Docker + docker-compose |
| CI | GitHub Actions |

## Modular monolith

One process, layered by technical role rather than one folder per domain —
appropriate at the current team size; see "When to reorganize" below.

```
backend/app/
├── api/v1/endpoints/   # HTTP layer (routing, request/response only)
├── api/v1/schemas/     # Pydantic request/response DTOs
├── services/           # business logic
├── db/repositories/    # database access (query construction only)
├── models/             # SQLAlchemy tables
└── core/                # config, security, logging, shared FastAPI dependencies
```

Request flow: `endpoint → service → repository → model`. Services never talk to each
other directly; repositories never contain business rules; endpoints never touch
the database or SQLAlchemy models directly.

### When to reorganize into domain modules

An earlier iteration of this repo used one folder per domain
(`modules/auth/{router,service,repository,models,schemas}.py`, etc.). It was removed
because it was a second, unwired implementation sitting next to this one — not
because domain-first organization is wrong. Revisit domain modules once multiple
engineers/squads own separate domains and folder-level ownership boundaries start
to matter more than the current low-friction shared layout.

## API base path

`/api/v1`

## Request flow

```
Mobile → API Router → Service → Repository → PostgreSQL
```

## Documents to add

- `system-design.md` — MVP / growth / scale stages
- `api-spec.yaml` — OpenAPI export
- `adrs/` — architecture decision records
