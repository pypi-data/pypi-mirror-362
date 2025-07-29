"""Pytest configuration for whoopy tests.

Copyright (c) 2024 Felix Geilert
"""

import asyncio

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Configure pytest-asyncio
pytest_plugins = ["pytest_asyncio"]
