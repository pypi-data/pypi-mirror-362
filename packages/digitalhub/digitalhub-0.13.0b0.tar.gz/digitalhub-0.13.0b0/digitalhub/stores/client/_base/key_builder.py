# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import abstractmethod

from digitalhub.entities._commons.enums import ApiCategories


class ClientKeyBuilder:
    """
    Class that build the key of entities.
    """

    def build_key(self, category: str, *args, **kwargs) -> str:
        """
        Build key.

        Parameters
        ----------
        category : str
            Key category.
        *args : tuple
            Positional arguments.
        **kwargs : dict
            Keyword arguments.

        Returns
        -------
        str
            Key.
        """
        if category == ApiCategories.BASE.value:
            return self.base_entity_key(*args, **kwargs)
        return self.context_entity_key(*args, **kwargs)

    @abstractmethod
    def base_entity_key(self, entity_id: str) -> str:
        """
        Build for base entity key.
        """

    @abstractmethod
    def context_entity_key(
        self,
        project: str,
        entity_type: str,
        entity_kind: str,
        entity_name: str,
        entity_id: str | None = None,
    ) -> str:
        """
        Build for context entity key.
        """
