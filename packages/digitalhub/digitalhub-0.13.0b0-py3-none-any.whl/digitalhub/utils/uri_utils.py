# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import re
from enum import Enum
from urllib.parse import unquote, urlparse

from digitalhub.utils.generic_utils import list_enum


class S3Schemes(Enum):
    """
    S3 schemes.
    """

    S3 = "s3"
    S3A = "s3a"
    S3N = "s3n"
    ZIP_S3 = "zip+s3"


class LocalSchemes(Enum):
    """
    Local schemes.
    """

    LOCAL = ""


class InvalidLocalSchemes(Enum):
    """
    Local schemes.
    """

    FILE = "file"
    LOCAL = "local"


class RemoteSchemes(Enum):
    """
    Remote schemes.
    """

    HTTP = "http"
    HTTPS = "https"
    ZIP_HTTP = "zip+http"
    ZIP_HTTPS = "zip+https"


class SqlSchemes(Enum):
    """
    Sql schemes.
    """

    SQL = "sql"
    POSTGRESQL = "postgresql"


class GitSchemes(Enum):
    """
    Git schemes.
    """

    GIT = "git"
    GIT_HTTP = "git+http"
    GIT_HTTPS = "git+https"


class SchemeCategory(Enum):
    """
    Scheme types.
    """

    S3 = "s3"
    LOCAL = "local"
    REMOTE = "remote"
    SQL = "sql"
    GIT = "git"


def map_uri_scheme(uri: str) -> str:
    """
    Map an URI scheme to a common scheme.

    Parameters
    ----------
    uri : str
        URI.

    Returns
    -------
    str
        Mapped scheme type.

    Raises
    ------
    ValueError
        If the scheme is unknown or invalid.
    """
    # Check for Windows paths (e.g. C:\path\to\file or \\network\share)
    if re.match(r"^[a-zA-Z]:\\", uri) or uri.startswith(r"\\"):
        return SchemeCategory.LOCAL.value

    scheme = urlparse(uri).scheme
    if scheme in list_enum(LocalSchemes):
        return SchemeCategory.LOCAL.value
    if scheme in list_enum(InvalidLocalSchemes):
        raise ValueError("For local URI, do not use any scheme.")
    if scheme in list_enum(RemoteSchemes):
        return SchemeCategory.REMOTE.value
    if scheme in list_enum(S3Schemes):
        return SchemeCategory.S3.value
    if scheme in list_enum(SqlSchemes):
        return SchemeCategory.SQL.value
    if scheme in list_enum(GitSchemes):
        return SchemeCategory.GIT.value
    raise ValueError(f"Unknown scheme '{scheme}'!")


def has_local_scheme(uri: str) -> bool:
    """
    Check if uri is local.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is local.
    """
    return map_uri_scheme(uri) == SchemeCategory.LOCAL.value


def has_remote_scheme(uri: str) -> bool:
    """
    Check if uri is remote.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is remote.
    """
    return map_uri_scheme(uri) == SchemeCategory.REMOTE.value


def has_s3_scheme(uri: str) -> bool:
    """
    Check if uri is s3.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is s3.
    """
    return map_uri_scheme(uri) == SchemeCategory.S3.value


def has_sql_scheme(uri: str) -> bool:
    """
    Check if uri is sql.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is sql.
    """
    return map_uri_scheme(uri) == SchemeCategory.SQL.value


def has_git_scheme(uri: str) -> bool:
    """
    Check if uri is git.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is git.
    """
    return map_uri_scheme(uri) == SchemeCategory.GIT.value


def has_zip_scheme(uri: str) -> bool:
    """
    Check if uri is zip.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    bool
        True if uri is zip.
    """
    return uri.startswith("zip+")


def get_filename_from_uri(uri: str) -> str:
    """
    Get filename from uri.

    Parameters
    ----------
    uri : str
        Uri of some source.

    Returns
    -------
    str
        Filename.
    """
    return unquote(urlparse(uri).path).split("/")[-1]
