from enum import auto, unique

from bclearer_core.common_knowledge.operation_types import (
    OperationTypes,
)


@unique
class AttributeToAssociationOperationSubtypes(
    OperationTypes,
):
    DIRECT_FOREIGN_TABLE = auto()
    SUBTYPE_OF_FOREIGN_TABLE = auto()

    def __operation_name(self) -> str:
        operation_name = (
            operation_name_mapping[self]
        )

        return operation_name

    operation_name = property(
        fget=__operation_name,
    )


operation_name_mapping = {
    AttributeToAssociationOperationSubtypes.DIRECT_FOREIGN_TABLE: "direct_foreign_table",
    AttributeToAssociationOperationSubtypes.SUBTYPE_OF_FOREIGN_TABLE: "subtype_of_foreign_table",
}
