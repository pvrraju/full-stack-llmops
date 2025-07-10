"""
tools/expense_calculator_tool.py
================================
Simple arithmetic utilities (multiply, add, divide) exposed as LangChain tools
so the agent can perform on-the-fly cost estimations without leaving the graph.

Why a separate tool?
--------------------
The LLM is great at reasoning but unreliable at exact arithmetic. Delegating
math-heavy work to a deterministic Python function guarantees accuracy in the
final itinerary cost breakdown.

Adding more math helpers
------------------------
• Extend `utils/expense_calculator.py` with new operations (e.g. currency
  formatting, percentage calculations).
• Decorate a new callable inside `_setup_tools()` with `@tool` and return it so
  it becomes available to the LLM.
"""
from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night:str, total_days:float) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool
        def calculate_total_expense(*costs: float) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]