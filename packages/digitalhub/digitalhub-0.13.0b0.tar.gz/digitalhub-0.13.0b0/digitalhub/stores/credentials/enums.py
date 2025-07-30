# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class CredsOrigin(Enum):
    """
    List credential origins.
    """

    ENV = "env"
    FILE = "file"


class SetCreds(Enum):
    """
    List supported environments.
    """

    DEFAULT = "__default"
    DH_ENV = "DH_NAME"


class CredsEnvVar(Enum):
    # S3
    S3_ENDPOINT_URL = "AWS_ENDPOINT_URL"
    S3_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
    S3_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
    S3_SESSION_TOKEN = "AWS_SESSION_TOKEN"
    S3_REGION = "AWS_REGION"
    S3_SIGNATURE_VERSION = "S3_SIGNATURE_VERSION"

    # SQL
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    DB_USERNAME = "DB_USERNAME"
    DB_PASSWORD = "DB_PASSWORD"
    DB_DATABASE = "DB_DATABASE"
    DB_PG_SCHEMA = "DB_SCHEMA"

    # DHCORE
    DHCORE_ENDPOINT = "DHCORE_ENDPOINT"
    DHCORE_ISSUER = "DHCORE_ISSUER"
    DHCORE_USER = "DHCORE_USER"
    DHCORE_PASSWORD = "DHCORE_PASSWORD"
    DHCORE_CLIENT_ID = "DHCORE_CLIENT_ID"
    DHCORE_ACCESS_TOKEN = "DHCORE_ACCESS_TOKEN"
    DHCORE_REFRESH_TOKEN = "DHCORE_REFRESH_TOKEN"
    DHCORE_PERSONAL_ACCESS_TOKEN = "DHCORE_PERSONAL_ACCESS_TOKEN"
    DHCORE_WORKFLOW_IMAGE = "DHCORE_WORKFLOW_IMAGE"
