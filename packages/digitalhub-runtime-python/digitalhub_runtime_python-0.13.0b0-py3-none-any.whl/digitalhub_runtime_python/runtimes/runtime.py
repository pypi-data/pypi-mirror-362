# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import Callable

from digitalhub.context.api import get_context
from digitalhub.runtimes._base import Runtime
from digitalhub.utils.logger import LOGGER

from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.utils.configuration import import_function_from_source
from digitalhub_runtime_python.utils.inputs import compose_inputs
from digitalhub_runtime_python.utils.outputs import build_status, parse_outputs


class RuntimePython(Runtime):
    """
    Runtime Python class.
    """

    def __init__(self, project: str) -> None:
        super().__init__(project)
        ctx = get_context(self.project)
        self.runtime_dir = ctx.root / "runtime_python"
        self.runtime_dir.mkdir(parents=True, exist_ok=True)

    def build(self, function: dict, task: dict, run: dict) -> dict:
        """
        Build run spec.

        Parameters
        ----------
        function : dict
            The function.
        task : dict
            The task.
        run : dict
            The run.

        Returns
        -------
        dict
            The run spec.
        """
        return {
            **function.get("spec", {}),
            **task.get("spec", {}),
            **run.get("spec", {}),
        }

    def run(self, run: dict) -> dict:
        """
        Run function.

        Returns
        -------
        dict
            Status of the executed run.
        """
        LOGGER.info("Validating task.")
        self._validate_task(run)

        LOGGER.info("Validating run.")
        self._validate_run(run)

        LOGGER.info("Starting task.")
        spec = run.get("spec")
        project = run.get("project")
        run_key = run.get("key")

        LOGGER.info("Configuring execution.")
        fnc, wrapped = self._configure_execution(spec)

        LOGGER.info("Composing function arguments.")
        fnc_args = self._compose_args(fnc, spec, project)

        LOGGER.info("Executing run.")
        if wrapped:
            results: dict = self._execute(fnc, project, run_key, **fnc_args)
        else:
            exec_result = self._execute(fnc, **fnc_args)
            LOGGER.info("Collecting outputs.")
            results = parse_outputs(exec_result, list(spec.get("outputs", {})), project, run_key)

        status = build_status(results, spec.get("outputs"))

        # Return run status
        LOGGER.info("Task completed, returning run status.")
        return status

    @staticmethod
    def _validate_run(run: dict) -> None:
        """
        Check if run is locally allowed.

        Parameters
        ----------
        run : dict
            Run object dictionary.

        Returns
        -------
        None
        """
        task_kind = run["spec"]["task"].split(":")[0]
        if task_kind != EntityKinds.TASK_PYTHON_JOB.value and run["spec"]["local_execution"]:
            msg = f"Local execution not allowed for task kind {task_kind}."
            LOGGER.exception(msg)
            raise RuntimeError(msg)

    ##############################
    # Configuration
    ##############################

    def _configure_execution(self, spec: dict) -> tuple[Callable, bool]:
        """
        Configure execution.

        Parameters
        ----------
        spec : dict
            Run spec.

        Returns
        -------
        Callable
            Function to execute.
        """
        fnc = import_function_from_source(
            self.runtime_dir,
            spec.get("source", {}),
        )
        return fnc, hasattr(fnc, "__wrapped__")

    def _compose_args(self, func: Callable, spec: dict, project: str) -> dict:
        """
        Collect inputs.

        Parameters
        ----------
        func : Callable
            Function to execute.
        spec : dict
            Run specs.
        project : str
            Project name.

        Returns
        -------
        dict
            Parameters.
        """
        inputs = spec.get("inputs", {})
        parameters = spec.get("parameters", {})
        local_execution = spec.get("local_execution")
        return compose_inputs(inputs, parameters, local_execution, func, project)
