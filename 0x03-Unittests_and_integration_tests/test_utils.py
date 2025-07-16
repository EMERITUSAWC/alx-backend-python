#!/usr/bin/env python3
"""
Unittests for utils.py
"""
import pytest
from utils import access_nested_map

class TestAccessNestedMap:
    @pytest.mark.parametrize(
        "nested_map, path, expected",
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ],
    )
    def test_access_nested_map(self, nested_map, path, expected):
        assert access_nested_map(nested_map, path) == expected

    @pytest.mark.parametrize(
        "nested_map, path",
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ],
    )
    def test_access_nested_map_key_error(self, nested_map, path):
        with pytest.raises(KeyError) as exc_info:
            access_nested_map(nested_map, path)
        # Assert that the exception’s argument matches the missing key
        missing_key = path[-1]
        assert exc_info.value.args[0] == missing_key