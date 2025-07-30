# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing
from typing import Any

from digitalhub.entities._commons.enums import ApiCategories, BackendOperations, Relationship, State
from digitalhub.entities._processors.utils import (
    get_context_from_identifier,
    get_context_from_project,
    parse_identifier,
)
from digitalhub.factory.factory import factory
from digitalhub.utils.exceptions import EntityAlreadyExistsError, EntityError, EntityNotExistsError
from digitalhub.utils.io_utils import read_yaml
from digitalhub.utils.types import SourcesOrListOfSources

if typing.TYPE_CHECKING:
    from digitalhub.context.context import Context
    from digitalhub.entities._base.context.entity import ContextEntity
    from digitalhub.entities._base.executable.entity import ExecutableEntity
    from digitalhub.entities._base.material.entity import MaterialEntity
    from digitalhub.entities._base.unversioned.entity import UnversionedEntity


class ContextEntityOperationsProcessor:
    """
    Processor for Entity operations.

    This object interacts with the context, check the category of the object,
    and then calls the appropriate method to perform the requested operation.
    Operations can be CRUD, search, list, etc.
    """

    ##############################
    # CRUD context entity
    ##############################

    def _create_context_entity(
        self,
        context: Context,
        entity_type: str,
        entity_dict: dict,
    ) -> dict:
        """
        Create object in backend.

        Parameters
        ----------
        context : Context
            Context instance.
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_dict : dict
            Object instance.

        Returns
        -------
        dict
            Object instance.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.CREATE.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.create_object(api, entity_dict)

    def create_context_entity(
        self,
        _entity: ContextEntity | None = None,
        **kwargs,
    ) -> ContextEntity:
        """
        Create object in backend.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        if _entity is not None:
            context = _entity._context()
            obj = _entity
        else:
            context = get_context_from_project(kwargs["project"])
            obj: ContextEntity = factory.build_entity_from_params(**kwargs)
        new_obj = self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        return factory.build_entity_from_dict(new_obj)

    def log_material_entity(
        self,
        **kwargs,
    ) -> MaterialEntity:
        """
        Create object in backend and upload file.

        Parameters
        ----------
        **kwargs : dict
            Parameters to pass to entity builder.

        Returns
        -------
        MaterialEntity
            Object instance.
        """
        source: SourcesOrListOfSources = kwargs.pop("source")
        context = get_context_from_project(kwargs["project"])
        obj = factory.build_entity_from_params(**kwargs)
        if context.is_running:
            obj.add_relationship(Relationship.PRODUCEDBY.value, context.get_run_ctx())

        new_obj: MaterialEntity = self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        new_obj = factory.build_entity_from_dict(new_obj)

        new_obj.status.state = State.UPLOADING.value
        new_obj = self._update_material_entity(new_obj)

        # Handle file upload
        try:
            new_obj.upload(source)
            uploaded = True
            msg = None
        except Exception as e:
            uploaded = False
            msg = str(e.args)

        new_obj.status.message = msg

        # Update status after upload
        if uploaded:
            new_obj.status.state = State.READY.value
            new_obj = self._update_material_entity(new_obj)
        else:
            new_obj.status.state = State.ERROR.value
            new_obj = self._update_material_entity(new_obj)
            raise EntityError(msg)

        return new_obj

    def _read_context_entity(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Read object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Object instance.
        """
        project, entity_type, _, entity_name, entity_id = parse_identifier(
            identifier,
            project=project,
            entity_type=entity_type,
            entity_id=entity_id,
        )

        if entity_id is None:
            kwargs["entity_name"] = entity_name
        kwargs = context.client.build_parameters(
            ApiCategories.CONTEXT.value,
            BackendOperations.READ.value,
            **kwargs,
        )

        if entity_id is None:
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.LIST.value,
                project=context.name,
                entity_type=entity_type,
            )
            return context.client.list_first_object(api, **kwargs)

        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.READ.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def read_context_entity(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> ContextEntity:
        """
        Read object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        VersionedEntity
            Object instance.
        """
        context = get_context_from_identifier(identifier, project)
        obj = self._read_context_entity(
            context,
            identifier,
            entity_type=entity_type,
            project=project,
            entity_id=entity_id,
            **kwargs,
        )
        entity = factory.build_entity_from_dict(obj)
        return self._post_process_get(entity)

    def read_unversioned_entity(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> UnversionedEntity:
        """
        Read object from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        UnversionedEntity
            Object instance.
        """
        if not identifier.startswith("store://"):
            entity_id = identifier
        else:
            splt = identifier.split(":")
            if len(splt) == 3:
                identifier = f"{splt[0]}:{splt[1]}"
        return self.read_context_entity(
            identifier,
            entity_type=entity_type,
            project=project,
            entity_id=entity_id,
            **kwargs,
        )

    def import_context_entity(
        self,
        file: str,
    ) -> ContextEntity:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        dict_obj: dict = read_yaml(file)
        dict_obj["status"] = {}
        context = get_context_from_project(dict_obj["project"])
        obj = factory.build_entity_from_dict(dict_obj)
        try:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")
        return obj

    def import_executable_entity(
        self,
        file: str,
    ) -> ExecutableEntity:
        """
        Import object from a YAML file and create a new object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ExecutableEntity
            Object instance.
        """
        dict_obj: dict | list[dict] = read_yaml(file)
        if isinstance(dict_obj, list):
            exec_dict = dict_obj[0]
            exec_dict["status"] = {}
            tsk_dicts = []
            for i in dict_obj[1:]:
                i["status"] = {}
                tsk_dicts.append(i)
        else:
            exec_dict = dict_obj
            tsk_dicts = []

        context = get_context_from_project(exec_dict["project"])
        obj: ExecutableEntity = factory.build_entity_from_dict(exec_dict)
        try:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        except EntityAlreadyExistsError:
            raise EntityError(f"Entity {obj.name} already exists. If you want to update it, use load instead.")

        obj.import_tasks(tsk_dicts)

        return obj

    def load_context_entity(
        self,
        file: str,
    ) -> ContextEntity:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        dict_obj: dict = read_yaml(file)
        context = get_context_from_project(dict_obj["project"])
        obj: ContextEntity = factory.build_entity_from_dict(dict_obj)
        try:
            self._update_context_entity(context, obj.ENTITY_TYPE, obj.id, obj.to_dict())
        except EntityNotExistsError:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        return obj

    def load_executable_entity(
        self,
        file: str,
    ) -> ExecutableEntity:
        """
        Load object from a YAML file and update an existing object into the backend.

        Parameters
        ----------
        file : str
            Path to YAML file.

        Returns
        -------
        ExecutableEntity
            Object instance.
        """
        dict_obj: dict | list[dict] = read_yaml(file)
        if isinstance(dict_obj, list):
            exec_dict = dict_obj[0]
            tsk_dicts = dict_obj[1:]
        else:
            exec_dict = dict_obj
            tsk_dicts = []

        context = get_context_from_project(exec_dict["project"])
        obj: ExecutableEntity = factory.build_entity_from_dict(exec_dict)

        try:
            self._update_context_entity(context, obj.ENTITY_TYPE, obj.id, obj.to_dict())
        except EntityNotExistsError:
            self._create_context_entity(context, obj.ENTITY_TYPE, obj.to_dict())
        obj.import_tasks(tsk_dicts)
        return obj

    def _read_context_entity_versions(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        **kwargs,
    ) -> list[dict]:
        """
        Get all versions object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            Object instances.
        """
        project, entity_type, _, entity_name, _ = parse_identifier(
            identifier,
            project=project,
            entity_type=entity_type,
        )

        kwargs = context.client.build_parameters(
            ApiCategories.CONTEXT.value,
            BackendOperations.READ_ALL_VERSIONS.value,
            entity_name=entity_name,
            **kwargs,
        )

        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LIST.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.list_objects(api, **kwargs)

    def read_context_entity_versions(
        self,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        Read object versions from backend.

        Parameters
        ----------
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = get_context_from_identifier(identifier, project)
        objs = self._read_context_entity_versions(
            context,
            identifier,
            entity_type=entity_type,
            project=project,
            **kwargs,
        )
        objects = []
        for o in objs:
            entity: ContextEntity = factory.build_entity_from_dict(o)
            entity = self._post_process_get(entity)
            objects.append(entity)
        return objects

    def _list_context_entities(
        self,
        context: Context,
        entity_type: str,
        **kwargs,
    ) -> list[dict]:
        """
        List objects from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            List of objects.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LIST.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.list_objects(api, **kwargs)

    def list_context_entities(
        self,
        project: str,
        entity_type: str,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        List all latest version objects from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = get_context_from_project(project)
        objs = self._list_context_entities(context, entity_type, **kwargs)
        objects = []
        for o in objs:
            entity: ContextEntity = factory.build_entity_from_dict(o)
            entity = self._post_process_get(entity)
            objects.append(entity)
        return objects

    def _update_material_entity(
        self,
        new_obj: MaterialEntity,
    ) -> dict:
        """
        Update material object shortcut.

        Parameters
        ----------
        new_obj : MaterialEntity
            Object instance.

        Returns
        -------
        dict
            Response from backend.
        """
        return self.update_context_entity(
            new_obj.project,
            new_obj.ENTITY_TYPE,
            new_obj.id,
            new_obj.to_dict(),
        )

    def _update_context_entity(
        self,
        context: Context,
        entity_type: str,
        entity_id: str,
        entity_dict: dict,
        **kwargs,
    ) -> dict:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        context : Context
            Context instance.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_dict : dict
            Entity dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.UPDATE.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.update_object(api, entity_dict, **kwargs)

    def update_context_entity(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        entity_dict: dict,
        **kwargs,
    ) -> ContextEntity:
        """
        Update object. Note that object spec are immutable.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_dict : dict
            Entity dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        ContextEntity
            Object instance.
        """
        context = get_context_from_project(project)
        obj = self._update_context_entity(
            context,
            entity_type,
            entity_id,
            entity_dict,
            **kwargs,
        )
        return factory.build_entity_from_dict(obj)

    def _delete_context_entity(
        self,
        context: Context,
        identifier: str,
        entity_type: str | None = None,
        project: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Delete object from backend.

        Parameters
        ----------
        context : Context
            Context instance.
        identifier : str
            Entity key (store://...) or entity name.
        entity_type : str
            Entity type.
        project : str
            Project name.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        project, entity_type, _, entity_name, entity_id = parse_identifier(
            identifier,
            project=project,
            entity_type=entity_type,
            entity_id=entity_id,
        )

        delete_all_versions: bool = kwargs.pop("delete_all_versions", False)
        kwargs = context.client.build_parameters(
            ApiCategories.CONTEXT.value,
            BackendOperations.DELETE.value,
            entity_id=entity_id,
            entity_name=entity_name,
            cascade=kwargs.pop("cascade", None),
            delete_all_versions=delete_all_versions,
            **kwargs,
        )

        if delete_all_versions:
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.LIST.value,
                project=context.name,
                entity_type=entity_type,
            )
        else:
            api = context.client.build_api(
                ApiCategories.CONTEXT.value,
                BackendOperations.DELETE.value,
                project=context.name,
                entity_type=entity_type,
                entity_id=entity_id,
            )
        return context.client.delete_object(api, **kwargs)

    def delete_context_entity(
        self,
        identifier: str,
        project: str | None = None,
        entity_type: str | None = None,
        entity_id: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Delete object from backend.

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
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = get_context_from_identifier(identifier, project)
        return self._delete_context_entity(
            context,
            identifier,
            entity_type,
            context.name,
            entity_id,
            **kwargs,
        )

    def _post_process_get(self, entity: ContextEntity) -> ContextEntity:
        """
        Post process get (files, metrics).

        Parameters
        ----------
        entity : ContextEntity
            Entity to post process.

        Returns
        -------
        ContextEntity
            Post processed entity.
        """
        if hasattr(entity.status, "metrics"):
            entity._get_metrics()
        if hasattr(entity.status, "files"):
            entity._get_files_info()
        return entity

    ##############################
    # Context entity operations
    ##############################

    def _build_context_entity_key(
        self,
        context: Context,
        entity_type: str,
        entity_kind: str,
        entity_name: str,
        entity_id: str | None = None,
    ) -> str:
        """
        Build object key.

        Parameters
        ----------
        context : Context
            Context instance.
        entity_type : str
            Entity type.
        entity_kind : str
            Entity kind.
        entity_name : str
            Entity name.
        entity_id : str
            Entity ID.

        Returns
        -------
        str
            Object key.
        """
        return context.client.build_key(
            ApiCategories.CONTEXT.value,
            project=context.name,
            entity_type=entity_type,
            entity_kind=entity_kind,
            entity_name=entity_name,
            entity_id=entity_id,
        )

    def build_context_entity_key(
        self,
        project: str,
        entity_type: str,
        entity_kind: str,
        entity_name: str,
        entity_id: str | None = None,
    ) -> str:
        """
        Build object key.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_kind : str
            Entity kind.
        entity_name : str
            Entity name.
        entity_id : str
            Entity ID.

        Returns
        -------
        str
            Object key.
        """
        context = get_context_from_project(project)
        return self._build_context_entity_key(context, entity_type, entity_kind, entity_name, entity_id)

    def read_secret_data(
        self,
        project: str,
        entity_type: str,
        **kwargs,
    ) -> dict:
        """
        Get data from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.DATA.value,
            project=context.name,
            entity_type=entity_type,
        )
        return context.client.read_object(api, **kwargs)

    def update_secret_data(
        self,
        project: str,
        entity_type: str,
        data: dict,
        **kwargs,
    ) -> None:
        """
        Set data in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        data : dict
            Data dictionary.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.DATA.value,
            project=context.name,
            entity_type=entity_type,
        )
        context.client.update_object(api, data, **kwargs)

    def read_run_logs(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> dict:
        """
        Get logs from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.LOGS.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def stop_run(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> None:
        """
        Stop object in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.STOP.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        context.client.create_object(api, **kwargs)

    def resume_run(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> None:
        """
        Resume object in backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.RESUME.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        context.client.create_object(api, **kwargs)

    def read_files_info(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        **kwargs,
    ) -> list[dict]:
        """
        Get files info from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[dict]
            Response from backend.
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.FILES.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.read_object(api, **kwargs)

    def update_files_info(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        entity_list: list[dict],
        **kwargs,
    ) -> None:
        """
        Get files info from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        entity_list : list[dict]
            Entity list.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.FILES.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
        )
        return context.client.update_object(api, entity_list, **kwargs)

    def read_metrics(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        metric_name: str | None = None,
        **kwargs,
    ) -> dict:
        """
        Get metrics from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.METRICS.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
            metric_name=metric_name,
        )
        return context.client.read_object(api, **kwargs)

    def update_metric(
        self,
        project: str,
        entity_type: str,
        entity_id: str,
        metric_name: str,
        metric_value: Any,
        **kwargs,
    ) -> None:
        """
        Get single metric from backend.

        Parameters
        ----------
        project : str
            Project name.
        entity_type : str
            Entity type.
        entity_id : str
            Entity ID.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        None
        """
        context = get_context_from_project(project)
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.METRICS.value,
            project=context.name,
            entity_type=entity_type,
            entity_id=entity_id,
            metric_name=metric_name,
        )
        context.client.update_object(api, metric_value, **kwargs)

    def _search(
        self,
        context: Context,
        **kwargs,
    ) -> dict:
        """
        Search in backend.

        Parameters
        ----------
        context : Context
            Context instance.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        dict
            Response from backend.
        """
        kwargs = context.client.build_parameters(
            ApiCategories.CONTEXT.value,
            BackendOperations.SEARCH.value,
            **kwargs,
        )
        api = context.client.build_api(
            ApiCategories.CONTEXT.value,
            BackendOperations.SEARCH.value,
            project=context.name,
        )
        entities_dict = context.client.read_object(api, **kwargs)
        return [self.read_context_entity(entity["key"]) for entity in entities_dict["content"]]

    def search_entity(
        self,
        project: str,
        query: str | None = None,
        entity_types: list[str] | None = None,
        name: str | None = None,
        kind: str | None = None,
        created: str | None = None,
        updated: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        **kwargs,
    ) -> list[ContextEntity]:
        """
        Search objects from backend.

        Parameters
        ----------
        project : str
            Project name.
        query : str
            Search query.
        entity_types : list[str]
            Entity types.
        name : str
            Entity name.
        kind : str
            Entity kind.
        created : str
            Entity creation date.
        updated : str
            Entity update date.
        description : str
            Entity description.
        labels : list[str]
            Entity labels.
        **kwargs : dict
            Parameters to pass to the API call.

        Returns
        -------
        list[ContextEntity]
            List of object instances.
        """
        context = get_context_from_project(project)
        return self._search(
            context,
            query=query,
            entity_types=entity_types,
            name=name,
            kind=kind,
            created=created,
            updated=updated,
            description=description,
            labels=labels,
            **kwargs,
        )


context_processor = ContextEntityOperationsProcessor()
