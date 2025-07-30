# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import time
import typing

import requests
from digitalhub.entities._commons.enums import State
from digitalhub.entities.run._base.entity import Run
from digitalhub.factory.factory import factory
from digitalhub.utils.exceptions import EntityError
from digitalhub.utils.logger import LOGGER

from digitalhub_runtime_container.entities._commons.enums import TaskActions

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_container.entities.run.container_run.spec import RunSpecContainerRun
    from digitalhub_runtime_container.entities.run.container_run.status import RunStatusContainerRun


class RunContainerRun(Run):
    """
    RunContainerRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecContainerRun,
        status: RunStatusContainerRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecContainerRun
        self.status: RunStatusContainerRun

    def wait(self, log_info: bool = True) -> Run:
        """
        Wait for run to finish.

        Parameters
        ----------
        log_info : bool
            If True, log information.

        Returns
        -------
        Run
            Run object.
        """
        task_kind = self.spec.task.split("://")[0]
        action = factory.get_action_from_task_kind(self.kind, task_kind)

        if action == TaskActions.SERVE.value:
            serve_timeout = 300
            start = time.time()

            while time.time() - start < serve_timeout:
                if log_info:
                    LOGGER.info(f"Waiting for run {self.id} to deploy service.")

                self.refresh()
                if self.status.service is not None:
                    if log_info:
                        msg = f"Run {self.id} service deployed."
                        LOGGER.info(msg)
                    return self

                elif self.status.state == State.ERROR.value:
                    if log_info:
                        msg = f"Run {self.id} serving failed."
                        LOGGER.info(msg)
                    return self

                time.sleep(5)

            if log_info:
                msg = f"Waiting for run {self.id} service timed out. Check logs for more information."
                LOGGER.info(msg)

            return self

        return super().wait(log_info=log_info)

    def invoke(
        self,
        method: str = "POST",
        url: str | None = None,
        **kwargs,
    ) -> requests.Response:
        """
        Invoke run.

        Parameters
        ----------
        method : str
            Method of the request.
        url : str
            URL of the request.
        **kwargs : dict
            Keyword arguments to pass to the request.

        Returns
        -------
        requests.Response
            Response from service.
        """
        if self._context().local:
            raise EntityError("Invoke not supported locally.")
        if url is None:
            try:
                url = f"http://{self.status.service.get('url')}"
            except AttributeError:
                msg = "Url not specified and service not found on run status. If a service is deploying, use run.wait() or try again later."
                raise EntityError(msg)
        return requests.request(method=method, url=url, **kwargs)
