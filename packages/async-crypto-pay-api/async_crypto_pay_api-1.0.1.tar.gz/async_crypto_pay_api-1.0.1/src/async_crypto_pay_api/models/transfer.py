from datetime import datetime as Datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel

from async_crypto_pay_api.models import CryptoAsset


class Transfer(BaseModel, frozen=True):
    transfer_id: int
    spend_id: str
    user_id: int
    asset: CryptoAsset
    amount: Decimal
    status: Literal["completed"]
    completed_at: Datetime
    comment: str | None = None


__all__ = [
    "Transfer",
]
