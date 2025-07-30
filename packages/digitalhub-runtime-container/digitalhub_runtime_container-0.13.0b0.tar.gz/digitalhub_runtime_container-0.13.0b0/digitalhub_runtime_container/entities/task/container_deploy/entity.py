# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_container.entities.task.container_deploy.spec import TaskSpecContainerDeploy
    from digitalhub_runtime_container.entities.task.container_deploy.status import TaskStatusContainerDeploy


class TaskContainerDeploy(Task):
    """
    TaskContainerDeploy class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecContainerDeploy,
        status: TaskStatusContainerDeploy,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecContainerDeploy
        self.status: TaskStatusContainerDeploy
