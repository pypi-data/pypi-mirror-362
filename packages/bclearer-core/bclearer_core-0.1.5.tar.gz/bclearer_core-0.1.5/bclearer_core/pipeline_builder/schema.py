"""JSON schema for bclearer pipeline configurations."""

from dataclasses import dataclass
from typing import (
    Dict,
    List,
    Optional,
    Union,
)


@dataclass
class BUnitConfig:
    """Configuration for a bUnit in a pipeline stage."""

    name: str


@dataclass
class SubStageConfig:
    """Configuration for a sub-stage in a pipeline stage."""

    name: str
    b_units: List[str]


@dataclass
class StageConfig:
    """Configuration for a stage in a pipeline."""

    name: str
    sub_stages: List[SubStageConfig]
    b_units: List[str]


@dataclass
class ThinSliceConfig:
    """Configuration for a thin slice in a pipeline."""

    name: str
    stages: List[StageConfig]


@dataclass
class PipelineConfig:
    """Configuration for a pipeline in a domain."""

    name: str
    thin_slices: List[ThinSliceConfig]


@dataclass
class DomainConfig:
    """Top-level configuration for a domain with pipelines."""

    domain_name: str
    pipelines: List[PipelineConfig]


def validate_pipeline_config(
    config_dict: Dict,
) -> DomainConfig:
    """
    Validates the pipeline configuration dictionary and converts it to a DomainConfig object.

    Args:
        config_dict: Dictionary containing the pipeline configuration

    Returns:
        DomainConfig object
    """
    try:
        domain_name = config_dict.get(
            "domain_name"
        )
        if not domain_name:
            raise ValueError(
                "domain_name is required"
            )

        pipelines_data = (
            config_dict.get(
                "pipelines", []
            )
        )
        pipelines = []

        for (
            pipeline_data
        ) in pipelines_data:
            pipeline_name = (
                pipeline_data.get(
                    "name"
                )
            )
            if not pipeline_name:
                raise ValueError(
                    "Pipeline name is required"
                )

            thin_slices_data = (
                pipeline_data.get(
                    "thin_slices", []
                )
            )
            thin_slices = []

            for (
                thin_slice_data
            ) in thin_slices_data:
                thin_slice_name = (
                    thin_slice_data.get(
                        "name"
                    )
                )
                if not thin_slice_name:
                    raise ValueError(
                        f"Thin slice name is required in pipeline '{pipeline_name}'"
                    )

                stages_data = (
                    thin_slice_data.get(
                        "stages", []
                    )
                )
                stages = []

                for (
                    stage_data
                ) in stages_data:
                    stage_name = (
                        stage_data.get(
                            "name"
                        )
                    )
                    if not stage_name:
                        raise ValueError(
                            f"Stage name is required in thin slice '{thin_slice_name}'"
                        )

                    sub_stages_data = stage_data.get(
                        "sub_stages", []
                    )
                    sub_stages = []

                    for (
                        sub_stage_data
                    ) in (
                        sub_stages_data
                    ):
                        sub_stage_name = sub_stage_data.get(
                            "name"
                        )
                        if (
                            not sub_stage_name
                        ):
                            raise ValueError(
                                f"Sub-stage name is required in stage '{stage_name}'"
                            )

                        b_units = sub_stage_data.get(
                            "b_units",
                            [],
                        )

                        sub_stages.append(
                            SubStageConfig(
                                name=sub_stage_name,
                                b_units=b_units,
                            )
                        )

                    b_units = (
                        stage_data.get(
                            "b_units",
                            [],
                        )
                    )

                    stages.append(
                        StageConfig(
                            name=stage_name,
                            sub_stages=sub_stages,
                            b_units=b_units,
                        )
                    )

                thin_slices.append(
                    ThinSliceConfig(
                        name=thin_slice_name,
                        stages=stages,
                    )
                )

            pipelines.append(
                PipelineConfig(
                    name=pipeline_name,
                    thin_slices=thin_slices,
                )
            )

        return DomainConfig(
            domain_name=domain_name,
            pipelines=pipelines,
        )
    except Exception as e:
        raise ValueError(
            f"Invalid pipeline configuration: {str(e)}"
        )


def get_sample_config() -> Dict:
    """
    Returns a sample pipeline configuration.

    Returns:
        Dict containing a sample pipeline configuration
    """
    return {
        "domain_name": "example_domain",
        "pipelines": [
            {
                "name": "pipeline_name",
                "thin_slices": [
                    {
                        "name": "thin_slice_1",
                        "stages": [
                            {
                                "name": "1c_collect",
                                "sub_stages": [],
                                "b_units": [
                                    "ca_b_unit",
                                    "cb_b_unit",
                                ],
                            },
                            {
                                "name": "2l_load",
                                "sub_stages": [],
                                "b_units": [
                                    "la_b_unit",
                                    "lb_b_unit",
                                ],
                            },
                            {
                                "name": "3e_evolve",
                                "sub_stages": [
                                    {
                                        "name": "sub_stage_1",
                                        "b_units": [
                                            "ea1_b_unit",
                                            "ea2_b_unit",
                                        ],
                                    },
                                    {
                                        "name": "sub_stage_2",
                                        "b_units": [
                                            "eb1_b_unit",
                                            "eb2_b_unit",
                                        ],
                                    },
                                ],
                                "b_units": [],
                            },
                            {
                                "name": "4a_assimilate",
                                "sub_stages": [],
                                "b_units": [
                                    "aa_b_unit",
                                    "ab_b_unit",
                                ],
                            },
                            {
                                "name": "5r_reuse",
                                "sub_stages": [],
                                "b_units": [
                                    "ra_b_unit",
                                    "rb_b_unit",
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    }
