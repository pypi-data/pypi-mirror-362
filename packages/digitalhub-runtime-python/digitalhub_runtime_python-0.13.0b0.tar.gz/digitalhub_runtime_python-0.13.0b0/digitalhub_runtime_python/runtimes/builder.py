# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.runtimes.builder import RuntimeBuilder

from digitalhub_runtime_python.runtimes.runtime import RuntimePython


class RuntimePythonBuilder(RuntimeBuilder):
    """RuntaimePythonBuilder class."""

    RUNTIME_CLASS = RuntimePython
