from datetime import datetime as Datetime
from decimal import Decimal

from pydantic import BaseModel


class AppStats(BaseModel, frozen=True):
    volume: Decimal
    conversion: Decimal
    unique_users_count: int
    created_invoice_count: int
    paid_invoice_count: int
    start_at: Datetime
    end_at: Datetime


__all__ = [
    "AppStats",
]
