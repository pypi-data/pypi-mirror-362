# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities.task._base.utils import build_task_actions

from digitalhub_runtime_python.entities._commons.enums import EntityKinds, TaskActions


class RuntimeEntityBuilderPython(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.FUNCTION_PYTHON.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_PYTHON_JOB.value,
                TaskActions.JOB.value,
            ),
            (
                EntityKinds.TASK_PYTHON_BUILD.value,
                TaskActions.BUILD.value,
            ),
            (
                EntityKinds.TASK_PYTHON_SERVE.value,
                TaskActions.SERVE.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_PYTHON.value
