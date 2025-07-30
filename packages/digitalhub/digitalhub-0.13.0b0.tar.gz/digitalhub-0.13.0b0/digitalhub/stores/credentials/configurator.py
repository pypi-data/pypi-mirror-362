# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import abstractmethod

from digitalhub.stores.credentials.enums import CredsOrigin
from digitalhub.stores.credentials.handler import creds_handler


class Configurator:
    # Must be set in implementing class
    keys: list[str] = []
    required_keys: list[str] = []

    # Origin of the credentials
    _env = CredsOrigin.ENV.value
    _file = CredsOrigin.FILE.value

    # Credentials handler
    _creds_handler = creds_handler

    def get_credentials(self, origin: str) -> dict:
        return creds_handler.get_credentials(origin)

    @abstractmethod
    def load_configs(self) -> None:
        ...

    def _check_credentials(self, creds: dict) -> list[str]:
        missing_keys = []
        for k, v in creds.items():
            if v is None and k in self.required_keys:
                missing_keys.append(k)
        return missing_keys
