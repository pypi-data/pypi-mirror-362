"""Template for thin slice orchestrator."""

THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE = """from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.stages.{pipeline_name}_{stage_name}_orchestrator import (
    orchestrate_{pipeline_name}_{stage_name},
)
"""

THIN_SLICE_ORCHESTRATOR_FUNCTION_START = """

def orchestrate_{thin_slice_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() -> (
    None
):
"""

ORCHESTRATE_STAGE_CALL = """    orchestrate_{pipeline_name}_{stage_name}()
"""

EMPTY_FUNCTION_BODY = """    pass
"""
