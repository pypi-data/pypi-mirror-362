# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.spec import FunctionSpec, FunctionValidator
from digitalhub.entities.task._base.models import CorePullPolicy

from digitalhub_runtime_container.entities.function.container.models import SourceValidator


class FunctionSpecContainer(FunctionSpec):
    """
    FunctionSpecContainer specifications.
    """

    def __init__(
        self,
        image: str | None = None,
        base_image: str | None = None,
        image_pull_policy: str | None = None,
        command: str | None = None,
        args: list[str] | None = None,
        source: dict | None = None,
    ) -> None:
        super().__init__()

        self.image = image
        self.base_image = base_image
        self.image_pull_policy = image_pull_policy
        self.command = command
        self.source = source


class FunctionValidatorContainer(FunctionValidator):
    """
    FunctionValidatorContainer validator.
    """

    image: str = None
    """Name of the Function's container image."""

    base_image: str = None
    """Function's base container image."""

    image_pull_policy: CorePullPolicy = None
    """Function's container image pull policy."""

    command: str = None
    """Command to run inside the container."""

    source: SourceValidator = None
    """Source code params."""
