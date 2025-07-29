from .playwright import get_browser, get_browser_context

# Import page module to ensure monkey patches are applied
from . import page  # noqa: F401

__all__ = ["get_browser", "get_browser_context"]
