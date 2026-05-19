# Binance Futures Testnet Trading Bot

A CLI-based Python trading bot for placing BUY and SELL orders on the Binance USDT-M Futures Testnet.

This project demonstrates:
- Binance Futures API integration
- MARKET and LIMIT order placement
- Structured logging
- Input validation
- Exception handling
- Clean modular architecture

---

# Features

- Binance Futures Testnet integration
- MARKET order support
- LIMIT order support
- BUY and SELL functionality
- CLI-based interaction using argparse
- Structured logging to log files
- Input validation
- Error handling for API/network failures
- Modular and reusable code structure

---

# Tech Stack

- Python 3.x
- python-binance
- argparse
- python-dotenv
- logging

---

# Project Structure

```bash
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # MARKET and LIMIT order logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging configuration
│
├── logs/
│   ├── trading.log
│   └── sample_trading.log
│
├── cli.py                 # CLI entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# Setup Instructions

## 1. Clone the Repository

```bash
git clone https://github.com/snehaaojha/trading_bot.git
cd trading_bot
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the project root.

Example:

```env
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
```

You can generate Binance Futures Testnet API credentials from:

https://testnet.binancefuture.com

---

# Usage Examples

## Test Binance Connection

```bash
venv\Scripts\python cli.py --test-connection
```

Expected output:

```bash
SUCCESS: Connected to Binance Futures Testnet
```

---

# Place MARKET BUY Order

```bash
venv\Scripts\python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

---

# Place LIMIT SELL Order

```bash
venv\Scripts\python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 120000
```

---

# Logging

All application activity is logged to:

```bash
logs/trading.log
```

Logs include:
- API connection attempts
- Order requests
- Order responses
- Errors and exceptions
- Success/failure messages

A sample log file is also included:

```bash
logs/sample_trading.log
```

---

# Validation and Error Handling

The application validates:
- Symbol input
- BUY/SELL side
- MARKET/LIMIT order type
- Quantity values
- Price requirement for LIMIT orders

Handled exceptions include:
- BinanceAPIException
- BinanceOrderException
- Network failures
- Invalid API credentials
- Invalid symbols
- Invalid quantities

---

# Assumptions

- Binance USDT-M Futures Testnet only
- LIMIT orders use `GTC` (Good Till Cancelled)
- Testnet API credentials are required
- Python 3.x environment assumed

---

# Sample Successful Outputs

## MARKET Order

```bash
===== ORDER SUMMARY =====
Symbol   : BTCUSDT
Side     : BUY
Type     : MARKET
Quantity : 0.001

===== RESPONSE =====
Order ID     : 13163399752
Status       : NEW
Executed Qty : 0.0000

SUCCESS: Market order placed successfully.
```

---

## LIMIT Order

```bash
===== ORDER SUMMARY =====
Symbol   : BTCUSDT
Side     : SELL
Type     : LIMIT
Quantity : 0.001
Price    : 120000

===== RESPONSE =====
Order ID     : 13163415891
Status       : NEW
Executed Qty : 0.0000

SUCCESS: Limit order placed successfully.
```

---

# Author

Sneha Ojha
