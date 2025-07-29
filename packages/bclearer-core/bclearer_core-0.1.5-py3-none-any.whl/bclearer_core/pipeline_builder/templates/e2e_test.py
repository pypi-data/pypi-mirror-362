"""Template for e2e test."""

E2E_TEST_TEMPLATE = """import pytest
from {domain_name}.b_source.app_runners.{domain_name}_b_clearer_pipeline_b_application_runner import (
    run_{domain_name}_b_clearer_pipeline_b_application,
)


def test_{domain_name}_b_clearer_pipeline_b_application(e2e_test_setup, e2e_test_teardown):
    # Run the pipeline
    run_{domain_name}_b_clearer_pipeline_b_application()

    # Add assertions here
    assert True
"""
