# bclearer core

The `bclearer_core` package is the foundational component of the bclearer framework, providing essential utilities and services required for the data pipeline architecture in semantic engineering. It encompasses core functionalities that are utilized across the entire framework, ensuring consistency and extensibility.

## Overview

The `bclearer_core` library offers a collection of modules responsible for handling common tasks and configurations that are integral to the bclearer framework. These components form the backbone of the system and enable efficient management of knowledge, configurations, constants, and stages within the pipeline.

## Structure

The package consists of several key modules:

- **ckids**: Manages unique identifiers within the bclearer framework, ensuring consistency and traceability across components.
- **common_knowledge**: Contains shared knowledge and common utilities that are used across the framework.
- **configuration_managers**: Responsible for managing and handling various configurations for bclearer applications and processes.
- **configurations**: Defines standard configuration structures and utilities for the framework.
- **constants**: Stores and manages global constants used throughout the bclearer framework.
- **nf**: Manages foundational operations, providing core support for various tasks.
- **pipeline_builder**: Provides CLI tooling to generate and manage pipeline structures based on configuration.
- **substages**: Handles the different substages of the data pipeline, offering utilities to manage transitions and execution within stages.

## Installation

To install this package, use pip:

```bash
pip install bclearer_core
```

Or, clone this repository and install it locally:

```bash
git clone <repository-url>
cd bclearer_core
pip install .
```

## Usage

To use the core functionalities, import the desired module. For example:

```python
from bclearer_core import configurations

# Example usage
config = configurations.load_configuration(config_path="path/to/config.yaml")
print(config)
```

## Pipeline Builder

The Pipeline Builder is a powerful tool included in bclearer_core that helps you generate and manage bclearer pipeline structures based on JSON configuration. It eliminates the need to manually create the complex directory and file structure required for bclearer pipelines.

### Using the Pipeline Builder CLI

To access the pipeline builder CLI tool, you need to install the full bclearer PDK (not just bclearer-core). The tool can be used in two ways:

#### Option 1: Using Python module syntax

```bash
# Generate a sample configuration file
python -m bclearer_core.pipeline_builder sample --output my_config.json

# Create a new pipeline from configuration file
python -m bclearer_core.pipeline_builder create --config my_config.json

# Create a pipeline interactively
python -m bclearer_core.pipeline_builder create --interactive

# Create a pipeline in a specific output directory
python -m bclearer_core.pipeline_builder create --config my_config.json --output /path/to/output/directory

# Update an existing pipeline with new components
python -m bclearer_core.pipeline_builder update --config updated_config.json --pipeline path/to/domain_name_pipelines

# Show detailed help
python -m bclearer_core.pipeline_builder help
```

#### Option 2: Installing the full bclearer package

If you install the full bclearer package (which includes all components including core, interop_services, and orchestration_services), you'll have access to the `bclearer-pipeline-builder` command directly:

```bash
# First, install the full package from the GitHub repository
pip install git+https://github.com/your-org/bclearer.git

# Then you can use the command directly
bclearer-pipeline-builder sample --output my_config.json
bclearer-pipeline-builder create --config my_config.json
bclearer-pipeline-builder create --interactive
```

### Configuration Structure

The pipeline configuration uses a JSON structure that defines the domain, pipelines, thin slices, stages, sub-stages, and b-units:

```json
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
```

### Creating a New Pipeline in Your Project

Follow these steps to create a new bclearer pipeline in your project:

1. First, make sure you have bclearer_core installed in your project:
   ```bash
   pip install bclearer-core
   ```

2. Generate a sample configuration file:
   ```bash
   python -m bclearer_core.pipeline_builder sample --output my_pipeline_config.json
   ```

3. Edit the configuration file to match your pipeline requirements.

4. Create the pipeline structure:
   ```bash
   python -m bclearer_core.pipeline_builder create --config my_pipeline_config.json --output ./pipelines/
   ```

5. The tool will generate a complete pipeline structure including:
   - Pipeline orchestrators
   - Stage orchestrators
   - Sub-stage orchestrators
   - Thin slice orchestrators
   - B-unit skeletons
   - Application runner
   - Test infrastructure

6. Customize the generated code to implement your specific pipeline logic.

### Updating an Existing Pipeline

When your pipeline requirements change, you can update an existing pipeline:

1. Modify your configuration file to add new components.

2. Run the update command:
   ```bash
   python -m bclearer_core.pipeline_builder update --config updated_config.json --pipeline ./pipelines/example_domain_pipelines
   ```

3. This will add new components without modifying existing ones.

### Interactive Pipeline Creation

For guided pipeline creation:

```bash
python -m bclearer_core.pipeline_builder create --interactive
```

This will walk you through a series of prompts to define your pipeline structure.

## Contributions

Contributions are highly appreciated! Feel free to submit issues, pull requests, or feature requests to enhance the core functionality.
