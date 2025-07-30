from decimal import Decimal

from pydantic import BaseModel

from async_crypto_pay_api.models import CryptoAsset, FiatAsset


class ExchangeRate(BaseModel, frozen=True):
    is_valid: bool
    is_crypto: bool
    is_fiat: bool
    source: CryptoAsset | FiatAsset
    target: FiatAsset
    rate: Decimal


__all__ = [
    "ExchangeRate",
]
