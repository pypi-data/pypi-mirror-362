# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function.python.builder import FunctionPythonBuilder
from digitalhub_runtime_python.entities.run.python_run.builder import RunPythonRunBuilder
from digitalhub_runtime_python.entities.task.python_build.builder import TaskPythonBuildBuilder
from digitalhub_runtime_python.entities.task.python_job.builder import TaskPythonJobBuilder
from digitalhub_runtime_python.entities.task.python_serve.builder import TaskPythonServeBuilder
from digitalhub_runtime_python.utils.utils import handler

entity_builders = (
    (EntityKinds.FUNCTION_PYTHON.value, FunctionPythonBuilder),
    (EntityKinds.TASK_PYTHON_BUILD.value, TaskPythonBuildBuilder),
    (EntityKinds.TASK_PYTHON_JOB.value, TaskPythonJobBuilder),
    (EntityKinds.TASK_PYTHON_SERVE.value, TaskPythonServeBuilder),
    (EntityKinds.RUN_PYTHON.value, RunPythonRunBuilder),
)

try:
    from digitalhub_runtime_python.runtimes.builder import RuntimePythonBuilder

    runtime_builders = ((kind, RuntimePythonBuilder) for kind in [e.value for e in EntityKinds])
except ImportError:
    runtime_builders = tuple()
