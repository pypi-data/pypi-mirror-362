# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os
import shutil
import warnings
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

try:
    from git import Repo
except ImportError as e:
    if "Bad git executable." in e.args[0]:
        warnings.warn("git is not installed. Please install git and try again.", RuntimeWarning)


class GitCredentialsType(Enum):
    """
    Supported git credentials types.
    """

    USERNAME = "GIT_USERNAME"
    PASSWORD = "GIT_PASSWORD"
    TOKEN = "GIT_TOKEN"


def clone_repository(path: Path, url: str) -> None:
    """
    Clone git repository.

    Parameters
    ----------
    path : Path
        Path where to save the repository.
    url : str
        URL of the repository.

    Returns
    -------
    None
    """
    clean_path(path)
    checkout_object = get_checkout_object(url)
    url = add_credentials_git_remote_url(url)
    repo = clone_from_url(url, path)
    if checkout_object != "":
        repo.git.checkout(checkout_object)


def get_checkout_object(url: str) -> str:
    """
    Get checkout object from url fragment.

    Parameters
    ----------
    url : str
        URL of the repository.

    Returns
    -------
    str
        Checkout object (branch, tag, commit).
    """
    return urlparse(url).fragment


def clean_path(path: Path) -> None:
    """
    Clean path from any files.

    Parameters
    ----------
    path : Path

    Returns
    -------
    None
    """

    shutil.rmtree(path, ignore_errors=True)


def get_git_username_password_from_token(token: str) -> tuple[str, str]:
    """
    Parse token to get username and password. The token
    can be one of the following:

    - GitHub/GitLab personal access token (github_pat_.../glpat...)
    - GitHub/GitLab access token
    - Other generic token

    Parameters
    ----------
    token : str
        Token to parse.

    Returns
    -------
    tuple[str, str]
        Username and password.
    """
    # Mutued from mlrun
    if token.startswith("github_pat_") or token.startswith("glpat"):
        return "oauth2", token
    return token, "x-oauth-basic"


def add_credentials_git_remote_url(url: str) -> str:
    """
    Add credentials to git remote url.

    Parameters
    ----------
    url : str
        URL of the repository.

    Returns
    -------
    str
        URL with credentials.
    """
    url_obj = urlparse(url)

    # Get credentials from environment variables
    username = os.getenv(GitCredentialsType.USERNAME.value)
    password = os.getenv(GitCredentialsType.PASSWORD.value)
    token = os.getenv(GitCredentialsType.TOKEN.value)

    # Get credentials from token. Override username and password
    if token is not None:
        username, password = get_git_username_password_from_token(token)

    # Add credentials to url if needed
    if username is not None and password is not None:
        return f"https://{username}:{password}@{url_obj.hostname}{url_obj.path}"
    return f"https://{url_obj.hostname}{url_obj.path}"


def clone_from_url(url: str, path: Path) -> Repo:
    """
    Clone repository from url. Wraps git.Repo.clone_from.

    Parameters
    ----------
    url : str
        HTTP(S) URL of the repository.
    path : Path
        Path where to save the repository.

    Returns
    -------
    Repo
        Cloned repository.
    """
    return Repo.clone_from(url=url, to_path=path)
