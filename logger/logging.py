"""
logger/logging.py
=================
Reserved for any project-wide logging configuration.  At the moment we rely on
FastAPI/Streamlit default loggers, but if you want structured logging (e.g.
JSON to stdout or integrations with Logstash) this is where you would configure
`logging.basicConfig` or set up loguru.

Feel free to place helper functions like `get_logger(__name__)` in this file
and import them throughout the project.
"""
