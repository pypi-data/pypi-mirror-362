from datetime import datetime as Datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

from async_crypto_pay_api.models import CryptoAsset


class CheckStatus(Enum):
    ACTIVE = "active"
    ACTIVATED = "activated"


class Check(BaseModel, frozen=True):
    check_id: int
    hash: str
    asset: CryptoAsset
    amount: Decimal
    bot_check_url: str
    status: CheckStatus
    created_at: Datetime
    activated_at: Datetime | None = None


__all__ = []
