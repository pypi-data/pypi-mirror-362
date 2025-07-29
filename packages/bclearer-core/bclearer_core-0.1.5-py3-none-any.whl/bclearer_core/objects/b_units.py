from abc import abstractmethod

from bclearer_orchestration_services.reporting_service.wrappers.run_and_log_function_wrapper import (
    run_and_log_function,
)

# #from bie_base.b_source.common.configurations.b_unit_domain_configurations import BUnitDomainConfigurations
# #from core_graph_mvp_base.b_source.neo4j_entification_pipeline.objects.universes.neo4j_import_spoke_bclearer_run_universes import Neo4JImportSpokeBClearerRunUniverses
# from core_graph_mvp_base.b_source.neo4j_entification_pipeline.operations.b_units.registrations.output_domain_dataframes_registerer import register_output_domain_dataframes_in_domain_universe
# from core_graph_mvp_base.b_source.neo4j_entification_pipeline.objects.enums.reportable.bclearer_neo4j_entification_bunits import \
#     BClearerNeo4jEntificationBunits
# from core_graph_mvp_base.b_source.neo4j_entification_pipeline.operations.b_units.registrations.in_parallel_bie_universe_registerer import register_in_parallel_bie_universe
# from bie_base.b_source.common.enums.bie_enums import BieEnums
# # from bie_base.b_source.uncommon.bclearer_processing.registrations.b_unit_input_output_lists import \
# #     BUnitInputOutputLists


class BUnits:
    def __init__(
        self,
        # neo4j_import_spoke_bclearer_run_universe: Neo4JImportSpokeBClearerRunUniverses,
        # b_unit_bie_enum: BieEnums,
        # parent_bie_pipeline_component_enum: BieEnums
    ):
        # self.neo4j_import_spoke_bclearer_run_universe = \
        #     neo4j_import_spoke_bclearer_run_universe

        # self.b_unit_domain_configuration = \
        #     BUnitDomainConfigurations(
        #         b_unit_bie_enum=b_unit_bie_enum,
        #         parent_bie_pipeline_component_enum=parent_bie_pipeline_component_enum)
        pass

    def run(self) -> None:
        function_discriminator_name = (
            self.b_unit_domain_configuration.b_unit_bie_enum.b_enum_item_name
        )

        self.__run_b_unit(
            function_discriminator_name=function_discriminator_name
        )

    @run_and_log_function()
    def __run_b_unit(self) -> None:
        self.b_unit_process_function()

        # register_output_domain_dataframes_in_domain_universe(
        #     neo4j_import_spoke_bclearer_run_universe=self.neo4j_import_spoke_bclearer_run_universe,
        #     b_unit_domain_configuration=self.b_unit_domain_configuration)

        # # TODO: added here to avoid crashing because missing column
        # if self.b_unit_domain_configuration.b_unit_bie_enum != BClearerNeo4jEntificationBunits.LOAD_NEO4J:
        #     register_in_parallel_bie_universe(
        #         bie_universe=self.neo4j_import_spoke_bclearer_run_universe.parallel_bie_universe,
        #         b_unit_domain_configuration=self.b_unit_domain_configuration)

    @abstractmethod
    def b_unit_process_function(
        self,
    ) -> ():
        pass
