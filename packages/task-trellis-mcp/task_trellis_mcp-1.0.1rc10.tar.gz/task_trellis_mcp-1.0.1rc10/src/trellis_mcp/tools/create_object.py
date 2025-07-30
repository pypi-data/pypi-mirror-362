"""Create object tool for Trellis MCP server.

Creates new Trellis MCP objects (Project, Epic, Feature, or Task) with proper YAML
front-matter and Markdown structure. Handles ID generation, validation, and
acyclic dependency checking.
"""

from datetime import datetime

from fastmcp import FastMCP

from ..fs_utils import ensure_parent_dirs
from ..graph_utils import DependencyGraph
from ..id_utils import generate_id
from ..io_utils import write_markdown
from ..path_resolver import resolve_path_for_new_object, resolve_project_roots
from ..settings import Settings
from ..validation import (
    TrellisValidationError,
    validate_front_matter,
    validate_object_data,
)


def create_create_object_tool(settings: Settings):
    """Create a createObject tool configured with the provided settings.

    Args:
        settings: Server configuration settings

    Returns:
        Configured createObject tool function
    """
    mcp = FastMCP()

    @mcp.tool
    def createObject(
        kind: str,
        title: str,
        projectRoot: str,
        id: str = "",
        parent: str = "",
        status: str = "",
        priority: str = "",
        prerequisites: list[str] = [],
        description: str = "",
    ) -> dict[str, str]:
        """Create a new Trellis MCP object (Project, Epic, Feature, or Task).

        Creates a new object file with proper YAML front-matter and Markdown structure.
        When no ID is provided, automatically generates a unique ID based on the title.
        Uses comprehensive validation to ensure object consistency and acyclic prerequisites.

        Args:
            kind: Object type ('project', 'epic', 'feature', or 'task')
            title: Human-readable title for the object
            projectRoot: Root directory for the planning structure
            id: Optional custom ID (auto-generated if not provided)
            parent: Parent object ID (required for epics, features, tasks)
            status: Object status (defaults based on kind)
            priority: Priority level ('high', 'normal', 'low' - defaults to 'normal')
            prerequisites: List of prerequisite object IDs (defaults to empty list)
            description: Optional description for the object body

        Returns:
            Dictionary containing the created object information including id, file_path, and status

        Raises:
            ValueError: If kind is invalid or required parameters are missing
            TrellisValidationError: If validation fails (front-matter, object data,
                or acyclic prerequisites)
            FileExistsError: If object with the same ID already exists
            OSError: If file cannot be created due to permissions or disk space
        """
        # Basic parameter validation
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")

        if not projectRoot or not projectRoot.strip():
            raise ValueError("Project root cannot be empty")

        # Resolve project roots to get planning directory
        _, planning_root = resolve_project_roots(projectRoot)

        # Generate ID if not provided
        if not id or not id.strip():
            id = generate_id(kind, title, planning_root)

        # Set default status based on kind
        if not status or not status.strip():
            status = "draft" if kind in {"project", "epic", "feature"} else "open"

        # Set default priority
        if not priority or not priority.strip():
            priority = "normal"

        # Set default prerequisites
        if not prerequisites:
            prerequisites = []

        # Generate timestamps
        now = datetime.now().isoformat()

        # Create YAML front-matter
        front_matter = {
            "kind": kind,
            "id": f"{kind[0].upper()}-{id}",
            "title": title,
            "status": status,
            "priority": priority,
            "prerequisites": prerequisites,
            "created": now,
            "updated": now,
            "schema_version": settings.schema_version,
        }

        # Add parent if provided
        if parent and parent.strip():
            front_matter["parent"] = parent

        # Validate front-matter using validation utilities
        try:
            front_matter_errors = validate_front_matter(front_matter, kind)
            if front_matter_errors:
                raise TrellisValidationError(front_matter_errors)
        except TrellisValidationError:
            raise
        except Exception as e:
            raise TrellisValidationError([f"Front-matter validation failed: {str(e)}"])

        # Comprehensive object validation (includes parent existence check)
        try:
            validate_object_data(front_matter, planning_root)
        except TrellisValidationError:
            raise
        except Exception as e:
            raise TrellisValidationError([f"Object validation failed: {str(e)}"])

        # Determine file path using centralized path logic
        try:
            file_path = resolve_path_for_new_object(kind, id, parent, planning_root, status)
        except ValueError as e:
            raise ValueError(str(e))
        except FileNotFoundError as e:
            raise ValueError(str(e))

        # Check if file already exists
        if file_path.exists():
            raise FileExistsError(f"Object with ID '{id}' already exists at {file_path}")

        # Ensure parent directories exist
        ensure_parent_dirs(file_path)

        # Create markdown body content
        body_content = ""
        if description and description.strip():
            body_content += f"{description}\n\n"
        body_content += "### Log\n\n"

        # Write file using io_utils
        try:
            write_markdown(file_path, front_matter, body_content)
        except OSError as e:
            raise OSError(f"Failed to create object file: {e}") from e

        # Validate acyclic prerequisites after file creation as fallback safety measure
        # This ensures the newly created object doesn't introduce cycles (defense in depth)
        try:
            # Build dependency graph with the new object included
            dependency_graph = DependencyGraph()
            dependency_graph.build(planning_root)

            # Check if the new object created a cycle
            if dependency_graph.has_cycle():
                # If cycles are detected, remove the created file and raise error
                try:
                    file_path.unlink()
                except OSError:
                    pass  # File removal failed, but we still need to report the cycle
                raise TrellisValidationError(
                    ["Creating this object would introduce circular dependencies in prerequisites"]
                )
        except TrellisValidationError:
            raise
        except Exception as e:
            # If cycle check fails for other reasons, remove the created file
            try:
                file_path.unlink()
            except OSError:
                pass
            raise TrellisValidationError([f"Failed to validate prerequisites: {str(e)}"])

        # Return success information
        return {
            "id": front_matter["id"],
            "kind": kind,
            "title": title,
            "status": status,
            "file_path": str(file_path),
            "created": now,
        }

    return createObject
