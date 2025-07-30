# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from requests.exceptions import HTTPError, RequestException

from digitalhub.utils.exceptions import (
    BackendError,
    BadRequestError,
    EntityAlreadyExistsError,
    EntityNotExistsError,
    ForbiddenError,
    MissingSpecError,
    UnauthorizedError,
)

if typing.TYPE_CHECKING:
    from requests import Response


class ErrorParser:
    @staticmethod
    def parse(response: Response) -> None:
        """
        Handle DHCore API errors.

        Parameters
        ----------
        response : Response
            The response object.

        Returns
        -------
        None
        """
        try:
            response.raise_for_status()

        # Backend errors
        except RequestException as e:
            # Handle timeout
            if isinstance(e, TimeoutError):
                msg = "Request to DHCore backend timed out."
                raise TimeoutError(msg)

            # Handle connection error
            elif isinstance(e, ConnectionError):
                msg = "Unable to connect to DHCore backend."
                raise ConnectionError(msg)

            # Handle HTTP errors
            elif isinstance(e, HTTPError):
                txt_resp = f"Response: {response.text}."

                # Bad request
                if response.status_code == 400:
                    # Missing spec in backend
                    if "missing spec" in response.text:
                        msg = f"Missing spec in backend. {txt_resp}"
                        raise MissingSpecError(msg)

                    # Duplicated entity
                    elif "Duplicated entity" in response.text:
                        msg = f"Entity already exists. {txt_resp}"
                        raise EntityAlreadyExistsError(msg)

                    # Other errors
                    else:
                        msg = f"Bad request. {txt_resp}"
                        raise BadRequestError(msg)

                # Unauthorized errors
                elif response.status_code == 401:
                    msg = f"Unauthorized. {txt_resp}"
                    raise UnauthorizedError(msg)

                # Forbidden errors
                elif response.status_code == 403:
                    msg = f"Forbidden. {txt_resp}"
                    raise ForbiddenError(msg)

                # Entity not found
                elif response.status_code == 404:
                    # Put with entity not found
                    if "No such EntityName" in response.text:
                        msg = f"Entity does not exists. {txt_resp}"
                        raise EntityNotExistsError(msg)

                    # Other cases
                    else:
                        msg = f"Not found. {txt_resp}"
                        raise BackendError(msg)

                # Other errors
                else:
                    msg = f"Backend error. {txt_resp}"
                    raise BackendError(msg) from e

            # Other requests errors
            else:
                msg = f"Some error occurred. {e}"
                raise BackendError(msg) from e

        # Other generic errors
        except Exception as e:
            msg = f"Some error occurred: {e}"
            raise RuntimeError(msg) from e
