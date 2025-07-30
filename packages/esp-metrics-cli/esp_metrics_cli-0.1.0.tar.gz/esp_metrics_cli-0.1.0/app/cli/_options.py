# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import difflib
import logging
import os
import shutil

import click

from app.models.config import BucketType

logger = logging.getLogger(__name__)


###########
# Options #
###########
def option_input_file(func):
    """Add input file option for metrics validation/upload."""
    return click.option(
        '--input',
        '-i',
        'input_file',
        type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
        required=True,
        help='Path to the metrics.json file to validate or upload',
    )(func)


def option_definitions_file(func):
    """Add definitions file option for schema validation."""
    return click.option(
        '--definitions',
        '-d',
        'definitions_file',
        type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
        required=True,
        help='Path to the definitions.yaml file containing schema specifications',
    )(func)


def option_verbose(func):
    """Add verbose option for detailed output."""
    return click.option(
        '--verbose',
        '-v',
        is_flag=True,
        default=False,
        help='Enable verbose output with detailed information',
    )(func)


def option_bucket_type(func):
    """Add bucket type option for upload commands."""
    return click.option(
        '--bucket-type',
        type=click.Choice([bt.value for bt in BucketType], case_sensitive=False),
        help=(
            'Override bucket selection: auto (detect from branch), long_term (releases), '
            'short_term (development), custom (specify bucket name)'
        ),
    )(func)


def option_custom_bucket(func):
    """Add custom bucket option for upload commands."""
    return click.option(
        '--custom-bucket',
        type=str,
        help='Custom bucket name to use when --bucket-type=custom',
    )(func)


#########
# Utils #
#########
def create_config_file(template_filepath: str, dest: str | None = None) -> str:
    """Create a configuration file from a template."""
    if dest is None:
        dest = os.getcwd()

    if os.path.isdir(dest):
        filepath = os.path.join(dest, os.path.basename(template_filepath))
    else:
        filepath = dest

    if not os.path.isfile(filepath):
        shutil.copyfile(template_filepath, filepath)
        click.echo(f'Created {filepath}')
        return filepath

    with open(template_filepath) as template_file:
        template_content = template_file.readlines()
    with open(filepath) as existing_file:
        existing_content = existing_file.readlines()

    diff = list(difflib.unified_diff(existing_content, template_content, fromfile='existing', tofile='template'))
    if not diff:
        click.secho(f'{filepath} already exists and is identical to the template.', fg='yellow')
        return filepath

    click.secho(f'{filepath} already exists. Showing diff:', fg='yellow')
    for line in diff:
        if line.startswith('+'):
            click.secho(line, fg='green', nl=False)
        elif line.startswith('-'):
            click.secho(line, fg='red', nl=False)
        elif line.startswith('@@'):
            click.secho(line, fg='cyan', nl=False)
        else:
            click.secho(line, nl=False)

    return filepath
