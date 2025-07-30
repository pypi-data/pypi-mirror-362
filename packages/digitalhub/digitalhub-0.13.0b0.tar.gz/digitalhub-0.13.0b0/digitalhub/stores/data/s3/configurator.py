# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from botocore.config import Config

from digitalhub.stores.credentials.configurator import Configurator
from digitalhub.stores.credentials.enums import CredsEnvVar


class S3StoreConfigurator(Configurator):
    """
    Configure the store by getting the credentials from user
    provided config or from environment.
    """

    keys = [
        CredsEnvVar.S3_ENDPOINT_URL,
        CredsEnvVar.S3_ACCESS_KEY_ID,
        CredsEnvVar.S3_SECRET_ACCESS_KEY,
        CredsEnvVar.S3_REGION,
        CredsEnvVar.S3_SIGNATURE_VERSION,
        CredsEnvVar.S3_SESSION_TOKEN,
    ]
    required_keys = [
        CredsEnvVar.S3_ENDPOINT_URL,
        CredsEnvVar.S3_ACCESS_KEY_ID,
        CredsEnvVar.S3_SECRET_ACCESS_KEY,
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

    def get_client_config(self, origin: str) -> dict:
        """
        Get S3 credentials (access key, secret key, session token and other config).

        Parameters
        ----------
        origin : str
            The origin of the credentials.

        Returns
        -------
        dict
            The credentials.
        """
        creds = self.get_credentials(origin)
        return {
            "endpoint_url": creds[CredsEnvVar.S3_ENDPOINT_URL.value],
            "aws_access_key_id": creds[CredsEnvVar.S3_ACCESS_KEY_ID.value],
            "aws_secret_access_key": creds[CredsEnvVar.S3_SECRET_ACCESS_KEY.value],
            "aws_session_token": creds[CredsEnvVar.S3_SESSION_TOKEN.value],
            "config": Config(
                region_name=creds[CredsEnvVar.S3_REGION.value],
                signature_version=creds[CredsEnvVar.S3_SIGNATURE_VERSION.value],
            ),
        }
