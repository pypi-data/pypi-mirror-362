from enum import Enum, auto


class LoggingInspectionLevelBEnums(
    Enum
):
    NOT_SET = auto()

    VERBOSE = auto()

    INFO = auto()

    WARNING = auto()

    ERROR = auto()

    CRITICAL = auto()

    def __enum_level_weight(
        self,
    ) -> str:
        enum_level_weight = (
            enum_level_weight_mapping[
                self
            ]
        )

        return enum_level_weight

    enum_level_weight = property(
        fget=__enum_level_weight
    )


enum_level_weight_mapping = {
    LoggingInspectionLevelBEnums.NOT_SET: int(),
    LoggingInspectionLevelBEnums.VERBOSE: 1,
    LoggingInspectionLevelBEnums.INFO: 2,
    LoggingInspectionLevelBEnums.WARNING: 3,
    LoggingInspectionLevelBEnums.ERROR: 4,
    LoggingInspectionLevelBEnums.CRITICAL: 5,
}
