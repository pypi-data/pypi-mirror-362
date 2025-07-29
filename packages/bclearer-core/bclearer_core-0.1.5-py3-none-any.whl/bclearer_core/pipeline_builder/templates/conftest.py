"""Template for conftest.py."""

CONFTEST_TEMPLATE = """import pytest


@pytest.fixture(scope="module")
def e2e_test_setup():
    # Add setup code here
    pass


@pytest.fixture(scope="module")
def e2e_test_teardown():
    # Add teardown code here
    pass
"""
