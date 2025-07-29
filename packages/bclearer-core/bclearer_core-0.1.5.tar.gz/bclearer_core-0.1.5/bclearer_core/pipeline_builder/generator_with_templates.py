"""Pipeline generator module for creating pipeline structure from configuration."""

import os
import shutil
from pathlib import Path
from typing import (
    Dict,
    List,
    Optional,
    Set,
    Tuple,
)

from bclearer_core.pipeline_builder.schema import (
    DomainConfig,
    PipelineConfig,
    StageConfig,
    SubStageConfig,
    ThinSliceConfig,
)
from bclearer_core.pipeline_builder.templates import (
    APPLICATION_RUNNER_TEMPLATE,
    B_UNIT_CREATOR_AND_RUNNER_TEMPLATE,
    B_UNIT_IMPORT_TEMPLATE,
    B_UNIT_TEMPLATE,
    CONFTEST_TEMPLATE,
    E2E_TEST_TEMPLATE,
    ORCHESTRATE_STAGE_CALL,
    ORCHESTRATE_SUB_STAGE_CALL,
    ORCHESTRATE_THIN_SLICE_CALL,
    PIPELINE_EMPTY_FUNCTION_BODY,
    PIPELINE_IMPORT_TEMPLATE,
    PIPELINE_ORCHESTRATOR_FUNCTION_START,
    PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE,
    PIPELINE_RUNNER_CALL,
    PIPELINE_RUNNER_TEMPLATE,
    PIPELINES_EMPTY_FUNCTION_BODY,
    PIPELINES_RUNNER_FUNCTION_START,
    PIPELINES_RUNNER_TEMPLATE_HEADER,
    STAGE_B_UNIT_CREATOR_IMPORT,
    STAGE_CREATE_AND_RUN_B_UNIT_CALL,
    STAGE_EMPTY_FUNCTION_BODY,
    STAGE_ORCHESTRATOR_FUNCTION_START,
    STAGE_ORCHESTRATOR_HEADER,
    SUB_STAGE_B_UNIT_CREATOR_IMPORT,
    SUB_STAGE_B_UNIT_IMPORT_TEMPLATE,
    SUB_STAGE_CREATE_AND_RUN_B_UNIT_CALL,
    SUB_STAGE_EMPTY_FUNCTION_BODY,
    SUB_STAGE_IMPORT_TEMPLATE,
    SUB_STAGE_ORCHESTRATOR_FUNCTION_START,
    SUB_STAGE_ORCHESTRATOR_HEADER,
    THIN_SLICE_EMPTY_FUNCTION_BODY,
    THIN_SLICE_ORCHESTRATOR_FUNCTION_START,
    THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE,
)


