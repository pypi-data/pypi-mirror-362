from __future__ import annotations

import ast
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, TypeVar

import bytewax.operators as op
from pydantic import BaseModel, ConfigDict, Field


def DeriverInput(workspace: str, asset: str, division: str, unit: str, signal: str):
    return Field(
        description="DeriverInput",
        json_schema_extra={
            "workspace": workspace,
            "asset": asset,
            "division": division,
            "unit": unit,
            "signal": signal,
        },
    )


def DeriverOutput(
    workspace: str,
    asset: str,
    division: str,
    unit: str,
    signal: str,
    physical_unit: str | None = None,
    description: str | None = None,
    long_description: str | None = None,
):
    return Field(
        description="output",
        json_schema_extra={
            "workspace": workspace,
            "asset": asset,
            "division": division,
            "unit": unit,
            "signal": signal,
            "physical_unit": physical_unit,
            "description": description,
            "long_description": long_description,
        },
    )


class DeriverIO(BaseModel):
    timestamp: datetime = Field(description="Timestamp")

    model_config = ConfigDict(
        extra="allow",
    )


def get_type_from_json_schema(type_str: str | list[str]) -> type:
    type_map = {
        "string": str,
        "number": float,
        "integer": int,
        "boolean": bool,
        "null": type(None),
        "object": dict,
        "array": list,
    }
    if isinstance(type_str, list):
        types = [get_type_from_json_schema(item) for item in type_str]
        if len(types) == 0 or len(types) > 2:
            raise ValueError(f"Unsupported JSON Schema type: {type_str}")
        elif len(types) == 2:
            if types[0] == type(None):
                return types[1]
            else:
                return types[0]
        else:
            return types[0]
    else:
        normalized = type_str.strip().lower()
        if normalized not in type_map:
            raise ValueError(f"Unsupported JSON Schema type: {type_str}")
        return type_map[normalized]


class DeriverInputs(DeriverIO):
    @classmethod
    def list(cls):
        return [
            (
                field,
                get_type_from_json_schema(
                    value.get(
                        "type",
                        list(map(lambda x: x.get("type"), value.get("anyOf", []))),
                    )
                ),
            )
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("description") == "DeriverInput"
        ]


InputType = TypeVar("InputType", bound=DeriverInputs)


class DeriverOutputs(DeriverIO):
    @classmethod
    def list(cls) -> list[tuple[str, type]]:
        return [
            (
                field,
                get_type_from_json_schema(
                    value.get(
                        "type",
                        list(map(lambda x: x.get("type"), value.get("anyOf", []))),
                    )
                ),
            )
            for field, value in cls.model_json_schema()["properties"].items()
            if value.get("description") == "DeriverOutput"
        ]


OutputType = TypeVar("OutputType", bound=DeriverOutputs)


class Deriver(ABC):
    class Inputs(DeriverInputs):
        pass

    class Outputs(DeriverOutputs):
        pass

    @classmethod
    @abstractmethod
    def transform_stream(cls, stream: op.Stream[Deriver.Inputs]) -> op.Stream[Deriver.Outputs]:
        raise NotImplementedError


def validate_deriver(deriver: type) -> type[Deriver]:
    if not issubclass(deriver, Deriver):
        raise ValueError("Deriver must be a subclass of Deriver.")

    deriver_inputs = deriver.Inputs.list()
    if len(deriver_inputs) == 0:
        raise ValueError("Deriver must have at least one input.")

    deriver_outputs = deriver.Outputs.list()
    if len(deriver_outputs) == 0:
        raise ValueError("Deriver must have at least one output.")
    for name, typ in deriver_outputs:
        if typ not in [float, int, str, bool, dict]:
            raise ValueError(f"Deriver output '{name}' has type '{typ}', which is not allowed.")

    try:
        deriver.transform_stream(None)  # type: ignore
    except Exception as e:
        if isinstance(e, NotImplementedError):
            raise ValueError("Deriver must implement the transform_stream method.")
        return deriver
    return deriver


def get_deriver_from_script(script: str) -> type[Deriver]:
    tree = ast.parse(script)
    if len(tree.body) != 1:
        raise ValueError("Script must define exactly one class.")

    class_def = tree.body[0]
    if not isinstance(class_def, ast.ClassDef):
        raise ValueError("Script must define a class.")

    namespace: dict[str, Any] = {}
    exec(script, globals(), namespace)

    cls = namespace.get(class_def.name)
    if isinstance(cls, type):
        return validate_deriver(cls)
    raise ValueError("No valid Deriver subclass found in script.")
