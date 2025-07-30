# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecContainerDeploy(TaskSpecFunction):
    """
    TaskSpecContainerDeploy specifications.
    """

    def __init__(
        self,
        function: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        runtime_class: str | None = None,
        priority_class: str | None = None,
        replicas: int | None = None,
        run_as_user: int | None = None,
        run_as_group: int | None = None,
        fs_group: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            runtime_class,
            priority_class,
            **kwargs,
        )
        self.replicas = replicas
        self.run_as_user = run_as_user
        self.run_as_group = run_as_group
        self.fs_group = fs_group


class TaskValidatorContainerDeploy(TaskValidatorFunction):
    """
    TaskValidatorContainerDeploy validator.
    """

    replicas: int = Field(default=None, ge=1)
    """Number of replicas."""

    run_as_user: int = Field(default=None, ge=0)
    """RunAsUser."""

    run_as_group: int = Field(default=None, ge=0)
    """RunAsGroup."""

    fs_group: int = Field(default=None, ge=1)
    """FSGroup."""
