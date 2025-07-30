# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.models import CoreServiceType
from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction
from pydantic import Field


class TaskSpecPythonServe(TaskSpecFunction):
    """TaskSpecPythonServe specifications."""

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
        service_type: str | None = None,
        service_name: str | None = None,
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
        self.service_type = service_type
        self.service_name = service_name


class TaskValidatorPythonServe(TaskValidatorFunction):
    """
    TaskValidatorPythonServe validator.
    """

    replicas: int = Field(default=None, ge=1)
    """Number of replicas."""

    service_type: CoreServiceType = None
    """Service type."""

    service_name: str = None
    """Service name."""
