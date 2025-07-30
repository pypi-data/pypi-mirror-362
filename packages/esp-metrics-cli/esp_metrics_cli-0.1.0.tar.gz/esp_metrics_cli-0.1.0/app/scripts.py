# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import time
import typing as t

from datetime import datetime
from urllib.parse import urlparse

import jsonschema

from pydantic import ValidationError

from app.clients.minio_client import MinioClient
from app.models.config import BucketType
from app.models.config import MetricsSettings
from app.models.metrics import MetricsData
from app.models.result import UploadResult
from app.models.result import ValidationResult
from app.utils import format_bytes
from app.utils import get_file_size
from app.utils import load_json_file
from app.utils import load_yaml_file
from app.utils import validate_file_size

logger = logging.getLogger(__name__)


def _fail(result: ValidationResult, error_message: str) -> None:
    """Add an error to the validation result."""
    result.errors.append(error_message)
    result.is_valid = False


def _generate_object_name(metrics: dict) -> str:
    """Generate S3 object name from validated metrics data.

    Format: project_host/projectid_project_path/commit_sha/timestamp.json
    Example: https_gitlab.espressif.cn_6688/1111_espressif_esp-idf/commit_sha/2024-01-15_14-30-00.json
    """
    parsed_url = urlparse(metrics['project_url'])

    project_host = f'{parsed_url.scheme}_{parsed_url.netloc}'.replace(':', '_').replace('.', '_')

    project_path = parsed_url.path.lstrip('/').replace('/', '_')
    projectid_project_path = f'{metrics["project_id"]}_{project_path}'

    timestamp = metrics['timestamp'].replace(':', '-').replace('T', '_')
    return f'{project_host}/{projectid_project_path}/{metrics["commit_sha"]}/{timestamp}.json'


def _validate_file_size_and_load(
    input_file: str, verbose: bool, result: ValidationResult, max_metrics_size: int
) -> dict | None:
    """Validate file size and load it."""
    try:
        result.file_size = get_file_size(input_file)
        if verbose:
            logger.info(f'Metrics file size: {format_bytes(result.file_size)}')

        try:
            validate_file_size(input_file, max_metrics_size)
        except ValueError as e:
            _fail(result, str(e))
            return None

        if verbose:
            logger.info(f'Loading metrics file: {input_file}')
        try:
            return load_json_file(input_file)  # type: ignore
        except ValueError as e:
            _fail(result, f'Failed to load metrics file: {e}')
            return None
    except Exception as e:
        _fail(result, f'Unexpected file loading error: {e}')
        return None


def _load_definitions_schema(definitions_file: str, verbose: bool, result: ValidationResult) -> t.Any:
    """Load definitions file and extract schema."""
    if verbose:
        logger.info(f'Loading definitions file: {definitions_file}')
    try:
        definitions = load_yaml_file(definitions_file)
        return definitions
    except Exception as e:
        _fail(result, f'Unexpected definitions loading error: {e}')
        return None


def _validate_json_schema(metrics_data: dict, schema: dict, verbose: bool, result: ValidationResult) -> bool:
    """Validate metrics data against JSON schema."""
    if verbose:
        logger.info('Validating metrics against JSON schema')
    try:
        jsonschema.validate(metrics_data, schema)
        if verbose:
            logger.info('Metrics passed JSON schema validation')
        return True
    except jsonschema.ValidationError as e:
        _fail(result, f'JSON schema validation error: {e}')
        return False
    except Exception as e:
        _fail(result, f'JSON schema validation error: {e}')
        return False


def _validate_model(metrics_data: dict, verbose: bool, result: ValidationResult) -> bool:
    """Validate metrics data against Pydantic model."""
    if verbose:
        logger.info('Validating metrics against schema model')
    try:
        validated_metrics = MetricsData(**metrics_data)
        result.metrics_count = len(validated_metrics.metrics)
        if verbose:
            logger.info('Metrics structure validated successfully')
            logger.info(f'Metrics keys: {list(validated_metrics.metrics.keys())}')
        return True
    except ValidationError as e:
        for error in e.errors():
            field_path = ' -> '.join(str(p) for p in error['loc']) if error['loc'] else 'root'
            result.errors.append(f'Pydantic validation failed at {field_path}: {error["msg"]}')
        return False
    except Exception as e:
        _fail(result, f'Unexpected Pydantic validation error: {e}')
        return False


def validate_metrics(
    input_file: str,
    definitions_file: str,
    settings: MetricsSettings,
    verbose: bool = False,
) -> ValidationResult:
    """Validate a metrics file against Pydantic model."""
    start_time = time.time()
    result = ValidationResult(is_valid=False)

    try:
        metrics_payload = _validate_file_size_and_load(input_file, verbose, result, settings.max_metrics_size)
        if metrics_payload is None:
            return result

        schema = _load_definitions_schema(definitions_file, verbose, result)
        if schema is None:
            return result

        if not _validate_json_schema(metrics_payload, schema, verbose, result):
            return result

        metrics_data = {
            'commit_sha': settings.commit_sha,
            'project_url': settings.project_url,
            'project_id': settings.project_id,
            'schema_version': settings.schema_version,
            'timestamp': datetime.utcnow().isoformat(timespec='milliseconds'),
            'metrics': metrics_payload,
        }
        if not _validate_model(metrics_data, verbose, result):
            return result

        result.is_valid = not result.errors
        result.data = metrics_data
        if verbose:
            logger.info(f'Validation completed: {result.is_valid=}')
            logger.info(f'Found {result.metrics_count} metrics')
            if result.warnings:
                logger.warning(f'Found {len(result.warnings)} warnings')

    except Exception as e:
        logger.exception('Unexpected error during validation')
        result.errors.append(f'Unexpected validation error: {e}')
    finally:
        result.validation_time = time.time() - start_time

    return result


def upload_metrics(
    input_file: str,
    definitions_file: str,
    settings: MetricsSettings,
    verbose: bool = False,
    bucket_type: BucketType | str | None = None,
    custom_bucket: str | None = None,
) -> UploadResult:
    """Upload validated metrics to the service using MinIO client."""
    start_time = time.time()
    validation_result = validate_metrics(input_file, definitions_file, settings)
    result = UploadResult(validation_result=validation_result)

    if not validation_result.is_valid:
        return result

    try:
        target_bucket = settings.get_target_bucket(bucket_type, custom_bucket)

        minio_client = MinioClient(settings)
        if not minio_client.client:
            result.upload_error = 'MinIO client not available - check S3 credentials'
            return result
        if not minio_client.bucket_exists(target_bucket):
            result.upload_error = f'Bucket {target_bucket} does not exist - check S3 configuration'
            return result
        object_name = _generate_object_name(metrics=validation_result.data)
        if verbose:
            logger.info(f'Bucket selection mode: {settings.metrics_upload_bucket_type}')
            logger.info(f'Uploading to bucket: {target_bucket}, object: {object_name}')
        minio_client.upload_json(target_bucket, object_name, validation_result.data)
        result.bytes_uploaded = len(json.dumps(validation_result.data).encode('utf-8'))
        result.upload_url = minio_client.generate_presigned_url(
            bucket=target_bucket,
            object_name=object_name,
        )
        result.upload_successful = True
        if verbose:
            logger.info(f'Upload completed: {result.upload_url} ({result.bytes_uploaded} bytes)')
    except Exception as e:
        logger.exception('Unexpected error during upload')
        result.upload_error = f'Upload failed: {e}'
    finally:
        result.upload_time = time.time() - start_time
    return result
