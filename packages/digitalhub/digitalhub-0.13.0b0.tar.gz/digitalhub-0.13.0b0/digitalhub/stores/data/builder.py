# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.stores.credentials.api import get_current_env
from digitalhub.stores.data.local.store import LocalStore
from digitalhub.stores.data.remote.store import RemoteStore
from digitalhub.stores.data.s3.configurator import S3StoreConfigurator
from digitalhub.stores.data.s3.store import S3Store
from digitalhub.stores.data.sql.configurator import SqlStoreConfigurator
from digitalhub.stores.data.sql.store import SqlStore
from digitalhub.utils.uri_utils import SchemeCategory, map_uri_scheme

if typing.TYPE_CHECKING:
    from digitalhub.stores.credentials.configurator import Configurator
    from digitalhub.stores.data._base.store import Store
    from digitalhub.utils.exceptions import StoreError


class StoreInfo:
    def __init__(self, store: Store, configurator: Configurator | None = None) -> None:
        self._store = store
        self._configurator = configurator


class StoreBuilder:
    """
    Store builder class.
    """

    def __init__(self) -> None:
        self._builders: dict[str, StoreInfo] = {}
        self._instances: dict[str, dict[str, Store]] = {}

    def register(
        self,
        store_type: str,
        store: Store,
        configurator: Configurator | None = None,
    ) -> None:
        if store_type not in self._builders:
            self._builders[store_type] = StoreInfo(store, configurator)
        else:
            raise StoreError(f"Store type {store_type} already registered")

    def get(self, uri: str) -> Store:
        """
        Get a store instance by URI, building it if necessary.

        Parameters
        ----------
        uri : str
            URI to parse.

        Returns
        -------
        Store
            The store instance.
        """
        env_profile = get_current_env()
        store_type = map_uri_scheme(uri)

        # Ensure env exists in _instances
        if env_profile not in self._instances:
            self._instances[env_profile] = {}

        # Build the store instance if not already present
        if store_type not in self._instances[env_profile]:
            store_info = self._builders[store_type]
            store_cls = store_info._store
            cfgrt_cls = store_info._configurator

            if cfgrt_cls is None:
                store = store_cls()
            else:
                store = store_cls(cfgrt_cls())
            self._instances[env_profile][store_type] = store

        return self._instances[env_profile][store_type]


store_builder = StoreBuilder()
store_builder.register(SchemeCategory.S3.value, S3Store, S3StoreConfigurator)
store_builder.register(SchemeCategory.SQL.value, SqlStore, SqlStoreConfigurator)
store_builder.register(SchemeCategory.LOCAL.value, LocalStore)
store_builder.register(SchemeCategory.REMOTE.value, RemoteStore)
