"""Template for stage orchestrator."""

STAGE_ORCHESTRATOR_HEADER = """from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper_latest import (
    run_and_log_function,
)
"""

SUB_STAGE_IMPORT_TEMPLATE = """from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.sub_stages.{pipeline_name}_{stage_name}_{sub_stage_name}.{pipeline_name}_{stage_name}_{sub_stage_name}_orchestrator import (
    orchestrate_{pipeline_name}_{stage_name}_{sub_stage_name},
)
"""

B_UNIT_CREATOR_IMPORT = """from bclearer_pipelines.{domain_name}.b_source.common.operations.b_units.b_unit_creator_and_runner import (
    create_and_run_b_unit,
)
"""

B_UNIT_IMPORT_TEMPLATE = """from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.objects.b_units.{pipeline_name}_{stage_name}.{b_unit_lower}_b_units import (
    {b_unit_class}BUnits,
)
"""

STAGE_ORCHESTRATOR_FUNCTION_START = """

@run_and_log_function()
def orchestrate_{pipeline_name}_{stage_name}() -> None:
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() -> (
    None
):
"""

ORCHESTRATE_SUB_STAGE_CALL = """    orchestrate_{pipeline_name}_{stage_name}_{sub_stage_name}()
"""

CREATE_AND_RUN_B_UNIT_CALL = """    create_and_run_b_unit(
        b_unit_type={b_unit_class}BUnits
    )
"""

EMPTY_FUNCTION_BODY = """    pass
"""
