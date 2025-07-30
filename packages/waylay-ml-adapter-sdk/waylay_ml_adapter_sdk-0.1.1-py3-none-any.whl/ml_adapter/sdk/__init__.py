"""ML Adapter plugin for waylay-sdk."""

import importlib.metadata

from .tool import MLTool

__version__ = importlib.metadata.version("waylay-ml-adapter-sdk")

PLUGINS = [MLTool]

__all__ = ["MLTool"]
