"""
utils/expense_calculator.py
==========================
Pure-Python arithmetic helper used by `tools/expense_calculator_tool.py`.
Provides methods for basic math needed in travel cost estimation.  We keep the
implementation small on purpose—if you need spreadsheet-grade functionality
consider importing *NumPy* or *Pandas* instead.

Adding new operations
---------------------
1. Implement a `@staticmethod` on `Calculator` that performs your desired
   calculation.
2. Expose it to the LLM by wrapping it inside a new `@tool` decorator in
   `tools/expense_calculator_tool.py`.
"""
class Calculator:
    @staticmethod
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
    
    @staticmethod
    def calculate_total(*x: float) -> float:
        """
        Calculate sum of the given list of numbers

        Args:
            x (list): List of floating numbers

        Returns:
            float: The sum of numbers in the list x
        """
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        """
        Calculate daily budget

        Args:
            total (float): Total cost.
            days (int): Total number of days

        Returns:
            float: Expense for a single day
        """
        return total / days if days > 0 else 0
    
    