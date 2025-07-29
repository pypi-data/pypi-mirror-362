from bclearer_core.configurations.adjustment_operations_substage_configurations import (
    AdjustmentOperationsSubstageConfigurations,
)
from bclearer_core.substages.operations.b_evolve.adjustment_operations.adjustment_operations_substages import (
    AdjustmentOperationsSubstages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def run_adjustment_operations_substage(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_universe: NfEaComUniverses,
    adjustment_operations_substage_configuration: AdjustmentOperationsSubstageConfigurations,
) -> NfEaComUniverses:
    with AdjustmentOperationsSubstages(
        ea_tools_session_manager=ea_tools_session_manager,
        content_universe=content_universe,
        adjustment_operations_substage_configuration=adjustment_operations_substage_configuration,
    ) as adjustment_operations_substage:
        adjustment_operations_substage_output_universe = (
            adjustment_operations_substage.run()
        )

        return adjustment_operations_substage_output_universe
