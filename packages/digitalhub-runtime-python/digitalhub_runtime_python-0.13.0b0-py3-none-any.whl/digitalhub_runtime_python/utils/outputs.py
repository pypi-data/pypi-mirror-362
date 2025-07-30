# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import pickle
import typing
from typing import Any

from digitalhub.entities._commons.enums import EntityKinds, Relationship, State
from digitalhub.entities.artifact._base.entity import Artifact
from digitalhub.entities.artifact.crud import log_artifact
from digitalhub.entities.dataitem._base.entity import Dataitem
from digitalhub.entities.dataitem.crud import log_dataitem
from digitalhub.entities.model._base.entity import Model
from digitalhub.stores.readers.data.api import get_supported_dataframes
from digitalhub.utils.exceptions import EntityNotExistsError
from digitalhub.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from digitalhub.entities.dataitem.table.entity import DataitemTable


def collect_outputs(results: Any, outputs: list[str], project_name: str, run_key: str) -> dict:
    """
    Collect outputs. Use the produced results directly.

    Parameters
    ----------
    results : Any
        Function outputs.
    outputs : list[str]
        List of named outputs to collect.
    project_name : str
        Project name.
    run_key : str
        Run key.

    Returns
    -------
    dict
        Function outputs.
    """
    objects = {}
    results = listify_results(results)

    for idx, item in enumerate(results):
        # Get mapping of outputs, if not found, create a new one
        try:
            name = outputs[idx]
        except IndexError:
            name = f"output_{idx}"

        if isinstance(item, (str, int, float, bool, bytes)):
            objects[name] = item

        else:
            # Recieve a dataframe object
            if f"{item.__class__.__module__}.{item.__class__.__name__}" in get_supported_dataframes():
                obj = _log_dataitem(name, project_name, item)

            # Recieve a digitalhub object
            elif isinstance(item, (Dataitem, Artifact, Model)):
                obj = item

                # Add relationship to object, update it
                dest = run_key + ":" + run_key.split("/")[-1]
                obj.add_relationship(relation=Relationship.PRODUCEDBY.value, dest=dest)

                try:
                    obj.save(update=True)
                except EntityNotExistsError:
                    obj.save()

            # Recieve a generic python object
            else:
                obj = _log_artifact(name, project_name, item)

            objects[name] = obj

    return objects


def parse_outputs(results: Any, run_outputs: list, project_name: str, run_key: str) -> dict:
    """
    Parse outputs.

    Parameters
    ----------
    results : Any
        Function outputs.
    run_outputs : list
        Run outputs.
    project_name : str
        Project name.
    run_key : str
        Run key.

    Returns
    -------
    dict
        Function outputs.
    """
    results_list = listify_results(results)
    out_list = []
    for idx, _ in enumerate(results_list):
        try:
            out_list.append(run_outputs.pop(0))
        except IndexError:
            out_list.append(f"output_{idx}")
    return collect_outputs(results, out_list, project_name, run_key)


def listify_results(results: Any) -> list:
    """
    Listify results.

    Parameters
    ----------
    results : Any
        Function outputs.

    Returns
    -------
    list
        Function outputs.
    """
    if results is None:
        return []

    if not isinstance(results, (tuple, list)):
        results = [results]

    return results


def _log_dataitem(name: str, project_name: str, data: Any) -> DataitemTable:
    """
    Log dataitem.

    Parameters
    ----------
    name : str
        Dataitem name.
    project_name : str
        Project name.
    data : Any
        Data.

    Returns
    -------
    str
        Dataitem key.
    """
    try:
        return log_dataitem(
            project=project_name,
            name=name,
            kind=EntityKinds.DATAITEM_TABLE.value,
            data=data,
        )
    except Exception as e:
        msg = f"Some error occurred while logging dataitem. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def _log_artifact(name: str, project_name: str, data: Any) -> Artifact:
    """
    Log artifact.

    Parameters
    ----------
    name : str
        Artifact name.
    project_name : str
        Project name.
    data : Any
        Data.

    Returns
    -------
    str
        Artifact key.
    """
    try:
        # Dump item to pickle
        pickle_file = f"{name}.pickle"
        with open(pickle_file, "wb") as f:
            f.write(pickle.dumps(data))
        return log_artifact(
            project=project_name,
            name=name,
            kind=EntityKinds.ARTIFACT_ARTIFACT.value,
            source=pickle_file,
        )

    except Exception as e:
        msg = f"Some error occurred while logging artifact. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def build_status(
    parsed_execution: dict,
    mapped_outputs: dict | None = None,
) -> dict:
    """
    Collect outputs.

    Parameters
    ----------
    parsed_execution : dict
        Parsed execution dict.
    mapped_outputs : dict
        Mapped outputs.

    Returns
    -------
    dict
        Status dict.
    """
    results = {}
    outputs = {}
    if mapped_outputs is None:
        mapped_outputs = {}

    try:
        for key, value in parsed_execution.items():
            if isinstance(value, (Dataitem, Artifact, Model)):
                outputs[key] = value.key
            else:
                results[key] = value
        return {
            "state": State.COMPLETED.value,
            "outputs": outputs,
            "results": results,
        }
    except Exception as e:
        msg = f"Something got wrong during run status building. Exception: {e.__class__}. Error: {e.args}"
        LOGGER.exception(msg)
        raise RuntimeError(msg) from e
