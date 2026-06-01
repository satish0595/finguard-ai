# FinGuard AI — Frontend

Minimal Vite + React 19 + TypeScript scaffold.

Quick start:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Development notes:
- API_BASE is provided via `VITE_API_BASE` env var (defaults to `/api/v1`).
- Basic pages: Home, Login, Customers, Transactions.
- This scaffold provides a simple API client using `fetch` and stores a stub token in `sessionStorage` for now.
