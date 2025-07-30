# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.credentials.handler import creds_handler


def set_current_env(environment: str) -> None:
    """
    Set the current credentials set.

    Parameters
    ----------
    environment : str
        Credentials set name.

    Returns
    -------
    None
    """
    creds_handler.set_current_env(environment)


def get_current_env() -> str:
    """
    Get the current credentials set.

    Returns
    -------
    str
        Credentials set name.
    """
    return creds_handler.get_current_env()
