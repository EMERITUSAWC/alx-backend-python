#!/usr/bin/env python3
"""Utils module."""

from typing import Mapping, Any, Tuple


def access_nested_map(nested_map: Mapping, path: Tuple) -> Any:
    """Access nested map with path of keys."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map