"""Template for b_unit creator and runner."""

B_UNIT_CREATOR_AND_RUNNER_TEMPLATE = """# TODO: Minimal version of the method developed in core graph mvp dev that should be promoted to a bCLEARer importable
#  library
def create_and_run_b_unit(
    b_unit_type,
) -> None:
    b_unit = b_unit_type()

    b_unit.run()
"""
