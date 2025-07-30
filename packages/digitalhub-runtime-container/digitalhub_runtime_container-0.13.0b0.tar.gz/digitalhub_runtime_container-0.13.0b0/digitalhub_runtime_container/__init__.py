# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_container.entities._commons.enums import EntityKinds
from digitalhub_runtime_container.entities.function.container.builder import FunctionContainerBuilder
from digitalhub_runtime_container.entities.run.container_run.builder import RunContainerRunBuilder
from digitalhub_runtime_container.entities.task.container_build.builder import TaskContainerBuildBuilder
from digitalhub_runtime_container.entities.task.container_deploy.builder import TaskContainerDeployBuilder
from digitalhub_runtime_container.entities.task.container_job.builder import TaskContainerJobBuilder
from digitalhub_runtime_container.entities.task.container_serve.builder import TaskContainerServeBuilder

entity_builders = (
    (EntityKinds.FUNCTION_CONTAINER.value, FunctionContainerBuilder),
    (EntityKinds.TASK_CONTAINER_BUILD.value, TaskContainerBuildBuilder),
    (EntityKinds.TASK_CONTAINER_DEPLOY.value, TaskContainerDeployBuilder),
    (EntityKinds.TASK_CONTAINER_JOB.value, TaskContainerJobBuilder),
    (EntityKinds.TASK_CONTAINER_SERVE.value, TaskContainerServeBuilder),
    (EntityKinds.RUN_CONTAINER.value, RunContainerRunBuilder),
)

try:
    from digitalhub_runtime_container.runtimes.builder import RuntimeContainerBuilder

    runtime_builders = ((kind, RuntimeContainerBuilder) for kind in [e.value for e in EntityKinds])
except ImportError:
    runtime_builders = tuple()
