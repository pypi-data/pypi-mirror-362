"""
Test package for OpenSearchEval
"""

import pytest
import sys
import os

# Add the package to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Test configuration
pytest_plugins = [
    'pytest_asyncio',
    'pytest_mock',
    'pytest_cov'
]

__all__ = [
    'pytest'
] 