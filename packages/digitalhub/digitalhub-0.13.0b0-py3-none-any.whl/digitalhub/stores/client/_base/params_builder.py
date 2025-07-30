# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from abc import abstractmethod


class ClientParametersBuilder:
    """
    This class is used to build the parameters for the client call.
    Depending on the client, the parameters are built differently.
    """

    @abstractmethod
    def build_parameters(self, category: str, operation: str, **kwargs) -> dict:
        """
        Build the parameters for the client call.
        """
