# Binance Futures Testnet Trading Bot

A CLI-based trading bot for placing BUY/SELL orders on the Binance USDT-M Futures Testnet.

---

## Project Overview

This bot lets you place MARKET and LIMIT orders on Binance Futures Testnet directly from the command line. It is built with a clean modular architecture, structured logging, and input validation.

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py        # Package init
│   ├── client.py          # Binance client wrapper
│   ├── orders.py          # Order placement functions
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/
│   └── trading.log        # Log output
├── cli.py                 # CLI entry point
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment setup

Copy `.env.example` to `.env` and fill in your Binance Futures Testnet API credentials:

```bash
cp .env.example .env
```

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret
```

You can generate Testnet API keys at: https://testnet.binancefuture.com

---

## Example CLI Commands

Place a MARKET BUY order:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Place a LIMIT SELL order:

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3000
```

---

## Logging

All activity is logged to `logs/trading.log` with timestamps, log levels, and messages. Console output shows INFO and above.
