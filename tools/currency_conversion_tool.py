"""
tools/currency_conversion_tool.py
================================
Provides a single `convert_currency` LangChain tool that turns an amount from
one currency into another using *ExchangeRate-API*.

Configuration
-------------
Set the `EXCHANGE_RATE_API_KEY` environment variable in your `.env` file (or in
your cloud secret manager) before running the agent.

Extending
---------
If you’d like to support bulk conversions or display the exchange rate table:
1. Expand `utils/currency_converter.py` with a new helper method.
2. Add an `@tool` decorated callable inside `_setup_tools()` that wraps the new
   helper.
"""
import os
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.currency_service = CurrencyConverter(self.api_key)
        self.currency_converter_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""
        @tool
        def convert_currency(amount:float, from_currency:str, to_currency:str):
            """Convert amount from one currency to another"""
            return self.currency_service.convert(amount, from_currency, to_currency)
        
        return [convert_currency]