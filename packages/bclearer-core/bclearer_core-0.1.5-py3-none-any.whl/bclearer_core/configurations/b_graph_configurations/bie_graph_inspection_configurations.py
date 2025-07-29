from bclearer_core.configurations.bie_configurations.bie_configurations import (
    BieConfigurations,
)


class BieGraphMlInspectionConfigurations(
    BieConfigurations
):
    def __init__(self):
        super().__init__()

    PERSIST_GRAPH_ML_FOR_INSPECTION = (
        True
    )
