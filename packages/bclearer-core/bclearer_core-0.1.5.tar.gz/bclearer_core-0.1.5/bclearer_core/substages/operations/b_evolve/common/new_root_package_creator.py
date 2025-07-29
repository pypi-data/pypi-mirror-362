# TODO: this should not be needed,need a pandas concat function
import pandas as pd
from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_core.substages.operations.common.ea_guid_from_nf_uuid_creator import (
    create_ea_guid_from_nf_uuid,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.nf_ea_com_universes import (
    NfEaComUniverses,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.column_types.ea_t.ea_t_package_column_types import (
    EaTPackageColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def create_root_package(
    nf_ea_com_universe: NfEaComUniverses,
    package_name: str,
) -> str:
    package_collection = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_PACKAGES
    ]

    package_nf_uuid = create_new_uuid()

    package_ea_guid = (
        create_ea_guid_from_nf_uuid(
            nf_uuid=package_nf_uuid,
        )
    )

    package_ea_package_path = (
        package_name
    )

    ea_package_dictionary = {
        EaTPackageColumnTypes.T_PACKAGE_EA_GUIDS.nf_column_name: package_ea_guid,
        "ea_package_path": package_ea_package_path,
        "parent_package_ea_guid": DEFAULT_NULL_VALUE,
        "parent_package_name": DEFAULT_NULL_VALUE,
        NfColumnTypes.NF_UUIDS.column_name: package_nf_uuid,
        NfEaComColumnTypes.PACKAGES_CONTAINED_EA_PACKAGES.column_name: [],
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name: EaElementTypes.PACKAGE.type_name,
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS.column_name: [],
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name: DEFAULT_NULL_VALUE,
        NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: package_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: package_ea_guid,
    }

    new_row_df = pd.DataFrame(
        [ea_package_dictionary]
    )

    updated_package_collection = (
        pd.concat(
            [
                package_collection,
                new_row_df,
            ],
            ignore_index=True,
        )
    )

    nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        NfEaComCollectionTypes.EA_PACKAGES
    ] = updated_package_collection

    return package_nf_uuid
