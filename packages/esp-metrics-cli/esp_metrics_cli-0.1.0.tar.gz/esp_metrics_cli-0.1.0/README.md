<a href="https://www.espressif.com">
    <img src="https://www.espressif.com/sites/all/themes/espressif/logo-black.svg" alt="Espressif logo" title="Espressif" align="right" height="20" />
</a>

# ESP Metrics CLI

A command-line tool for standardizing metrics collection, validation, and upload across all Espressif projects. This tool enables consistent metrics processing in CI/CD pipelines by providing a unified interface for generating, validating, and submitting project metrics to the central Espressif metrics service.

- [ESP Metrics CLI](#esp-metrics-cli)
  - [Why ESP Metrics CLI?](#why-esp-metrics-cli)
    - [The Problem](#the-problem)
    - [The Solution](#the-solution)
  - [Architecture Overview](#architecture-overview)
  - [Getting Started](#getting-started)
    - [Installation](#installation)
      - [Option 1: Install from PyPI (Recommended)](#option-1-install-from-pypi-recommended)
      - [Option 2: Standalone Binary](#option-2-standalone-binary)
      - [Option 3: From Source (Development)](#option-3-from-source-development)
    - [Quick Start](#quick-start)
  - [Developer Integration Guide](#developer-integration-guide)
    - [Step 1: Add esp-metrics-cli to Your Project](#step-1-add-esp-metrics-cli-to-your-project)
    - [Step 2: Generate Metrics](#step-2-create-metric-definitions)
    - [Step 3: Create Metric Definitions](#step-3-generate-metrics)
    - [Step 4: Integrate with CI Pipeline](#step-4-integrate-with-ci-pipeline)
  - [Metrics Validation](#metrics-schema--validation)
    - [Local Validation](#local-validation)
  - [Command Reference](#command-reference)
    - [`esp-metrics-cli init`](#esp-metrics-cli-init)
    - [`esp-metrics-cli validate`](#esp-metrics-cli-validate)
    - [`esp-metrics-cli upload`](#esp-metrics-cli-upload)
    - [Global Options](#global-options)
  - [Configuration](#configuration)
    - [Configuration File (Recommended for Local Development)](#configuration-file-recommended-for-local-development)
    - [Environment Variables (Required for CI/CD)](#environment-variables-required-for-cicd)
    - [Bucket Types](#bucket-types)
  - [Integration Points](#integration-points)
    - [CI/CD Pipeline Integration](#cicd-pipeline-integration)
    - [MinIO Object Storage](#minio-object-storage)
    - [Backend Metrics Service](#backend-metrics-service)
  - [Local Development Workflow](#local-development-workflow)
  - [Development](#development)

---

## Why ESP Metrics CLI?

### The Problem

Espressif has multiple projects (esp-idf, esp-bluetooth, esp-matter, etc.) that need to track various metrics like:

- **Build metrics**: Binary sizes, compilation times, memory usage
- **Test metrics**: Pass/fail rates, execution times, coverage
- **Custom metrics**: Project-specific measurements

Without standardization, each project would:

- Implement metrics collection differently
- Use incompatible data formats
- Duplicate validation and upload logic

### The Solution

ESP Metrics CLI provides a **standardized client-side architecture** that:

- **Unifies metrics collection** across all Espressif projects
- **Enforces consistent data schemas** via validation
- **Centralizes upload logic** to object storage
- **Enables cross-project analytics** and dashboards
- **Integrates seamlessly** with existing CI/CD pipelines

## Architecture Overview

The ESP Metrics CLI follows a three-stage workflow designed for CI/CD integration:

![ESP Metrics CLI Architecture](docs/diagram.png)

**Key Principles:**

- **Project-side generation**: Projects create custom scripts to transform raw artifacts into meaningful metrics
- **Standardized validation**: All metrics conform to a contracted JSON schema
- **Centralized upload**: Single tool handles validation and upload to object storage
- **Backend integration**: Uploaded metrics trigger webhook processing for dashboard/API consumption

## Getting Started

### Installation

Choose your preferred installation method:

#### Option 1: Install from PyPI (Recommended)

```bash
# Using pip
pip install esp-metrics-cli

# Using uv (faster)
uv tool install esp-metrics-cli

# Verify installation
esp-metrics-cli --help
```

#### Option 2: Standalone Binary

Download pre-built binaries from the GitLab Package Registry on the project page.

#### Option 3: From Source (Development)

```bash
# Clone repository
cd esp-metrics-cli

# Install with uv
uv venv && source .venv/bin/activate
uv sync --all-extras

# Verify installation
python -m app.cli --help
```

## Developer Integration Guide

### Step 1: Add esp-metrics-cli to Your Project

Install the tool in your project environment:

```bash
# Add to requirements.txt
echo "esp-metrics-cli>=0.1.0" >> requirements.txt

# Or add to pyproject.toml
esp-metrics-cli = ">=0.1.0"

# Or install directly
pip install esp-metrics-cli
```

### Step 2: Generate Metrics

Create a script that transforms your raw artifacts into JSON which satisfies the format you described in `metrics_definitions.yaml`.

The script can be implemented in any language, or you can use tools like `jq` to produce `metrics.json` in the required format.

The `metrics.json` file should contain a JSON object where the top-level keys are metric categories (like "builds", "tests", "coverage", etc.) and the values follow the hierarchical structure you defined in your `metrics_definitions.yaml`. Read more in [Step 3: Create Metric Definitions](#step-3-generate-metrics):

Here is an example script:

```python
#!/usr/bin/env python3
# tools/generate_metrics.py

import json


def generate_metrics():
    """Generate metrics from your project artifacts."""

    return {
        'builds': {
            'apps/my_app/build': {
                'size': {'flash_size_bytes': 1048576, 'ram_size_bytes': 65536},
                'build': {'time_seconds': 45.2, 'warnings_count': 3},
            }
        },
        'tests': {'unit_tests': {'passed_count': 42, 'failed_count': 1, 'duration_seconds': 12.5}},
        'coverage': {'line_coverage_percent': 85.3, 'branch_coverage_percent': 78.9},
    }


if __name__ == '__main__':
    metrics = generate_metrics()
    with open('metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
```

Notes about the format of JSON file:

- Top-level keys are the metrics and can be anything meaningful to your project.
- You can mix flat metrics and nested structures at the same level
- Metric names must use snake_case with units/dimensions at the end (e.g., time_seconds, size_bytes)
- Lists of dictionaries are supported in the metrics structure
- The JSON structure must match what you've defined in your `metrics_definitions.yaml` [Step 3: Create Metric Definitions](#step-3-generate-metrics)

### Step 3: Create Metric Definitions

Definition files (`metrics_definitions.yaml`) serve multiple purposes:

1. **Schema validation**: Ensures your `metrics.json` file has the correct structure and data types
2. **Documentation**: Describes what each metric represents and its purpose
3. **Type safety**: Prevents errors by enforcing consistent data types across uploads
4. **API contract**: Defines the expected format for service consuming your metrics

#### Schema Structure

The schema follows JSON Schema specification and should contain:

- **`type: object`** - Root level must be an object
- **`properties`** - Define your top-level metric categories (e.g. builds, tests, coverage, etc.)
- **`description`** - Human-readable explanation of what each section contains
- **Data types** - `number`, `integer`, `string`, `boolean`, `array`, `object`
- **`patternProperties`** - For dynamic keys (like build paths or test suite names)

Create a `metrics_definitions.yaml` file that defines your project's metrics schema. Look at the example below:

```yaml
type: object
properties:
  builds:
    type: object
    description: "Build-related metrics organized by path"
    patternProperties:
      "^.+$":  # Matches any build path like 'apps/my_app/build'
        type: object
        properties:
          size:
            type: object
            properties:
              flash_size_bytes:
                type: number
                description: "Flash memory usage in bytes"
              ram_size_bytes:
                type: number
                description: "RAM memory usage in bytes"
          build:
            type: object
            properties:
              time_seconds:
                type: number
                description: "Build time in seconds"
              warnings_count:
                type: integer
                description: "Number of build warnings"
  tests:
    type: object
    description: "Test-related metrics organized by test suite"
    patternProperties:
      "^.+$":  # Matches any test suite name like 'unit_tests'
        type: object
        properties:
          passed_count:
            type: integer
            description: "Number of passed tests"
          failed_count:
            type: integer
            description: "Number of failed tests"
          duration_seconds:
            type: number
            description: "Total test execution time in seconds"
  coverage:
    type: object
    description: "Code coverage metrics"
    properties:
      line_coverage_percent:
        type: number
        description: "Line coverage percentage"
      branch_coverage_percent:
        type: number
        description: "Branch coverage percentage"
```

### Step 4: Integrate with CI Pipeline

#### File Organization

To keep your metrics infrastructure organized and maintainable, create a centralized structure for all metrics-related files.

As an example:

```
project-root/
├── tools/
│   └── ci/
│       └── metrics/
│           ├── build/
│           │   ├── metrics_definitions.yaml
│           │   └── generate_metrics.py
│           ├── tests/
│           │   ├── metrics_definitions.yaml
│           │   └── generate_metrics.py
│           └── coverage/
│               ├── metrics_definitions.yaml
│               └── generate_metrics.py
└── .gitlab-ci.yml
```

**Key principles:**

- **Centralized location**: All metrics files under one location, e.g. `tools/ci/metrics/`
- **Category-based organization**: Separate directories for `build/`, `tests/`, `coverage/`, etc.
- **Consistent naming**: Each category has its own `metrics_definitions.yaml` and `generate_metrics.py`
- **Version controlled**: All files committed to your repository for reproducibility

Update your existing jobs to generate and upload metrics. Make sure the following variables are defined in your GitLab CI settings:

- `ESP_METRICS_S3_SERVER`
- `ESP_METRICS_S3_ACCESS_KEY`
- `ESP_METRICS_S3_SECRET_KEY`
- `ESP_METRICS_S3_LONG_TERM_BUCKET`
- `ESP_METRICS_S3_SHORT_TERM_BUCKET`

The CLI automatically uses the following GitLab CI built-in variables, make sure to have them available in the variables section.

- `CI_PROJECT_URL` - for project identification
- `CI_PROJECT_ID` - for project identification
- `CI_COMMIT_SHA` - for commit identification

Update your existing jobs to generate and upload metrics in gitlab ci config for the build job that produces build-related metrics:

```yaml
# .gitlab-ci.yml
variables:
  ESP_METRICS_PROJECT_URL: "$CI_PROJECT_URL"
  ESP_METRICS_PROJECT_ID: "$CI_PROJECT_ID"
  ESP_METRICS_COMMIT_SHA: "$CI_COMMIT_SHA"
build_job:
  stage: build
  script:
    - make build
    - pip install esp-metrics-cli
    - python tools/ci/metrics/build/generate_metrics.py > metrics.json
    - esp-metrics-cli upload -d tools/ci/metrics/build/metrics_definitions.yaml -i metrics.json --verbose
```

## Metrics Validation

### Local Validation

Validate your metrics before CI upload:

```bash
# Basic validation
esp-metrics-cli validate -d definitions.yaml -i metrics.json

# Verbose validation with detailed output
esp-metrics-cli validate -d definitions.yaml -i metrics.json --verbose
```

**Validation checks:**

- Required fields present
- Data types match schema
- Custom validation rules

## Command Reference

### `esp-metrics-cli init`

Create a configuration file with default settings. The config file (git ignored by default) is used for the local development. **For the production environment it is recommended to use environment variables**.

```bash
esp-metrics-cli init [OPTIONS]
```

**Options:**

- `--path TEXT`: Configuration file path (default: `.esp_metrics.toml`)
- `--force`: Overwrite existing configuration file

**Examples:**

```bash
# Create default config
esp-metrics-cli init

# Create config with custom path
esp-metrics-cli init --path config/metrics.toml

# Overwrite existing config
esp-metrics-cli init --force
```

### `esp-metrics-cli validate`

Validate metrics against schema definitions.

```bash
esp-metrics-cli validate [OPTIONS]
```

**Required Options:**

- `-d, --definitions PATH`: Path to definitions.yaml file
- `-i, --input PATH`: Path to metrics.json file

**Optional Options:**

- `-v, --verbose`: Enable detailed output

**Examples:**

```bash
# Basic validation
esp-metrics-cli validate -d definitions.yaml -i metrics.json

# Verbose validation
esp-metrics-cli validate -d definitions.yaml -i metrics.json --verbose

```

### `esp-metrics-cli upload`

Upload metrics to the service. **Note: This command automatically validates metrics before upload**, so a separate validation step is not required.

```bash
esp-metrics-cli upload [OPTIONS]
```

**Required Options:**

- `-d, --definitions PATH`: Path to definitions.yaml file
- `-i, --input PATH`: Path to metrics.json file

**Optional Options:**

- `-v, --verbose`: Enable detailed output
- `--bucket-type CHOICE`: Override bucket selection (`auto|long_term|short_term|custom`)
- `--custom-bucket TEXT`: Custom bucket name (required with `--bucket-type=custom`)

**Examples:**

```bash
# Upload with auto bucket detection
esp-metrics-cli upload -d definitions.yaml -i metrics.json

# Force upload to long-term bucket
esp-metrics-cli upload -d definitions.yaml -i metrics.json --bucket-type long_term

# Upload to custom bucket
esp-metrics-cli upload -d definitions.yaml -i metrics.json --bucket-type custom --custom-bucket my-bucket

# Verbose upload with detailed validation output
esp-metrics-cli upload -d definitions.yaml -i metrics.json --verbose
```

### Global Options

Available for all commands:

- `-c, --config-file PATH`: Path to configuration file (for local dev)
- `-h, --help`: Show help message

**Examples:**

```bash
# Use custom config file
esp-metrics-cli -c /path/to/config.toml validate -d definitions.yaml -i metrics.json

esp-metrics-cli upload -d definitions.yaml -i metrics.json
```

## Configuration

ESP Metrics CLI supports two configuration methods depending on your use case:

### Configuration File (Recommended for Local Development)

For local development and testing, use the `.esp_metrics.toml` configuration file. This method provides:

- **Easy editing**
- **Clear documentation** with inline comments
- **Persistent settings** across development sessions
- **Template generation** via `esp-metrics-cli init`

Create and customize your configuration file:

```bash
# Generate default configuration file
esp-metrics-cli init
```

The `.esp_metrics.toml` file contains all configuration settings with helpful comments. Look at the [example](app/templates/.esp_metrics.toml).

### Environment Variables (Required for CI/CD)

For CI/CD pipelines, use environment variables instead of configuration files. This approach provides:

- **Secure credential handling** via CI/CD secrets
- **No file management**
- **Dynamic configuration** per pipeline run

All configuration can be set via environment variables with the `ESP_METRICS_` prefix.

You can take a look at the [example](examples/env.template).

### Bucket Types

The tool supports different bucket types for upload destinations:

- **`auto`** (default): Automatically selects bucket based on branch name
  - Release branches → long-term bucket
  - Other branches → short-term bucket
- **`long_term`**: Always use long-term bucket (for releases)
- **`short_term`**: Always use short-term bucket (for development)
- **`custom`**: Use custom bucket name (requires `--custom-bucket`)

## Integration Points

### CI/CD Pipeline Integration

ESP Metrics CLI provides a reusable template for uploading metrics generated by your existing jobs. The example is shown in [Step 4: Integrate with CI Pipeline](#step-4-integrate-with-ci-pipeline).

### MinIO Object Storage

The tool uploads metrics to MinIO-compatible S3 storage:

- **Authentication**: S3 access/secret keys
- **Bucket selection**: Automatic or manual bucket routing
- **File naming**: Structured naming convention for easy retrieval
- **Retry logic**: Automatic retry on upload failures

**Upload path structure:**

```
bucket/
├── project_host/
│   ├── projectid_project_path/
│   │   ├── commit_sha/
│   │   │   └── {timestamp}.json
│   │   ├── commit_sha/
│   │   │   └── {timestamp}.json
│   │   └── ...
│   ├── projectid_project_path/
│   │   └── ...
│   └── ...
├── project_host/
│   └── ...
└── ...

Example:

esp-metrics-bucket/
├── https_gitlab_example_com_8080/
│   ├── 1111_myorg_esp-project/
│   │   ├── abc123def456/
│   │   │   ├── 2024-01-15_14-30-00.507.json
│   │   │   └── 2024-01-15_15-45-30.507.json
│   │   └── def789ghi012/
│   │       └── 2024-01-16_09-15-22.507.json
│   └── 2222_myorg_esp-components/
│       └── xyz987uvw654/
│           └── 2024-01-17_11-20-45.507.json
├── https_github_example_com/
│   └── 3333_myteam_my-project/
│       └── 1a2b3c4d5e6f/
│           └── 2024-01-18_16-55-10.507.json
└── https_git_example_com/
    └── 4444_devteam_repo-name/
        └── 9z8y7x6w5v4u/
            └── 2024-01-19_12-00-00.507.json
```

### Backend Metrics Service

Uploaded metrics trigger backend processing:

1. **Webhook trigger**: MinIO notifies backend service of new uploads
2. **Data validation**: Backend re-validates metrics schema
3. **Database storage**: Metrics stored in MongoDB for analytics
4. **API exposure**: Metrics available via REST API
5. **Dashboard updates**: Real-time dashboard updates

**Integration flow:**

```
CLI Upload → MinIO → Webhook → Backend Service → MongoDB → Dashboard/API
```

### Local Development Workflow

Developer workflow for testing metrics locally using configuration files:

```bash
# 1. Set up development environment with configuration file
esp-metrics-cli init
# Edit .esp_metrics.toml with your S3 settings and preferences

# 2. Generate test metrics
python tools/generate_metrics.py

# 3. Upload and validate in one step (if S3 credentials are configured)
esp-metrics-cli upload -d definitions.yaml -i metrics.json --verbose

# Optional: Validate only (for testing schema without uploading)
esp-metrics-cli validate -d definitions.yaml -i metrics.json --verbose
```

---

## Development

This project uses modern Python development tools for maintainability and code quality.

**Development setup:**

```bash
# Clone repository
cd esp-metrics-cli

# Install with development dependencies
uv venv && source .venv/bin/activate
uv sync --all-extras

# Install pre-commit hooks
pre-commit install && pre-commit autoupdate

# Run tests
pytest

# Run quality checks
pre-commit run --all-files
```

**Tools used:**

- **UV**: Fast package manager
- **Hatchling**: Modern build system
- **Ruff**: Fast linter and formatter
- **Pytest**: Testing framework
- **Pre-commit**: Code quality hooks
- **Mypy**: Type checking
