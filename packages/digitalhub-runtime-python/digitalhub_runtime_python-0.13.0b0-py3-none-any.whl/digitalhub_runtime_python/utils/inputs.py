# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import inspect
import typing
from typing import Any, Callable

from digitalhub.context.api import get_context
from digitalhub.entities.project.crud import get_project
from digitalhub.factory.factory import factory
from digitalhub.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.entity import Entity
    from digitalhub.entities.project._base.entity import Project

    from digitalhub_runtime_python.entities.run.python_run.entity import RunPythonRun


def get_project_(project_name: str) -> Project:
    """
    Get project.

    Parameters
    ----------
    project_name : str
        Project name.

    Returns
    -------
    Project
        Project.
    """
    try:
        ctx = get_context(project_name)
        return get_project(project_name, local=ctx.local)
    except Exception as e:
        msg = f"Error during project collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_run_(project_name: str) -> RunPythonRun:
    """
    Get run.

    Parameters
    ----------
    project_name : str
        Project name.
    run_id : str
        Run id.

    Returns
    -------
    Run
        Run.
    """
    try:
        ctx = get_context(project_name)
        proj = get_project(project_name, local=ctx.local)
        run_key = ctx.get_run_ctx()
        return proj.get_run(run_key)
    except Exception as e:
        msg = f"Error during run collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def get_entity_inputs(inputs: dict) -> dict[str, Entity]:
    """
    Set inputs.

    Parameters
    ----------
    inputs : dict
        Run inputs.
    parameters : dict
        Run parameters.
    tmp_dir : Path
        Temporary directory for storing dataitms and artifacts.

    Returns
    -------
    dict
        Dictionary of inputs.
    """
    try:
        return {k: factory.build_entity_from_dict(v) for k, v in inputs.items()}
    except Exception as e:
        msg = f"Error during inputs collection. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def compose_inputs(
    inputs: dict,
    parameters: dict,
    local_execution: bool,
    func: Callable,
    project: str | Project,
    context: Any | None = None,
    event: Any | None = None,
) -> dict:
    """
    Compose inputs.

    Parameters
    ----------
    inputs : dict
        Run inputs.
    parameters : dict
        Run parameters.
    local_execution : bool
        Local execution.
    func : Callable
        Function to execute.
    project : str
        Project name.
    context : nuclio_sdk.Context
        Nuclio context.
    event : nuclio_sdk.Event
        Nuclio event.

    Returns
    -------
    dict
        Function inputs.
    """
    try:
        entity_inputs = get_entity_inputs(inputs)
        fnc_args = {**parameters, **entity_inputs}

        fnc_parameters = inspect.signature(func).parameters

        _has_project = "project" in fnc_parameters
        _has_run = "run" in fnc_parameters
        _has_context = "context" in fnc_parameters
        _has_event = "event" in fnc_parameters

        # Project is reserved keyword argument
        # both in local and remote executions
        if _has_project:
            if _has_context and not local_execution:
                fnc_args["project"] = context.project
            elif isinstance(project, str):
                fnc_args["project"] = get_project_(project)
            else:
                fnc_args["project"] = project

        if _has_context and not local_execution:
            project_name: str = context.project.name
        elif isinstance(project, str):
            project_name = project
        else:
            project_name = project.name

        if _has_run:
            if _has_context and not local_execution:
                fnc_args["run"] = context.run
            else:
                fnc_args["run"] = get_run_(project_name)

        # Context and event are reserved keyword arguments
        # only in remote executions
        if not local_execution:
            if _has_context:
                fnc_args["context"] = context
            if _has_event:
                fnc_args["event"] = event

        return fnc_args

    except Exception as e:
        msg = f"Error during function arguments compostion. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e


def compose_init(init_function: Callable, context: Any, parameters: dict) -> dict:
    """
    Compose init function.

    Parameters
    ----------
    init_function : Callable
        Init function.
    context : Any
        Context.
    parameters : dict
        Parameters.

    Returns
    -------
    dict
        Init parameters.
    """
    signature_parameters = dict(inspect.signature(init_function).parameters)
    if "context" not in signature_parameters:
        raise RuntimeError("Init function must have 'context' parameter.")
    if len(parameters) != (len(signature_parameters) - 1):
        signature_parameters.pop("context")
        expected_parameters = list(signature_parameters.keys())
        raise RuntimeError(
            f"Init function parameters mismatch. Expected: {expected_parameters}, " f"Got: {list(parameters)}"
        )
    return {**parameters, "context": context}
