"""
Exchange identifiers and constants.
"""

from typing import Final, List


class ExchangeConstants:
    """Constants for supported exchanges."""

    # Binance
    BINANCE_SPOT: Final[str] = "binance_spot"
    BINANCE_FUTURES: Final[str] = "binance_futures"

    # Bybit
    BYBIT_SPOT: Final[str] = "bybit_spot"
    BYBIT_FUTURES: Final[str] = "bybit"

    # Kraken
    KRAKEN_SPOT: Final[str] = "kraken_spot"
    KRAKEN_FUTURES: Final[str] = "kraken_derivatives"

    # OKX
    OKX_SPOT: Final[str] = "okx_spot"
    OKX_FUTURES: Final[str] = "okx_futures"

    # Bitget
    BITGET_SPOT: Final[str] = "bitget_spot"
    BITGET_FUTURES: Final[str] = "bitget_futures"

    @classmethod
    def get_all_exchanges(cls) -> List[str]:
        """Get a list of all supported exchange identifiers."""
        return [
            value
            for name, value in cls.__dict__.items()
            if isinstance(value, str) and not name.startswith("_")
        ]

    @classmethod
    def is_valid_exchange(cls, exchange: str) -> bool:
        """Check if an exchange identifier is valid."""
        return exchange in cls.get_all_exchanges()

    @classmethod
    def get_exchange_type(cls, exchange: str) -> str:
        """Get the exchange type (spot, futures, options, etc.)."""
        if exchange in [cls.BINANCE_FUTURES, cls.BYBIT_FUTURES]:
            return "futures"
        elif exchange in [cls.BINANCE_SPOT, cls.BYBIT_SPOT]:
            return "spot"
        else:
            return "unknown"

    @classmethod
    def get_exchange_name(cls, exchange: str) -> str:
        """Get the exchange name without the market type."""
        if "_" in exchange:
            return exchange.split("_", 1)[0]
        return exchange


# Create the exchanges instance that users will import
exchanges = ExchangeConstants()
