from bclearer_core.configurations.convention_shift_operation_configurations import (
    ConventionShiftOperationConfigurations,
)
from bclearer_core.substages.operations.b_evolve.convention_shift_operations.convention_shift_operations_substages import (
    ConventionShiftOperationsSubstages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def run_convention_shift_operation_substage(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_universe: NfEaComUniverses,
    convention_shift_operation_configuration: ConventionShiftOperationConfigurations,
) -> NfEaComUniverses:
    with ConventionShiftOperationsSubstages(
        ea_tools_session_manager=ea_tools_session_manager,
        convention_shift_operation_configuration=convention_shift_operation_configuration,
        content_universe=content_universe,
    ) as convention_shift_operations_substage:
        convention_shift_operations_substage_output_universe = (
            convention_shift_operations_substage.run()
        )

        return convention_shift_operations_substage_output_universe