class PipelineUpdater:
    """Updater class for updating existing pipeline structure with new configuration."""

    def __init__(
        self, pipeline_path: str
    ):
        """
        Initialize the PipelineUpdater.

        Args:
            pipeline_path: Path to the existing pipeline directory
        """
        self.pipeline_path = Path(
            pipeline_path
        )

        if (
            not self.pipeline_path.exists()
        ):
            raise FileNotFoundError(
                f"Pipeline path not found: {pipeline_path}"
            )

        if (
            not self.pipeline_path.is_dir()
        ):
            raise NotADirectoryError(
                f"Pipeline path is not a directory: {pipeline_path}"
            )

        # Extract domain name from path - format is expected to be bclearer_pipelines/domain_name
        if "bclearer_pipelines" in str(
            self.pipeline_path
        ):
            self.existing_domain_name = (
                self.pipeline_path.name
            )
        else:
            raise ValueError(
                f"Path does not follow the expected format bclearer_pipelines/domain_name: {pipeline_path}"
            )

    def update_pipeline(
        self, config: DomainConfig
    ) -> str:
        """
        Update pipeline structure from configuration.

        Args:
            config: Domain configuration

        Returns:
            Path to the updated pipeline
        """
        # Verify domain name matches
        if (
            config.domain_name
            != self.existing_domain_name
        ):
            raise ValueError(
                f"Domain name in configuration ('{config.domain_name}') does not match "
                f"existing domain name ('{self.existing_domain_name}')"
            )

        domain_path = self.pipeline_path
        b_source_path = (
            domain_path / "b_source"
        )

        # Update app_runners/runners directory
        runners_path = (
            b_source_path
            / "app_runners"
            / "runners"
        )

        # Get existing pipelines
        existing_pipelines = self._get_existing_pipelines(
            runners_path
        )

        # Create or update pipelines
        for (
            pipeline_config
        ) in config.pipelines:
            pipeline_name = (
                pipeline_config.name
            )
            pipeline_path = (
                b_source_path
                / pipeline_name
            )

            if (
                pipeline_name
                not in existing_pipelines
            ):
                # Create new pipeline directory if it doesn't exist
                pipeline_path.mkdir(
                    exist_ok=True
                )
                self._create_init_file(
                    pipeline_path
                )

                # Create pipeline subdirectories
                self._create_pipeline_subdirectories(
                    pipeline_path
                )

                # Create pipeline runner
                self._create_pipeline_runner(
                    runners_path,
                    config.domain_name,
                    pipeline_name,
                )

                # Add to existing pipelines list for pipelines_runner update
                existing_pipelines.add(
                    pipeline_name
                )

            # Process thin slices for this pipeline
            self._update_pipeline_thin_slices(
                b_source_path,
                pipeline_config,
                config.domain_name,
            )

        # Update the pipelines_runner to include all pipelines
        self._update_pipelines_runner(
            runners_path,
            config.domain_name,
            list(existing_pipelines),
            config.pipelines,
        )

        return str(domain_path)

    def _get_existing_pipelines(
        self, runners_path: Path
    ) -> Set[str]:
        """
        Get names of existing pipelines from runner files.

        Args:
            runners_path: Path to the runners directory

        Returns:
            Set of existing pipeline names
        """
        existing_pipelines = set()

        for (
            file_path
        ) in runners_path.glob(
            "*_runner.py"
        ):
            pipeline_name = (
                file_path.stem.replace(
                    "_runner", ""
                )
            )
            # Exclude pipelines_runner from the list
            if not pipeline_name.endswith(
                "_b_clearer_pipelines"
            ):
                existing_pipelines.add(
                    pipeline_name
                )

        return existing_pipelines

    def _create_pipeline_subdirectories(
        self, pipeline_path: Path
    ) -> None:
        """
        Create subdirectories for a new pipeline.

        Args:
            pipeline_path: Path to the pipeline directory
        """
        # Create objects directory structure
        objects_path = (
            pipeline_path / "objects"
        )
        objects_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            objects_path
        )

        enums_path = (
            objects_path / "enums"
        )
        enums_path.mkdir(exist_ok=True)
        self._create_init_file(
            enums_path
        )

        universes_path = (
            objects_path / "universes"
        )
        universes_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            universes_path
        )

        b_units_path = (
            objects_path / "b_units"
        )
        b_units_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            b_units_path
        )

        # Create operations directory
        operations_path = (
            pipeline_path / "operations"
        )
        operations_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            operations_path
        )

        # Create orchestrators directory structure
        orchestrators_path = (
            pipeline_path
            / "orchestrators"
        )
        orchestrators_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            orchestrators_path
        )

        pipeline_orchestrators_path = (
            orchestrators_path
            / "pipeline"
        )
        pipeline_orchestrators_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            pipeline_orchestrators_path
        )

        thin_slices_path = (
            orchestrators_path
            / "thin_slices"
        )
        thin_slices_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            thin_slices_path
        )

        stages_path = (
            orchestrators_path
            / "stages"
        )
        stages_path.mkdir(exist_ok=True)
        self._create_init_file(
            stages_path
        )

        sub_stages_path = (
            orchestrators_path
            / "sub_stages"
        )
        sub_stages_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            sub_stages_path
        )

    def _update_pipeline_thin_slices(
        self,
        b_source_path: Path,
        pipeline_config: PipelineConfig,
        domain_name: str,
    ) -> None:
        """
        Update or create thin slices for a pipeline.

        Args:
            b_source_path: Path to the b_source directory
            pipeline_config: Pipeline configuration
            domain_name: Name of the domain
        """
        pipeline_name = (
            pipeline_config.name
        )
        pipeline_path = (
            b_source_path
            / pipeline_name
        )

        # Get orchestrators paths
        orchestrators_path = (
            pipeline_path
            / "orchestrators"
        )
        thin_slices_path = (
            orchestrators_path
            / "thin_slices"
        )
        stages_path = (
            orchestrators_path
            / "stages"
        )
        sub_stages_path = (
            orchestrators_path
            / "sub_stages"
        )
        pipeline_orchestrators_path = (
            orchestrators_path
            / "pipeline"
        )

        # Get b_units path
        b_units_path = (
            pipeline_path
            / "objects"
            / "b_units"
        )

        # Create or update pipeline orchestrator
        self._create_pipeline_orchestrator(
            pipeline_orchestrators_path,
            domain_name,
            pipeline_name,
            pipeline_config,
        )

        # Process each thin slice
        for (
            thin_slice
        ) in (
            pipeline_config.thin_slices
        ):
            # Create thin slice orchestrator
            self._create_thin_slice(
                domain_name,
                pipeline_name,
                thin_slice,
                thin_slices_path,
                stages_path,
                sub_stages_path,
                b_units_path,
            )

    def _update_pipelines_runner(
        self,
        runners_path: Path,
        domain_name: str,
        existing_pipelines: List[str],
        new_pipelines: List[
            PipelineConfig
        ],
    ) -> None:
        """
        Update the pipelines runner file to include all pipelines.

        Args:
            runners_path: Path to the runners directory
            domain_name: Name of the domain
            existing_pipelines: List of existing pipeline names
            new_pipelines: List of new pipeline configurations
        """
        # Add any new pipelines that aren't in existing_pipelines yet
        pipeline_names = set(
            existing_pipelines
        )
        for pipeline in new_pipelines:
            pipeline_names.add(
                pipeline.name
            )

        # Sort pipeline names for consistent output
        sorted_pipeline_names = sorted(
            list(pipeline_names)
        )

        file_path = (
            runners_path
            / f"{domain_name}_b_clearer_pipelines_runner.py"
        )

        # Create header with imports
        content = PIPELINES_RUNNER_TEMPLATE_HEADER

        # Add imports for each pipeline
        for (
            pipeline_name
        ) in sorted_pipeline_names:
            pipeline_import = PIPELINE_IMPORT_TEMPLATE.format(
                domain_name=domain_name,
                pipeline_name=pipeline_name,
            )
            content += pipeline_import

        # Add function definition
        content += PIPELINES_RUNNER_FUNCTION_START.format(
            domain_name=domain_name
        )

        # Add function calls
        if sorted_pipeline_names:
            for (
                pipeline_name
            ) in sorted_pipeline_names:
                content += PIPELINE_RUNNER_CALL.format(
                    pipeline_name=pipeline_name
                )
        else:
            content += PIPELINES_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_init_file(
        self, directory_path: Path
    ) -> None:
        """
        Create an empty __init__.py file in a directory.

        Args:
            directory_path: Path to the directory
        """
        init_file = (
            directory_path
            / "__init__.py"
        )
        init_file.touch(exist_ok=True)

    def _create_pipeline_orchestrator(
        self,
        pipeline_orchestrators_path: Path,
        domain_name: str,
        pipeline_name: str,
        pipeline_config: PipelineConfig,
    ) -> None:
        """
        Create pipeline orchestrator file.

        Args:
            pipeline_orchestrators_path: Path to the pipeline orchestrators directory
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            pipeline_config: Pipeline configuration
        """
        file_path = (
            pipeline_orchestrators_path
            / f"{pipeline_name}_orchestrator.py"
        )

        content = ""
        # Add imports for each thin slice
        if pipeline_config.thin_slices:
            for (
                thin_slice
            ) in (
                pipeline_config.thin_slices
            ):
                content += PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    thin_slice_name=thin_slice.name,
                )

        # Add function definition
        content += PIPELINE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name
        )

        # Add calls to thin slice orchestrators
        if pipeline_config.thin_slices:
            for (
                thin_slice
            ) in (
                pipeline_config.thin_slices
            ):
                content += ORCHESTRATE_THIN_SLICE_CALL.format(
                    thin_slice_name=thin_slice.name
                )
        else:
            content += PIPELINE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_pipeline_runner(
        self,
        runners_path: Path,
        domain_name: str,
        pipeline_name: str,
    ) -> None:
        """
        Create a pipeline runner file.

        Args:
            runners_path: Path to the runners directory
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
        """
        file_path = (
            runners_path
            / f"{pipeline_name}_runner.py"
        )

        content = PIPELINE_RUNNER_TEMPLATE.format(
            domain_name=domain_name,
            pipeline_name=pipeline_name,
        )

        with open(file_path, "w") as f:
            f.write(content)

    def _create_thin_slice(
        self,
        domain_name: str,
        pipeline_name: str,
        thin_slice: ThinSliceConfig,
        thin_slices_path: Path,
        stages_path: Path,
        sub_stages_path: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create thin slice orchestrator and related files.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            thin_slice: Thin slice configuration
            thin_slices_path: Path to the thin slices directory
            stages_path: Path to the stages directory
            sub_stages_path: Path to the sub-stages directory
            b_units_path: Path to the b_units directory
        """
        slice_name = thin_slice.name
        file_path = (
            thin_slices_path
            / f"{slice_name}_orchestrator.py"
        )

        content = ""
        # Add imports for each stage
        for stage in thin_slice.stages:
            stage_name = stage.name
            content += THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE.format(
                domain_name=domain_name,
                pipeline_name=pipeline_name,
                stage_name=stage_name,
            )

            # Create stage orchestrator
            self._create_stage_orchestrator(
                domain_name,
                pipeline_name,
                stage,
                stages_path,
                sub_stages_path,
                b_units_path,
            )

        # Add function definition
        content += THIN_SLICE_ORCHESTRATOR_FUNCTION_START.format(
            thin_slice_name=slice_name
        )

        # Add calls to stage orchestrators
        if thin_slice.stages:
            for (
                stage
            ) in thin_slice.stages:
                content += ORCHESTRATE_STAGE_CALL.format(
                    pipeline_name=pipeline_name,
                    stage_name=stage.name,
                )
        else:
            content += THIN_SLICE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_stage_orchestrator(
        self,
        domain_name: str,
        pipeline_name: str,
        stage: StageConfig,
        stages_path: Path,
        sub_stages_path: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create stage orchestrator file.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            stage: Stage configuration
            stages_path: Path to the stages directory
            sub_stages_path: Path to the sub-stages directory
            b_units_path: Path to the b_units directory
        """
        stage_name = stage.name
        file_path = (
            stages_path
            / f"{pipeline_name}_{stage_name}_orchestrator.py"
        )

        # Start with the header imports
        content = (
            STAGE_ORCHESTRATOR_HEADER
        )

        # Add imports for sub-stages if they exist
        if stage.sub_stages:
            for (
                sub_stage
            ) in stage.sub_stages:
                sub_stage_name = (
                    sub_stage.name
                )
                content += SUB_STAGE_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                )

                # Create sub-stage directory and orchestrator
                sub_stage_dir = (
                    sub_stages_path
                    / f"{pipeline_name}_{stage_name}_{sub_stage_name}"
                )
                sub_stage_dir.mkdir(
                    exist_ok=True
                )
                self._create_init_file(
                    sub_stage_dir
                )
                self._create_sub_stage_orchestrator(
                    domain_name,
                    pipeline_name,
                    stage_name,
                    sub_stage,
                    sub_stage_dir,
                    b_units_path,
                )

        # Add b_unit creator import if there are b_units
        if stage.b_units:
            content += STAGE_B_UNIT_CREATOR_IMPORT.format(
                domain_name=domain_name
            )

            # Create stage directory for b_units if doesn't exist
            stage_b_units_dir = (
                b_units_path
                / f"{pipeline_name}_{stage_name}"
            )
            stage_b_units_dir.mkdir(
                exist_ok=True
            )
            self._create_init_file(
                stage_b_units_dir
            )

            # Add imports for each b_unit
            for b_unit in stage.b_units:
                # Format the class name by removing underscores and capitalizing words
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += B_UNIT_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    b_unit_lower=b_unit.lower(),
                    b_unit_class=class_name,
                )

                # Create b_unit file
                self._create_b_unit(
                    b_unit,
                    stage_b_units_dir,
                )

        # Add function definition
        content += STAGE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name,
            stage_name=stage_name,
        )

        # Add sub-stage calls
        if stage.sub_stages:
            for (
                sub_stage
            ) in stage.sub_stages:
                sub_stage_name = (
                    sub_stage.name
                )
                content += ORCHESTRATE_SUB_STAGE_CALL.format(
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                )

        # Add b_unit calls
        if stage.b_units:
            if stage.sub_stages:
                content += "\n"

            for b_unit in stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += STAGE_CREATE_AND_RUN_B_UNIT_CALL.format(
                    b_unit_class=class_name,
                )

        # Add empty function body if needed
        if (
            not stage.sub_stages
            and not stage.b_units
        ):
            content += STAGE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_sub_stage_orchestrator(
        self,
        domain_name: str,
        pipeline_name: str,
        stage_name: str,
        sub_stage: SubStageConfig,
        sub_stage_dir: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create sub-stage orchestrator file.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            stage_name: Name of the stage
            sub_stage: Sub-stage configuration
            sub_stage_dir: Path to the sub-stage directory
            b_units_path: Path to the b_units directory
        """
        sub_stage_name = sub_stage.name
        file_path = (
            sub_stage_dir
            / f"{pipeline_name}_{stage_name}_{sub_stage_name}_orchestrator.py"
        )

        # Start with the header imports
        content = SUB_STAGE_ORCHESTRATOR_HEADER

        # Add b_unit creator import if there are b_units
        if sub_stage.b_units:
            content += SUB_STAGE_B_UNIT_CREATOR_IMPORT.format(
                domain_name=domain_name
            )

            # Create sub-stage directory for b_units if doesn't exist
            sub_stage_b_units_dir = (
                b_units_path
                / f"{pipeline_name}_{stage_name}"
                / f"{pipeline_name}_{stage_name}_{sub_stage_name}"
            )
            sub_stage_b_units_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
            self._create_init_file(
                sub_stage_b_units_dir
            )

            # Add imports for each b_unit
            for (
                b_unit
            ) in sub_stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += SUB_STAGE_B_UNIT_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                    b_unit_lower=b_unit.lower(),
                    b_unit_class=class_name,
                )

                # Create b_unit file
                self._create_b_unit(
                    b_unit,
                    sub_stage_b_units_dir,
                )

        # Add function definition
        content += SUB_STAGE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name,
            stage_name=stage_name,
            sub_stage_name=sub_stage_name,
        )

        # Add b_unit calls
        if sub_stage.b_units:
            for (
                b_unit
            ) in sub_stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += SUB_STAGE_CREATE_AND_RUN_B_UNIT_CALL.format(
                    b_unit_class=class_name,
                )
        else:
            content += SUB_STAGE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_b_unit(
        self,
        b_unit: str,
        directory_path: Path,
    ) -> None:
        """
        Create a b_unit file.

        Args:
            b_unit: Name of the b_unit
            directory_path: Path to the directory for the b_unit
        """
        file_path = (
            directory_path
            / f"{b_unit.lower()}_b_units.py"
        )

        # Skip if the file already exists
        if file_path.exists():
            return

        # Format the class name by removing underscores and capitalizing words
        class_name_parts = b_unit.split(
            "_"
        )
        class_name = "".join(
            part.capitalize()
            for part in class_name_parts
        )

        # Use template to create b_unit file
        content = (
            B_UNIT_TEMPLATE.format(
                class_name=class_name
            )
        )

        with open(file_path, "w") as f:
            f.write(content)


class PipelineGenerator:
    """Generator class for creating pipeline structure from configuration."""

    def __init__(
        self,
        output_base_path: str,
    ):
        """
        Initialize the PipelineGenerator.

        Args:
            output_base_path: Base path where the new pipeline will be created
        """
        self.output_base_path = Path(
            output_base_path
        )

    def generate_pipeline(
        self, config: DomainConfig
    ) -> str:
        """
        Generate pipeline structure from configuration.

        Args:
            config: Domain configuration

        Returns:
            Path to the generated pipeline
        """
        domain_name = config.domain_name
        domain_path = (
            self.output_base_path
            / "bclearer_pipelines"
            / domain_name
        )

        if domain_path.exists():
            raise FileExistsError(
                f"Domain path already exists: {domain_path}"
            )

        # Create domain directory
        domain_path.mkdir(
            parents=True, exist_ok=True
        )

        # Initialize the directory structure
        self._copy_template_structure(
            domain_path
        )

        # Create b_source directory
        b_source_path = (
            domain_path / "b_source"
        )
        b_source_path.mkdir(
            exist_ok=True
        )

        # Create __init__.py in b_source
        self._create_init_file(
            b_source_path
        )

        # Create app_runners directory
        app_runners_path = (
            b_source_path
            / "app_runners"
        )
        app_runners_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            app_runners_path
        )

        # Create aa_b_clearer_pipeline_b_application_runner.py
        self._create_application_runner(
            app_runners_path,
            domain_name,
        )

        # Create app_runners/runners directory
        runners_path = (
            app_runners_path / "runners"
        )
        runners_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            runners_path
        )

        # Create aa_b_clearer_pipelines_runner.py
        self._create_pipelines_runner(
            runners_path,
            domain_name,
            config.pipelines,
        )

        # Create common directory structure
        common_path = (
            b_source_path / "common"
        )
        common_path.mkdir(exist_ok=True)
        self._create_init_file(
            common_path
        )

        common_objects_path = (
            common_path / "objects"
        )
        common_objects_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            common_objects_path
        )

        common_enums_path = (
            common_objects_path
            / "enums"
        )
        common_enums_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            common_enums_path
        )

        common_universes_path = (
            common_objects_path
            / "universes"
        )
        common_universes_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            common_universes_path
        )

        common_operations_path = (
            common_path / "operations"
        )
        common_operations_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            common_operations_path
        )

        b_units_path = (
            common_operations_path
            / "b_units"
        )
        b_units_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            b_units_path
        )

        # Create b_unit_creator_and_runner.py
        self._create_b_unit_creator_and_runner(
            b_units_path
        )

        # Process each pipeline
        for (
            pipeline_config
        ) in config.pipelines:
            self._create_pipeline(
                b_source_path,
                pipeline_config,
                domain_name,
            )

            # Create pipeline runner
            self._create_pipeline_runner(
                runners_path,
                domain_name,
                pipeline_config.name,
            )

        # Create resources directory
        resources_path = (
            domain_path / "resources"
        )
        resources_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            resources_path
        )

        collect_path = (
            resources_path / "collect"
        )
        collect_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            collect_path
        )

        # Create tests directory structure
        tests_path = (
            domain_path / "tests"
        )
        tests_path.mkdir(exist_ok=True)
        self._create_init_file(
            tests_path
        )

        common_tests_path = (
            tests_path / "common"
        )
        common_tests_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            common_tests_path
        )

        fixtures_path = (
            common_tests_path
            / "fixtures"
        )
        fixtures_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            fixtures_path
        )

        inputs_path = (
            common_tests_path / "inputs"
        )
        inputs_path.mkdir(exist_ok=True)
        self._create_init_file(
            inputs_path
        )

        universal_path = (
            tests_path / "universal"
        )
        universal_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            universal_path
        )

        e2e_path = (
            universal_path / "e2e"
        )
        e2e_path.mkdir(exist_ok=True)
        self._create_init_file(e2e_path)

        e2e_fixtures_path = (
            e2e_path / "fixtures"
        )
        e2e_fixtures_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            e2e_fixtures_path
        )

        e2e_outputs_path = (
            e2e_path / "outputs"
        )
        e2e_outputs_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            e2e_outputs_path
        )

        # Create basic test files
        self._create_conftest(e2e_path)
        self._create_e2e_test(
            e2e_path, domain_name
        )

        return str(domain_path)

    def _copy_template_structure(
        self, domain_path: Path
    ) -> None:
        """
        Create basic pipeline structure.

        Args:
            domain_path: Path to the domain directory
        """
        # We create all directories and files from scratch for each pipeline
        # This ensures we don't depend on any external template
        pass

    def _create_init_file(
        self, directory_path: Path
    ) -> None:
        """
        Create an empty __init__.py file in a directory.

        Args:
            directory_path: Path to the directory
        """
        init_file = (
            directory_path
            / "__init__.py"
        )
        init_file.touch()

    def _create_application_runner(
        self,
        app_runners_path: Path,
        domain_name: str,
    ) -> None:
        """
        Create the main application runner file.

        Args:
            app_runners_path: Path to the app_runners directory
            domain_name: Name of the domain
        """
        file_path = (
            app_runners_path
            / f"{domain_name}_b_clearer_pipeline_b_application_runner.py"
        )

        content = APPLICATION_RUNNER_TEMPLATE.format(
            domain_name=domain_name
        )

        with open(file_path, "w") as f:
            f.write(content)

    def _create_pipelines_runner(
        self,
        runners_path: Path,
        domain_name: str,
        pipelines: List[PipelineConfig],
    ) -> None:
        """
        Create the pipelines runner file.

        Args:
            runners_path: Path to the runners directory
            domain_name: Name of the domain
            pipelines: List of pipeline configurations
        """
        file_path = (
            runners_path
            / f"{domain_name}_b_clearer_pipelines_runner.py"
        )

        # Start with the header imports
        content = PIPELINES_RUNNER_TEMPLATE_HEADER

        # Add imports for each pipeline
        for pipeline in pipelines:
            content += PIPELINE_IMPORT_TEMPLATE.format(
                domain_name=domain_name,
                pipeline_name=pipeline.name,
            )

        # Add function definition
        content += PIPELINES_RUNNER_FUNCTION_START.format(
            domain_name=domain_name
        )

        # Add function calls
        if pipelines:
            for pipeline in pipelines:
                content += PIPELINE_RUNNER_CALL.format(
                    pipeline_name=pipeline.name
                )
        else:
            content += PIPELINES_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_pipeline_runner(
        self,
        runners_path: Path,
        domain_name: str,
        pipeline_name: str,
    ) -> None:
        """
        Create a pipeline runner file.

        Args:
            runners_path: Path to the runners directory
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
        """
        file_path = (
            runners_path
            / f"{pipeline_name}_runner.py"
        )

        content = PIPELINE_RUNNER_TEMPLATE.format(
            domain_name=domain_name,
            pipeline_name=pipeline_name,
        )

        with open(file_path, "w") as f:
            f.write(content)

    def _create_pipeline(
        self,
        b_source_path: Path,
        pipeline_config: PipelineConfig,
        domain_name: str,
    ) -> None:
        """
        Create a pipeline directory structure.

        Args:
            b_source_path: Path to the b_source directory
            pipeline_config: Pipeline configuration
            domain_name: Name of the domain
        """
        pipeline_name = (
            pipeline_config.name
        )
        pipeline_path = (
            b_source_path
            / pipeline_name
        )
        pipeline_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            pipeline_path
        )

        # Create pipeline objects directory
        objects_path = (
            pipeline_path / "objects"
        )
        objects_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            objects_path
        )

        enums_path = (
            objects_path / "enums"
        )
        enums_path.mkdir(exist_ok=True)
        self._create_init_file(
            enums_path
        )

        universes_path = (
            objects_path / "universes"
        )
        universes_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            universes_path
        )

        b_units_path = (
            objects_path / "b_units"
        )
        b_units_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            b_units_path
        )

        # Create operations directory
        operations_path = (
            pipeline_path / "operations"
        )
        operations_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            operations_path
        )

        # Create orchestrators directory
        orchestrators_path = (
            pipeline_path
            / "orchestrators"
        )
        orchestrators_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            orchestrators_path
        )

        pipeline_orchestrators_path = (
            orchestrators_path
            / "pipeline"
        )
        pipeline_orchestrators_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            pipeline_orchestrators_path
        )

        # Create thin_slices directory
        thin_slices_path = (
            orchestrators_path
            / "thin_slices"
        )
        thin_slices_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            thin_slices_path
        )

        # Create stages directory
        stages_path = (
            orchestrators_path
            / "stages"
        )
        stages_path.mkdir(exist_ok=True)
        self._create_init_file(
            stages_path
        )

        # Create sub_stages directory
        sub_stages_path = (
            orchestrators_path
            / "sub_stages"
        )
        sub_stages_path.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            sub_stages_path
        )

        # Create pipeline orchestrator
        self._create_pipeline_orchestrator(
            pipeline_orchestrators_path,
            domain_name,
            pipeline_name,
            pipeline_config,
        )

        # Create thin slices
        for (
            thin_slice
        ) in (
            pipeline_config.thin_slices
        ):
            self._create_thin_slice(
                domain_name,
                pipeline_name,
                thin_slice,
                thin_slices_path,
                stages_path,
                sub_stages_path,
                b_units_path,
            )

    def _create_pipeline_orchestrator(
        self,
        pipeline_orchestrators_path: Path,
        domain_name: str,
        pipeline_name: str,
        pipeline_config: PipelineConfig,
    ) -> None:
        """
        Create pipeline orchestrator file.

        Args:
            pipeline_orchestrators_path: Path to the pipeline orchestrators directory
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            pipeline_config: Pipeline configuration
        """
        file_path = (
            pipeline_orchestrators_path
            / f"{pipeline_name}_orchestrator.py"
        )

        content = ""
        # Add imports for each thin slice
        if pipeline_config.thin_slices:
            for (
                thin_slice
            ) in (
                pipeline_config.thin_slices
            ):
                content += PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    thin_slice_name=thin_slice.name,
                )

        # Add function definition
        content += PIPELINE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name
        )

        # Add calls to thin slice orchestrators
        if pipeline_config.thin_slices:
            for (
                thin_slice
            ) in (
                pipeline_config.thin_slices
            ):
                content += ORCHESTRATE_THIN_SLICE_CALL.format(
                    thin_slice_name=thin_slice.name
                )
        else:
            content += PIPELINE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_thin_slice(
        self,
        domain_name: str,
        pipeline_name: str,
        thin_slice: ThinSliceConfig,
        thin_slices_path: Path,
        stages_path: Path,
        sub_stages_path: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create thin slice orchestrator and related files.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            thin_slice: Thin slice configuration
            thin_slices_path: Path to the thin slices directory
            stages_path: Path to the stages directory
            sub_stages_path: Path to the sub-stages directory
            b_units_path: Path to the b_units directory
        """
        slice_name = thin_slice.name
        file_path = (
            thin_slices_path
            / f"{slice_name}_orchestrator.py"
        )

        content = ""
        # Add imports for each stage
        for stage in thin_slice.stages:
            stage_name = stage.name
            content += THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE.format(
                domain_name=domain_name,
                pipeline_name=pipeline_name,
                stage_name=stage_name,
            )

            # Create stage orchestrator
            self._create_stage_orchestrator(
                domain_name,
                pipeline_name,
                stage,
                stages_path,
                sub_stages_path,
                b_units_path,
            )

        # Add function definition
        content += THIN_SLICE_ORCHESTRATOR_FUNCTION_START.format(
            thin_slice_name=slice_name
        )

        # Add calls to stage orchestrators
        if thin_slice.stages:
            for (
                stage
            ) in thin_slice.stages:
                content += ORCHESTRATE_STAGE_CALL.format(
                    pipeline_name=pipeline_name,
                    stage_name=stage.name,
                )
        else:
            content += THIN_SLICE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_stage_orchestrator(
        self,
        domain_name: str,
        pipeline_name: str,
        stage: StageConfig,
        stages_path: Path,
        sub_stages_path: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create stage orchestrator file.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            stage: Stage configuration
            stages_path: Path to the stages directory
            sub_stages_path: Path to the sub-stages directory
            b_units_path: Path to the b_units directory
        """
        stage_name = stage.name
        file_path = (
            stages_path
            / f"{pipeline_name}_{stage_name}_orchestrator.py"
        )

        # Always create stage directory for b_units and __init__.py file
        stage_b_units_dir = (
            b_units_path
            / f"{pipeline_name}_{stage_name}"
        )
        stage_b_units_dir.mkdir(
            exist_ok=True
        )
        self._create_init_file(
            stage_b_units_dir
        )

        # Start with the header imports
        content = (
            STAGE_ORCHESTRATOR_HEADER
        )

        # Add imports for sub-stages if they exist
        if stage.sub_stages:
            for (
                sub_stage
            ) in stage.sub_stages:
                sub_stage_name = (
                    sub_stage.name
                )
                content += SUB_STAGE_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                )

                # Create sub-stage directory and orchestrator
                sub_stage_dir = (
                    sub_stages_path
                    / f"{pipeline_name}_{stage_name}_{sub_stage_name}"
                )
                sub_stage_dir.mkdir(
                    exist_ok=True
                )
                self._create_init_file(
                    sub_stage_dir
                )
                self._create_sub_stage_orchestrator(
                    domain_name,
                    pipeline_name,
                    stage_name,
                    sub_stage,
                    sub_stage_dir,
                    b_units_path,
                )

        # Add b_unit creator import if there are b_units
        if stage.b_units:
            content += STAGE_B_UNIT_CREATOR_IMPORT.format(
                domain_name=domain_name
            )

            for b_unit in stage.b_units:
                # Format the class name by removing underscores and capitalizing words
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += B_UNIT_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    b_unit_lower=b_unit.lower(),
                    b_unit_class=class_name,
                )

                # Create b_unit file
                self._create_b_unit(
                    b_unit,
                    stage_b_units_dir,
                )

        # Add function definition
        content += STAGE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name,
            stage_name=stage_name,
        )

        # Add sub-stage calls
        if stage.sub_stages:
            for (
                sub_stage
            ) in stage.sub_stages:
                sub_stage_name = (
                    sub_stage.name
                )
                content += ORCHESTRATE_SUB_STAGE_CALL.format(
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                )

        # Add b_unit calls
        if stage.b_units:
            if stage.sub_stages:
                content += "\n"

            for b_unit in stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += STAGE_CREATE_AND_RUN_B_UNIT_CALL.format(
                    b_unit_class=class_name,
                )

        # Add empty function body if needed
        if (
            not stage.sub_stages
            and not stage.b_units
        ):
            content += STAGE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_sub_stage_orchestrator(
        self,
        domain_name: str,
        pipeline_name: str,
        stage_name: str,
        sub_stage: SubStageConfig,
        sub_stage_dir: Path,
        b_units_path: Path,
    ) -> None:
        """
        Create sub-stage orchestrator file.

        Args:
            domain_name: Name of the domain
            pipeline_name: Name of the pipeline
            stage_name: Name of the stage
            sub_stage: Sub-stage configuration
            sub_stage_dir: Path to the sub-stage directory
            b_units_path: Path to the b_units directory
        """
        sub_stage_name = sub_stage.name
        file_path = (
            sub_stage_dir
            / f"{pipeline_name}_{stage_name}_{sub_stage_name}_orchestrator.py"
        )

        # Start with the header imports
        content = SUB_STAGE_ORCHESTRATOR_HEADER

        # Add b_unit creator import if there are b_units
        if sub_stage.b_units:
            content += SUB_STAGE_B_UNIT_CREATOR_IMPORT.format(
                domain_name=domain_name
            )

            # Create sub-stage directory for b_units if doesn't exist
            sub_stage_b_units_dir = (
                b_units_path
                / f"{pipeline_name}_{stage_name}"
                / f"{pipeline_name}_{stage_name}_{sub_stage_name}"
            )
            sub_stage_b_units_dir.mkdir(
                parents=True,
                exist_ok=True,
            )
            self._create_init_file(
                sub_stage_b_units_dir
            )

            # Add imports for each b_unit
            for (
                b_unit
            ) in sub_stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += SUB_STAGE_B_UNIT_IMPORT_TEMPLATE.format(
                    domain_name=domain_name,
                    pipeline_name=pipeline_name,
                    stage_name=stage_name,
                    sub_stage_name=sub_stage_name,
                    b_unit_lower=b_unit.lower(),
                    b_unit_class=class_name,
                )

                # Create b_unit file
                self._create_b_unit(
                    b_unit,
                    sub_stage_b_units_dir,
                )

        # Add function definition
        content += SUB_STAGE_ORCHESTRATOR_FUNCTION_START.format(
            pipeline_name=pipeline_name,
            stage_name=stage_name,
            sub_stage_name=sub_stage_name,
        )

        # Add b_unit calls
        if sub_stage.b_units:
            for (
                b_unit
            ) in sub_stage.b_units:
                # Format the class name
                class_name_parts = (
                    b_unit.split("_")
                )
                class_name = "".join(
                    part.capitalize()
                    for part in class_name_parts
                )

                content += SUB_STAGE_CREATE_AND_RUN_B_UNIT_CALL.format(
                    b_unit_class=class_name,
                )
        else:
            content += SUB_STAGE_EMPTY_FUNCTION_BODY

        with open(file_path, "w") as f:
            f.write(content)

    def _create_b_unit(
        self,
        b_unit: str,
        directory_path: Path,
    ) -> None:
        """
        Create a b_unit file.

        Args:
            b_unit: Name of the b_unit
            directory_path: Path to the directory for the b_unit
        """
        file_path = (
            directory_path
            / f"{b_unit.lower()}_b_units.py"
        )

        # Skip if the file already exists
        if file_path.exists():
            return

        # Format the class name by removing underscores and capitalizing words
        class_name_parts = b_unit.split(
            "_"
        )
        class_name = "".join(
            part.capitalize()
            for part in class_name_parts
        )

        # Use template to create b_unit file
        content = (
            B_UNIT_TEMPLATE.format(
                class_name=class_name
            )
        )

        with open(file_path, "w") as f:
            f.write(content)

    def _create_b_unit_creator_and_runner(
        self, b_units_path: Path
    ) -> None:
        """
        Create b_unit_creator_and_runner.py file.

        Args:
            b_units_path: Path to the b_units directory
        """
        file_path = (
            b_units_path
            / "b_unit_creator_and_runner.py"
        )

        with open(file_path, "w") as f:
            f.write(
                B_UNIT_CREATOR_AND_RUNNER_TEMPLATE
            )

    def _create_conftest(
        self, e2e_path: Path
    ) -> None:
        """
        Create a basic conftest.py file for tests.

        Args:
            e2e_path: Path to the e2e directory
        """
        file_path = (
            e2e_path / "conftest.py"
        )

        with open(file_path, "w") as f:
            f.write(CONFTEST_TEMPLATE)

    def _create_e2e_test(
        self,
        e2e_path: Path,
        domain_name: str,
    ) -> None:
        """
        Create a basic e2e test file.

        Args:
            e2e_path: Path to the e2e directory
            domain_name: Name of the domain
        """
        file_path = (
            e2e_path
            / f"test_{domain_name}_b_clearer_pipeline_b_application_runner.py"
        )

        content = (
            E2E_TEST_TEMPLATE.format(
                domain_name=domain_name
            )
        )

        with open(file_path, "w") as f:
            f.write(content)


def generate_pipeline(
    config: Dict,
    output_base_path: str,
) -> str:
    """
    Generate a pipeline from configuration.

    Args:
        config: Pipeline configuration dictionary
        output_base_path: Base path where the new pipeline will be created

    Returns:
        Path to the generated pipeline
    """
    from bclearer_core.pipeline_builder.schema import (
        validate_pipeline_config,
    )

    config_obj = (
        validate_pipeline_config(config)
    )
    generator = PipelineGenerator(
        output_base_path
    )

    return generator.generate_pipeline(
        config_obj
    )


def update_pipeline(
    config: Dict, pipeline_path: str
) -> str:
    """
    Update an existing pipeline with new configuration.

    Args:
        config: Pipeline configuration dictionary
        pipeline_path: Path to the existing pipeline

    Returns:
        Path to the updated pipeline
    """
    from bclearer_core.pipeline_builder.schema import (
        validate_pipeline_config,
    )

    config_obj = (
        validate_pipeline_config(config)
    )
    updater = PipelineUpdater(
        pipeline_path
    )
    return updater.update_pipeline(
        config_obj
    )
