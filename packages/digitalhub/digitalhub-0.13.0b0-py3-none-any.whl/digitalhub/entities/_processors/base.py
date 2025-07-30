# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.context.api import delete_context
from digitalhub.entities._commons.enums import ApiCategories, BackendOperations
from digitalhub.factory.factory import factory
from digitalhub.stores.client.api import get_client
from digitalhub.utils.exceptions import EntityAlreadyExistsError, EntityError, EntityNotExistsError
from digitalhub.utils.io_utils import read_yaml

if typing.TYPE_CHECKING:
    from digitalhub.entities.project._base.entity import Project
    from digitalhub.stores.client._base.client import Client


class BaseEntityOperationsProcessor:
    """
    Processor for Base Entity operations.

    This object interacts with the context, check the category of the object,
    and then calls the appropriate method to perform the requested operation.
    Operations can be CRUD, search, list, etc.
    """

    ##############################
    # CRUD base entity
    ##############################

    def _create_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Create object in backend.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.CREATE.value,
            entity_type=entity_type,
        )
        return client.create_object(api, entity_dict, **kwargs)

    def create_project_entity(
        self,
        _entity: Project | None = None,
        **kwargs,
    ) -> Project:
        """
        Create object in backend.

        Parameters
        ----------
        _entity : Project
            Object instance.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        Project
            Object instance.
        """
        if _entity is not None:
            client = _entity._client
            obj = _entity
        else:
            client = get_client(kwargs.get("local"))
            obj = factory.build_entity_from_params(**kwargs)
        ent = self._create_base_entity(client, obj.ENTITY_TYPE, obj.to_dict())
        ent["local"] = client.is_local()
        return factory.build_entity_from_dict(ent)

    def _read_base_entity(
        self,
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

    def read_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> Project:
        """
        Read object from backend.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        Project
            Object instance.
        """
        client = get_client(kwargs.pop("local", False))
        obj = self._read_base_entity(client, entity_type, entity_name, **kwargs)
        obj["local"] = client.is_local()
        return factory.build_entity_from_dict(obj)

    def import_project_entity(
        self,
        file: str,
        **kwargs,
    ) -> Project:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        Project
            Object instance.
        """
        client = get_client(kwargs.pop("local", False))
        obj: dict = read_yaml(file)
        obj["status"] = {}
        obj["local"] = client.is_local()
        ent: Project = factory.build_entity_from_dict(obj)

        try:
            self._create_base_entity(ent._client, ent.ENTITY_TYPE, ent.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {ent.name} already exists. If you want to update it, use load instead.")

        # Import related entities
        ent._import_entities(obj)
        ent.refresh()
        return ent

    def load_project_entity(
        self,
        file: str,
        **kwargs,
    ) -> Project:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        Project
            Object instance.
        """
        client = get_client(kwargs.pop("local", False))
        obj: dict = read_yaml(file)
        obj["local"] = client.is_local()
        ent: Project = factory.build_entity_from_dict(obj)

        try:
            self._update_base_entity(ent._client, ent.ENTITY_TYPE, ent.name, ent.to_dict())
        except EntityNotExistsError:
            self._create_base_entity(ent._client, ent.ENTITY_TYPE, ent.to_dict())

        # Load related entities
        ent._load_entities(obj)
        ent.refresh()
        return ent

    def _list_base_entities(
        self,
        client: Client,
        entity_type: str,
        **kwargs,
    ) -> list[dict]:
        """
        List objects from backend.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.LIST.value,
            entity_type=entity_type,
        )
        return client.list_objects(api, **kwargs)

    def list_project_entities(
        self,
        entity_type: str,
        **kwargs,
    ) -> list[Project]:
        """
        List objects from backend.

        Parameters
        ----------
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to API call.

        Returns
        -------
        list[Project]
            List of objects.
        """
        client = get_client(kwargs.pop("local", False))
        objs = self._list_base_entities(client, entity_type, **kwargs)
        entities = []
        for obj in objs:
            obj["local"] = client.is_local()
            ent = factory.build_entity_from_dict(obj)
            entities.append(ent)
        return entities

    def _update_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_name: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Update object method.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.UPDATE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        return client.update_object(api, entity_dict, **kwargs)

    def update_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        entity_dict: dict,
        **kwargs,
    ) -> Project:
        """
        Update object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        entity_dict : dict
            Object instance.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        Project
            Object instance.
        """
        client = get_client(kwargs.pop("local", False))
        obj = self._update_base_entity(client, entity_type, entity_name, entity_dict, **kwargs)
        obj["local"] = client.is_local()
        return factory.build_entity_from_dict(obj)

    def _delete_base_entity(
        self,
        client: Client,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> dict:
        """
        Delete object method.

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
            Response from backend.
        """
        kwargs = client.build_parameters(
            ApiCategories.BASE.value,
            BackendOperations.DELETE.value,
            **kwargs,
        )
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.DELETE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )
        return client.delete_object(api, **kwargs)

    def delete_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> dict:
        """
        Delete object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        dict
            Response from backend.
        """
        if kwargs.pop("clean_context", True):
            delete_context(entity_name)
        client = get_client(kwargs.pop("local", False))
        return self._delete_base_entity(
            client,
            entity_type,
            entity_name,
            **kwargs,
        )

    ##############################
    # Base entity operations
    ##############################

    def _build_base_entity_key(
        self,
        client: Client,
        entity_id: str,
    ) -> str:
        """
        Build object key.

        Parameters
        ----------
        client : Client
            Client instance.
        entity_id : str
            Entity ID.

        Returns
        -------
        str
            Object key.
        """
        return client.build_key(ApiCategories.BASE.value, entity_id)

    def build_project_key(
        self,
        entity_id: str,
        **kwargs,
    ) -> str:
        """
        Build object key.

        Parameters
        ----------
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        str
            Object key.
        """
        client = get_client(kwargs.pop("local", False))
        return self._build_base_entity_key(client, entity_id)

    def share_project_entity(
        self,
        entity_type: str,
        entity_name: str,
        **kwargs,
    ) -> None:
        """
        Share object method.

        Parameters
        ----------
        entity_type : str
            Entity type.
        entity_name : str
            Entity name.
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        None
        """
        client = get_client(kwargs.pop("local", False))
        api = client.build_api(
            ApiCategories.BASE.value,
            BackendOperations.SHARE.value,
            entity_type=entity_type,
            entity_name=entity_name,
        )

        user = kwargs.pop("user", None)
        if unshare := kwargs.pop("unshare", False):
            users = client.read_object(api, **kwargs)
            for u in users:
                if u["user"] == user:
                    kwargs["id"] = u["id"]
                break
            else:
                raise ValueError(f"User '{user}' does not have access to project.")

        kwargs = client.build_parameters(
            ApiCategories.BASE.value,
            BackendOperations.SHARE.value,
            unshare=unshare,
            user=user,
            **kwargs,
        )
        if unshare:
            client.delete_object(api, **kwargs)
            return
        client.create_object(api, obj={}, **kwargs)


base_processor = BaseEntityOperationsProcessor()
