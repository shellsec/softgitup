"""
Compatibility module with python's now removed imp module.
"""

from importlib import reload
from importlib.util import cache_from_source, source_from_cache

__all__ = ['reload', 'cache_from_source', 'source_from_cache']
