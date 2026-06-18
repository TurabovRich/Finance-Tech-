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

Each domain module owns:

```
modules/<name>/
├── router.py      # HTTP layer
├── service.py     # business logic
├── repository.py  # database access
├── models.py      # SQLAlchemy tables
└── schemas.py     # Pydantic request/response
```

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
