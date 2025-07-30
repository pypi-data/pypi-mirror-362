# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities.task._base.utils import build_task_actions

from digitalhub_runtime_container.entities._commons.enums import EntityKinds, TaskActions


class RuntimeEntityBuilderContainer(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_CONTAINER.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_CONTAINER_JOB.value,
                TaskActions.JOB.value,
            ),
            (
                EntityKinds.TASK_CONTAINER_BUILD.value,
                TaskActions.BUILD.value,
            ),
            (
                EntityKinds.TASK_CONTAINER_SERVE.value,
                TaskActions.SERVE.value,
            ),
            (
                EntityKinds.TASK_CONTAINER_DEPLOY.value,
                TaskActions.DEPLOY.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_CONTAINER.value
