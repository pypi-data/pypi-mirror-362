"""Template for pipeline runner."""

PIPELINE_RUNNER_TEMPLATE = """from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.pipeline.{pipeline_name}_orchestrator import (
    orchestrate_{pipeline_name},
)


@run_and_log_function()
def run_{pipeline_name}() -> None:
    orchestrate_{pipeline_name}()
"""
