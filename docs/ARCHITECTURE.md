# FinGuard AI — Locked Architecture

This document is the source of truth. Structure, versions, and workflow do not change without an explicit project decision.

## Directory structure

```
finguard-ai/
├── backend/
│   ├── app/
│   │   ├── api/v1/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── workers/
│   │   ├── ai/
│   │   └── tests/
│   ├── alembic/
│   ├── requirements/
│   ├── scripts/
│   ├── .env
│   ├── alembic.ini
│   └── main.py
├── frontend/
├── infra/
└── docs/
```

## Locked technology versions

| Component | Version |
|-----------|---------|
| Python | 3.12 |
| FastAPI | 0.116+ |
| SQLAlchemy | 2.0+ |
| Alembic | 1.16+ |
| PostgreSQL | 16 |
| Redis | 7 |
| Celery | 5.5+ |
| Pydantic | 2 |
| React | 19 |
| TypeScript | 5 |
| Docker Compose | v2 |

## Git branch strategy

- `main` — production
- `develop` — integration
- `feature/auth`, `feature/customers`, `feature/transactions`, `feature/alerts` — vertical slices

## Database table order

`users` → `customers` → `transactions` → `alerts` → `cases` → `documents` → `audit_logs` → `policy_chunks`

## Per-phase development

1. Create folders  
2. Create models  
3. Create schemas  
4. Create repository  
5. Create service  
6. Create API  
7. Test manually  
8. Write pytest  
9. Commit  

## Current phase

**Phase 1 — `users` (complete):** model, schemas, repository, service, API (`/api/v1/users`), pytest. Next: **Phase 2 — `customers`** on `feature/customers`. No other tables until each phase is committed.
