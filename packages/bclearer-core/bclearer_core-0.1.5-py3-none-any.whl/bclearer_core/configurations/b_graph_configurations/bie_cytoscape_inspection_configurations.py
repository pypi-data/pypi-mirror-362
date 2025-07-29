from bclearer_core.configurations.bie_configurations.bie_configurations import (
    BieConfigurations,
)


class BieCytoscapeInspectionConfigurations(
    BieConfigurations
):
    def __init__(self):
        super().__init__()

    ENABLE_CYTOSCAPE_GRAPH_INSPECTION = (
        True
    )

    CYTOSCAPE_IS_RUNNING = False

    CYTOSCAPE_MAXIMUM_ALLOCATED_RAM_MEMORY = (
        "4"
    )

    CYTOSCAPE_WAIT_TIME = 30

    CYTOSCAPE_NUMBER_OF_WAIT_INTERVALS = (
        5
    )
