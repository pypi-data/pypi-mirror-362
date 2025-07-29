import re
from enum import Enum


class BEnums(Enum):
    @classmethod
    def b_enum_name(cls):
        class_name = cls.__qualname__

        pattern = re.compile(
            r"(?<!^)(?=[A-Z])"
        )

        b_enum_name = pattern.sub(
            "_", class_name
        ).lower()

        return b_enum_name

    @property
    def b_enum_item_name(self):
        b_enum_item_name = str.casefold(
            self.name
        )

        return b_enum_item_name
