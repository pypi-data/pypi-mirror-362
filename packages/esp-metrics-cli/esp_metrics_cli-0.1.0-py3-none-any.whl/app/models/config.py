# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

"""Configuration models for ESP Metrics CLI."""

import logging
import os
import typing as t

from enum import Enum
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import InitSettingsSource
from pydantic_settings import PydanticBaseSettingsSource
from tomlkit import load

from app.utils import get_current_branch

logger = logging.getLogger(__name__)


class BucketType(str, Enum):
    """Enumeration of bucket type selection modes."""

    AUTO = 'auto'
    LONG_TERM = 'long_term'
    SHORT_TERM = 'short_term'
    CUSTOM = 'custom'


class MetricsSettings(BaseSettings):
    """ESP Metrics CLI settings from environment variables and config files."""

    model_config = {'env_prefix': 'ESP_METRICS_', 'env_file': '.env'}
    CONFIG_FILE_PATH: t.ClassVar[Path | None] = None

    # S3 Storage Configuration
    s3_server: str | None = Field(default=None, description='S3 server endpoint URL')
    s3_access_key: str | None = Field(default=None, description='S3 access key for authentication')
    s3_secret_key: str | None = Field(default=None, description='S3 secret key for authentication')

    # Upload destination settings
    s3_long_term_bucket: str = Field(default='esp-metrics-releases', description='Long-term bucket for releases')
    s3_short_term_bucket: str = Field(default='esp-metrics-dev', description='Short-term bucket for development/MRs')
    metrics_upload_bucket_type: BucketType = Field(
        default=BucketType.AUTO, description='Bucket type selection: auto|long_term|short_term|custom'
    )
    custom_bucket_name: str | None = Field(
        default=None, description='Custom bucket name when metrics_upload_bucket_type=custom'
    )
    release_branches: list[str] = Field(
        default_factory=lambda: ['main', 'master', 'release/*', 'v*'],
        description='Branch patterns that trigger long-term bucket usage',
    )

    max_metrics_size: int = Field(default=10 * 1024 * 1024, description='Maximum metrics file size in bytes')

    # Upload Configuration
    upload_retries: int = Field(default=3, description='Number of upload retry attempts')
    upload_retry_delay: int = Field(default=1, description='Delay between retries in seconds')

    # Project Specific
    project_url: str = Field(
        default='https://gitlab.example.com:8080/myorg/my-project', min_length=1, description='Project URL'
    )
    project_id: int = Field(default=1, description='Project identifier')
    commit_sha: str = Field(
        default='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', max_length=64, description='Git commit hash'
    )

    schema_version: str = Field(default='1.0', description='Metrics Schema Version')

    def get_target_bucket(
        self,
        bucket_type_override: BucketType | str | None = None,
        custom_bucket_override: str | None = None,
    ) -> str:
        """Get the appropriate bucket based on upload bucket type and context."""
        if bucket_type_override:
            bucket_type = (
                BucketType(bucket_type_override) if isinstance(bucket_type_override, str) else bucket_type_override
            )
        else:
            bucket_type = self.metrics_upload_bucket_type
        custom_bucket = custom_bucket_override or self.custom_bucket_name
        branch_name = get_current_branch()
        if bucket_type == BucketType.LONG_TERM:
            return self.s3_long_term_bucket
        elif bucket_type == BucketType.SHORT_TERM:
            return self.s3_short_term_bucket
        elif bucket_type == BucketType.CUSTOM and custom_bucket:
            return custom_bucket
        elif bucket_type == BucketType.AUTO and branch_name is not None:
            return self._detect_bucket_from_branch(branch_name)
        else:
            return self.s3_short_term_bucket

    def _detect_bucket_from_branch(self, branch_name: str) -> str:
        """Auto-detect bucket based on branch patterns."""
        import fnmatch

        for pattern in self.release_branches:
            if fnmatch.fnmatch(branch_name, pattern):
                return self.s3_long_term_bucket
        return self.s3_short_term_bucket

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(
                settings_cls,
                cls.CONFIG_FILE_PATH if cls.CONFIG_FILE_PATH is not None else '.esp_metrics.toml',  # type: ignore
            ),
        )


class TomlConfigSettingsSource(InitSettingsSource):
    """A source class that loads variables from a TOML file"""

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        toml_file: os.PathLike | None = Path(''),
    ):
        self.toml_file_path = self._pick_toml_file(
            toml_file,
            '.idf_ci.toml',
        )
        self.toml_data = self._read_file(self.toml_file_path)
        super().__init__(settings_cls, self.toml_data)

    def _read_file(self, path: Path | None) -> t.Any:
        if not path or not path.is_file():
            return {}

        with open(path) as f:
            return load(f)

    @staticmethod
    def _pick_toml_file(provided: os.PathLike | None, filename: str) -> Path | None:
        """Pick a file path to use."""
        if provided:
            provided_p = Path(provided)
            if provided_p.is_file():
                fp = provided_p.resolve()
                logger.debug(f'Loading config file: {fp}')
                return fp

        rv = Path.cwd()
        while len(rv.parts) > 1:
            fp = rv / filename
            if fp.is_file():
                logger.debug(f'Loading config file: {fp}')
                return fp

            rv = rv.parent

        return None
