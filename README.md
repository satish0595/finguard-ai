# FinGuard AI

AML/fraud monitoring platform. Architecture, versions, and workflow are locked in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Repository layout

- `backend/` — FastAPI, SQLAlchemy, Celery, AI workers
- `frontend/` — React 19 + TypeScript 5
- `infra/` — Docker Compose (PostgreSQL 16, Redis 7)
- `docs/` — Architecture and runbooks

## Git branches

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready |
| `develop` | Integration |
| `feature/auth` | Users / authentication |
| `feature/customers` | Customers |
| `feature/transactions` | Transactions |
| `feature/alerts` | Alerts |

## Database migration order

1. `users`
2. `customers`
3. `transactions`
4. `alerts`
5. `cases`
6. `documents`
7. `audit_logs`
8. `policy_chunks`

One domain per phase; never migrate all tables at once.

## Quick start (backend)

```bash
cd infra
docker compose up -d

cd ../backend
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements/dev.txt
copy .env.example .env
alembic upgrade head
uvicorn main:app --reload
```

## Development pattern (every phase)

1. Folders → 2. Models → 3. Schemas → 4. Repository → 5. Service → 6. API → 7. Manual test → 8. pytest → 9. Commit
