"""API v1 route aggregation."""

from fastapi import APIRouter

from app.api.v1 import alerts, cases, customers, transactions, users

api_v1_router = APIRouter()
api_v1_router.include_router(users.router)
api_v1_router.include_router(customers.router)
api_v1_router.include_router(transactions.router)
api_v1_router.include_router(alerts.router)
api_v1_router.include_router(cases.router)
