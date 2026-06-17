"""Dashboard summary schemas."""

from pydantic import BaseModel


class DashboardSummary(BaseModel):
    customers_total: int
    customers_high_risk: int
    customers_pending_review: int
    transactions_total: int
    transactions_pending: int
    open_alerts: int
    critical_alerts: int
    open_cases: int
    urgent_cases: int