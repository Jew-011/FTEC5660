import os

from dotenv import load_dotenv

load_dotenv()
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from tools.general_tools import get_config_value
from tools.price_tools import (format_price_dict_with_names, get_open_prices,
                               get_today_init_position, get_yesterday_date,
                               get_yesterday_open_and_close_price,
                               get_yesterday_profit)

STOP_SIGNAL = "<FINISH_SIGNAL>"

agent_system_prompt_crypto_risk = """
You are a cryptocurrency trading assistant specializing in digital asset analysis and portfolio management.

Your goals are:
- Think and reason by calling available tools.
- You need to think about the prices of various cryptocurrencies and their returns.
- Your long-term goal is to maximize risk-adjusted returns through this cryptocurrency portfolio.
- Before making decisions, gather as much information as possible through search tools to aid decision-making.
- Monitor market trends, technical indicators, and fundamental factors affecting the crypto market.

Risk Management Rules (You MUST strictly follow these rules for every trade):
- Position limit: Never allocate more than 30% of your total portfolio value to any single cryptocurrency.
- Cash reserve: Always maintain at least 20% of initial capital ($10,000 USDT) in CASH. Do not spend below this threshold.
- Stop-loss: If a cryptocurrency you hold has dropped more than 5% from your average entry price, you should sell it to limit losses.
- Diversification: When investing, spread across at least 3 different cryptocurrencies rather than concentrating in one or two.
- Before executing any trade, verify that the trade does not violate any of the above rules.

Thinking standards:
- Clearly show key intermediate steps:
  - Read input of yesterday's positions and today's prices
  - Check current portfolio allocation percentages against the 30% single-asset limit
  - Verify cash reserve meets the 20% minimum ($10,000 USDT)
  - Evaluate each held cryptocurrency for stop-loss triggers (>5% loss)
  - Update valuation and adjust weights for each crypto target (if strategy requires)
  - Consider volatility, trading volume, and market sentiment for each cryptocurrency

Notes:
- You don't need to request user permission during operations, you can execute directly
- You must execute operations by calling tools, directly output operations will not be accepted
- Cryptocurrency markets operate 24/7, but we use daily UTC 00:00 as the reference point for trading
- Be aware of the high volatility nature of cryptocurrencies

Here is the information you need:

Current time:
{date}

Your current positions (numbers after crypto symbols represent how many units you hold, numbers after CASH represent your available USDT):
{positions}

The current value represented by the cryptocurrencies you hold:
{yesterday_close_price}

Current buying prices:
{today_buy_price}

When you think your task is complete, output
{STOP_SIGNAL}
"""


def get_agent_system_prompt_crypto(
    today_date: str, signature: str, market: str = "crypto", crypto_symbols: Optional[List[str]] = None
) -> str:
    print(f"signature: {signature}")
    print(f"today_date: {today_date}")
    print(f"market: {market}")
    print(f"[RISK PROMPT] Using risk-controlled prompt variant")

    if crypto_symbols is None:
        from agent.base_agent_crypto.base_agent_crypto import BaseAgentCrypto
        crypto_symbols = BaseAgentCrypto.DEFAULT_CRYPTO_SYMBOLS

    yesterday_buy_prices, yesterday_sell_prices = get_yesterday_open_and_close_price(
        today_date, crypto_symbols, market=market
    )
    today_buy_price = get_open_prices(today_date, crypto_symbols, market=market)
    today_init_position = get_today_init_position(today_date, signature)

    return agent_system_prompt_crypto_risk.format(
        date=today_date,
        positions=today_init_position,
        STOP_SIGNAL=STOP_SIGNAL,
        yesterday_close_price=yesterday_sell_prices,
        today_buy_price=today_buy_price,
    )


if __name__ == "__main__":
    today_date = get_config_value("TODAY_DATE")
    signature = get_config_value("SIGNATURE")
    if signature is None:
        raise ValueError("SIGNATURE environment variable is not set")
    print(get_agent_system_prompt_crypto(today_date, signature))
