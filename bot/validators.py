# validators.py
# Input validation functions for order parameters.
# Each function raises ValueError with a descriptive message on invalid input.

from bot.logging_config import get_logger

logger = get_logger(__name__)

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> str:
    """
    Validates the trading pair symbol.

    Args:
        symbol: e.g. "BTCUSDT"

    Returns:
        Uppercased symbol string.

    Raises:
        ValueError: If symbol is empty or not a string.
    """
    if not isinstance(symbol, str) or not symbol.strip():
        raise ValueError("Symbol must be a non-empty string (e.g. BTCUSDT).")
    return symbol.strip().upper()


def validate_side(side: str) -> str:
    """
    Validates the order side.

    Args:
        side: "BUY" or "SELL"

    Returns:
        Uppercased side string.

    Raises:
        ValueError: If side is not BUY or SELL.
    """
    normalized = side.strip().upper()
    if normalized not in VALID_SIDES:
        raise ValueError(f"Side must be one of {VALID_SIDES}. Got: '{side}'.")
    return normalized


def validate_order_type(order_type: str) -> str:
    """
    Validates the order type.

    Args:
        order_type: "MARKET" or "LIMIT"

    Returns:
        Uppercased order type string.

    Raises:
        ValueError: If order type is not MARKET or LIMIT.
    """
    normalized = order_type.strip().upper()
    if normalized not in VALID_ORDER_TYPES:
        raise ValueError(f"Order type must be one of {VALID_ORDER_TYPES}. Got: '{order_type}'.")
    return normalized


def validate_quantity(quantity: float) -> float:
    """
    Validates the order quantity.

    Args:
        quantity: Amount of the asset to trade.

    Returns:
        The validated quantity.

    Raises:
        ValueError: If quantity is not a positive number.
    """
    if not isinstance(quantity, (int, float)) or quantity <= 0:
        raise ValueError(f"Quantity must be a positive number. Got: {quantity}.")
    return float(quantity)


def validate_price(price: float) -> float:
    """
    Validates the order price (required for LIMIT orders).

    Args:
        price: Limit price for the order.

    Returns:
        The validated price.

    Raises:
        ValueError: If price is not a positive number.
    """
    if not isinstance(price, (int, float)) or price <= 0:
        raise ValueError(f"Price must be a positive number. Got: {price}.")
    return float(price)
