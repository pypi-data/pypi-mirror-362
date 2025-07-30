"""Patch for MLflow GCS Artifact Repository to handle file download errors"""

import importlib.metadata
import os
import posixpath

from mlflow.store.artifact.gcs_artifact_repo import GCSArtifactRepository
from packaging.version import Version


def _patched_download_file(self, remote_file_path, local_path):
    from google.cloud.exceptions import NotFound
    from google.resumable_media.common import DataCorruption

    (bucket, remote_root_path) = self.parse_gcs_uri(self.artifact_uri)
    remote_full_path = posixpath.join(remote_root_path, remote_file_path)
    gcs_bucket = self._get_bucket(bucket)

    try:
        gcs_bucket.blob(
            remote_full_path, chunk_size=self._GCS_DOWNLOAD_CHUNK_SIZE
        ).download_to_filename(local_path, timeout=self._GCS_DEFAULT_TIMEOUT)
    except (NotFound, DataCorruption):
        os.remove(local_path)
        raise


try:
    gcs_version = Version(importlib.metadata.version("google-cloud-storage"))
    if gcs_version < Version("3.0.0"):
        GCSArtifactRepository._download_file = _patched_download_file
except importlib.metadata.PackageNotFoundError:
    pass
