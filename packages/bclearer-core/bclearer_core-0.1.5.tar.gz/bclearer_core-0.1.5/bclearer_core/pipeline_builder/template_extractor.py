"""Utility to extract templates from the pipeline template directory."""

import os
import re
from pathlib import Path


class TemplateExtractor:
    """Extracts templates from the pipeline template directory and updates the constants."""

    def __init__(
        self, template_path: str
    ):
        """
        Initialize the TemplateExtractor.

        Args:
            template_path: Path to the template pipeline directory
        """
        self.template_path = Path(
            template_path
        )

        if (
            not self.template_path.exists()
        ):
            raise FileNotFoundError(
                f"Template path not found: {template_path}"
            )

        if (
            not self.template_path.is_dir()
        ):
            raise NotADirectoryError(
                f"Template path is not a directory: {template_path}"
            )

    def extract_templates(
        self, output_directory: str
    ) -> None:
        """
        Extract templates from the template pipeline and save them to output directory.

        Args:
            output_directory: Path to save the extracted templates
        """
        output_path = Path(
            output_directory
        )
        output_path.mkdir(
            parents=True, exist_ok=True
        )

        # Extract application runner
        self._extract_application_runner(
            output_path
        )

        # Extract pipelines runner
        self._extract_pipelines_runner(
            output_path
        )

        # Extract pipeline runner
        self._extract_pipeline_runner(
            output_path
        )

        # Extract pipeline orchestrator
        self._extract_pipeline_orchestrator(
            output_path
        )

        # Extract thin slice orchestrator
        self._extract_thin_slice_orchestrator(
            output_path
        )

        # Extract stage orchestrator
        self._extract_stage_orchestrator(
            output_path
        )

        # Extract sub-stage orchestrator
        self._extract_sub_stage_orchestrator(
            output_path
        )

        # Extract b_unit
        self._extract_b_unit(
            output_path
        )

        # Extract b_unit_creator_and_runner
        self._extract_b_unit_creator_and_runner(
            output_path
        )

        # Extract conftest
        self._extract_conftest(
            output_path
        )

        # Extract e2e test
        self._extract_e2e_test(
            output_path
        )

        # Create __init__.py
        self._create_init(output_path)

    def _extract_application_runner(
        self, output_path: Path
    ) -> None:
        """
        Extract application runner template.

        Args:
            output_path: Path to save the template
        """
        template_file = (
            self.template_path
            / "b_source"
            / "app_runners"
            / "aa_b_clearer_pipeline_b_application_runner.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Application runner template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Replace domain-specific names with placeholders
        content = content.replace(
            "aa", "{domain_name}"
        )

        # Save to output file
        output_file = (
            output_path
            / "application_runner.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for application runner."""\n\n'
            )
            f.write(
                f'APPLICATION_RUNNER_TEMPLATE = """{content}"""'
            )

    def _extract_pipelines_runner(
        self, output_path: Path
    ) -> None:
        """
        Extract pipelines runner template.

        Args:
            output_path: Path to save the template
        """
        template_file = (
            self.template_path
            / "b_source"
            / "app_runners"
            / "runners"
            / "aa_b_clearer_pipelines_runner.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Pipelines runner template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Extract header (imports)
        header_match = re.search(
            r"^.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if header_match:
            header = header_match.group(
                0
            )
        else:
            header = ""

        # Extract pipeline import pattern
        import_match = re.search(
            r"^from.*?xx_runner.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if import_match:
            pipeline_import = (
                import_match.group(0)
            )
            pipeline_import = (
                pipeline_import.replace(
                    "aa",
                    "{domain_name}",
                )
            )
            pipeline_import = (
                pipeline_import.replace(
                    "xx",
                    "{pipeline_name}",
                )
            )
        else:
            pipeline_import = ""

        # Extract function start
        function_start_match = re.search(
            r"@run_and_log_function\(\).*?def run_aa_b_clearer_pipelines.*?:.*?\n",
            content,
            re.DOTALL,
        )
        if function_start_match:
            function_start = function_start_match.group(
                0
            )
            function_start = (
                function_start.replace(
                    "aa",
                    "{domain_name}",
                )
            )
        else:
            function_start = ""

        # Extract pipeline call
        pipeline_call_match = re.search(
            r"^\s+run_xx\(\)",
            content,
            re.MULTILINE,
        )
        if pipeline_call_match:
            pipeline_call = pipeline_call_match.group(
                0
            )
            pipeline_call = (
                pipeline_call.replace(
                    "xx",
                    "{pipeline_name}",
                )
            )
        else:
            pipeline_call = "    run_{pipeline_name}()"

        # Extract empty function body if it exists
        empty_body_match = re.search(
            r"^\s+pass$",
            content,
            re.MULTILINE,
        )
        if empty_body_match:
            empty_body = (
                empty_body_match.group(
                    0
                )
            )
        else:
            empty_body = "    pass"

        # Save to output file
        output_file = (
            output_path
            / "pipelines_runner.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for pipelines runner."""\n\n'
            )
            f.write(
                f'PIPELINES_RUNNER_TEMPLATE_HEADER = """{header}"""\n\n'
            )
            f.write(
                f'PIPELINE_IMPORT_TEMPLATE = """{pipeline_import}"""\n\n'
            )
            f.write(
                f'PIPELINES_RUNNER_FUNCTION_START = """{function_start}"""\n\n'
            )
            f.write(
                f'PIPELINE_RUNNER_CALL = """{pipeline_call}\n"""\n\n'
            )
            f.write(
                f'EMPTY_FUNCTION_BODY = """{empty_body}\n"""'
            )

    # Add the remaining extraction methods here following the same pattern
    def _extract_pipeline_runner(
        self, output_path: Path
    ) -> None:
        """Extract pipeline runner template."""
        template_file = (
            self.template_path
            / "b_source"
            / "app_runners"
            / "runners"
            / "xx_runner.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Pipeline runner template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Replace domain-specific names with placeholders
        content = content.replace(
            "aa", "{domain_name}"
        )
        content = content.replace(
            "xx", "{pipeline_name}"
        )

        # Save to output file
        output_file = (
            output_path
            / "pipeline_runner.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for pipeline runner."""\n\n'
            )
            f.write(
                f'PIPELINE_RUNNER_TEMPLATE = """{content}"""'
            )

    def _extract_pipeline_orchestrator(
        self, output_path: Path
    ) -> None:
        """Extract pipeline orchestrator template."""
        template_file = (
            self.template_path
            / "b_source"
            / "xx_pipeline"
            / "orchestrators"
            / "pipeline"
            / "xx_pipeline_orchestrator.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Pipeline orchestrator template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Extract import pattern
        import_match = re.search(
            r"^from.*?thin_slices.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if import_match:
            import_pattern = (
                import_match.group(0)
            )
            import_pattern = (
                import_pattern.replace(
                    "aa",
                    "{domain_name}",
                )
            )
            import_pattern = (
                import_pattern.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            import_pattern = (
                import_pattern.replace(
                    "thin_slice_1",
                    "{thin_slice_name}",
                )
            )
        else:
            import_pattern = ""

        # Extract function start
        function_start_match = re.search(
            r"def orchestrate_xx_pipeline.*?__run_contained_bie_pipeline_components.*?def __run_contained_bie_pipeline_components.*?:.*?\n",
            content,
            re.DOTALL,
        )
        if function_start_match:
            function_start = function_start_match.group(
                0
            )
            function_start = (
                function_start.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
        else:
            function_start = ""

        # Extract thin slice call
        thin_slice_call_match = re.search(
            r"^\s+orchestrate_thin_slice_1\(\)",
            content,
            re.MULTILINE,
        )
        if thin_slice_call_match:
            thin_slice_call = thin_slice_call_match.group(
                0
            )
            thin_slice_call = (
                thin_slice_call.replace(
                    "thin_slice_1",
                    "{thin_slice_name}",
                )
            )
        else:
            thin_slice_call = "    orchestrate_{thin_slice_name}()"

        # Extract empty function body if it exists
        empty_body_match = re.search(
            r"^\s+pass$",
            content,
            re.MULTILINE,
        )
        if empty_body_match:
            empty_body = (
                empty_body_match.group(
                    0
                )
            )
        else:
            empty_body = "    pass"

        # Save to output file
        output_file = (
            output_path
            / "pipeline_orchestrator.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for pipeline orchestrator."""\n\n'
            )
            f.write(
                f'PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE = """{import_pattern}"""\n\n'
            )
            f.write(
                f'PIPELINE_ORCHESTRATOR_FUNCTION_START = """{function_start}"""\n\n'
            )
            f.write(
                f'ORCHESTRATE_THIN_SLICE_CALL = """{thin_slice_call}\n"""\n\n'
            )
            f.write(
                f'EMPTY_FUNCTION_BODY = """{empty_body}\n"""'
            )

    def _extract_thin_slice_orchestrator(
        self, output_path: Path
    ) -> None:
        """Extract thin slice orchestrator template."""
        template_file = (
            self.template_path
            / "b_source"
            / "xx_pipeline"
            / "orchestrators"
            / "thin_slices"
            / "thin_slice_1_orchestrator.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Thin slice orchestrator template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Extract import pattern
        import_match = re.search(
            r"^from.*?stages.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if import_match:
            import_pattern = (
                import_match.group(0)
            )
            import_pattern = (
                import_pattern.replace(
                    "aa",
                    "{domain_name}",
                )
            )
            import_pattern = (
                import_pattern.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            if (
                "2l_load"
                in import_pattern
            ):
                import_pattern = import_pattern.replace(
                    "2l_load",
                    "{stage_name}",
                )
            else:
                import_pattern = import_pattern.replace(
                    "1c_collect",
                    "{stage_name}",
                )
        else:
            import_pattern = ""

        # Extract function start
        function_start_match = re.search(
            r"def orchestrate_thin_slice_1.*?__run_contained_bie_pipeline_components.*?def __run_contained_bie_pipeline_components.*?:.*?\n",
            content,
            re.DOTALL,
        )
        if function_start_match:
            function_start = function_start_match.group(
                0
            )
            function_start = (
                function_start.replace(
                    "thin_slice_1",
                    "{thin_slice_name}",
                )
            )
        else:
            function_start = ""

        # Extract stage call
        stage_call_match = re.search(
            r"^\s+orchestrate_xx_pipeline_[12][lc]_\w+\(\)",
            content,
            re.MULTILINE,
        )
        if stage_call_match:
            stage_call = (
                stage_call_match.group(
                    0
                )
            )
            stage_call = (
                stage_call.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            stage_call = re.sub(
                r"_[12][lc]_\w+",
                "_{stage_name}",
                stage_call,
            )
        else:
            stage_call = "    orchestrate_{pipeline_name}_{stage_name}()"

        # Extract empty function body if it exists
        empty_body_match = re.search(
            r"^\s+pass$",
            content,
            re.MULTILINE,
        )
        if empty_body_match:
            empty_body = (
                empty_body_match.group(
                    0
                )
            )
        else:
            empty_body = "    pass"

        # Save to output file
        output_file = (
            output_path
            / "thin_slice_orchestrator.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for thin slice orchestrator."""\n\n'
            )
            f.write(
                f'THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE = """{import_pattern}"""\n\n'
            )
            f.write(
                f'THIN_SLICE_ORCHESTRATOR_FUNCTION_START = """{function_start}"""\n\n'
            )
            f.write(
                f'ORCHESTRATE_STAGE_CALL = """{stage_call}\n"""\n\n'
            )
            f.write(
                f'EMPTY_FUNCTION_BODY = """{empty_body}\n"""'
            )

    def _extract_stage_orchestrator(
        self, output_path: Path
    ) -> None:
        """Extract stage orchestrator template."""
        template_file = (
            self.template_path
            / "b_source"
            / "xx_pipeline"
            / "orchestrators"
            / "stages"
            / "xx_pipeline_2l_load_orchestrator.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Stage orchestrator template file not found: {template_file}"
            )
            # Try alternative
            template_file = (
                self.template_path
                / "b_source"
                / "xx_pipeline"
                / "orchestrators"
                / "stages"
                / "xx_pipeline_3e_evolve_orchestrator.py"
            )
            if (
                not template_file.exists()
            ):
                print(
                    f"Warning: Alternative stage orchestrator template file not found: {template_file}"
                )
                return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Extract header
        header_match = re.search(
            r"^from.*?run_and_log_function.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if header_match:
            header = header_match.group(
                0
            )
        else:
            header = ""

        # Extract sub_stage import if exists
        sub_stage_import_match = re.search(
            r"^from.*?sub_stages.*?orchestrator import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if sub_stage_import_match:
            sub_stage_import = sub_stage_import_match.group(
                0
            )
            sub_stage_import = sub_stage_import.replace(
                "aa", "{domain_name}"
            )
            sub_stage_import = sub_stage_import.replace(
                "xx_pipeline",
                "{pipeline_name}",
            )
            sub_stage_import = re.sub(
                r"_[123][elc]_\w+",
                "_{stage_name}",
                sub_stage_import,
            )
            sub_stage_import = re.sub(
                r"_[a-z0-9_]+_sub_stage",
                "_{sub_stage_name}",
                sub_stage_import,
            )
        else:
            sub_stage_import = ""

        # Extract b_unit creator import if exists
        b_unit_creator_import_match = re.search(
            r"^from.*?b_units\.b_unit_creator_and_runner import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if b_unit_creator_import_match:
            b_unit_creator_import = b_unit_creator_import_match.group(
                0
            )
            b_unit_creator_import = b_unit_creator_import.replace(
                "aa", "{domain_name}"
            )
        else:
            b_unit_creator_import = ""

        # Extract b_unit import if exists
        b_unit_import_match = re.search(
            r"^from.*?b_units import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if (
            b_unit_import_match
            and "objects.b_units"
            in b_unit_import_match.group(
                0
            )
        ):
            b_unit_import = b_unit_import_match.group(
                0
            )
            b_unit_import = (
                b_unit_import.replace(
                    "aa",
                    "{domain_name}",
                )
            )
            b_unit_import = (
                b_unit_import.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            b_unit_import = re.sub(
                r"_[123][elc]_\w+",
                "_{stage_name}",
                b_unit_import,
            )
            # Extract pattern for b_unit import
            unit_match = re.search(
                r"\/([a-z0-9_]+)_b_units.py",
                b_unit_import,
            )
            if unit_match:
                unit_name = (
                    unit_match.group(1)
                )
                b_unit_import = b_unit_import.replace(
                    f"{unit_name}_b_units",
                    "{b_unit_lower}_b_units",
                )

            # Handle class name
            class_match = re.search(
                r"([A-Za-z0-9]+)BUnits",
                b_unit_import,
            )
            if class_match:
                class_name = (
                    class_match.group(1)
                )
                b_unit_import = b_unit_import.replace(
                    f"{class_name}BUnits",
                    "{b_unit_class}BUnits",
                )
        else:
            b_unit_import = ""

        # Extract function start
        function_start_match = re.search(
            r"@run_and_log_function\(\).*?def orchestrate_xx_pipeline_[123][elc]_\w+.*?__run_contained_bie_pipeline_components.*?def __run_contained_bie_pipeline_components.*?:.*?\n",
            content,
            re.DOTALL,
        )
        if function_start_match:
            function_start = function_start_match.group(
                0
            )
            function_start = (
                function_start.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            function_start = re.sub(
                r"_[123][elc]_\w+\(\)",
                "_{stage_name}()",
                function_start,
            )
        else:
            function_start = ""

        # Extract sub stage call if exists
        sub_stage_call_match = re.search(
            r"^\s+orchestrate_xx_pipeline_[123][elc]_[a-z0-9_]+_[a-z0-9_]+\(\)",
            content,
            re.MULTILINE,
        )
        if sub_stage_call_match:
            sub_stage_call = sub_stage_call_match.group(
                0
            )
            sub_stage_call = (
                sub_stage_call.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            sub_stage_call = re.sub(
                r"_[123][elc]_\w+_",
                "_{stage_name}_",
                sub_stage_call,
            )
            sub_stage_call = re.sub(
                r"_[a-z0-9_]+\(\)",
                "_{sub_stage_name}()",
                sub_stage_call,
            )
        else:
            sub_stage_call = "    orchestrate_{pipeline_name}_{stage_name}_{sub_stage_name}()"

        # Extract create_and_run_b_unit call if exists
        create_run_match = re.search(
            r"^\s+create_and_run_b_unit\(.*?b_unit_type=[A-Za-z0-9]+BUnits.*?\)",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if create_run_match:
            create_run = (
                create_run_match.group(
                    0
                )
            )
            class_match = re.search(
                r"b_unit_type=([A-Za-z0-9]+)BUnits",
                create_run,
            )
            if class_match:
                class_name = (
                    class_match.group(1)
                )
                create_run = create_run.replace(
                    f"{class_name}BUnits",
                    "{b_unit_class}BUnits",
                )
        else:
            create_run = """    create_and_run_b_unit(
        b_unit_type={b_unit_class}BUnits
    )"""

        # Extract empty function body if it exists
        empty_body_match = re.search(
            r"^\s+pass$",
            content,
            re.MULTILINE,
        )
        if empty_body_match:
            empty_body = (
                empty_body_match.group(
                    0
                )
            )
        else:
            empty_body = "    pass"

        # Save to output file
        output_file = (
            output_path
            / "stage_orchestrator.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for stage orchestrator."""\n\n'
            )
            f.write(
                f'STAGE_ORCHESTRATOR_HEADER = """{header}"""\n\n'
            )
            f.write(
                f'SUB_STAGE_IMPORT_TEMPLATE = """{sub_stage_import}"""\n\n'
            )
            f.write(
                f'B_UNIT_CREATOR_IMPORT = """{b_unit_creator_import}"""\n\n'
            )
            f.write(
                f'B_UNIT_IMPORT_TEMPLATE = """{b_unit_import}"""\n\n'
            )
            f.write(
                f'STAGE_ORCHESTRATOR_FUNCTION_START = """{function_start}"""\n\n'
            )
            f.write(
                f'ORCHESTRATE_SUB_STAGE_CALL = """{sub_stage_call}\n"""\n\n'
            )
            f.write(
                f'CREATE_AND_RUN_B_UNIT_CALL = """{create_run}\n"""\n\n'
            )
            f.write(
                f'EMPTY_FUNCTION_BODY = """{empty_body}\n"""'
            )

    def _extract_sub_stage_orchestrator(
        self, output_path: Path
    ) -> None:
        """Extract sub-stage orchestrator template."""
        template_file = (
            self.template_path
            / "b_source"
            / "xx_pipeline"
            / "orchestrators"
            / "sub_stages"
            / "xx_pipeline_3e_evolve_1_sub_stage_name"
            / "xx_pipeline_3e_evolve_1_sub_stage_name_orchestrator.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Sub-stage orchestrator template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Extract header
        header_match = re.search(
            r"^from.*?run_and_log_function.*?import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if header_match:
            header = header_match.group(
                0
            )
        else:
            header = ""

        # Extract b_unit creator import if exists
        b_unit_creator_import_match = re.search(
            r"^from.*?b_units\.b_unit_creator_and_runner import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if b_unit_creator_import_match:
            b_unit_creator_import = b_unit_creator_import_match.group(
                0
            )
            b_unit_creator_import = b_unit_creator_import.replace(
                "aa", "{domain_name}"
            )
        else:
            b_unit_creator_import = ""

        # Extract b_unit import if exists
        b_unit_import_match = re.search(
            r"^from.*?b_units import \(.*?\)$",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if (
            b_unit_import_match
            and "objects.b_units"
            in b_unit_import_match.group(
                0
            )
        ):
            b_unit_import = b_unit_import_match.group(
                0
            )
            b_unit_import = (
                b_unit_import.replace(
                    "aa",
                    "{domain_name}",
                )
            )
            b_unit_import = (
                b_unit_import.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            b_unit_import = re.sub(
                r"_[123][elc]_\w+",
                "_{stage_name}",
                b_unit_import,
            )
            b_unit_import = re.sub(
                r"_[0-9]_[a-z0-9_]+",
                "_{sub_stage_name}",
                b_unit_import,
            )

            # Extract pattern for b_unit import
            unit_match = re.search(
                r"\/([a-z0-9_]+)_b_units.py",
                b_unit_import,
            )
            if unit_match:
                unit_name = (
                    unit_match.group(1)
                )
                b_unit_import = b_unit_import.replace(
                    f"{unit_name}_b_units",
                    "{b_unit_lower}_b_units",
                )

            # Handle class name
            class_match = re.search(
                r"([A-Za-z0-9]+)BUnits",
                b_unit_import,
            )
            if class_match:
                class_name = (
                    class_match.group(1)
                )
                b_unit_import = b_unit_import.replace(
                    f"{class_name}BUnits",
                    "{b_unit_class}BUnits",
                )
        else:
            b_unit_import = ""

        # Extract function start
        function_start_match = re.search(
            r"@run_and_log_function\(\).*?def orchestrate_xx_pipeline_3e_evolve_1_sub_stage_name.*?__run_contained_bie_pipeline_components.*?def __run_contained_bie_pipeline_components.*?:.*?\n",
            content,
            re.DOTALL,
        )
        if function_start_match:
            function_start = function_start_match.group(
                0
            )
            function_start = (
                function_start.replace(
                    "xx_pipeline",
                    "{pipeline_name}",
                )
            )
            function_start = re.sub(
                r"_[123][elc]_\w+_",
                "_{stage_name}_",
                function_start,
            )
            function_start = re.sub(
                r"_[0-9]_[a-z0-9_]+\(",
                "_{sub_stage_name}(",
                function_start,
            )
        else:
            function_start = ""

        # Extract create_and_run_b_unit call if exists
        create_run_match = re.search(
            r"^\s+create_and_run_b_unit\(.*?b_unit_type=[A-Za-z0-9]+BUnits.*?\)",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if create_run_match:
            create_run = (
                create_run_match.group(
                    0
                )
            )
            class_match = re.search(
                r"b_unit_type=([A-Za-z0-9]+)BUnits",
                create_run,
            )
            if class_match:
                class_name = (
                    class_match.group(1)
                )
                create_run = create_run.replace(
                    f"{class_name}BUnits",
                    "{b_unit_class}BUnits",
                )
        else:
            create_run = """    create_and_run_b_unit(
        b_unit_type={b_unit_class}BUnits
    )"""

        # Extract empty function body if it exists
        empty_body_match = re.search(
            r"^\s+pass$",
            content,
            re.MULTILINE,
        )
        if empty_body_match:
            empty_body = (
                empty_body_match.group(
                    0
                )
            )
        else:
            empty_body = "    pass"

        # Save to output file
        output_file = (
            output_path
            / "sub_stage_orchestrator.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for sub-stage orchestrator."""\n\n'
            )
            f.write(
                f'SUB_STAGE_ORCHESTRATOR_HEADER = """{header}"""\n\n'
            )
            f.write(
                f'B_UNIT_CREATOR_IMPORT = """{b_unit_creator_import}"""\n\n'
            )
            f.write(
                f'SUB_STAGE_B_UNIT_IMPORT_TEMPLATE = """{b_unit_import}"""\n\n'
            )
            f.write(
                f'SUB_STAGE_ORCHESTRATOR_FUNCTION_START = """{function_start}"""\n\n'
            )
            f.write(
                f'CREATE_AND_RUN_B_UNIT_CALL = """{create_run}\n"""\n\n'
            )
            f.write(
                f'EMPTY_FUNCTION_BODY = """{empty_body}\n"""'
            )

    def _extract_b_unit(
        self, output_path: Path
    ) -> None:
        """Extract b_unit template."""
        template_file = (
            self.template_path
            / "b_source"
            / "xx_pipeline"
            / "objects"
            / "b_units"
            / "xx_pipeline_1c_collect"
            / "ca_b_unit_b_units.py"
        )

        if not template_file.exists():
            print(
                f"Warning: B-unit template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Replace class name with placeholder
        class_match = re.search(
            r"class ([A-Za-z0-9]+)BUnits:",
            content,
        )
        if class_match:
            class_name = (
                class_match.group(1)
            )
            content = content.replace(
                f"class {class_name}BUnits:",
                "class {class_name}BUnits:",
            )

        # Save to output file
        output_file = (
            output_path / "b_unit.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for b_unit class."""\n\n'
            )
            f.write(
                f'B_UNIT_TEMPLATE = """{content}"""'
            )

    def _extract_b_unit_creator_and_runner(
        self, output_path: Path
    ) -> None:
        """Extract b_unit_creator_and_runner template."""
        template_file = (
            self.template_path
            / "b_source"
            / "common"
            / "operations"
            / "b_units"
            / "b_unit_creator_and_runner.py"
        )

        if not template_file.exists():
            print(
                f"Warning: B-unit creator and runner template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Save to output file
        output_file = (
            output_path
            / "b_unit_creator_and_runner.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for b_unit creator and runner."""\n\n'
            )
            f.write(
                f'B_UNIT_CREATOR_AND_RUNNER_TEMPLATE = """{content}"""'
            )

    def _extract_conftest(
        self, output_path: Path
    ) -> None:
        """Extract conftest template."""
        template_file = (
            self.template_path
            / "tests"
            / "universal"
            / "e2e"
            / "conftest.py"
        )

        if not template_file.exists():
            print(
                f"Warning: Conftest template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Save to output file
        output_file = (
            output_path / "conftest.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for conftest.py."""\n\n'
            )
            f.write(
                f'CONFTEST_TEMPLATE = """{content}"""'
            )

    def _extract_e2e_test(
        self, output_path: Path
    ) -> None:
        """Extract e2e test template."""
        template_file = (
            self.template_path
            / "tests"
            / "universal"
            / "e2e"
            / "test_aa_b_clearer_pipeline_b_application_runner.py"
        )

        if not template_file.exists():
            print(
                f"Warning: E2E test template file not found: {template_file}"
            )
            return

        with open(
            template_file, "r"
        ) as f:
            content = f.read()

        # Replace domain-specific names with placeholders
        content = content.replace(
            "aa", "{domain_name}"
        )

        # Save to output file
        output_file = (
            output_path / "e2e_test.py"
        )
        with open(
            output_file, "w"
        ) as f:
            f.write(
                f'"""Template for e2e test."""\n\n'
            )
            f.write(
                f'E2E_TEST_TEMPLATE = """{content}"""'
            )

    def _create_init(
        self, output_path: Path
    ) -> None:
        """Create __init__.py with imports for all templates."""
        output_file = (
            output_path / "__init__.py"
        )

        content = """\"\"\"Template constants for pipeline builder.\"\"\"\n
# Import all template modules to make them accessible from the templates package
from .application_runner import APPLICATION_RUNNER_TEMPLATE
from .b_unit import B_UNIT_TEMPLATE
from .b_unit_creator_and_runner import B_UNIT_CREATOR_AND_RUNNER_TEMPLATE
from .conftest import CONFTEST_TEMPLATE
from .e2e_test import E2E_TEST_TEMPLATE
from .pipeline_orchestrator import (
    EMPTY_FUNCTION_BODY as PIPELINE_EMPTY_FUNCTION_BODY,
    ORCHESTRATE_THIN_SLICE_CALL,
    PIPELINE_ORCHESTRATOR_FUNCTION_START,
    PIPELINE_ORCHESTRATOR_IMPORT_TEMPLATE,
)
from .pipeline_runner import PIPELINE_RUNNER_TEMPLATE
from .pipelines_runner import (
    EMPTY_FUNCTION_BODY as PIPELINES_EMPTY_FUNCTION_BODY,
    PIPELINE_IMPORT_TEMPLATE,
    PIPELINE_RUNNER_CALL,
    PIPELINES_RUNNER_FUNCTION_START,
    PIPELINES_RUNNER_TEMPLATE_HEADER,
)
from .stage_orchestrator import (
    B_UNIT_CREATOR_IMPORT as STAGE_B_UNIT_CREATOR_IMPORT,
    B_UNIT_IMPORT_TEMPLATE,
    CREATE_AND_RUN_B_UNIT_CALL as STAGE_CREATE_AND_RUN_B_UNIT_CALL,
    EMPTY_FUNCTION_BODY as STAGE_EMPTY_FUNCTION_BODY,
    ORCHESTRATE_SUB_STAGE_CALL,
    STAGE_ORCHESTRATOR_FUNCTION_START,
    STAGE_ORCHESTRATOR_HEADER,
    SUB_STAGE_IMPORT_TEMPLATE,
)
from .sub_stage_orchestrator import (
    B_UNIT_CREATOR_IMPORT as SUB_STAGE_B_UNIT_CREATOR_IMPORT,
    CREATE_AND_RUN_B_UNIT_CALL as SUB_STAGE_CREATE_AND_RUN_B_UNIT_CALL,
    EMPTY_FUNCTION_BODY as SUB_STAGE_EMPTY_FUNCTION_BODY,
    SUB_STAGE_B_UNIT_IMPORT_TEMPLATE,
    SUB_STAGE_ORCHESTRATOR_FUNCTION_START,
    SUB_STAGE_ORCHESTRATOR_HEADER,
)
from .thin_slice_orchestrator import (
    EMPTY_FUNCTION_BODY as THIN_SLICE_EMPTY_FUNCTION_BODY,
    ORCHESTRATE_STAGE_CALL,
    THIN_SLICE_ORCHESTRATOR_FUNCTION_START,
    THIN_SLICE_ORCHESTRATOR_IMPORT_TEMPLATE,
)"""

        with open(
            output_file, "w"
        ) as f:
            f.write(content)


def update_templates_from_pipeline(
    template_path: str,
    output_directory: str,
) -> None:
    """
    Update template constants from a pipeline template.

    Args:
        template_path: Path to the template pipeline
        output_directory: Path to save the extracted templates
    """
    extractor = TemplateExtractor(
        template_path
    )
    extractor.extract_templates(
        output_directory
    )
