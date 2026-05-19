# client.py
# Wraps the Binance Futures Testnet client.
# Loads API credentials from .env and provides a connect() method
# that pings the API, fetches server time, and returns connection status.

import os
from datetime import datetime, timezone
from typing import Dict, Any

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout

from bot.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)

# Binance Futures Testnet base URLs
FUTURES_TESTNET_URL = "https://testnet.binancefuture.com"


class BinanceClient:
    """
    Wrapper around the Binance Futures Testnet client.

    Reads API_KEY and API_SECRET from the .env file.
    Call connect() to initialise and verify the connection.
    """

    def __init__(self) -> None:
        self.api_key: str = os.getenv("API_KEY", "").strip()
        self.api_secret: str = os.getenv("API_SECRET", "").strip()
        self.client: Client | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def connect(self) -> Dict[str, Any]:
        """
        Initialises the Binance Futures Testnet client, pings the API,
        and fetches the current server time.

        Returns:
            dict with keys:
                success (bool)   – True if connection succeeded.
                message (str)    – Human-readable status message.
                server_time (str | None) – ISO-formatted server time, or None on failure.

        Raises:
            Nothing – all exceptions are caught and reflected in the return dict.
        """
        logger.info("Attempting to connect to Binance Futures Testnet...")

        # 1. Validate credentials are present
        if not self.api_key or not self.api_secret:
            msg = "API_KEY and API_SECRET must be set in the .env file."
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}

        # 2. Build client pointed at Futures Testnet
        try:
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True,
            )
            # Override base URL to Futures Testnet (python-binance testnet=True
            # targets Spot testnet by default; futures needs its own endpoint).
            self.client.FUTURES_URL = FUTURES_TESTNET_URL + "/fapi"
            logger.info("Client initialised. Pinging API...")
        except Exception as exc:
            msg = f"Failed to initialise Binance client: {exc}"
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}

        # 3. Ping
        try:
            self.client.futures_ping()
            logger.info("Ping successful.")
        except (ConnectionError, Timeout) as exc:
            msg = f"Unable to connect to Binance API: {exc}"
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}
        except BinanceRequestException as exc:
            msg = f"Network error while pinging Binance API: {exc}"
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}
        except BinanceAPIException as exc:
            msg = self._api_error_message(exc)
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}

        # 4. Fetch server time
        try:
            response = self.client.futures_time()
            server_ts: int = response["serverTime"]
            server_time_iso = datetime.fromtimestamp(
                server_ts / 1000, tz=timezone.utc
            ).strftime("%Y-%m-%d %H:%M:%S UTC")
            logger.info("Server time fetched: %s", server_time_iso)
        except BinanceAPIException as exc:
            msg = self._api_error_message(exc)
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}
        except Exception as exc:
            msg = f"Unexpected error fetching server time: {exc}"
            logger.error(msg)
            return {"success": False, "message": msg, "server_time": None}

        logger.info("Connected to Binance Futures Testnet successfully.")
        return {
            "success": True,
            "message": "Connected to Binance Futures Testnet",
            "server_time": server_time_iso,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _api_error_message(exc: BinanceAPIException) -> str:
        """Maps common Binance API error codes to readable messages."""
        code_messages = {
            -2014: "Invalid API key format.",
            -2015: "Invalid API key, secret, or permissions.",
            -1022: "Invalid API signature — check your API_SECRET.",
            -1100: "Illegal characters in a parameter.",
        }
        readable = code_messages.get(exc.code, str(exc))
        return f"Binance API error ({exc.code}): {readable}"
