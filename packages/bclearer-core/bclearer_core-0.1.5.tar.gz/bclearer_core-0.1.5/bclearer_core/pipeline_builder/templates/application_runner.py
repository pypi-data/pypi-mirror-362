"""Template for application runner."""

APPLICATION_RUNNER_TEMPLATE = """from bclearer_orchestration_services.b_app_runner_service.b_application_runner import (
    run_b_application,
)
from bclearer_pipelines.{domain_name}.b_source.app_runners.runners.{domain_name}_b_clearer_pipelines_runner import (
    run_{domain_name}_b_clearer_pipelines,
)


def run_{domain_name}_b_clearer_pipeline_b_application() -> (
    None
):
    run_b_application(
        app_startup_method=run_{domain_name}_b_clearer_pipelines
    )
"""
