# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from requests import request

from digitalhub.stores.client.dhcore.enums import AuthType
from digitalhub.stores.credentials.configurator import Configurator
from digitalhub.stores.credentials.enums import CredsEnvVar, CredsOrigin
from digitalhub.stores.credentials.handler import creds_handler
from digitalhub.utils.exceptions import ClientError
from digitalhub.utils.generic_utils import list_enum
from digitalhub.utils.uri_utils import has_remote_scheme

if typing.TYPE_CHECKING:
    from requests import Response


class ClientDHCoreConfigurator(Configurator):
    """
    Configurator object used to configure the client.

    The configurator starts reading the credentials from the
    environment and from the ini file and stores them into the
    creds_handler object.

    While reading the credentials from the two sources (environment and file),
    the configurator evaluate if the required keys are present in both sources.
    If the required keys are not present in both sources, the configurator
    will rise an error, otherwise decide which source to use.

    Once the credentials are read, the configurator check the current profile
    name from the ini file, and set it. The default one is __default. The
    profile is used to discriminate a set of credentials inside the ini file.

    The configurator finally set the authentication type based on the credentials.
    The logic is the following:

        1. Check for a personal access token. Use it immediately to
           require a timed access token in an exchange endpoint.
           Switche then the origin to file and .
           Set the auth type to EXCHANGE.
        2. Check for an access token and a refresh token.
           Set the auth type to OAUTH2.
        3. Check for username and password.
           Set the auth type to BASIC.
        4. If none of the above is true, leave the auth type to None.
    """

    keys = [*list_enum(CredsEnvVar)]
    required_keys = [CredsEnvVar.DHCORE_ENDPOINT.value]
    keys_to_unprefix = [
        CredsEnvVar.DHCORE_REFRESH_TOKEN.value,
        CredsEnvVar.DHCORE_ACCESS_TOKEN.value,
        CredsEnvVar.DHCORE_ISSUER.value,
        CredsEnvVar.DHCORE_CLIENT_ID.value,
    ]

    def __init__(self) -> None:
        super().__init__()
        self.load_configs()
        self._origin = self.set_origin()
        self._current_profile = creds_handler.get_current_env()
        self._auth_type: str | None = None
        self.set_auth_type()

    ##############################
    # Credentials methods
    ##############################

    def load_configs(self) -> str:
        """
        Load the configuration from the environment and from the file.
        """
        self.load_env_vars()
        self.load_file_vars()

    def load_env_vars(self) -> None:
        """
        Load the credentials from the environment.
        """
        env_creds = {var: self._creds_handler.load_from_env(var) for var in self.keys}
        env_creds = self._sanitize_env_vars(env_creds)
        self._creds_handler.set_credentials(self._env, env_creds)

    def _sanitize_env_vars(self, creds: dict) -> dict:
        """
        Sanitize the env vars. We expect issuer to have the
        form "DHCORE_ISSUER" in env.

        Parameters
        ----------
        creds : dict
            Credentials dictionary.

        Returns
        -------
        dict
        """
        creds[CredsEnvVar.DHCORE_ENDPOINT.value] = self._sanitize_endpoint(creds[CredsEnvVar.DHCORE_ENDPOINT.value])
        creds[CredsEnvVar.DHCORE_ISSUER.value] = self._sanitize_endpoint(creds[CredsEnvVar.DHCORE_ISSUER.value])
        return creds

    def load_file_vars(self) -> None:
        """
        Load the credentials from the file.
        """
        keys = [*self._remove_prefix_dhcore()]
        file_creds = {var: self._creds_handler.load_from_file(var) for var in keys}

        # Because in the response there is no endpoint
        if file_creds[CredsEnvVar.DHCORE_ENDPOINT.value] is None:
            file_creds[CredsEnvVar.DHCORE_ENDPOINT.value] = self._creds_handler.load_from_env(
                CredsEnvVar.DHCORE_ENDPOINT.value
            )

        # Because in the response there is no personal access token
        if file_creds[CredsEnvVar.DHCORE_PERSONAL_ACCESS_TOKEN.value] is None:
            file_creds[CredsEnvVar.DHCORE_PERSONAL_ACCESS_TOKEN.value] = self._creds_handler.load_from_env(
                CredsEnvVar.DHCORE_PERSONAL_ACCESS_TOKEN.value
            )

        file_creds = self._sanitize_file_vars(file_creds)
        self._creds_handler.set_credentials(self._file, file_creds)

    def _sanitize_file_vars(self, creds: dict) -> dict:
        """
        Sanitize the file vars. We expect issuer, client_id and access_token and
        refresh_token to not have the form "DHCORE_" in the file.

        Parameters
        ----------
        creds : dict
            Credentials dictionary.

        Returns
        -------
        dict
        """
        creds[CredsEnvVar.DHCORE_ENDPOINT.value] = self._sanitize_endpoint(creds[CredsEnvVar.DHCORE_ENDPOINT.value])
        creds[CredsEnvVar.DHCORE_ISSUER.value] = self._sanitize_endpoint(
            creds[CredsEnvVar.DHCORE_ISSUER.value.removeprefix("DHCORE_")]
        )
        creds[CredsEnvVar.DHCORE_REFRESH_TOKEN.value] = creds[
            CredsEnvVar.DHCORE_REFRESH_TOKEN.value.removeprefix("DHCORE_")
        ]
        creds[CredsEnvVar.DHCORE_ACCESS_TOKEN.value] = creds[
            CredsEnvVar.DHCORE_ACCESS_TOKEN.value.removeprefix("DHCORE_")
        ]
        creds[CredsEnvVar.DHCORE_CLIENT_ID.value] = creds[CredsEnvVar.DHCORE_CLIENT_ID.value.removeprefix("DHCORE_")]
        return {k: v for k, v in creds.items() if k in self.keys}

    @staticmethod
    def _sanitize_endpoint(endpoint: str | None = None) -> str | None:
        """
        Sanitize the endpoint.

        Returns
        -------
        str | None
            The sanitized endpoint.
        """
        if endpoint is None:
            return
        if not has_remote_scheme(endpoint):
            raise ClientError("Invalid endpoint scheme. Must start with http:// or https://.")

        endpoint = endpoint.strip()
        return endpoint.removesuffix("/")

    def check_config(self) -> None:
        """
        Check if the config is valid.

        Parameters
        ----------
        config : dict
            Configuration dictionary.

        Returns
        -------
        None
        """
        if (current := creds_handler.get_current_env()) != self._current_profile:
            self.load_file_vars()
            self._current_profile = current

    def get_endpoint(self) -> str:
        """
        Get the DHCore endpoint.

        Returns
        -------
        str
            The endpoint.
        """
        creds = self._creds_handler.get_credentials(self._origin)
        return creds[CredsEnvVar.DHCORE_ENDPOINT.value]

    ##############################
    # Origin methods
    ##############################

    def set_origin(self) -> str:
        """
        Evaluate the default origin from the credentials.

        Returns
        -------
        str
            The origin.
        """
        origin = CredsOrigin.ENV.value

        env_creds = self._creds_handler.get_credentials(self._env)
        missing_env = self._check_credentials(env_creds)

        file_creds = self._creds_handler.get_credentials(self._file)
        missing_file = self._check_credentials(file_creds)

        msg = ""
        if missing_env:
            msg = f"Missing required vars in env: {', '.join(missing_env)}"
            origin = CredsOrigin.FILE.value
        elif missing_file:
            msg += f"Missing required vars in .dhcore.ini file: {', '.join(missing_file)}"

        if missing_env and missing_file:
            raise ClientError(msg)

        return origin

    def change_origin(self) -> None:
        """
        Change the origin of the credentials.
        """
        if self._origin == CredsOrigin.ENV.value:
            self.change_to_file()
        else:
            self.change_to_env()

        # Re-evaluate the auth type
        self.set_auth_type()

    def change_to_file(self) -> None:
        """
        Change the origin to file. Re-evaluate the auth type.
        """
        self._origin = CredsOrigin.FILE.value

    def change_to_env(self) -> None:
        """
        Change the origin to env. Re-evaluate the auth type.
        """
        self._origin = CredsOrigin.ENV.value

    ##############################
    # Auth methods
    ##############################

    def set_auth_type(self) -> None:
        """
        Evaluate the auth type from the credentials.

        Returns
        -------
        None
        """
        creds = creds_handler.get_credentials(self._origin)
        self._auth_type = self._eval_auth_type(creds)
        # If we have an exchange token, we need to get a new access token.
        # Therefore, we change the origin to file, where the refresh token is written.
        # We also try to fetch the PAT from both env and file
        if self._auth_type == AuthType.EXCHANGE.value:
            self.get_new_access_token(change_origin=True)
            # Just to ensure we get the right source from file
            self.change_to_file()

    def refreshable_auth_types(self) -> bool:
        """
        Check if the auth type is refreshable.

        Returns
        -------
        bool
            True if the auth type is refreshable, False otherwise.
        """
        return self._auth_type in [AuthType.OAUTH2.value, AuthType.EXCHANGE.value]

    def get_auth_parameters(self, kwargs: dict) -> dict:
        """
        Get the authentication header for the request.
        It is given for granted that the auth type is set and that,
        if the auth type is EXCHANGE, the refresh token is set.

        Parameters
        ----------
        kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        dict
            Authentication parameters.
        """
        creds = creds_handler.get_credentials(self._origin)
        if self._auth_type in (AuthType.EXCHANGE.value, AuthType.OAUTH2.value):
            access_token = creds[CredsEnvVar.DHCORE_ACCESS_TOKEN.value]
            if "headers" not in kwargs:
                kwargs["headers"] = {}
            kwargs["headers"]["Authorization"] = f"Bearer {access_token}"
        elif self._auth_type == AuthType.BASIC.value:
            user = creds[CredsEnvVar.DHCORE_USER.value]
            password = creds[CredsEnvVar.DHCORE_PASSWORD.value]
            kwargs["auth"] = (user, password)
        return kwargs

    def get_new_access_token(self, change_origin: bool = False) -> None:
        """
        Get a new access token.

        Parameters
        ----------
        change_origin : bool, optional
            Whether to change the origin of the credentials, by default False

        Returns
        -------
        None
        """
        if not self.refreshable_auth_types():
            raise ClientError(f"Auth type {self._auth_type} does not support refresh.")

        # Get refresh endpoint
        url = self._get_refresh_endpoint()

        # Get credentials
        creds = self._creds_handler.get_credentials(self._origin)

        # Get client id
        if (client_id := creds.get(CredsEnvVar.DHCORE_CLIENT_ID.value)) is None:
            raise ClientError("Client id not set.")

        # Handling of token exchange or refresh
        if self._auth_type == AuthType.OAUTH2.value:
            response = self._call_refresh_token_endpoint(
                url,
                client_id=client_id,
                refresh_token=creds.get(CredsEnvVar.DHCORE_REFRESH_TOKEN.value),
                grant_type="refresh_token",
                scope="credentials",
            )
        elif self._auth_type == AuthType.EXCHANGE.value:
            response = self._call_refresh_token_endpoint(
                url,
                client_id=client_id,
                subject_token=creds.get(CredsEnvVar.DHCORE_PERSONAL_ACCESS_TOKEN.value),
                subject_token_type="urn:ietf:params:oauth:token-type:pat",
                grant_type="urn:ietf:params:oauth:grant-type:token-exchange",
                scope="credentials",
            )

        # Change origin of creds if needed
        if response.status_code in (400, 401, 403):
            if not change_origin:
                raise ClientError("Unable to refresh token. Please check your credentials.")
            self.change_origin()
            self.get_new_access_token(change_origin=False)

        response.raise_for_status()

        # Read new credentials and propagate to config file
        self._export_new_creds(response.json())

    def _export_new_creds(self, response: dict) -> None:
        """
        Set new credentials.

        Parameters
        ----------
        response : dict
            Response from refresh token endpoint.

        Returns
        -------
        None
        """
        creds_handler.write_env(response)
        self.load_file_vars()

        # Change current origin to file because of refresh
        self._origin = CredsOrigin.FILE.value

    def _remove_prefix_dhcore(self) -> list[str]:
        """
        Remove prefix from selected keys. (Compatibility with CLI)

        Parameters
        ----------
        keys : list[str]
            List of keys.

        Returns
        -------
        list[str]
            List of keys without prefix.
        """
        new_list = []
        for key in self.keys:
            if key in self.keys_to_unprefix:
                new_list.append(key.removeprefix("DHCORE_"))
            else:
                new_list.append(key)
        return new_list

    def _get_refresh_endpoint(self) -> str:
        """
        Get the refresh endpoint.

        Returns
        -------
        str
            Refresh endpoint.
        """
        # Get issuer endpoint
        creds = self._creds_handler.get_credentials(self._origin)
        endpoint_issuer = creds.get(CredsEnvVar.DHCORE_ISSUER.value)
        if endpoint_issuer is None:
            raise ClientError("Issuer endpoint not set.")

        # Standard issuer endpoint path
        url = endpoint_issuer + "/.well-known/openid-configuration"

        # Call issuer to get refresh endpoint
        r = request("GET", url, timeout=60)
        r.raise_for_status()
        return r.json().get("token_endpoint")

    def _call_refresh_token_endpoint(
        self,
        url: str,
        **kwargs,
    ) -> Response:
        """
        Call the refresh token endpoint.

        Parameters
        ----------
        url : str
            Refresh token endpoint.
        kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        Response
            Response object.
        """
        # Send request to get new access token
        payload = {**kwargs}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return request("POST", url, data=payload, headers=headers, timeout=60)

    def _eval_auth_type(self, creds: dict) -> str | None:
        if creds[CredsEnvVar.DHCORE_PERSONAL_ACCESS_TOKEN.value] is not None:
            return AuthType.EXCHANGE.value
        if (
            creds[CredsEnvVar.DHCORE_ACCESS_TOKEN.value] is not None
            and creds[CredsEnvVar.DHCORE_REFRESH_TOKEN.value] is not None
        ):
            return AuthType.OAUTH2.value
        if creds[CredsEnvVar.DHCORE_USER.value] is not None and creds[CredsEnvVar.DHCORE_PASSWORD.value] is not None:
            return AuthType.BASIC.value
        return None
