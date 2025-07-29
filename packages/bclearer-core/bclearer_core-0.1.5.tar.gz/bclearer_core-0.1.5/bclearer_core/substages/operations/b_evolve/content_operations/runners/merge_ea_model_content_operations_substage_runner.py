from bclearer_core.configurations.content_operation_configurations import (
    ContentOperationConfigurations,
)
from bclearer_core.configurations.load_ea_model_configurations import (
    LoadEaModelConfigurations,
)
from bclearer_core.substages.operations.a_load.content_operations.runners.ea_model_to_content_universe_loader import (
    load_ea_model_to_content_universe,
)
from bclearer_core.substages.operations.b_evolve.content_operations.content_operations_substages import (
    ContentOperationsSubstages,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.session.orchestrators.ea_tools_session_managers import (
    EaToolsSessionManagers,
)


def run_merge_ea_model_content_operations_substage(
    ea_tools_session_manager: EaToolsSessionManagers,
    content_1_universe: NfEaComUniverses,
    load_ea_model_configuration: LoadEaModelConfigurations,
    content_operation_configuration: ContentOperationConfigurations,
) -> NfEaComUniverses:
    content_2_universe = load_ea_model_to_content_universe(
        ea_tools_session_manager=ea_tools_session_manager,
        load_ea_model_configuration=load_ea_model_configuration,
    )

    with ContentOperationsSubstages(
        ea_tools_session_manager=ea_tools_session_manager,
        content_1_universe=content_1_universe,
        content_2_universe=content_2_universe,
        content_operation_configuration=content_operation_configuration,
    ) as content_operations_substage:
        content_operations_substage_output_universe = (
            content_operations_substage.run()
        )

        return content_operations_substage_output_universe
