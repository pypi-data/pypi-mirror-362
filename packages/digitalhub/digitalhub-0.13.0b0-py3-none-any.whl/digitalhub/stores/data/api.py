# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.context.api import get_context
from digitalhub.stores.credentials.handler import creds_handler
from digitalhub.stores.data.builder import store_builder
from digitalhub.stores.data.enums import StoreEnv

if typing.TYPE_CHECKING:
    from digitalhub.stores.data._base.store import Store


def get_default_store(project: str) -> str:
    """
    Get default store URI.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    str
        Default store URI.
    """
    context = get_context(project)
    store = context.config.get(StoreEnv.DEFAULT_FILES_STORE.value.lower())
    if store is not None:
        return store

    store = creds_handler.load_from_env(StoreEnv.DEFAULT_FILES_STORE.value)
    if store is None:
        store = creds_handler.load_from_file(StoreEnv.DEFAULT_FILES_STORE.value)

    if store is None or store == "":
        raise ValueError(
            "No default store found. "
            "Please set a default store "
            f"in your environment (e.g. export {StoreEnv.DEFAULT_FILES_STORE.value}=) "
            "or set it in project config."
        )
    return store


def get_store(project: str, uri: str) -> Store:
    """
    Get store instance by URI.

    Parameters
    ---------
    project : str
        Project name.
    uri : str
        URI to parse.
    config : dict
        Store configuration.

    Returns
    -------
    Store
        Store instance.
    """
    return store_builder.get(uri)
