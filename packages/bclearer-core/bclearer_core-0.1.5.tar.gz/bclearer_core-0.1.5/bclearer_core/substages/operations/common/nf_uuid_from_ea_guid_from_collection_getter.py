from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
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


def get_nf_uuid_from_ea_guid_from_collection(
    nf_ea_com_universe: NfEaComUniverses,
    collection_type: NfEaComCollectionTypes,
    ea_guid: str,
) -> str:
    collection = nf_ea_com_universe.nf_ea_com_registry.dictionary_of_collections[
        collection_type
    ]

    nf_uuid = collection.at[
        collection[
            NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name
        ]
        .eq(ea_guid)
        .idxmax(),
        NfColumnTypes.NF_UUIDS.column_name,
    ]

    return nf_uuid
