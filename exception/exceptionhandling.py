"""
exception/exceptionhandling.py
==============================
Placeholder for custom exception classes or error-handling utilities. Having a
centralised module makes it easier to maintain consistent error messages and
HTTP status codes across the codebase.

Example
-------
```python
class ExternalAPITimeout(Exception):
    "Raised when a third-party service does not respond in time."

    def __init__(self, service: str, timeout: int):
        super().__init__(f"{service} timed out after {timeout}s")
```
"""