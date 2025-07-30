# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from boto3 import client as boto3_client

from digitalhub.stores.credentials.enums import CredsOrigin
from digitalhub.stores.data.s3.configurator import S3StoreConfigurator
from digitalhub.utils.exceptions import StoreError


def get_bucket_name(path: str) -> str:
    """
    Get bucket name from path.

    Parameters
    ----------
    path : str
        The source path to get the key from.

    Returns
    -------
    str
        The bucket name.
    """
    return urlparse(path).netloc


def get_bucket_and_key(path: str) -> tuple[str, str]:
    """
    Get bucket and key from path.

    Parameters
    ----------
    path : str
        The source path to get the key from.

    Returns
    -------
    tuple[str, str]
        The bucket and key.
    """
    parsed = urlparse(path)
    return parsed.netloc, parsed.path


def get_s3_source(bucket: str, key: str, filename: Path) -> None:
    """
    Get S3 source.

    Parameters
    ----------
    bucket : str
        S3 bucket name.
    key : str
        S3 object key.
    filename : Path
        Path where to save the function source.

    Returns
    -------
    None
    """
    # Try to get client from environment variables
    try:
        cfg = S3StoreConfigurator().get_boto3_client_config(CredsOrigin.ENV.value)
        s3 = boto3_client("s3", **cfg)
        s3.download_file(bucket, key, filename)

    # Fallback to file
    except StoreError:
        cfg = S3StoreConfigurator().get_boto3_client_config(CredsOrigin.FILE.value)
        s3.download_file(bucket, key, filename)
