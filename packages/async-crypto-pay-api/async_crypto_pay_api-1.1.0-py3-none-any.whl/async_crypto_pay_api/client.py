from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from secrets import token_hex
from typing import Any, Literal, TypeVar, overload

from aiohttp import ClientSession
from pydantic import ValidationError

from async_crypto_pay_api import models as m
from async_crypto_pay_api.exceptions import InvalidResponseError, RequestError


def serialize_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    elif isinstance(value, (int, float, Decimal)):
        return str(value)
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, list):
        return ",".join(map(serialize_value, value))
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, Enum):
        return value.value
    else:
        raise ValueError(f"unsupported type for serialization: '{type(value)}'")


def serialize_body(body: dict[str, Any]) -> dict[str, Any]:
    return {k: serialize_value(v) for k, v in body.items() if v is not None}


R = TypeVar("R")


class CryptoPayApi:
    __token: str
    __is_test_backend: bool
    __session: ClientSession | None

    def __init__(self, token: str, test_backend: bool = False) -> None:
        self.__token = token
        self.__is_test_backend = test_backend
        self.__session = None

    async def __aenter__(self) -> "CryptoPayApi":
        self.__get_session()
        return self

    async def __aexit__(self, *_) -> bool:
        await self.close()
        return False

    def __get_session(self) -> ClientSession:
        if self.__session is None:
            self.__session = ClientSession(
                base_url=(
                    "https://testnet-pay.crypt.bot/api/"
                    if self.__is_test_backend
                    else "https://pay.crypt.bot/api/"
                ),
                headers={"Crypto-Pay-API-Token": self.__token},
            )

        return self.__session

    async def __process_request(
        self,
        method_name: str,
        result_model: type[R],
        body: dict[str, Any] | None = None,
    ) -> R:
        async with (
            self.__get_session().post(
                method_name,
                json={} if body is None else body,
            ) as http_response,
        ):
            json = await http_response.json()
            try:
                response = m.Response[result_model].model_validate(json)
            except ValidationError:
                raise InvalidResponseError("invalid response body")

            if response.ok:
                if response.result is None:
                    raise InvalidResponseError(
                        "response.result is empty while response.ok = True"
                    )

                return response.result
            else:
                if response.error is None:
                    raise InvalidResponseError(
                        "response.error is empty while response.ok = False"
                    )

                raise RequestError(response.error.code, response.error.name)

    @property
    def token(self) -> str:
        return self.__token

    async def close(self) -> None:
        if self.__session is None:
            return

        await self.__session.close()
        self.__session = None

    async def get_me(self) -> m.AppInfo:
        return await self.__process_request("getMe", result_model=m.AppInfo)

    @overload
    async def create_invoice(
        self,
        *,
        currency_type: Literal[m.CurrencyType.CRYPTO],
        asset: m.CryptoAsset,
        amount: int | float | Decimal,
        swap_to: m.SwapAsset | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        paid_btn_name: None = None,
        paid_btn_url: None = None,
        payload: str | None = None,
        allow_comments: bool = True,
        allow_anonymous: bool = True,
        expires_in: timedelta | None = None,
    ) -> m.Invoice: ...

    @overload
    async def create_invoice(
        self,
        *,
        currency_type: Literal[m.CurrencyType.CRYPTO],
        asset: m.CryptoAsset,
        amount: int | float | Decimal,
        paid_btn_name: m.PaidButtonName,
        paid_btn_url: str,
        swap_to: m.SwapAsset | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        payload: str | None = None,
        allow_comments: bool = True,
        allow_anonymous: bool = True,
        expires_in: timedelta | None = None,
    ) -> m.Invoice: ...

    @overload
    async def create_invoice(
        self,
        *,
        currency_type: Literal[m.CurrencyType.FIAT],
        fiat: m.FiatAsset,
        accepted_assets: list[m.CryptoAsset] | None = None,
        amount: int | float | Decimal,
        swap_to: m.SwapAsset | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        paid_btn_name: None = None,
        paid_btn_url: None = None,
        payload: str | None = None,
        allow_comments: bool = True,
        allow_anonymous: bool = True,
        expires_in: timedelta | None = None,
    ) -> m.Invoice: ...

    @overload
    async def create_invoice(
        self,
        *,
        currency_type: Literal[m.CurrencyType.FIAT],
        fiat: m.FiatAsset,
        amount: int | float | Decimal,
        paid_btn_name: m.PaidButtonName,
        paid_btn_url: str,
        accepted_assets: list[m.CryptoAsset] | None = None,
        swap_to: m.SwapAsset | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        payload: str | None = None,
        allow_comments: bool = True,
        allow_anonymous: bool = True,
        expires_in: timedelta | None = None,
    ) -> m.Invoice: ...

    async def create_invoice(self, **body: Any) -> m.Invoice:
        return await self.__process_request(
            "createInvoice",
            result_model=m.Invoice,
            body=serialize_body(body),
        )

    async def delete_invoice(self, invoice_id: int) -> bool:
        return await self.__process_request(
            "deleteInvoice",
            result_model=bool,
            body=serialize_body(dict(invoice_id=invoice_id)),
        )

    async def create_check(
        self,
        *,
        asset: m.CryptoAsset,
        amount: int | float | Decimal,
        pin_to_user_id: int | None = None,
        pin_to_username: str | None = None,
    ) -> m.Check:
        return await self.__process_request(
            "createCheck",
            result_model=m.Check,
            body=serialize_body(
                dict(
                    asset=asset,
                    amount=amount,
                    pin_to_user_id=pin_to_user_id,
                    pin_to_username=pin_to_username,
                )
            ),
        )

    async def delete_check(self, check_id: int) -> bool:
        return await self.__process_request(
            "deleteCheck",
            result_model=bool,
            body=serialize_body(dict(check_id=check_id)),
        )

    async def transfer(
        self,
        *,
        user_id: int,
        asset: m.CryptoAsset,
        amount: int | float | Decimal,
        comment: str | None = None,
        disable_send_notification: bool = False,
    ) -> m.Transfer:
        return await self.__process_request(
            "transfer",
            m.Transfer,
            body=serialize_body(
                dict(
                    user_id=user_id,
                    asset=asset,
                    amount=amount,
                    spend_id=token_hex(32),
                    comment=comment,
                    disable_send_notification=disable_send_notification,
                )
            ),
        )

    @overload
    async def get_invoices(
        self,
        *,
        asset: m.CryptoAsset,
        invoice_ids: list[int] | None = None,
        status: m.InvoiceSearchStatus | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> list[m.Invoice]: ...

    @overload
    async def get_invoices(
        self,
        *,
        fiat: m.FiatAsset,
        invoice_ids: list[int] | None = None,
        status: m.InvoiceSearchStatus | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> list[m.Invoice]: ...

    @overload
    async def get_invoices(
        self,
        *,
        asset: None = None,
        fiat: None = None,
        invoice_ids: list[int] | None = None,
        status: m.InvoiceSearchStatus | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> list[m.Invoice]: ...

    async def get_invoices(self, **body: Any) -> list[m.Invoice]:
        items = await self.__process_request(
            "getInvoices",
            m.Items[m.Invoice],
            serialize_body(body),
        )
        return items.items

    async def get_transfers(
        self,
        asset: m.CryptoAsset | None = None,
        transfer_ids: list[int] | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> list[m.Transfer]:
        items = await self.__process_request(
            "getTransfers",
            m.Items[m.Transfer],
            serialize_body(
                dict(
                    asset=asset,
                    transfer_ids=transfer_ids,
                    offset=offset,
                    count=count,
                )
            ),
        )
        return items.items

    async def get_checks(
        self,
        asset: m.CryptoAsset | None = None,
        check_ids: list[int] | None = None,
        status: m.CheckStatus | None = None,
        offset: int = 0,
        count: int = 100,
    ) -> list[m.Check]:
        items = await self.__process_request(
            "getChecks",
            m.Items[m.Check],
            serialize_body(
                dict(
                    asset=asset,
                    check_ids=check_ids,
                    status=status,
                    offset=offset,
                    count=count,
                )
            ),
        )
        return items.items

    async def get_balance(self) -> list[m.Balance]:
        return await self.__process_request("getBalance", list[m.Balance])

    async def get_exchange_rates(self) -> list[m.ExchangeRate]:
        return await self.__process_request("getExchangeRates", list[m.ExchangeRate])

    async def get_currencies(self) -> list[m.Currency]:
        return await self.__process_request("getCurrencies", list[m.Currency])

    async def get_stats(
        self,
        *,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> m.AppStats:
        return await self.__process_request(
            "getStats",
            m.AppStats,
            serialize_body(
                dict(
                    start_at=start_at,
                    end_at=end_at,
                )
            ),
        )


__all__ = [
    "CryptoPayApi",
]
