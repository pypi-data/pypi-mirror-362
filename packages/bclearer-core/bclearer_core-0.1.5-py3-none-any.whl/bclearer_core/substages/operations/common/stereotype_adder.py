from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_property_types import (
    EaPropertyTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def add_new_stereotype_usage_to_dictionary(
    new_stereotype_usage_dictionary: dict,
    client_nf_uuid: str,
    client_collection_type: NfEaComCollectionTypes,
    stereotype_nf_uuid: str,
) -> None:
    if (
        client_collection_type
        == NfEaComCollectionTypes.EA_CLASSIFIERS
    ):
        property_type = (
            EaPropertyTypes.ELEMENT_PROPERTY.type_name
        )

    elif (
        client_collection_type
        == NfEaComCollectionTypes.EA_CONNECTORS
    ):
        property_type = (
            EaPropertyTypes.CONNECTOR_PROPERTY.type_name
        )

    elif (
        client_collection_type
        == NfEaComCollectionTypes.EA_ATTRIBUTES
    ):
        property_type = (
            EaPropertyTypes.ATTRIBUTE_PROPERTY.type_name
        )

    else:
        raise NotImplementedError

    stereotype_usage_row_dictionary = {
        NfEaComColumnTypes.STEREOTYPE_CLIENT_NF_UUIDS.column_name: client_nf_uuid,
        "stereotype_nf_uuids": stereotype_nf_uuid,
        NfEaComColumnTypes.STEREOTYPE_PROPERTY_TYPE.column_name: property_type,
    }

    new_stereotype_usage_dictionary[
        create_new_uuid()
    ] = stereotype_usage_row_dictionary
