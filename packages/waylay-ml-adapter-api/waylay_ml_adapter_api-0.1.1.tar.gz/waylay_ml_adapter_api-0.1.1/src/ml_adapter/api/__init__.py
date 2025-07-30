"""ML Adapter API."""

import importlib.metadata

from .data import v1, v2

__version__ = importlib.metadata.version("waylay-ml-adapter-api")

__all__ = ["v1", "v2"]
