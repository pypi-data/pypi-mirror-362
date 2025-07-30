# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecContainerRun(RunSpec):
    """
    RunSpecContainerRun specifications.
    """

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        workflow: str | None = None,
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
        source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        image_pull_policy: str | None = None,
        command: str | None = None,
        args: list[str] | None = None,
        replicas: int | None = None,
        service_ports: list | None = None,
        service_type: str | None = None,
        service_name: str | None = None,
        instructions: dict | None = None,
        run_as_user: int | None = None,
        run_as_group: int | None = None,
        fs_group: int | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
            function,
            workflow,
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
        self.args = args

        self.source = source
        self.image = image
        self.base_image = base_image
        self.image_pull_policy = image_pull_policy
        self.command = command

        self.replicas = replicas
        self.service_ports = service_ports
        self.service_type = service_type
        self.service_name = service_name
        self.instructions = instructions
        self.run_as_user = run_as_user
        self.run_as_group = run_as_group
        self.fs_group = fs_group


class RunValidatorContainerRun(RunValidator):
    """
    RunValidatorContainerRun validator.
    """

    # Run parameters
    args: list[str] = None
    """Arguments to pass to the entrypoint."""

    # Function parameters
    source: dict = None
    image: str = None
    base_image: str = None
    image_pull_policy: str = None
    command: str = None

    # Task deploy
    replicas: int = None

    # Task serve
    service_ports: list[dict] = None
    service_type: str = None
    service_name: str = None

    # Task build
    instructions: list[str] = None

    # Shared task
    run_as_user: int = None
    run_as_group: int = None
    fs_group: int = None
