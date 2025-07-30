# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import os

from digitalhub.stores.credentials.enums import SetCreds
from digitalhub.stores.credentials.ini_module import load_from_file, read_env_from_file, set_current_env, write_config
from digitalhub.stores.credentials.store import CredentialsStore


class CredentialHandler:
    """
    Configurator object used to configure clients and store credentials.
    """

    def __init__(self) -> None:
        # Store
        self._creds_store = CredentialsStore()

        # Current credentials set (__default by default)
        self._environment = os.getenv(SetCreds.DH_ENV.value, SetCreds.DEFAULT.value)

    ##############################
    # Public methods
    ##############################

    def set_current_env(self, creds_set: str) -> None:
        """
        Set the current credentials set.

        Parameters
        ----------
        creds_set : str
            Credentials set name.

        Returns
        -------
        None
        """
        self._environment = creds_set
        set_current_env(creds_set)

    def get_current_env(self) -> str:
        """
        Get the current credentials set.

        Returns
        -------
        str
            Credentials set name.
        """
        return self._environment

    def load_from_env(self, var: str) -> str | None:
        """
        Load variable from env.

        Parameters
        ----------
        var : str
            Environment variable name.

        Returns
        -------
        str | None
            Environment variable value.
        """
        env_var = os.getenv(var)
        if env_var != "":
            return env_var

    def load_from_file(self, var: str) -> str | None:
        """
        Load variable from config file.

        Parameters
        ----------
        var : str
            Environment variable name.

        Returns
        -------
        str | None
            Environment variable value.
        """
        env_from_file = read_env_from_file()
        if env_from_file is not None:
            self._environment = env_from_file
        return load_from_file(var)

    def write_env(self, creds: dict) -> None:
        """
        Write the env variables to the .dhcore file.

        Parameters
        ----------
        creds : dict
            Credentials.

        Returns
        -------
        None
        """
        write_config(creds, self._environment)

    ##############################
    # Credentials store methods
    ##############################

    def set_credentials(self, origin: str, creds: dict) -> None:
        """
        Set credentials.

        Parameters
        ----------
        origin : str
            The origin of the credentials.
        creds : dict
            The credentials.

        Returns
        -------
        None
        """
        self._creds_store.set_credentials(self._environment, origin, creds)

    def get_credentials(self, origin: str) -> dict:
        """
        Get credentials from origin.

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        dict
            The credentials.
        """
        return self._creds_store.get_credentials(self._environment, origin)


# Define global configurator
creds_handler = CredentialHandler()
