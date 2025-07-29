"""Command-line interface for the bclearer pipeline builder.

This CLI tool helps create and update bclearer pipeline structures based on configuration.
The pipeline structure is generated entirely from scratch - no external template is needed.

Usage examples:
  # Generate a sample configuration file
  pipeline_builder sample --output my_config.json

  # Create a new pipeline from configuration file
  pipeline_builder create --config my_config.json

  # Create a pipeline interactively
  pipeline_builder create --interactive

  # Create a pipeline in a specific output directory
  pipeline_builder create --config my_config.json --output /path/to/output/directory

  # Update an existing pipeline with new components
  pipeline_builder update --config updated_config.json --pipeline path/to/domain_name_pipelines

  # Show detailed help
  pipeline_builder help
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

from bclearer_core.pipeline_builder.generator import (
    generate_pipeline,
    update_pipeline,
)
from bclearer_core.pipeline_builder.schema import (
    get_sample_config,
)
from bclearer_core.pipeline_builder.template_extractor import (
    update_templates_from_pipeline,
)


def create_parser() -> (
    argparse.ArgumentParser
):
    """
    Create argument parser for the CLI.

    Returns:
        ArgumentParser object
    """
    parser = argparse.ArgumentParser(
        description="BClearer Pipeline Builder CLI"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Command to execute",
    )

    # help command
    help_parser = subparsers.add_parser(
        "help",
        help="Show detailed help and configuration guide",
    )

    # update-templates command
    update_templates_parser = subparsers.add_parser(
        "update-templates",
        help="Update template constants from a pipeline template",
    )
    update_templates_parser.add_argument(
        "--template-path",
        "-t",
        required=True,
        help="Path to the template pipeline directory",
    )
    update_templates_parser.add_argument(
        "--output",
        "-o",
        required=False,
        default=None,
        help="Output directory for templates (default: bclearer_core/pipeline_builder/templates)",
    )

    # create command
    create_parser = subparsers.add_parser(
        "create",
        help="Create a new pipeline",
    )
    create_parser.add_argument(
        "--config",
        "-c",
        required=False,
        help="Path to the pipeline configuration JSON file",
    )
    # Template parameter removed - structure is generated from scratch
    create_parser.add_argument(
        "--output",
        "-o",
        required=False,
        default=os.getcwd(),
        help="Base path where the new pipeline will be created (default: current directory)",
    )
    create_parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode to create pipeline configuration",
    )

    # update command
    update_parser = subparsers.add_parser(
        "update",
        help="Update an existing pipeline",
    )
    update_parser.add_argument(
        "--config",
        "-c",
        required=True,
        help="Path to the pipeline configuration JSON file",
    )
    update_parser.add_argument(
        "--pipeline",
        "-p",
        required=True,
        help="Path to the existing pipeline directory",
    )

    # sample command
    sample_parser = subparsers.add_parser(
        "sample",
        help="Generate a sample configuration file",
    )
    sample_parser.add_argument(
        "--output",
        "-o",
        required=False,
        default="pipeline_config_sample.json",
        help="Output file path for sample configuration (default: pipeline_config_sample.json)",
    )

    return parser


def interactive_config() -> Dict:
    """
    Create pipeline configuration interactively.

    Returns:
        Dictionary with pipeline configuration
    """
    print(
        "=== BClearer Pipeline Builder Interactive Configuration ==="
    )

    domain_name = input("Domain name: ")

    pipelines = []
    pipeline_count = int(
        input("Number of pipelines: ")
    )

    for i in range(pipeline_count):
        pipeline_name = input(
            f"Pipeline {i+1} name: "
        )

        thin_slices = []
        slice_count = int(
            input(
                f"Number of thin slices for pipeline '{pipeline_name}': "
            )
        )

        for j in range(slice_count):
            slice_name = input(
                f"Thin slice {j+1} name for pipeline '{pipeline_name}': "
            )

            # Create standard stages
            stages = []
            for stage_info in [
                (
                    "1c_collect",
                    "Collect",
                ),
                ("2l_load", "Load"),
                ("3e_evolve", "Evolve"),
                (
                    "4a_assimilate",
                    "Assimilate",
                ),
                ("5r_reuse", "Reuse"),
            ]:
                (
                    stage_name,
                    stage_desc,
                ) = stage_info

                print(
                    f"\nStage: {stage_desc} ({stage_name})"
                )
                include_stage = (
                    input(
                        f"Include {stage_desc} stage? (y/n): "
                    ).lower()
                    == "y"
                )

                if include_stage:
                    b_units = []
                    has_b_units = (
                        input(
                            f"Does {stage_desc} stage have direct b_units? (y/n): "
                        ).lower()
                        == "y"
                    )

                    if has_b_units:
                        b_units_input = input(
                            "Enter b_unit names (comma-separated, e.g., ca,cb): "
                        )
                        b_units = [
                            unit.strip()
                            for unit in b_units_input.split(
                                ","
                            )
                            if unit.strip()
                        ]

                    sub_stages = []
                    has_sub_stages = (
                        input(
                            f"Does {stage_desc} stage have sub-stages? (y/n): "
                        ).lower()
                        == "y"
                    )

                    if has_sub_stages:
                        sub_stage_count = int(
                            input(
                                f"Number of sub-stages for {stage_desc}: "
                            )
                        )

                        for k in range(
                            sub_stage_count
                        ):
                            sub_stage_name = input(
                                f"Sub-stage {k+1} name for {stage_desc}: "
                            )

                            sub_b_units = (
                                []
                            )
                            sub_b_units_input = input(
                                f"Enter b_unit names for sub-stage {sub_stage_name} (comma-separated): "
                            )
                            sub_b_units = [
                                unit.strip()
                                for unit in sub_b_units_input.split(
                                    ","
                                )
                                if unit.strip()
                            ]

                            sub_stages.append(
                                {
                                    "name": sub_stage_name,
                                    "b_units": sub_b_units,
                                }
                            )

                    stages.append(
                        {
                            "name": stage_name,
                            "sub_stages": sub_stages,
                            "b_units": b_units,
                        }
                    )

            thin_slices.append(
                {
                    "name": slice_name,
                    "stages": stages,
                }
            )

        pipelines.append(
            {
                "name": pipeline_name,
                "thin_slices": thin_slices,
            }
        )

    return {
        "domain_name": domain_name,
        "pipelines": pipelines,
    }


def save_sample_config(
    output_path: str,
) -> None:
    """
    Save a sample configuration file.

    Args:
        output_path: Path to save the sample configuration file
    """
    sample_config = get_sample_config()

    with open(output_path, "w") as f:
        json.dump(
            sample_config, f, indent=2
        )

    print(
        f"Sample configuration saved to '{output_path}'"
    )


def show_detailed_help() -> None:
    """
    Show detailed help about pipeline configuration structure and usage.
    """
    help_text = """
