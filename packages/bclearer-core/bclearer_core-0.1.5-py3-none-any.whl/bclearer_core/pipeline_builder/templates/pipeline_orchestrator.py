"""Template for pipeline orchestrator."""

PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE = """from bclearer_pipelines.{domain_name}.b_source.{pipeline_name}.orchestrators.thin_slices.{thin_slice_name}_orchestrator import (
    orchestrate_{thin_slice_name},
)
"""

PIPELINE_ORCHESTRATOR_FUNCTION_START = """

def orchestrate_{pipeline_name}():
    __run_contained_bie_pipeline_components()


def __run_contained_bie_pipeline_components() -> (
    None
):
"""

ORCHESTRATE_THIN_SLICE_CALL = """    orchestrate_{thin_slice_name}()
"""

EMPTY_FUNCTION_BODY = """    pass
"""
