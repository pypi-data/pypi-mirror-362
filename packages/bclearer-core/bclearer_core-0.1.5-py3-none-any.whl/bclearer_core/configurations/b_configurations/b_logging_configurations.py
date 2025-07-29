from bclearer_core.configurations.b_configurations.b_configurations import (
    BConfigurations,
)
from bclearer_core.configurations.datastructure.logging_inspection_level_b_enums import (
    LoggingInspectionLevelBEnums,
)
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)
from bclearer_orchestration_services.logging_service.configuration.process_logging_levels import (
    ProcessLoggingLevels,
)


class BLoggingConfigurations(
    BConfigurations
):
    # TODO: should this be None instead?
    #  how could we switch between log_process_message() and log_message() in @run_and_log_function()?
    LOG_PROCESS_MESSAGES_FLAG = True

    console_process_logging_level = (
        ProcessLoggingLevels.PROCESS_LEVEL_10
    )

    file_process_logging_level = (
        ProcessLoggingLevels.PROCESS_LEVEL_2
    )

    # TODO: default level is WARNING - to agree
    LOGGING_INSPECTION_REPORTING_LEVEL_ENUM = (
        LoggingInspectionLevelBEnums.WARNING
    )

    # TODO: default level is ERROR - to agree
    LOGGING_INSPECTION_SUMMARISING_LEVEL_ENUM = (
        LoggingInspectionLevelBEnums.ERROR
    )

    ENVIRONMENT_LOG_LEVEL_TYPE = (
        EnvironmentLogLevelTypes.FILTERED
    )
