from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_core.substages.operations.b_evolve.common.universes_merge_registers import (
    UniversesMergeRegisters,
)
from bclearer_core.substages.operations.b_evolve.content_operations.merge_universes.nf_ea_com_collection_processes.collection_type_compliation_constants import (
    LIST_OF_COLLECTION_TYPES_OF_OBJECTS_WITHOUT_EA_GUIDS,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import concat


def concat_universe_collections(
    collection_type: NfEaComCollectionTypes,
    universe_merge_register: UniversesMergeRegisters,
    output_universe: NfEaComUniverses,
):
    if not collection_type:
        log_message(
            message="CONTENT OPERATION: Concat universes - concatenating collections - No Collection type - Skipped",
        )
        return

    log_message(
        message="CONTENT OPERATION: Concat universes - concatenating collections - "
        + collection_type.collection_name,
    )

    primary_collection = universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections.get(
        collection_type
    )
    aligned_collection = universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections.get(
        collection_type
    )

    if (
        collection_type
        in LIST_OF_COLLECTION_TYPES_OF_OBJECTS_WITHOUT_EA_GUIDS
    ):
        concatenated_collection = (
            primary_collection.copy()
        )
    else:
        # Filter out empty DataFrames before concatenation
        collections_to_concat = [
            df
            for df in [
                primary_collection,
                aligned_collection,
            ]
            if not df.empty
        ]

        if collections_to_concat:
            concatenated_collection = concat(
                collections_to_concat
            )
        else:
            concatenated_collection = (
                primary_collection
            )

    concatenated_collection.reset_index(
        drop=True,
        inplace=True,
    )

    if (
        NfColumnTypes.NF_UUIDS.column_name
        in concatenated_collection.columns
    ):
        concatenated_collection.drop_duplicates(
            subset=NfColumnTypes.NF_UUIDS.column_name,
            inplace=True,
        )

    output_universe.nf_ea_com_registry.dictionary_of_collections[
        collection_type
    ] = concatenated_collection


# TODO: patched, needs to be replaced
#
# def concat_universe_collections(
#     collection_type: NfEaComCollectionTypes,
#     universe_merge_register: UniversesMergeRegisters,
#     output_universe: NfEaComUniverses,
# ):
#     if not collection_type:
#         log_message(
#             message="CONTENT OPERATION: Concat universes - concatenating collections - No Collection type - Skipped",
#         )
#
#         return
#
#     log_message(
#         message="CONTENT OPERATION: Concat universes - concatenating collections - "
#         + collection_type.collection_name,
#     )
#
#     if (
#         collection_type
#         in LIST_OF_COLLECTION_TYPES_OF_OBJECTS_WITHOUT_EA_GUIDS
#     ):
#         concatenated_collection = universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections[
#             collection_type
#         ].copy()
#
#     else:
#         concatenated_collection = concat(
#             [
#                 universe_merge_register.primary_universe.nf_ea_com_registry.dictionary_of_collections[
#                     collection_type
#                 ],
#                 universe_merge_register.aligned_universe.nf_ea_com_registry.dictionary_of_collections[
#                     collection_type
#                 ],
#             ],
#         )
#
#     concatenated_collection.reset_index(
#         drop=True,
#         inplace=True,
#     )
#
#     if (
#         NfColumnTypes.NF_UUIDS.column_name
#         in concatenated_collection.columns
#     ):
#         concatenated_collection.drop_duplicates(
#             subset=NfColumnTypes.NF_UUIDS.column_name,
#             inplace=True,
#         )
#
#     output_universe.nf_ea_com_registry.dictionary_of_collections[
#         collection_type
#     ] = concatenated_collection
