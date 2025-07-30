# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.task.python_serve.entity import TaskPythonServe
from digitalhub_runtime_python.entities.task.python_serve.spec import TaskSpecPythonServe, TaskValidatorPythonServe
from digitalhub_runtime_python.entities.task.python_serve.status import TaskStatusPythonServe


class TaskPythonServeBuilder(TaskBuilder, RuntimeEntityBuilderPython):
    """
    TaskPythonServeBuilder serveer.
    """

    ENTITY_CLASS = TaskPythonServe
    ENTITY_SPEC_CLASS = TaskSpecPythonServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorPythonServe
    ENTITY_STATUS_CLASS = TaskStatusPythonServe
    ENTITY_KIND = EntityKinds.TASK_PYTHON_SERVE.value
