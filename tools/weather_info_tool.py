"""
tools/weather_info_tool.py
=========================
Provides LangChain `@tool` wrappers around OpenWeatherMap so the agent can fetch
current conditions and multi-day forecasts.

Quick start
-----------
1. Set the `OPENWEATHERMAP_API_KEY` environment variable (see your `.env` file).
2. Instantiate `WeatherInfoTool` and append its `weather_tool_list` to the agent’s
tool registry.

Extending this tool
-------------------
• Add additional helper methods to `utils/weather_info.py` for other endpoints
  (air-quality, UV index, etc.).
• Decorate new callables inside `_setup_tools()` with `@tool` and return them in
the list so LangGraph can surface them to the LLM.

The class is intentionally lightweight and stateless so you can duplicate the
pattern for other third-party APIs with minimal effort.
"""
import os
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
        self.weather_service = WeatherForecastTool(self.api_key)
        self.weather_tool_list = self._setup_tools()
    
    def _setup_tools(self) -> List:
        """Setup all tools for the weather forecast tool"""
        @tool
        def get_current_weather(city: str) -> str:
            """Get current weather for a city"""
            weather_data = self.weather_service.get_current_weather(city)
            if weather_data:
                temp = weather_data.get('main', {}).get('temp', 'N/A')
                desc = weather_data.get('weather', [{}])[0].get('description', 'N/A')
                return f"Current weather in {city}: {temp}°C, {desc}"
            return f"Could not fetch weather for {city}"
        
        @tool
        def get_weather_forecast(city: str) -> str:
            """Get weather forecast for a city"""
            forecast_data = self.weather_service.get_forecast_weather(city)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                return f"Weather forecast for {city}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {city}"
    
        return [get_current_weather, get_weather_forecast]