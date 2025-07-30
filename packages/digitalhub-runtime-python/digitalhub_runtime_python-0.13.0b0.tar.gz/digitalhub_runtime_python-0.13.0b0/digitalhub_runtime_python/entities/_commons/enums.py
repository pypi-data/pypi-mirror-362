# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    FUNCTION_PYTHON = "python"
    TASK_PYTHON_BUILD = "python+build"
    TASK_PYTHON_JOB = "python+job"
    TASK_PYTHON_SERVE = "python+serve"
    RUN_PYTHON = "python+run"


class TaskActions(Enum):
    """
    Task actions.
    """

    BUILD = "build"
    JOB = "job"
    SERVE = "serve"
