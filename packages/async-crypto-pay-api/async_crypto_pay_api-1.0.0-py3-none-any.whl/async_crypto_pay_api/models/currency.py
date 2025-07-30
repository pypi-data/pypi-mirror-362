from pydantic import BaseModel

from async_crypto_pay_api.models import CryptoAsset, FiatAsset


class Currency(BaseModel, frozen=True):
    is_blockchain: bool
    is_stablecoin: bool
    is_fiat: bool
    name: str
    code: CryptoAsset | FiatAsset
    url: str | None = None
    decimals: int


__all__ = [
    "Currency",
]