=== BClearer Pipeline Builder - Detailed Help ===

COMMANDS:
  create    - Create a new pipeline structure from configuration (no template needed)
  update    - Update an existing pipeline with new components
  sample    - Generate a sample configuration file
  help      - Show this detailed help message

CONFIGURATION STRUCTURE:
  The pipeline configuration is a JSON file with the following structure:

  {
    "domain_name": "example_domain",
    "pipelines": [
      {
        "name": "example_pipeline",
        "thin_slices": [
          {
            "name": "example_thin_slice",
            "stages": [
              {
                "name": "1c_collect",
                "sub_stages": [
                  {
                    "name": "sub_stage_1",
                    "b_units": ["example_b_unit"]
                  }
                ],
                "b_units": ["collector_b_unit"]
              },
              // More stages: 2l_load, 3e_evolve, 4a_assimilate, 5r_reuse
            ]
          }
        ]
      }
    ]
  }

COMPONENT DETAILS:
  domain_name - The domain name for which pipelines are being built
  pipelines   - List of pipelines within the domain
  thin_slices - List of thin slices within a pipeline
  stages      - List of stages within a thin slice (standard stages: 1c_collect, 2l_load, 3e_evolve, 4a_assimilate, 5r_reuse)
  sub_stages  - Optional list of sub-stages within a stage
  b_units     - List of b_units (basic units of work) within a stage or sub-stage

