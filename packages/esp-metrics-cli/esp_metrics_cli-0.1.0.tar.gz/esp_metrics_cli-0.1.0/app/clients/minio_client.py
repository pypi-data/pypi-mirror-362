# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0

import json
import logging
import time
import typing as t

from datetime import timedelta
from io import BytesIO

import minio
import urllib3

from minio import Minio

from app.models.config import MetricsSettings

logger = logging.getLogger(__name__)


class MinioError(Exception):
    """Exception raised for Minio-related errors."""


class MinioClient:
    """Minio client for S3-compatible storage operations."""

    def __init__(self, settings: MetricsSettings | None = None):
        self.settings = settings or MetricsSettings()
        self._client: Minio | None = None

    @property
    def client(self) -> Minio | None:
        """Get or create the Minio client."""
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> Minio | None:
        """Create a new Minio client instance."""
        if not all(
            [
                self.settings.s3_server,
                self.settings.s3_access_key,
                self.settings.s3_secret_key,
            ]
        ):
            logger.info('S3 credentials not available. Make sure you setup env config. Skipping S3 features...')
            return None

        if self.settings.s3_server.startswith('https://'):  # type: ignore
            host = self.settings.s3_server.replace('https://', '')  # type: ignore
            secure = True
        elif self.settings.s3_server.startswith('http://'):  # type: ignore
            host = self.settings.s3_server.replace('http://', '')  # type: ignore
            secure = False
        else:
            raise ValueError('Please provide a http or https server URL for S3')

        return minio.Minio(
            host,
            access_key=self.settings.s3_access_key,
            secret_key=self.settings.s3_secret_key,
            secure=secure,
            http_client=urllib3.PoolManager(
                num_pools=10,
                timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
                retries=urllib3.Retry(
                    total=5,
                    backoff_factor=0.2,
                    status_forcelist=[500, 502, 503, 504],
                ),
            ),
        )

    def generate_presigned_url(
        self,
        *,
        bucket: str,
        object_name: str,
        expire_in_days: int = 7,
    ) -> t.Any:
        """Generate a presigned URL for a single object in S3 storage."""
        if not self.client:
            raise MinioError('S3 client not available')

        url = self.client.get_presigned_url(
            'GET',
            bucket_name=bucket,
            object_name=object_name,
            expires=timedelta(days=expire_in_days),
        )
        if not url:
            raise MinioError(f'Failed to generate presigned URL for {object_name}')

        return url

    def upload_json(self, bucket: str, object_name: str, data: dict[str, t.Any]) -> None:
        """Upload JSON data to S3 storage with retry logic."""
        if not self.client:
            raise MinioError('S3 client not available')

        json_data = json.dumps(data, indent=2).encode('utf-8')

        for attempt in range(self.settings.upload_retries + 1):
            try:
                data_stream = BytesIO(json_data)

                self.client.put_object(
                    bucket_name=bucket,
                    object_name=object_name,
                    data=data_stream,
                    length=len(json_data),
                    content_type='application/json',
                )

                logger.info(f'Uploaded JSON data to {bucket}/{object_name}')
                return

            except Exception as e:
                if attempt < self.settings.upload_retries:
                    logger.warning(
                        f'Upload attempt {attempt + 1} failed for {bucket}/{object_name}: {e}. '
                        f'Retrying in {self.settings.upload_retry_delay} seconds...'
                    )
                    time.sleep(self.settings.upload_retry_delay)
                else:
                    logger.error(
                        f'Upload failed after {self.settings.upload_retries + 1} attempts '
                        f'for {bucket}/{object_name}: {e}'
                    )
                    raise

    def bucket_exists(self, bucket: str) -> t.Any:
        """Check if bucket exists."""
        if not self.client:
            return False

        try:
            return self.client.bucket_exists(bucket)
        except Exception as e:
            logger.error(f'Error checking bucket existence: {e}')
            return False
