"""
tools/place_search_tool.py
=========================
This module bundles a set of LangChain `@tool` callables that query **Google Places**
or **Tavily** (fallback) to retrieve attractions, restaurants, activities, and
transportation options for a given location.

Environment variables
---------------------
• `GPLACES_API_KEY` – required for Google Places API access. If the key is *not*
  available or the request fails, the tool automatically falls back to Tavily so
  the agent still produces an answer.

Extending / Customizing
-----------------------
1. Implement additional methods in `utils/place_info_search.py` for new search
   categories (e.g. nightlife, coworking spaces).
2. Inside `_setup_tools()` add a new `@tool` decorated function that calls the
   corresponding helper and append it to the returned list.
3. Register the updated tool list in `agent/agentic_workflow.py`.

The design goal is to make it trivial to plug in alternative data providers or
add new endpoints with minimal code changes.
"""
import os
from utils.place_info_search import GooglePlaceSearchTool, TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.google_api_key = os.environ.get("GPLACES_API_KEY")
        self.google_places_search = GooglePlaceSearchTool(self.google_api_key)
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool"""
        @tool
        def search_attractions(place:str) -> str:
            """Search attractions of a place"""
            try:
                attraction_result = self.google_places_search.google_search_attractions(place)
                if attraction_result:
                    return f"Following are the attractions of {place} as suggested by google: {attraction_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the attractions of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_restaurants(place:str) -> str:
            """Search restaurants of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_restaurants(place)
                if restaurants_result:
                    return f"Following are the restaurants of {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the restaurants of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_activities(place:str) -> str:
            """Search activities of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_activity(place)
                if restaurants_result:
                    return f"Following are the activities in and around {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the activities of {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        @tool
        def search_transportation(place:str) -> str:
            """Search transportation of a place"""
            try:
                restaurants_result = self.google_places_search.google_search_transportation(place)
                if restaurants_result:
                    return f"Following are the modes of transportation available in {place} as suggested by google: {restaurants_result}"
            except Exception as e:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Google cannot find the details due to {e}. \nFollowing are the modes of transportation available in {place}: {tavily_result}"  ## Fallback search using tavily in case google places fail
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]