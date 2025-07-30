# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

__all__ = ['click_cli']

import logging
import os

from pathlib import Path

import click

from app.cli.metrics_group import upload
from app.cli.metrics_group import validate
from app.models.config import MetricsSettings
from app.utils import setup_logging

logger = logging.getLogger(__name__)


@click.group(context_settings={'show_default': True, 'help_option_names': ['-h', '--help']})
@click.option(
    '-c',
    '--config-file',
    type=click.Path(dir_okay=False, file_okay=True, exists=True),
    help='Path to the esp-metrics-cli config file',
)
@click.option('--debug', is_flag=True, default=False, help='Enable debug logging')
def click_cli(config_file: str, debug: bool) -> None:
    """ESP Metrics CLI Tool - Validate and upload project metrics to metrics service."""
    if debug:
        setup_logging(logging.DEBUG)
    else:
        setup_logging()

    if config_file:
        logger.debug(f'Using config file: {config_file}')
        MetricsSettings.CONFIG_FILE_PATH = Path(config_file)
        logger.debug(f'Settings reloaded from: {config_file}')


@click.command()
@click.option(
    '--path', default='.esp_metrics.toml', help='Path where to create the config file (default: .esp_metrics.toml)'
)
@click.option('--force', is_flag=True, default=False, help='Overwrite existing config file if it exists')
def init(path: str, force: bool) -> None:
    """Create .esp_metrics.toml configuration file with default values."""

    if os.path.exists(path) and not force:
        click.secho(f'Configuration file already exists: {path}', fg='yellow')
        click.echo('Use --force to overwrite or specify a different --path')
        return

    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', '.esp_metrics.toml')

    try:
        with open(template_path) as template_file:
            toml_content = template_file.read()

        # Write the content to the target file
        with open(path, 'w') as f:
            f.write(toml_content)

        click.secho(f'✓ Created configuration file: {path}', fg='green')
        click.echo('You can now:')
        click.echo('  1. Edit the file to configure S3 settings')
        click.echo('  2. Uncomment s3_server, s3_access_key, s3_secret_key as needed')
        click.echo('  3. Adjust other settings as required')

    except FileNotFoundError as err:
        click.secho(f'✗ Template file not found: {template_path}', fg='red')
        raise click.ClickException(f'Template file missing: {template_path}') from err
    except Exception as e:
        click.secho(f'✗ Failed to create configuration file: {e}', fg='red')
        raise click.ClickException(f'Could not create {path}: {e}') from e


click_cli.add_command(init)
click_cli.add_command(validate)
click_cli.add_command(upload)
