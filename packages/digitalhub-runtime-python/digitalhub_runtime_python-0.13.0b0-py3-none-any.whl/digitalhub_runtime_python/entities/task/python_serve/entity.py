# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_python.entities.task.python_serve.spec import TaskSpecPythonServe
    from digitalhub_runtime_python.entities.task.python_serve.status import TaskStatusPythonServe


class TaskPythonServe(Task):
    """
    TaskPythonServe class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecPythonServe,
        status: TaskStatusPythonServe,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecPythonServe
        self.status: TaskStatusPythonServe
