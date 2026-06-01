"""API v1 route aggregation."""

from fastapi import APIRouter

from app.api.v1 import alerts, audit_logs, auth, cases, customers, documents, policy_chunks, transactions, users

api_v1_router = APIRouter()
api_v1_router.include_router(auth.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(customers.router)
api_v1_router.include_router(transactions.router)
api_v1_router.include_router(alerts.router)
api_v1_router.include_router(cases.router)
api_v1_router.include_router(documents.router)
api_v1_router.include_router(audit_logs.router)
api_v1_router.include_router(policy_chunks.router)
