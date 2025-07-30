from enum import Enum


class EnumWithUnknown(Enum):
    UNKNOWN = "UNKNOWN"


class CryptoAsset(Enum):
    USDT = "USDT"
    TON = "TON"
    SOL = "SOL"
    TRX = "TRX"
    GRAM = "GRAM"
    BTC = "BTC"
    ETH = "ETH"
    DOGE = "DOGE"
    LTC = "LTC"
    NOT = "NOT"
    TRUMP = "TRUMP"
    MELANIA = "MELANIA"
    PEPE = "PEPE"
    WIF = "WIF"
    BONK = "BONK"
    MAJOR = "MAJOR"
    MY = "MY"
    DOGS = "DOGS"
    MEMHASH = "MEMHASH"
    BNB = "BNB"
    HMSTR = "HMSTR"
    CATI = "CATI"
    USDC = "USDC"
    JET = "JET"
    SEND = "SEND"


class FiatAsset(Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"
    BYN = "BYN"
    UAH = "UAH"
    GBP = "GBP"
    CNY = "CNY"
    KZT = "KZT"
    UZS = "UZS"
    GEL = "GEL"
    TRY = "TRY"
    AMD = "AMD"
    THB = "THB"
    INR = "INR"
    BRL = "BRL"
    IDR = "IDR"
    AZN = "AZN"
    AED = "AED"
    PLN = "PLN"
    ILS = "ILS"
    KGS = "KGS"
    TJS = "TJS"


class SwapAsset(Enum):
    USDT = "USDT"
    TON = "TON"
    TRX = "TRX"
    ETH = "ETH"
    SOL = "SOL"
    BTC = "BTC"
    LTC = "LTC"


__all__ = [
    "CryptoAsset",
    "FiatAsset",
    "SwapAsset",
]
