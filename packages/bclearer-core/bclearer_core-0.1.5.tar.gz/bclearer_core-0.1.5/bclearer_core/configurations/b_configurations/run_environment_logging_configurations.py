from bclearer_core.configurations.b_configurations.b_configurations import (
    BConfigurations,
)
from bclearer_orchestration_services.log_environment_utility_service.common_knowledge.environment_log_level_types import (
    EnvironmentLogLevelTypes,
)


class RunEnvironmentLoggingConfigurations(
    BConfigurations
):
    # TODO: added here to be agreed
    ENVIRONMENT_LOG_LEVEL_TYPE = (
        EnvironmentLogLevelTypes.FILTERED
    )
