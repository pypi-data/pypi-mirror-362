class CryptoPayError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RequestError(CryptoPayError):
    status_code: int
    name: str

    def __init__(self, status_code: int, name: str) -> None:
        super().__init__(f"{name} [{status_code}]")

        self.status_code = status_code
        self.name = name


class InvalidResponseError(CryptoPayError):
    def __init__(self, info: str) -> None:
        super().__init__(f"server response is invalid: {info}")


__all__ = [
    "CryptoPayError",
    "RequestError",
    "InvalidResponseError",
]
