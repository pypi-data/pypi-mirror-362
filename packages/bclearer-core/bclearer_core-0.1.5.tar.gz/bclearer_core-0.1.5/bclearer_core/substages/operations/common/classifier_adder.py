from bclearer_core.constants.standard_constants import (
    DEFAULT_NULL_VALUE,
)
from bclearer_core.nf.types.nf_column_types import (
    NfColumnTypes,
)
from bclearer_core.substages.operations.common.ea_guid_from_nf_uuid_creator import (
    create_ea_guid_from_nf_uuid,
)
from bclearer_interop_services.ea_interop_service.general.nf_ea.com.common_knowledge.column_types.nf_ea_com_column_types import (
    NfEaComColumnTypes,
)
from bclearer_interop_services.ea_interop_service.nf_ea_common.common_knowledge.ea_element_types import (
    EaElementTypes,
)
from bclearer_orchestration_services.identification_services.uuid_service.uuid_helpers.uuid_factory import (
    create_new_uuid,
)


def add_new_classifier_to_dictionary(
    new_classifier_dictionary: dict,
    package_nf_uuid: str,
    ea_element_type: EaElementTypes,
    class_name: str = "",
    elements_classifier: str = DEFAULT_NULL_VALUE,
) -> str:
    class_nf_uuid = create_new_uuid()

    class_ea_guid = (
        create_ea_guid_from_nf_uuid(
            nf_uuid=class_nf_uuid,
        )
    )

    class_row_dictionary = {
        NfColumnTypes.NF_UUIDS.column_name: class_nf_uuid,
        NfEaComColumnTypes.ELEMENTS_CLASSIFIER.column_name: elements_classifier,
        NfEaComColumnTypes.CLASSIFIERS_ALL_COMPONENT_EA_ATTRIBUTES.column_name: [],
        NfEaComColumnTypes.ELEMENTS_EA_OBJECT_TYPE.column_name: ea_element_type.type_name,
        NfEaComColumnTypes.ELEMENTS_SUPPLIER_PLACE1_END_CONNECTORS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CLIENT_PLACE2_END_CONNECTORS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_DIAGRAMS.column_name: [],
        NfEaComColumnTypes.ELEMENTS_CONTAINED_EA_CLASSIFIERS.column_name: [],
        NfEaComColumnTypes.PACKAGEABLE_OBJECTS_PARENT_EA_ELEMENT.column_name: package_nf_uuid,
        NfEaComColumnTypes.STEREOTYPEABLE_OBJECTS_EA_OBJECT_STEREOTYPES.column_name: [],
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_OBJECT_NAME.column_name: class_name,
        NfEaComColumnTypes.EXPLICIT_OBJECTS_EA_GUID.column_name: class_ea_guid,
    }

    new_classifier_dictionary[
        class_nf_uuid
    ] = class_row_dictionary

    return class_nf_uuid
