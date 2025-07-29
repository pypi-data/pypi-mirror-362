from enum import auto, unique

from bclearer_core.nf.types.column_types import (
    ColumnTypes,
)


@unique
class NfColumnTypes(ColumnTypes):
    NF_UUIDS = auto()

    UNIVERSE_KEYS = auto()

    COLLECTION_TYPES = auto()

    def __column_name(self) -> str:
        column_name = (
            column_name_mapping[self]
        )

        return column_name

    column_name = property(
        fget=__column_name,
    )


column_name_mapping = {
    NfColumnTypes.NF_UUIDS: "nf_uuids",
    NfColumnTypes.UNIVERSE_KEYS: "universe_keys",
    NfColumnTypes.COLLECTION_TYPES: "collection_types",
}
