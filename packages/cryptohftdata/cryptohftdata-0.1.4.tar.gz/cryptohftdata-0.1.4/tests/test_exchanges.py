"""
Test cases for exchange constants and validation.
"""

import pytest

from cryptohftdata.exchanges import ExchangeConstants, exchanges


class TestExchangeConstants:
    """Test cases for the ExchangeConstants class."""

    def test_exchange_constants_exist(self):
        """Test that common exchange constants exist."""
        assert hasattr(ExchangeConstants, "BINANCE_SPOT")
        assert hasattr(ExchangeConstants, "BINANCE_FUTURES")
        assert hasattr(ExchangeConstants, "BYBIT_SPOT")
        assert hasattr(ExchangeConstants, "BYBIT_FUTURES")

    def test_exchange_values(self):
        """Test that exchange constants have correct values."""
        assert ExchangeConstants.BINANCE_SPOT == "binance_spot"
        assert ExchangeConstants.BINANCE_FUTURES == "binance_futures"
        assert ExchangeConstants.BYBIT_SPOT == "bybit_spot"
        assert ExchangeConstants.BYBIT_FUTURES == "bybit"

    def test_get_all_exchanges(self):
        """Test getting all supported exchanges."""
        all_exchanges = ExchangeConstants.get_all_exchanges()
        assert isinstance(all_exchanges, list)
        assert len(all_exchanges) > 0
        assert "binance_spot" in all_exchanges
        assert "bybit_spot" in all_exchanges

    def test_is_valid_exchange(self):
        """Test exchange validation."""
        assert ExchangeConstants.is_valid_exchange("binance_spot") is True
        assert ExchangeConstants.is_valid_exchange("bybit") is True
        assert ExchangeConstants.is_valid_exchange("invalid_exchange") is False
        assert ExchangeConstants.is_valid_exchange("") is False

    def test_get_exchange_type(self):
        """Test extracting exchange type."""
        assert ExchangeConstants.get_exchange_type("binance_spot") == "spot"
        assert ExchangeConstants.get_exchange_type("binance_futures") == "futures"
        assert ExchangeConstants.get_exchange_type("bybit_spot") == "spot"
        assert ExchangeConstants.get_exchange_type("bybit") == "futures"

    def test_get_exchange_name(self):
        """Test extracting exchange name."""
        assert ExchangeConstants.get_exchange_name("binance_spot") == "binance"
        assert ExchangeConstants.get_exchange_name("bybit") == "bybit"

    def test_exchanges_instance(self):
        """Test that the exchanges instance works correctly."""
        assert exchanges.BINANCE_SPOT == "binance_spot"
        assert exchanges.is_valid_exchange("binance_spot") is True
        assert isinstance(exchanges.get_all_exchanges(), list)
