# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._commons.enums import ApiCategories, BackendOperations
from digitalhub.stores.client._base.params_builder import ClientParametersBuilder


class ClientDHCoreParametersBuilder(ClientParametersBuilder):
    """
    This class is used to build the parameters for the DHCore client calls.
    """

    def build_parameters(self, category: str, operation: str, **kwargs) -> dict:
        """
        Build the parameters for the client call.

        Parameters
        ----------
        category : str
            API category.
        operation : str
            API operation.
        **kwargs : dict
            Parameters to build.

        Returns
        -------
        dict
            Parameters formatted.
        """
        if category == ApiCategories.BASE.value:
            return self.build_parameters_base(operation, **kwargs)
        return self.build_parameters_context(operation, **kwargs)

    def build_parameters_base(self, operation: str, **kwargs) -> dict:
        """
        Build the base parameters for the client call.

        Parameters
        ----------
        operation : str
            API operation.
        **kwargs : dict
            Parameters to build.

        Returns
        -------
        dict
            Parameters formatted.
        """
        kwargs = self._set_params(**kwargs)
        if operation == BackendOperations.DELETE.value:
            if (cascade := kwargs.pop("cascade", None)) is not None:
                kwargs["params"]["cascade"] = str(cascade).lower()
        elif operation == BackendOperations.SHARE.value:
            kwargs["params"]["user"] = kwargs.pop("user")
            if kwargs.pop("unshare", False):
                kwargs["params"]["id"] = kwargs.pop("id")

        return kwargs

    def build_parameters_context(self, operation: str, **kwargs) -> dict:
        """
        Build the context parameters for the client call.

        Parameters
        ----------
        operation : str
            API operation.
        **kwargs : dict
            Parameters to build.

        Returns
        -------
        dict
            Parameters formatted.
        """
        kwargs = self._set_params(**kwargs)

        # Handle read
        if operation == BackendOperations.READ.value:
            name = kwargs.pop("entity_name", None)
            if name is not None:
                kwargs["params"]["name"] = name
        elif operation == BackendOperations.READ_ALL_VERSIONS.value:
            kwargs["params"]["versions"] = "all"
            kwargs["params"]["name"] = kwargs.pop("entity_name")
        # Handle delete
        elif operation == BackendOperations.DELETE.value:
            # Handle cascade
            if (cascade := kwargs.pop("cascade", None)) is not None:
                kwargs["params"]["cascade"] = str(cascade).lower()

            # Handle delete all versions
            entity_id = kwargs.pop("entity_id")
            entity_name = kwargs.pop("entity_name")
            if not kwargs.pop("delete_all_versions", False):
                if entity_id is None:
                    raise ValueError(
                        "If `delete_all_versions` is False, `entity_id` must be provided,"
                        " either as an argument or in key `identifier`.",
                    )
            else:
                kwargs["params"]["name"] = entity_name
        # Handle search
        elif operation == BackendOperations.SEARCH.value:
            # Handle fq
            if (fq := kwargs.pop("fq", None)) is not None:
                kwargs["params"]["fq"] = fq

            # Add search query
            if (query := kwargs.pop("query", None)) is not None:
                kwargs["params"]["q"] = query

            # Add search filters
            fq = []

            # Entity types
            if (entity_types := kwargs.pop("entity_types", None)) is not None:
                if not isinstance(entity_types, list):
                    entity_types = [entity_types]
                if len(entity_types) == 1:
                    entity_types = entity_types[0]
                else:
                    entity_types = " OR ".join(entity_types)
                fq.append(f"type:({entity_types})")

            # Name
            if (name := kwargs.pop("name", None)) is not None:
                fq.append(f'metadata.name:"{name}"')

            # Kind
            if (kind := kwargs.pop("kind", None)) is not None:
                fq.append(f'kind:"{kind}"')

            # Time
            created = kwargs.pop("created", None)
            updated = kwargs.pop("updated", None)
            created = created if created is not None else "*"
            updated = updated if updated is not None else "*"
            fq.append(f"metadata.updated:[{created} TO {updated}]")

            # Description
            if (description := kwargs.pop("description", None)) is not None:
                fq.append(f'metadata.description:"{description}"')

            # Labels
            if (labels := kwargs.pop("labels", None)) is not None:
                if len(labels) == 1:
                    labels = labels[0]
                else:
                    labels = " AND ".join(labels)
                fq.append(f"metadata.labels:({labels})")

            # Add filters
            kwargs["params"]["fq"] = fq

        return kwargs

    @staticmethod
    def _set_params(**kwargs) -> dict:
        """
        Format params parameter.

        Parameters
        ----------
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        dict
            Parameters with initialized params.
        """
        if not kwargs:
            kwargs = {}
        if "params" not in kwargs:
            kwargs["params"] = {}
        return kwargs
