# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class CorePort(BaseModel):
    """
    Port mapper model.
    """

    port: int
    target_port: int
