# cli.py
# Entry point for the trading bot CLI.
# Routes --test-connection and MARKET order placement commands.

import argparse
import sys

from bot.logging_config import get_logger

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Builds and returns the argument parser."""
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="Binance Futures Testnet trading bot CLI",
    )

    parser.add_argument(
        "--test-connection",
        action="store_true",
        default=False,
        help="Test connectivity to Binance Futures Testnet and exit.",
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default=None,
        help="Trading pair symbol, e.g. BTCUSDT",
    )
    parser.add_argument(
        "--side",
        type=str,
        choices=["BUY", "SELL"],
        default=None,
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        dest="order_type",
        type=str,
        choices=["MARKET", "LIMIT"],
        default=None,
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        type=float,
        default=None,
        help="Quantity of the asset to trade",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Limit price (required for LIMIT orders)",
    )

    return parser


# ── Command handlers ──────────────────────────────────────────────────

def handle_test_connection() -> None:
    """Initialises BinanceClient, calls connect(), and prints the result."""
    from bot.client import BinanceClient

    print("Testing connection to Binance Futures Testnet...")
    client = BinanceClient()
    result = client.connect()

    if result["success"]:
        print(f"SUCCESS: {result['message']}")
        print(f"Server Time: {result['server_time']}")
    else:
        print(f"ERROR: {result['message']}")
        sys.exit(1)


def handle_market_order(symbol: str, side: str, quantity: float) -> None:
    """Connects to Binance, places a MARKET order, and prints a formatted summary."""
    from bot.client import BinanceClient
    from bot.orders import place_market_order

    # Print order summary before sending
    print("===== ORDER SUMMARY =====")
    print(f"Symbol   : {symbol.upper()}")
    print(f"Side     : {side.upper()}")
    print(f"Type     : MARKET")
    print(f"Quantity : {quantity}")

    # Connect
    client = BinanceClient()
    conn = client.connect()
    if not conn["success"]:
        print("\n===== RESPONSE =====")
        print(f"ERROR: {conn['message']}")
        sys.exit(1)

    # Place order
    result = place_market_order(client, symbol, side, quantity)

    print("\n===== RESPONSE =====")
    if result["success"]:
        print(f"Order ID     : {result['order_id']}")
        print(f"Status       : {result['status']}")
        print(f"Executed Qty : {result['executed_qty']}")
        print(f"\nSUCCESS: {result['message']}")
    else:
        print(f"ERROR: {result['message']}")
        sys.exit(1)


def handle_limit_order(symbol: str, side: str, quantity: float, price: float) -> None:
    """Connects to Binance, places a LIMIT GTC order, and prints a formatted summary."""
    from bot.client import BinanceClient
    from bot.orders import place_limit_order

    print("===== ORDER SUMMARY =====")
    print(f"Symbol   : {symbol.upper()}")
    print(f"Side     : {side.upper()}")
    print(f"Type     : LIMIT")
    print(f"Quantity : {quantity}")
    print(f"Price    : {price}")

    # Connect
    client = BinanceClient()
    conn = client.connect()
    if not conn["success"]:
        print("\n===== RESPONSE =====")
        print(f"ERROR: {conn['message']}")
        sys.exit(1)

    # Place order
    result = place_limit_order(client, symbol, side, quantity, price)

    print("\n===== RESPONSE =====")
    if result["success"]:
        print(f"Order ID     : {result['order_id']}")
        print(f"Status       : {result['status']}")
        print(f"Executed Qty : {result['executed_qty']}")
        print(f"\nSUCCESS: {result['message']}")
    else:
        print(f"ERROR: {result['message']}")
        sys.exit(1)


# ── Main ──────────────────────────────────────────────────────────────

def main() -> None:
    """Main CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    # --test-connection mode
    if args.test_connection:
        handle_test_connection()
        return

    # Order placement mode — all four core args are required
    required = {"symbol": "--symbol", "side": "--side", "order_type": "--type", "quantity": "--quantity"}
    missing = [flag for attr, flag in required.items() if getattr(args, attr) is None]
    if missing:
        parser.error(f"The following arguments are required: {', '.join(missing)}")

    logger.info("Order request | %s", vars(args))

    if args.order_type == "MARKET":
        handle_market_order(args.symbol, args.side, args.quantity)
    elif args.order_type == "LIMIT":
        if args.price is None:
            parser.error("--price is required for LIMIT orders.")
        handle_limit_order(args.symbol, args.side, args.quantity, args.price)


if __name__ == "__main__":
    main()
