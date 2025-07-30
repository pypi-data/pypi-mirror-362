# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecPythonBuild(TaskSpecFunction):
    """TaskSpecPythonBuild specifications."""

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
        instructions: list | None = None,
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
        self.instructions = instructions


class TaskValidatorPythonBuild(TaskValidatorFunction):
    """
    TaskValidatorPythonBuild validator.
    """

    instructions: list[str] = None
    """Build instructions."""
