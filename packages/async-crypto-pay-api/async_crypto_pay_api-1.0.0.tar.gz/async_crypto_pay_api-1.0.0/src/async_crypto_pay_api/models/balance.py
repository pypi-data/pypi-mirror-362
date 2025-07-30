from decimal import Decimal

from pydantic import BaseModel

from async_crypto_pay_api.models import CryptoAsset


class Balance(BaseModel, frozen=True):
    currency_code: CryptoAsset
    available: Decimal
    onhold: Decimal


__all__ = [
    "Balance",
]
