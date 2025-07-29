from bclearer_core.substages.operations.common.classifier_adder import (
    add_new_classifier_to_dictionary,
)
from bclearer_core.substages.operations.common.connector_adder import (
    add_new_connector_to_dictionary,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.collection_types.nf_ea_com_collection_types import (
    NfEaComCollectionTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_connector_types import (
    EaConnectorTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)


def add_new_connector_to_connector_to_dictionary(
    new_ea_objects_dictionary: dict,
    package_nf_uuid: str,
    connector_nf_uuid: str,
    class_nf_uuid: str,
) -> str:
    proxy_connector_nf_uuid = add_new_classifier_to_dictionary(
        new_classifier_dictionary=new_ea_objects_dictionary[
            NfEaComCollectionTypes.EA_CLASSIFIERS
        ],
        package_nf_uuid=package_nf_uuid,
        ea_element_type=EaElementTypes.PROXY_CONNECTOR,
        elements_classifier=connector_nf_uuid,
    )

    connector_nf_uuid = add_new_connector_to_dictionary(
        new_connector_dictionary=new_ea_objects_dictionary[
            NfEaComCollectionTypes.EA_CONNECTORS
        ],
        place_1_nf_uuid=proxy_connector_nf_uuid,
        place_2_nf_uuid=class_nf_uuid,
        connector_type=EaConnectorTypes.DEPENDENCY,
    )

    return connector_nf_uuid
