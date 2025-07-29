from enum import auto, unique

from bclearer_core.common_knowledge.operation_types import (
    OperationTypes,
)


@unique
class ContentOperationTypes(
    OperationTypes,
):
    MERGE_UNIVERSES = auto()

    def __operation_name(self) -> str:
        operation_name = (
            operation_name_mapping[self]
        )

        return operation_name

    operation_name = property(
        fget=__operation_name,
    )


operation_name_mapping = {
    ContentOperationTypes.MERGE_UNIVERSES: "merge_universes",
}
