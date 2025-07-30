# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.context.api import get_context
from digitalhub.entities._commons.enums import ApiCategories, BackendOperations, EntityTypes
from digitalhub.entities._commons.utils import get_project_from_key, parse_entity_key
from digitalhub.factory.factory import factory
from digitalhub.stores.client.api import get_client
from digitalhub.utils.exceptions import ContextError, EntityError, EntityNotExistsError

if typing.TYPE_CHECKING:
    from digitalhub.context.context import Context
    from digitalhub.stores.client._base.client import Client


def parse_identifier(
    identifier: str,
    project: str | None = None,
    entity_type: str | None = None,
    entity_kind: str | None = None,
    entity_id: str | None = None,
) -> tuple[str, str, str | None, str | None, str | None]:
    """
    Parse entity identifier.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    project : str
        Project name.
    entity_type : str
        Entity type.
    entity_id : str
        Entity ID.

    Returns
    -------
    tuple[str, str, str | None, str | None, str | None]
        Project name, entity type, entity kind, entity name, entity ID.
    """
    if not identifier.startswith("store://"):
        if project is None or entity_type is None:
            raise ValueError("Project and entity type must be specified.")
        return project, entity_type, entity_kind, identifier, entity_id
    return parse_entity_key(identifier)


def get_context_from_identifier(
    identifier: str,
    project: str | None = None,
) -> Context:
    """
    Get context from project.

    Parameters
    ----------
    identifier : str
        Entity key (store://...) or entity name.
    project : str
        Project name.

    Returns
    -------
    Context
        Context.
    """
    if not identifier.startswith("store://"):
        if project is None:
            raise EntityError("Specify project if you do not specify entity key.")
    else:
        project = get_project_from_key(identifier)

    return get_context_from_project(project)


def get_context_from_project(
    project: str,
) -> Context:
    """
    Check if the given project is in the context.
    Otherwise try to get the project from remote.
    Finally return the client.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    Context
        Context.
    """
    try:
        return get_context(project)
    except ContextError:
        return get_context_from_remote(project)


def get_context_from_remote(
    project: str,
) -> Client:
    """
    Get context from remote.

    Parameters
    ----------
    project : str
        Project name.

    Returns
    -------
    Client
        Client.
    """
    try:
        client = get_client()
        obj = _read_base_entity(client, EntityTypes.PROJECT.value, project)
        factory.build_entity_from_dict(obj)
        return get_context(project)
    except EntityNotExistsError:
        raise ContextError(f"Project '{project}' not found.")


def _read_base_entity(
    client: Client,
    entity_type: str,
    entity_name: str,
    **kwargs,
) -> dict:
    """
    Read object from backend.

    Parameters
    ----------
    client : Client
        Client instance.
    entity_type : str
        Entity type.
    entity_name : str
        Entity name.
    **kwargs : dict
        Parameters to pass to the API call.

    Returns
    -------
    dict
        Object instance.
    """
    api = client.build_api(
        ApiCategories.BASE.value,
        BackendOperations.READ.value,
        entity_type=entity_type,
        entity_name=entity_name,
    )
    return client.read_object(api, **kwargs)
