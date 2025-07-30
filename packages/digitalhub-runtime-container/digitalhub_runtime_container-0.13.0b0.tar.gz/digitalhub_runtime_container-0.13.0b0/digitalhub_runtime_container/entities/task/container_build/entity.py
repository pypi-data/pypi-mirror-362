# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_container.entities.task.container_build.spec import TaskSpecContainerBuild
    from digitalhub_runtime_container.entities.task.container_build.status import TaskStatusContainerBuild


class TaskContainerBuild(Task):
    """
    TaskContainerBuild class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecContainerBuild,
        status: TaskStatusContainerBuild,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecContainerBuild
        self.status: TaskStatusContainerBuild
