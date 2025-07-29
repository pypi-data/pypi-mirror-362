from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.reporting_service.reporters.log_with_datetime import (
    log_message,
)
from pandas import DataFrame


def shift_convention_objects_to_classes(
    content_universe: NfEaComUniverses,
    output_universe: NfEaComUniverses,
) -> None:
    __run_input_checks()

    __run_operation(
        content_universe=content_universe,
        output_universe=output_universe,
    )


def __run_operation(
    content_universe: NfEaComUniverses,
    output_universe: NfEaComUniverses,
) -> None:
    log_message(
        message="CONVENTION SHIFT OPERATION: Shift objects to classes - started",
    )

    content_collections_dictionary = (
        content_universe.nf_ea_com_registry.dictionary_of_collections
    )

    for (
        content_collection_type,
        content_collection_table,
    ) in (
        content_collections_dictionary.items()
    ):
        __process_content_collection(
            content_collection_type=content_collection_type,
            content_collection_table=content_collection_table,
            output_universe=output_universe,
        )

    log_message(
        message="CONVENTION SHIFT OPERATION: Shift objects to classes - finished",
    )


def __run_input_checks():
    pass


def __process_content_collection(
    content_collection_type: NfEaComCollectionTypes,
    content_collection_table: DataFrame,
    output_universe: NfEaComUniverses,
) -> None:
    output_collections_dictionary = (
        output_universe.nf_ea_com_registry.dictionary_of_collections
    )

    if (
        content_collection_type
        == NfEaComCollectionTypes.EA_CLASSIFIERS
    ):
        __convert_objects_to_classes(
            output_collections_dictionary=output_collections_dictionary,
            ea_classifiers=content_collection_table,
        )

    else:
        output_collections_dictionary[
            content_collection_type
        ] = content_collection_table


def __convert_objects_to_classes(
    output_collections_dictionary: dict,
    ea_classifiers: DataFrame,
) -> None:
    ea_object_type_column_name = (
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name
    )

    number_of_objects_before_conversion = len(
        ea_classifiers[
            ea_classifiers[
                ea_object_type_column_name
            ]
            == EaElementTypes.OBJECT.type_name
        ].index,
    )
    # TODO: replaced to address warning from pandas : FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
    #   The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a copy.
    # ea_classifiers[
    #     ea_object_type_column_name
    # ].replace(
    #     to_replace=EaElementTypes.OBJECT.type_name,
    #     value=EaElementTypes.CLASS.type_name,
    #     inplace=True,
    # )

    ea_classifiers[
        ea_object_type_column_name
    ] = ea_classifiers[
        ea_object_type_column_name
    ].replace(
        to_replace=EaElementTypes.OBJECT.type_name,
        value=EaElementTypes.CLASS.type_name,
    )

    number_of_objects_after_conversion = len(
        ea_classifiers[
            ea_classifiers[
                ea_object_type_column_name
            ]
            == EaElementTypes.OBJECT.type_name
        ].index,
    )

    number_of_objects_converted_to_classes = (
        number_of_objects_before_conversion
        - number_of_objects_after_conversion
    )

    log_message(
        message="CONVENTION SHIFT OPERATION: Shift objects to classes - Number of objects converted: "
        + str(
            number_of_objects_converted_to_classes,
        ),
    )

    output_collections_dictionary[
        NfEaComCollectionTypes.EA_CLASSIFIERS
    ] = ea_classifiers
