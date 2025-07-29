from enum import Enum


class ColumnTypes(Enum):
    def __column_name(self) -> str:
        raise NotImplementedError

    column_name = property(
        fget=__column_name,
    )
