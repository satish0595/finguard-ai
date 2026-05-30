"""FastAPI dependencies."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.alert_service import AlertService
from app.services.case_service import CaseService
from app.services.customer_service import CustomerService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


def get_customer_service(session: AsyncSession = Depends(get_db)) -> CustomerService:
    return CustomerService(session)


def get_transaction_service(
    session: AsyncSession = Depends(get_db),
) -> TransactionService:
    return TransactionService(session)


def get_alert_service(session: AsyncSession = Depends(get_db)) -> AlertService:
    return AlertService(session)


def get_case_service(session: AsyncSession = Depends(get_db)) -> CaseService:
    return CaseService(session)
