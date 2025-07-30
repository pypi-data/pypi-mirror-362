# async-crypto-pay-api

![PyPI version](https://img.shields.io/pypi/v/async-crypto-pay-api)
![Python versions](https://img.shields.io/pypi/pyversions/async-crypto-pay-api)
![License](https://img.shields.io/pypi/l/async-crypto-pay-api)

Async Crypto Pay API wrapper for [Telegram Crypto Bot](https://t.me/cryptobot) written in Python 3.10+.

## Requirements
- Python 3.10 or higher
- Valid Crypto Bot API token ([get one here](https://t.me/CryptoBot?start=pay))

## Installation
```bash
pip install async-crypto-pay-api
```

## Example
```python
from asyncio import run
from async_crypto_pay_api import CryptoPayApi
from async_crypto_pay_api.models import CurrencyType, FiatAsset

crypto = CryptoPayApi("{token}")

async def main() -> None:
    # Context manager handles connection lifecycle
    async with crypto:
        app_info = await crypto.get_me()
        print(app_info.model_dump_json(indent=4))

        # Create payment invoice
        invoice = await crypto.create_invoice(
            currency_type=CurrencyType.FIAT,
            fiat=FiatAsset.USD,
            amount=100,
        )
        print(f"Invoice URL: {invoice.bot_invoice_url}")

run(main())
```

## License
This project is licensed under the GNU Lesser General Public License v3.0 only.
See [LICENSE](LICENSE) for details.


## Contributing
Contributions are welcome! Please open an issue or submit a PR for:
- Bug fixes
- New features
- Documentation improvements
