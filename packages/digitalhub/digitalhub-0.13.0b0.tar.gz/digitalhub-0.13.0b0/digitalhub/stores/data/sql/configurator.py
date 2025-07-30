# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.stores.credentials.configurator import Configurator
from digitalhub.stores.credentials.enums import CredsEnvVar


class SqlStoreConfigurator(Configurator):
    """
    Configure the store by getting the credentials from user
    provided config or from environment.
    """

    keys = [
        CredsEnvVar.DB_USERNAME,
        CredsEnvVar.DB_PASSWORD,
        CredsEnvVar.DB_HOST,
        CredsEnvVar.DB_PORT,
        CredsEnvVar.DB_DATABASE,
    ]
    required_keys = [
        CredsEnvVar.DB_USERNAME,
        CredsEnvVar.DB_PASSWORD,
        CredsEnvVar.DB_HOST,
        CredsEnvVar.DB_PORT,
        CredsEnvVar.DB_DATABASE,
    ]

    def __init__(self):
        super().__init__()
        self.load_configs()

    ##############################
    # Configuration methods
    ##############################

    def load_configs(self) -> None:
        # Load from env
        env_creds = {var.value: self._creds_handler.load_from_env(var.value) for var in self.keys}
        self._creds_handler.set_credentials(self._env, env_creds)

        # Load from file
        file_creds = {var.value: self._creds_handler.load_from_file(var.value) for var in self.keys}
        self._creds_handler.set_credentials(self._file, file_creds)

    def get_sql_conn_string(self, origin: str) -> str:
        """
        Get the connection string from environment variables.

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        str
            The connection string.
        """
        creds = self.get_credentials(origin)
        user = creds[CredsEnvVar.DB_USERNAME.value]
        password = creds[CredsEnvVar.DB_PASSWORD.value]
        host = creds[CredsEnvVar.DB_HOST.value]
        port = creds[CredsEnvVar.DB_PORT.value]
        database = creds[CredsEnvVar.DB_DATABASE.value]
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