CREATING A NEW PIPELINE:
  1. Generate a sample configuration:
     pipeline_builder sample --output my_config.json

  2. Edit the configuration file to match your requirements

  3. Create the pipeline structure:
     pipeline_builder create --config my_config.json

  4. Specify an output directory (optional):
     pipeline_builder create --config my_config.json --output /path/to/output/directory

  Alternatively, use interactive mode:
     pipeline_builder create --interactive

UPDATING AN EXISTING PIPELINE:
  1. Modify your configuration to add new components
     - Add new pipelines, thin slices, stages, sub-stages, or b_units
     - The domain_name must match the existing pipeline
     - Existing components will not be modified

  2. Update the pipeline structure:
     pipeline_builder update --config updated_config.json --pipeline path/to/domain_name_pipelines

TECHNICAL DETAILS:
  - The pipeline structure is generated completely from scratch - no external template is required
  - The generator creates all necessary directories, files, and code based on your configuration
  - This makes the tool portable and easy to use in any environment

TEMPLATE MANAGEMENT:
  - The pipeline generator uses template constants stored in the code
  - To update these templates from an existing pipeline template:
     pipeline_builder update-templates --template-path /path/to/template_pipeline

  - This allows you to maintain your code generation templates separately
  - Workflow:
    1. Make changes to the template pipeline code
    2. Run the update-templates command to extract the new templates
    3. The generator will now use the updated templates for all future pipelines

For more information, visit the BClearer documentation.
"""
    print(help_text)


def run_cli() -> None:
    """Run the bclearer pipeline builder CLI."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "help":
        show_detailed_help()
        return

    if args.command == "sample":
        save_sample_config(args.output)
        return

    if args.command == "create":
        config = None

        if args.interactive:
            config = (
                interactive_config()
            )
        elif args.config:
            try:
                with open(
                    args.config, "r"
                ) as f:
                    config = json.load(
                        f
                    )
            except Exception as e:
                print(
                    f"Error loading configuration file: {str(e)}"
                )
                return
        else:
            print(
                "Error: Either --config or --interactive must be specified"
            )
            return

        try:
            pipeline_path = (
                generate_pipeline(
                    config,
                    args.output,
                )
            )
            print(
                f"Pipeline created successfully at '{pipeline_path}'"
            )
        except Exception as e:
            print(
                f"Error creating pipeline: {str(e)}"
            )
            return

    elif args.command == "update":
        try:
            with open(
                args.config, "r"
            ) as f:
                config = json.load(f)
        except Exception as e:
            print(
                f"Error loading configuration file: {str(e)}"
            )
            return

        try:
            pipeline_path = (
                update_pipeline(
                    config,
                    args.pipeline,
                )
            )
            print(
                f"Pipeline updated successfully at '{pipeline_path}'"
            )
        except Exception as e:
            print(
                f"Error updating pipeline: {str(e)}"
            )
            return

    elif (
        args.command
        == "update-templates"
    ):
        template_path = (
            args.template_path
        )

        if not os.path.exists(
            template_path
        ):
            print(
                f"Template path not found: {template_path}"
            )
            return

        if not os.path.isdir(
            template_path
        ):
            print(
                f"Template path is not a directory: {template_path}"
            )
            return

        # If output directory is not specified, use the default
        output_dir = args.output
        if output_dir is None:
            # Get the directory where this script is located
            script_dir = (
                os.path.dirname(
                    os.path.abspath(
                        __file__
                    )
                )
            )
            output_dir = os.path.join(
                script_dir, "templates"
            )

        try:
            update_templates_from_pipeline(
                template_path,
                output_dir,
            )
            print(
                f"Templates updated successfully in '{output_dir}'"
            )
        except Exception as e:
            print(
                f"Error updating templates: {str(e)}"
            )
            return


if __name__ == "__main__":
    run_cli()
