# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_container.entities._base.runtime_entity.builder import RuntimeEntityBuilderContainer
from digitalhub_runtime_container.entities._commons.enums import EntityKinds
from digitalhub_runtime_container.entities.run.container_run.entity import RunContainerRun
from digitalhub_runtime_container.entities.run.container_run.spec import RunSpecContainerRun, RunValidatorContainerRun
from digitalhub_runtime_container.entities.run.container_run.status import RunStatusContainerRun


class RunContainerRunBuilder(RunBuilder, RuntimeEntityBuilderContainer):
    """
    RunContainerRunBuilder runer.
    """

    ENTITY_CLASS = RunContainerRun
    ENTITY_SPEC_CLASS = RunSpecContainerRun
    ENTITY_SPEC_VALIDATOR = RunValidatorContainerRun
    ENTITY_STATUS_CLASS = RunStatusContainerRun
    ENTITY_KIND = EntityKinds.RUN_CONTAINER.value
