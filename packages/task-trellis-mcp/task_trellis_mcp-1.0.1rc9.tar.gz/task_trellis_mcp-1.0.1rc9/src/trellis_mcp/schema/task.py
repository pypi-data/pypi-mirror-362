"""Task model for Trellis MCP.

Defines the schema for task objects in the Trellis MCP hierarchy.
"""

from pydantic import Field

from .base_schema import BaseSchemaModel
from .kind_enum import KindEnum
from .status_enum import StatusEnum


class TaskModel(BaseSchemaModel):
    """Schema model for task objects.

    Tasks are the leaf objects in the Trellis MCP hierarchy.
    They are contained within features and represent actionable work items.
    """

    kind: KindEnum = Field(KindEnum.TASK, description="Must be 'task'")

    # Status transition matrix for tasks (includes shortcuts)
    _valid_transitions = {
        StatusEnum.OPEN: {
            StatusEnum.IN_PROGRESS,
            StatusEnum.DONE,
            StatusEnum.DELETED,
        },  # Can skip to done
        StatusEnum.IN_PROGRESS: {
            StatusEnum.REVIEW,
            StatusEnum.DONE,
            StatusEnum.DELETED,
        },  # Can skip to done
        StatusEnum.REVIEW: {StatusEnum.DONE, StatusEnum.DELETED},
        StatusEnum.DONE: {StatusEnum.DELETED},  # Only deletion allowed from done
    }
