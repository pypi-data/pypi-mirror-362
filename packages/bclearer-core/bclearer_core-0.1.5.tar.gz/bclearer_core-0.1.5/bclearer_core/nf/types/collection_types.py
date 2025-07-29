from enum import Enum


class CollectionTypes(Enum):
    def __collection_name(self) -> str:
        raise NotImplementedError

    collection_name = property(
        fget=__collection_name,
    )
