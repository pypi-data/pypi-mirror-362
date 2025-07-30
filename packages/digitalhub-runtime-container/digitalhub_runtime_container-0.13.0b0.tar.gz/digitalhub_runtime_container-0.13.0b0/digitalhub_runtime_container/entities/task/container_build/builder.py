# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer
from digitalhub_runtime_container.entities._commons.enums import EntityKinds
from digitalhub_runtime_container.entities.task.container_build.entity import TaskContainerBuild
from digitalhub_runtime_container.entities.task.container_build.spec import (
    TaskSpecContainerBuild,
    TaskValidatorContainerBuild,
)
from digitalhub_runtime_container.entities.task.container_build.status import TaskStatusContainerBuild


class TaskContainerBuildBuilder(TaskBuilder, RuntimeEntityBuilderContainer):
    """
    TaskContainerBuild builder.
    """

    ENTITY_CLASS = TaskContainerBuild
    ENTITY_SPEC_CLASS = TaskSpecContainerBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorContainerBuild
    ENTITY_STATUS_CLASS = TaskStatusContainerBuild
    ENTITY_KIND = EntityKinds.TASK_CONTAINER_BUILD.value
