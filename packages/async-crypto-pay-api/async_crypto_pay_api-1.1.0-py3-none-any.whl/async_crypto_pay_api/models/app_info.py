from typing import Literal

from pydantic import BaseModel


class AppInfo(BaseModel, frozen=True):
    app_id: int
    name: str
    payment_processing_bot_username: Literal["CryptoBot", "CryptoTestnetBot"]


__all__ = [
    "AppInfo",
]
