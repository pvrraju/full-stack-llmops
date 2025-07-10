"""
tools/arthamatic_op_tool.py
===========================
A grab-bag of quick arithmetic utilities that can be surfaced to the LLM via
LangChain’s `@tool` decorator.  Demonstrates that a *tool* can be as small as a
single function – you don't have to wrap everything in a class.

Included functions
------------------
• `multiply(a, b)` – Integer multiplication.  
• `add(a, b)` – Integer addition.  
• `currency_converter(from_curr, to_curr, value)` – Lightweight exchange-rate
  lookup using AlphaVantage (requires `ALPHAVANTAGE_API_KEY`).

Feel free to delete any of these or add your own math helpers.  Just remember:
1. Decorate with `@tool`.
2. Keep the signature *simple JSON-serialisable types* (str, int, float, bool);
   this is what the LLM can emit inside a function-call.
"""
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b

@tool
def currency_converter(from_curr: str, to_curr: str, value: float)->float:
    os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv('ALPHAVANTAGE_API_KEY')
    alpha_vantage = AlphaVantageAPIWrapper()
    response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
    exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
    return value * float(exchange_rate)



# Welcome to Alpha Vantage! Your dedicated access key is: 042PPUBHO4LGRZJ2. Please record this API key at a safe place for future data access.

