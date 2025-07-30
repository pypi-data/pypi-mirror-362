# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

"""Metrics data models for ESP Metrics CLI."""

import typing as t

from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class MetricsData(BaseModel):
    commit_sha: str = Field(..., max_length=64, description='Git commit hash', title='Commit Sha')
    metrics: dict[str, t.Any] = Field(..., description='Metrics dictionary', title='Metrics')
    project_url: str = Field(..., min_length=1, description='project url', title='project url')
    project_id: int = Field(..., description='Project identifier', title='Project Id')
    schema_version: str = Field(..., description='Schema version', title='Schema Version')
    timestamp: str = Field(..., description='ISO 8601 timestamp', title='Timestamp')

    @field_validator('commit_sha')
    @classmethod
    def validate_commit_sha(cls, v: str) -> str:
        if not all(c in '0123456789abcdef' for c in v.lower()):
            raise ValueError('Commit SHA must contain only hexadecimal characters')
        return v.lower()

    @field_validator('timestamp')
    @classmethod
    def validate_timestamp(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
        except ValueError as err:
            raise ValueError('Timestamp must be in ISO 8601 format') from err
        return v
