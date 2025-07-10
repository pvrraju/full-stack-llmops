"""
utils/weather_info.py
=====================
Lightweight wrapper around the OpenWeatherMap REST API.  The class is kept
framework-agnostic so it can be reused in notebooks, CLI scripts, or wrapped
into a LangChain tool (see `tools/weather_info_tool.py`).

Usage
-----
```
weather = WeatherForecastTool(os.getenv("OPENWEATHERMAP_API_KEY"))
weather.get_current_weather("Paris")
```

Extending
---------
OpenWeatherMap exposes many other endpoints (historical data, UV index, etc.).
Add a new helper method that builds the URL + parameters and returns the JSON
payload.  Keep the method stateless and handle exceptions gracefully so the
agent has a predictable error surface.
"""
import requests

class WeatherForecastTool:
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self, place:str):
        """Get current weather of a place"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "q": place,
                "appid": self.api_key,
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e
    
    def get_forecast_weather(self, place:str):
        """Get weather forecast of a place"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                "q": place,
                "appid": self.api_key,
                "cnt": 10,
                "units": "metric"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else {}
        except Exception as e:
            raise e