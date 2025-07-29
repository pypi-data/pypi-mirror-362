from bclearer_core.configurations.universe_modification_operation_configurations import (
    UniverseModificationOperationConfigurations,
)
from bclearer_core.substages.operations.b_evolve.universe_modification_operations.universe_modification_operation_substages import (
    UniverseModificationOperationsSubstages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def run_universe_modification_operations_substage(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_universe: NfEaComUniverses,
    universe_modification_operation_configuration: UniverseModificationOperationConfigurations,
) -> NfEaComUniverses:
    with UniverseModificationOperationsSubstages(
        ea_tools_session_manager=ea_tools_session_manager,
        universe_modification_operation_configuration=universe_modification_operation_configuration,
        content_universe=content_universe,
    ) as universe_modification_operations_substage:
        universe_modification_operations_substage_output_universe = (
            universe_modification_operations_substage.run()
        )

        return universe_modification_operations_substage_output_universe
