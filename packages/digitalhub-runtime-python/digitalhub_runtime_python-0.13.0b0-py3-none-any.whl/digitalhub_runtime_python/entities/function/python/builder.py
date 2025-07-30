# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.function._base.builder import FunctionBuilder

from digitalhub_runtime_python.entities._base.runtime_entity.builder import RuntimeEntityBuilderPython
from digitalhub_runtime_python.entities._commons.enums import EntityKinds
from digitalhub_runtime_python.entities.function.python.entity import FunctionPython
from digitalhub_runtime_python.entities.function.python.spec import FunctionSpecPython, FunctionValidatorPython
from digitalhub_runtime_python.entities.function.python.status import FunctionStatusPython
from digitalhub_runtime_python.entities.function.python.utils import source_check, source_post_check


class FunctionPythonBuilder(FunctionBuilder, RuntimeEntityBuilderPython):
    """
    FunctionPython builder.
    """

    ENTITY_CLASS = FunctionPython
    ENTITY_SPEC_CLASS = FunctionSpecPython
    ENTITY_SPEC_VALIDATOR = FunctionValidatorPython
    ENTITY_STATUS_CLASS = FunctionStatusPython
    ENTITY_KIND = EntityKinds.FUNCTION_PYTHON.value

    def build(
        self,
        kind: str,
        project: str,
        name: str,
        uuid: str | None = None,
        description: str | None = None,
        labels: list[str] | None = None,
        embedded: bool = False,
        **kwargs,
    ) -> FunctionPython:
        kwargs = source_check(**kwargs)
        obj = super().build(
            kind,
            project,
            name,
            uuid,
            description,
            labels,
            embedded,
            **kwargs,
        )
        return source_post_check(obj)

    def from_dict(self, obj: dict, validate: bool = True) -> FunctionPython:
        """
        Create a new object from dictionary.

        Parameters
        ----------
        obj : dict
            Dictionary to create object from.
        validate : bool
            Flag to indicate if arguments must be validated.

        Returns
        -------
        FunctionPython
            Object instance.
        """
        entity = super().from_dict(obj, validate=validate)
        return source_post_check(entity)

    def _parse_dict(self, obj: dict, validate: bool = True) -> dict:
        """
        Get dictionary and parse it to a valid entity dictionary.

        Parameters
        ----------
        entity : str
            Entity type.
        obj : dict
            Dictionary to parse.

        Returns
        -------
        dict
            A dictionary containing the attributes of the entity instance.
        """
        # Look for source in spec
        if spec_dict := obj.get("spec", {}):
            # Check source
            source = spec_dict.get("source", {})
            if source:
                spec_dict["source"] = source_check(source=source)["source"]

        return super()._parse_dict(obj, validate=validate)
