"""Template for pipelines runner."""

PIPELINES_RUNNER_TEMPLATE_HEADER = """from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
"""

PIPELINE_IMPORT_TEMPLATE = """from bclearer_pipelines.{domain_name}.b_source.app_runners.runners.{pipeline_name}_runner import (
    run_{pipeline_name},
)
"""

PIPELINES_RUNNER_FUNCTION_START = """

@run_and_log_function()
def run_{domain_name}_b_clearer_pipelines() -> (
    None
):
"""

PIPELINE_RUNNER_CALL = """    run_{pipeline_name}()
"""

EMPTY_FUNCTION_BODY = """    pass
"""
