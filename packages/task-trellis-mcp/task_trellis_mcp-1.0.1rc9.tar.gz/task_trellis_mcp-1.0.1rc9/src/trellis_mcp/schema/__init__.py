"""Trellis MCP Schema Package.

This package contains Pydantic models for the Trellis MCP v1.0 specification.
It provides type-safe data structures for Projects, Epics, Features, and Tasks
with validation and serialization capabilities.
"""

from typing import Type

from ..models.common import Priority
from .base import TrellisBaseModel
from .base_schema import BaseSchemaModel
from .epic import EpicModel
from .feature import FeatureModel
from .kind_enum import KindEnum
from .project import ProjectModel
from .status_enum import StatusEnum
from .task import TaskModel


def get_model_class_for_kind(kind: str | KindEnum) -> Type[BaseSchemaModel]:
    """Get the appropriate Pydantic model class for a given object kind.

    Args:
        kind: The object kind (string or KindEnum)

    Returns:
        The Pydantic model class for the given kind

    Raises:
        ValueError: If the kind is invalid
    """
    # Convert string to enum if needed
    if isinstance(kind, str):
        try:
            kind_enum = KindEnum(kind)
        except ValueError:
            raise ValueError(
                f"Invalid kind '{kind}'. Must be one of: {[k.value for k in KindEnum]}"
            )
    else:
        kind_enum = kind

    # Map kinds to model classes
    model_mapping: dict[KindEnum, Type[BaseSchemaModel]] = {
        KindEnum.PROJECT: ProjectModel,
        KindEnum.EPIC: EpicModel,
        KindEnum.FEATURE: FeatureModel,
        KindEnum.TASK: TaskModel,
    }

    return model_mapping[kind_enum]


__all__ = [
    "TrellisBaseModel",
    "BaseSchemaModel",
    "EpicModel",
    "FeatureModel",
    "KindEnum",
    "Priority",
    "ProjectModel",
    "StatusEnum",
    "TaskModel",
    "get_model_class_for_kind",
]
