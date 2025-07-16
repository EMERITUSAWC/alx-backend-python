#!/usr/bin/env python3
"""Utility functions for accessing nested maps, retrieving JSON, and memoization."""

import requests
from typing import Mapping, Any, Sequence, Callable
from functools import wraps


def access_nested_map(nested_map: Mapping, path: Sequence) -> Any:
    """Access a nested object in nested_map with path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Mapping:
    """Get JSON content from a URL."""
    response = requests.get(url)
    return response.json()


def memoize(fn: Callable) -> Callable:
    """Decorator to cache the output of a method."""

    @wraps(fn)
    def memoized(self):
        """Memoized function wrapper."""
        attr_name = "_{}".format(fn.__name__)
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return memoized
