from datetime import datetime as Datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field

from async_crypto_pay_api.models import CryptoAsset, FiatAsset, SwapAsset


class CurrencyType(Enum):
    CRYPTO = "crypto"
    FIAT = "fiat"


class InvoiceStatus(Enum):
    ACTIVE = "active"
    PAID = "paid"
    EXPIRED = "expired"


class PaidButtonName(Enum):
    VIEW_ITEM = "viewItem"
    OPEN_CHANNEL = "openChannel"
    OPEN_BOT = "openBot"
    CALLBACK = "callback"


class Invoice(BaseModel, frozen=True):
    invoice_id: int
    hash: str
    currency_type: CurrencyType
    asset: CryptoAsset | None = None
    fiat: FiatAsset | None = None
    amount: Decimal
    paid_asset: CryptoAsset | None = None
    paid_amount: Decimal | None = None
    paid_fiat_rate: Decimal | None = None
    accepted_assets: list[CryptoAsset] | None = None
    fee_asset: CryptoAsset | None = None
    fee_amount: Decimal | None = None
    # fee: Decimal | None = Field(deprecated=True)
    pay_url: str | None = Field(default=None, deprecated=True)
    bot_invoice_url: str
    mini_app_invoice_url: str
    web_app_invoice_url: str
    description: str | None = None
    status: InvoiceStatus
    swap_to: SwapAsset | None = None
    is_swapped: bool | None = None
    swapped_uid: str | None = None
    swapped_to: SwapAsset | None = None
    swapped_rate: Decimal | None = None
    swapped_output: Decimal | None = None
    swapped_usd_amount: Decimal | None = None
    swapped_usd_rate: Decimal | None = None
    created_at: Datetime
    paid_usd_rate: Decimal | None = None
    # usd_rate: Decimal | None = Field(deprecated=True)
    allow_comments: bool
    allow_anonymous: bool
    expiration_date: Datetime | None = None
    paid_at: Datetime | None = None
    paid_anonymously: bool | None = None
    comment: str | None = None
    hidden_message: str | None = None
    payload: str | None = None
    paid_btn_name: PaidButtonName | None = None
    paid_btn_url: str | None = None


class InvoiceSearchStatus(Enum):
    ACTIVE = "active"
    PAID = "paid"


__all__ = [
    "CurrencyType",
    "InvoiceStatus",
    "PaidButtonName",
    "Invoice",
    "InvoiceSearchStatus",
]
