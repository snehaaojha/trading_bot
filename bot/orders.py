# orders.py
# Order placement functions for Binance Futures Testnet.
# Each function validates inputs, calls the Futures API, and returns a result dict.

from typing import Dict, Any, TYPE_CHECKING

from binance.exceptions import BinanceAPIException, BinanceOrderException
from requests.exceptions import ConnectionError, Timeout

from bot.validators import validate_symbol, validate_side, validate_quantity, validate_price
from bot.logging_config import get_logger

if TYPE_CHECKING:
    from bot.client import BinanceClient

logger = get_logger(__name__)

# Common Binance error codes and readable descriptions
_API_ERROR_MESSAGES: Dict[int, str] = {
    -1121: "Invalid symbol. Check the trading pair (e.g. BTCUSDT).",
    -2010: "Insufficient balance to place this order.",
    -1111: "Precision is over the maximum defined for this asset.",
    -1013: "Quantity does not meet the minimum order size.",
    -2015: "Invalid API key, secret, or permissions.",
    -1022: "Invalid API signature — check your API_SECRET.",
}


def place_market_order(
    bot_client: "BinanceClient",
    symbol: str,
    side: str,
    quantity: float,
) -> Dict[str, Any]:
    """
    Places a MARKET order on Binance USDT-M Futures Testnet.

    Args:
        bot_client: An initialised and connected BinanceClient instance.
        symbol:     Trading pair, e.g. "BTCUSDT".
        side:       "BUY" or "SELL".
        quantity:   Amount of the asset to trade (must be > 0).

    Returns:
        dict with keys:
            success  (bool)        – True if the order was accepted.
            message  (str)         – Human-readable status.
            order_id (int | None)  – Binance order ID on success.
            status   (str | None)  – Order status string, e.g. "FILLED".
            executed_qty (str | None) – Quantity actually executed.
            raw      (dict | None) – Full raw API response.
    """
    # ── 1. Validate inputs ────────────────────────────────────────────
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_quantity(quantity)
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        return _error_result(str(exc))

    if bot_client.client is None:
        msg = "Client is not connected. Call connect() before placing orders."
        logger.error(msg)
        return _error_result(msg)

    # ── 2. Log the request ────────────────────────────────────────────
    logger.info(
        "Placing MARKET %s order | symbol=%s | quantity=%s",
        side, symbol, quantity,
    )

    # ── 3. Call Futures API ───────────────────────────────────────────
    try:
        response: Dict[str, Any] = bot_client.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity,
        )
    except BinanceOrderException as exc:
        msg = f"Order rejected by Binance: {exc.message}"
        logger.error("BinanceOrderException | code=%s | %s", exc.code, exc.message)
        return _error_result(msg)
    except BinanceAPIException as exc:
        msg = _readable_api_error(exc)
        logger.error("BinanceAPIException | code=%s | %s", exc.code, exc.message)
        return _error_result(msg)
    except (ConnectionError, Timeout) as exc:
        msg = f"Unable to reach Binance API: {exc}"
        logger.error(msg)
        return _error_result(msg)
    except Exception as exc:
        msg = f"Unexpected error placing order: {exc}"
        logger.exception(msg)
        return _error_result(msg)

    # ── 4. Parse and return response ──────────────────────────────────
    logger.info(
        "Order accepted | order_id=%s | status=%s | executed_qty=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
    )

    return {
        "success": True,
        "message": "Market order placed successfully.",
        "order_id": response.get("orderId"),
        "status": response.get("status"),
        "executed_qty": response.get("executedQty"),
        "raw": response,
    }


def place_limit_order(
    bot_client: "BinanceClient",
    symbol: str,
    side: str,
    quantity: float,
    price: float,
) -> Dict[str, Any]:
    """
    Places a LIMIT GTC order on Binance USDT-M Futures Testnet.

    Args:
        bot_client: An initialised and connected BinanceClient instance.
        symbol:     Trading pair, e.g. "BTCUSDT".
        side:       "BUY" or "SELL".
        quantity:   Amount of the asset to trade (must be > 0).
        price:      Limit price for the order (must be > 0).

    Returns:
        dict with keys:
            success      (bool)        – True if the order was accepted.
            message      (str)         – Human-readable status.
            order_id     (int | None)  – Binance order ID on success.
            status       (str | None)  – Order status, e.g. "NEW".
            executed_qty (str | None)  – Quantity filled so far.
            raw          (dict | None) – Full raw API response.
    """
    # ── 1. Validate inputs ────────────────────────────────────────────
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        quantity = validate_quantity(quantity)
        price = validate_price(price)
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        return _error_result(str(exc))

    if bot_client.client is None:
        msg = "Client is not connected. Call connect() before placing orders."
        logger.error(msg)
        return _error_result(msg)

    # ── 2. Log the request ────────────────────────────────────────────
    logger.info(
        "Placing LIMIT %s order | symbol=%s | quantity=%s | price=%s | timeInForce=GTC",
        side, symbol, quantity, price,
    )

    # ── 3. Call Futures API ───────────────────────────────────────────
    try:
        response: Dict[str, Any] = bot_client.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC",
        )
    except BinanceOrderException as exc:
        msg = f"Order rejected by Binance: {exc.message}"
        logger.error("BinanceOrderException | code=%s | %s", exc.code, exc.message)
        return _error_result(msg)
    except BinanceAPIException as exc:
        msg = _readable_api_error(exc)
        logger.error("BinanceAPIException | code=%s | %s", exc.code, exc.message)
        return _error_result(msg)
    except (ConnectionError, Timeout) as exc:
        msg = f"Unable to reach Binance API: {exc}"
        logger.error(msg)
        return _error_result(msg)
    except Exception as exc:
        msg = f"Unexpected error placing order: {exc}"
        logger.exception(msg)
        return _error_result(msg)

    # ── 4. Parse and return response ──────────────────────────────────
    logger.info(
        "Order accepted | order_id=%s | status=%s | executed_qty=%s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
    )

    return {
        "success": True,
        "message": "Limit order placed successfully.",
        "order_id": response.get("orderId"),
        "status": response.get("status"),
        "executed_qty": response.get("executedQty"),
        "raw": response,
    }


# ── Helpers ───────────────────────────────────────────────────────────

def _error_result(message: str) -> Dict[str, Any]:
    """Returns a standardised failure result dict."""
    return {
        "success": False,
        "message": message,
        "order_id": None,
        "status": None,
        "executed_qty": None,
        "raw": None,
    }


def _readable_api_error(exc: BinanceAPIException) -> str:
    """Maps a BinanceAPIException to a human-readable message."""
    readable = _API_ERROR_MESSAGES.get(exc.code, exc.message)
    return f"Binance API error ({exc.code}): {readable}"
