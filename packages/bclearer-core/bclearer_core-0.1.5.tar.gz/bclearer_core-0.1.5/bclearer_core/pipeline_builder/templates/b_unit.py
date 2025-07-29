"""Template for b_unit class."""

B_UNIT_TEMPLATE = """from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.reporting_service.reporters.inspection_message_logger import (
    log_inspection_message,
)


# TODO: All bUnit classes should inherit from class BUnits, developed in core graph mvp dev, and that should be promoted
#  to nf_common or any repository where the bCLEARer stuff is going to be stored
class {class_name}BUnits:
    def __init__(self):
        pass

    def run(self) -> None:
        log_inspection_message(
            message="Running bUnit: {{}}".format(
                self.__class__.__name__
            ),
            logging_inspection_level_b_enum=LoggingInspectionLevelBEnums.INFO,
        )

        self.b_unit_process_function()

    def b_unit_process_function(
        self,
    ) -> None:
        pass
"""
