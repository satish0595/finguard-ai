"""Dashboard summary business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.alert import AlertSeverity, AlertStatus
from app.models.case import CasePriority, CaseStatus
from app.models.customer import CustomerStatus, RiskLevel
from app.models.transaction import TransactionStatus
from app.repositories.alert_repository import AlertRepository
from app.repositories.case_repository import CaseRepository
from app.repositories.customer_repository import CustomerRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.dashboard import DashboardSummary


class DashboardService:
    def __init__(self, session: AsyncSession) -> None:
        self._customers = CustomerRepository(session)
        self._transactions = TransactionRepository(session)
        self._alerts = AlertRepository(session)
        self._cases = CaseRepository(session)

    async def get_summary(self) -> DashboardSummary:
        return DashboardSummary(
            customers_total=await self._customers.count(),
            customers_high_risk=await self._customers.count(risk_level=RiskLevel.HIGH),
            customers_pending_review=await self._customers.count(
                status=CustomerStatus.PENDING_REVIEW
            ),
            transactions_total=await self._transactions.count(),
            transactions_pending=await self._transactions.count(
                status=TransactionStatus.PENDING
            ),
            open_alerts=await self._alerts.count(status=AlertStatus.OPEN),
            critical_alerts=await self._alerts.count(
                status=AlertStatus.OPEN,
                severity=AlertSeverity.CRITICAL,
            ),
            open_cases=await self._cases.count(status=CaseStatus.OPEN),
            urgent_cases=await self._cases.count(
                status=CaseStatus.OPEN,
                priority=CasePriority.URGENT,
            ),
        )