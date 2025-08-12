#!/usr/bin/env python3
"""Utils module"""

import requests
from typing import Dict


def get_json(url: str) -> Dict:
    """Fetches JSON from a given URL."""
    response = requests.get(url)
    return response.json()
