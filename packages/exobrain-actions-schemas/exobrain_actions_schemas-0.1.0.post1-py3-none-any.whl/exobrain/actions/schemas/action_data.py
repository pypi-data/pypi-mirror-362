import typing as t
from enum import StrEnum
from uuid import UUID

from exobrain.actions.schemas.base_model import BaseModel
from pydantic import ConfigDict


class ActionSetting(BaseModel):
    """Defines the configuration settings for an action, including type and default values."""

    choice: bool
    default_value: t.Any
    name: str
    required: bool | None = None
    type: str | None = None


class ContextDataType(StrEnum):
    """Enumerates the possible data types for context values in actions."""

    AMOUNT = "AMOUNT"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    NUMBER = "NUMBER"
    STRING = "STRING"


class ContextDict(t.TypedDict):
    """Defines the structure for context type information."""

    TYPE: ContextDataType


class DataNeeded(BaseModel):
    """
    Specifies the required data structure for an action,
    including context, inputs, and outputs.
    """

    # noinspection PyTypeChecker
    model_config = ConfigDict(
        alias_generator=str.upper,
        populate_by_name=True,
        extra="forbid",
    )

    context: dict[str, ContextDict]
    inputs: dict[str, dict[str, t.Any]]
    outputs: dict[str, dict[str, t.Any]]


class ActionData(BaseModel):
    """
    Action data schema, including settings, required data, KPIs, and reason codes.
    """

    action_settings: dict[str, ActionSetting]
    data_needed: DataNeeded
    kpis: list[str]
    name: str
    reasons: list[UUID]
