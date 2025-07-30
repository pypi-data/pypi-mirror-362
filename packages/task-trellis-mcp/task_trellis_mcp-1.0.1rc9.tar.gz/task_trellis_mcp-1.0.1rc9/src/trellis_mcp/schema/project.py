"""Project model for Trellis MCP.

Defines the schema for project objects in the Trellis MCP hierarchy.
"""

from pydantic import Field

from .base_schema import BaseSchemaModel
from .kind_enum import KindEnum
from .status_enum import StatusEnum


class ProjectModel(BaseSchemaModel):
    """Schema model for project objects.

    Projects are the top-level objects in the Trellis MCP hierarchy.
    They contain epics and have no parent.
    """

    kind: KindEnum = Field(KindEnum.PROJECT, description="Must be 'project'")

    # Status transition matrix for projects
    _valid_transitions = {
        StatusEnum.DRAFT: {StatusEnum.IN_PROGRESS, StatusEnum.DELETED},
        StatusEnum.IN_PROGRESS: {StatusEnum.DONE, StatusEnum.DELETED},
        StatusEnum.DONE: {StatusEnum.DELETED},  # Only deletion allowed from done
    }
