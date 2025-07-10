"""
utils/currency_converter.py
===========================
A minimal wrapper around the **ExchangeRate-API** REST endpoint.  The helper is
kept slim (single request & multiply) because accuracy is handled by the remote
service.

Usage
-----
```
converter = CurrencyConverter(os.getenv("EXCHANGE_RATE_API_KEY"))
converter.convert(100, "USD", "INR")
```

Notes
-----
• ExchangeRate-API free tier caches results for ~24 h.  If you require
  intra-day updates, consider a different provider or use their *paid* plan.
• All amounts are converted as `float` – if you need higher precision wrap the
  output in `Decimal`.
"""
import requests

class CurrencyConverter:
    def __init__(self, api_key: str):
        self.base_url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/"
    
    def convert(self, amount:float, from_currency:str, to_currency:str):
        """Convert the amount from one currency to another"""
        url = f"{self.base_url}/{from_currency}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("API call failed:", response.json())
        rates = response.json()["conversion_rates"]
        if to_currency not in rates:
            raise ValueError(f"{to_currency} not found in exchange rates.")
        return amount * rates[to_currency]