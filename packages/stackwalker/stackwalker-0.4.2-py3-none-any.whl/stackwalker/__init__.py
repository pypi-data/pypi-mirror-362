"""
stackwalker/__init__.py
"""
import importlib.metadata

try:
    __version_number__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version_number__ = "0.0.0"
