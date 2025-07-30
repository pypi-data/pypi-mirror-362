# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import os
import subprocess
import sys
import typing as t

from pathlib import Path

import yaml


def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration for the application."""

    class ColoredFormatter(logging.Formatter):
        """Custom formatter with colors for different log levels."""

        COLORS = {
            'DEBUG': '\033[36m',  # Cyan
            'INFO': '\033[32m',  # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',  # Red
            'CRITICAL': '\033[35m',  # Magenta
        }
        RESET = '\033[0m'

        def format(self, record):
            if record.levelname in self.COLORS:
                record.levelname = f'{self.COLORS[record.levelname]}{record.levelname}{self.RESET}'
            return super().format(record)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    if sys.stdout.isatty():
        formatter: logging.Formatter = ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    logging.getLogger('urllib3').setLevel(logging.WARNING)


def load_json_file(file_path: str | Path) -> t.Any:
    """Load and parse a JSON file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f'Invalid JSON in file {file_path}: {e}') from e
    except Exception as e:
        raise ValueError(f'Cannot read file {file_path}: {e}') from e


def load_yaml_file(file_path: str | Path) -> t.Any:
    """Load and parse a YAML file."""
    try:
        with open(file_path, encoding='utf-8') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f'Invalid YAML in file {file_path}: {e}') from e
    except Exception as e:
        raise ValueError(f'Cannot read file {file_path}: {e}') from e


def get_file_size(file_path: str | Path) -> int:
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)


def validate_file_size(file_path: str | Path, max_size: int) -> None:
    """Validate that a file is not larger than the maximum allowed size."""
    file_size = get_file_size(file_path)
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        file_mb = file_size / (1024 * 1024)
        raise ValueError(f'File {file_path} is too large ({file_mb:.1f}MB), maximum allowed is {max_mb:.1f}MB')


def format_bytes(num_bytes: int) -> str:
    """Format a number of bytes as a human-readable string."""
    if num_bytes < 0:
        raise ValueError('Number of bytes cannot be negative')

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if num_bytes < 1024.0:
            return f'{num_bytes:.1f} {unit}'
        num_bytes = num_bytes / 1024.0  # type: ignore
    return f'{num_bytes:.1f} PB'


def get_current_branch() -> str | None:
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True, check=True, timeout=5
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        return None
