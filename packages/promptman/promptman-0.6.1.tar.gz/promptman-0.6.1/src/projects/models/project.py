"""
Project data models for the AI Prompt Manager application.

This module defines the Project class and related entities that represent
project management functionality with proper validation and serialization.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class ProjectType(Enum):
    """Project types defining different project workflows."""

    GENERAL = "general"
    SEQUENCED = "sequenced"
    LLM_COMPARISON = "llm_comparison"
    DEVELOPER = "developer"


class ProjectVisibility(Enum):
    """Project visibility levels."""

    PRIVATE = "private"
    PUBLIC = "public"


class ProjectMemberRole(Enum):
    """Project member roles defining access levels."""

    OWNER = "owner"
    MEMBER = "member"
    VIEWER = "viewer"


@dataclass
class Project:
    """
    Project entity representing a project in the system.

    This class encapsulates all project-related data and provides
    methods for project operations and validation.
    """

    # Required fields
    tenant_id: str
    user_id: str  # Project owner
    name: str
    title: str

    # Optional fields with defaults
    id: Optional[int] = None
    description: Optional[str] = None
    project_type: ProjectType = ProjectType.GENERAL
    visibility: ProjectVisibility = ProjectVisibility.PRIVATE
    shared_with_tenant: bool = False
    version: int = 1
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Ensure enums are proper types
        if isinstance(self.project_type, str):
            self.project_type = ProjectType(self.project_type)
        if isinstance(self.visibility, str):
            self.visibility = ProjectVisibility(self.visibility)

        # Set default timestamps
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

        if self.updated_at is None:
            self.updated_at = self.created_at

        # Validate required fields
        self._validate_fields()

    def _validate_fields(self) -> None:
        """Validate required fields and constraints."""
        if not self.name or not self.name.strip():
            raise ValueError("Project name cannot be empty")

        if not self.title or not self.title.strip():
            raise ValueError("Project title cannot be empty")

        if not self.tenant_id:
            raise ValueError("Tenant ID is required")

        if not self.user_id:
            raise ValueError("User ID is required")

        # Validate name format
        import re

        if not re.match(r"^[a-zA-Z0-9\s\-_]+$", self.name):
            raise ValueError(
                "Project name can only contain letters, numbers, spaces, "
                "hyphens, and underscores"
            )

    @property
    def is_public(self) -> bool:
        """Check if project is public."""
        return self.visibility == ProjectVisibility.PUBLIC

    @property
    def is_private(self) -> bool:
        """Check if project is private."""
        return self.visibility == ProjectVisibility.PRIVATE

    @property
    def is_general(self) -> bool:
        """Check if project is general type."""
        return self.project_type == ProjectType.GENERAL

    @property
    def is_sequenced(self) -> bool:
        """Check if project is sequenced type."""
        return self.project_type == ProjectType.SEQUENCED

    @property
    def is_llm_comparison(self) -> bool:
        """Check if project is LLM comparison type."""
        return self.project_type == ProjectType.LLM_COMPARISON

    @property
    def is_developer(self) -> bool:
        """Check if project is developer type."""
        return self.project_type == ProjectType.DEVELOPER

    def set_visibility(self, visibility: ProjectVisibility) -> None:
        """Set project visibility."""
        self.visibility = visibility
        self.updated_at = datetime.now(timezone.utc)

    def set_project_type(self, project_type: ProjectType) -> None:
        """Set project type."""
        self.project_type = project_type
        self.updated_at = datetime.now(timezone.utc)

    def set_description(self, description: str) -> None:
        """Set project description."""
        self.description = description
        self.updated_at = datetime.now(timezone.utc)

    def share_with_tenant(self, shared: bool = True) -> None:
        """Share or unshare project with tenant."""
        self.shared_with_tenant = shared
        self.updated_at = datetime.now(timezone.utc)

    def increment_version(self, changes_description: Optional[str] = None) -> int:
        """Increment project version."""
        self.version += 1
        self.updated_at = datetime.now(timezone.utc)
        return self.version

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value."""
        return self.metadata.get(key, default)

    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        self.metadata[key] = value
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self, include_metadata: bool = True) -> Dict[str, Any]:
        """
        Convert project to dictionary representation.

        Args:
            include_metadata: Whether to include metadata

        Returns:
            Dictionary representation of project
        """
        project_dict = {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
            "name": self.name,
            "title": self.title,
            "description": self.description,
            "project_type": self.project_type.value,
            "visibility": self.visibility.value,
            "shared_with_tenant": self.shared_with_tenant,
            "version": self.version,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_metadata:
            project_dict["metadata"] = self.metadata

        return project_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """
        Create Project from dictionary.

        Args:
            data: Dictionary containing project data

        Returns:
            Project instance
        """
        # Handle datetime fields
        created_at = None
        if data.get("created_at"):
            if isinstance(data["created_at"], str):
                created_at = datetime.fromisoformat(
                    data["created_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["created_at"], datetime):
                created_at = data["created_at"]

        updated_at = None
        if data.get("updated_at"):
            if isinstance(data["updated_at"], str):
                updated_at = datetime.fromisoformat(
                    data["updated_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["updated_at"], datetime):
                updated_at = data["updated_at"]

        return cls(
            id=data.get("id"),
            tenant_id=data["tenant_id"],
            user_id=data["user_id"],
            name=data["name"],
            title=data["title"],
            description=data.get("description"),
            project_type=ProjectType(data.get("project_type", "general")),
            visibility=ProjectVisibility(data.get("visibility", "private")),
            shared_with_tenant=data.get("shared_with_tenant", False),
            version=data.get("version", 1),
            created_at=created_at,
            updated_at=updated_at,
            metadata=data.get("metadata", {}),
        )

    def clone(
        self, new_name: Optional[str] = None, new_tenant_id: Optional[str] = None
    ) -> "Project":
        """
        Create a copy of this project.

        Args:
            new_name: New name for the cloned project
            new_tenant_id: New tenant ID for the cloned project

        Returns:
            New Project instance
        """
        cloned = Project(
            tenant_id=new_tenant_id or self.tenant_id,
            user_id=self.user_id,
            name=new_name or f"{self.name}_copy",
            title=self.title,
            description=self.description,
            project_type=self.project_type,
            visibility=self.visibility,
            shared_with_tenant=False,  # Don't copy sharing settings
            version=1,  # Reset version for cloned project
            metadata=self.metadata.copy(),
        )

        # Clear ID and timestamps for new project
        cloned.id = None
        cloned.created_at = datetime.now(timezone.utc)
        cloned.updated_at = cloned.created_at

        return cloned

    def __str__(self) -> str:
        """String representation of project."""
        return (
            f"Project(name={self.name}, type={self.project_type.value}, "
            f"tenant={self.tenant_id})"
        )

    def __repr__(self) -> str:
        """Detailed string representation of project."""
        return (
            f"Project(id={self.id}, name={self.name}, title={self.title}, "
            f"type={self.project_type.value}, visibility={self.visibility.value}, "
            f"tenant_id={self.tenant_id}, user_id={self.user_id})"
        )


@dataclass
class ProjectMember:
    """
    Project member entity representing user access to a project.
    """

    # Required fields
    project_id: int
    user_id: str
    role: ProjectMemberRole = ProjectMemberRole.MEMBER

    # Optional fields
    id: Optional[int] = None
    added_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Ensure role is proper type
        if isinstance(self.role, str):
            self.role = ProjectMemberRole(self.role)

        # Set default timestamp
        if self.added_at is None:
            self.added_at = datetime.now(timezone.utc)

    @property
    def is_owner(self) -> bool:
        """Check if member is owner."""
        return self.role == ProjectMemberRole.OWNER

    @property
    def is_member(self) -> bool:
        """Check if member has member role."""
        return self.role == ProjectMemberRole.MEMBER

    @property
    def is_viewer(self) -> bool:
        """Check if member is viewer."""
        return self.role == ProjectMemberRole.VIEWER

    @property
    def can_edit(self) -> bool:
        """Check if member can edit project."""
        return self.role in [ProjectMemberRole.OWNER, ProjectMemberRole.MEMBER]

    @property
    def can_manage(self) -> bool:
        """Check if member can manage project."""
        return self.role == ProjectMemberRole.OWNER

    def set_role(self, role: ProjectMemberRole) -> None:
        """Set member role."""
        self.role = role

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "role": self.role.value,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectMember":
        """Create ProjectMember from dictionary."""
        added_at = None
        if data.get("added_at"):
            if isinstance(data["added_at"], str):
                added_at = datetime.fromisoformat(
                    data["added_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["added_at"], datetime):
                added_at = data["added_at"]

        return cls(
            id=data.get("id"),
            project_id=data["project_id"],
            user_id=data["user_id"],
            role=ProjectMemberRole(data.get("role", "member")),
            added_at=added_at,
        )


@dataclass
class ProjectPrompt:
    """
    Project prompt entity representing a prompt association with a project.
    """

    # Required fields
    project_id: int
    prompt_id: int

    # Optional fields
    id: Optional[int] = None
    sequence_order: int = 0
    added_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Set default timestamp
        if self.added_at is None:
            self.added_at = datetime.now(timezone.utc)

    def set_sequence_order(self, order: int) -> None:
        """Set sequence order for sequenced projects."""
        self.sequence_order = order

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "prompt_id": self.prompt_id,
            "sequence_order": self.sequence_order,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectPrompt":
        """Create ProjectPrompt from dictionary."""
        added_at = None
        if data.get("added_at"):
            if isinstance(data["added_at"], str):
                added_at = datetime.fromisoformat(
                    data["added_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["added_at"], datetime):
                added_at = data["added_at"]

        return cls(
            id=data.get("id"),
            project_id=data["project_id"],
            prompt_id=data["prompt_id"],
            sequence_order=data.get("sequence_order", 0),
            added_at=added_at,
        )


@dataclass
class ProjectRule:
    """
    Project rule entity representing a rule association with a project.
    """

    # Required fields
    project_id: int
    rule_id: int

    # Optional fields
    id: Optional[int] = None
    rule_set_name: Optional[str] = None
    added_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Set default timestamp
        if self.added_at is None:
            self.added_at = datetime.now(timezone.utc)

    def set_rule_set_name(self, rule_set_name: str) -> None:
        """Set rule set name for grouping rules."""
        self.rule_set_name = rule_set_name

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "rule_id": self.rule_id,
            "rule_set_name": self.rule_set_name,
            "added_at": self.added_at.isoformat() if self.added_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectRule":
        """Create ProjectRule from dictionary."""
        added_at = None
        if data.get("added_at"):
            if isinstance(data["added_at"], str):
                added_at = datetime.fromisoformat(
                    data["added_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["added_at"], datetime):
                added_at = data["added_at"]

        return cls(
            id=data.get("id"),
            project_id=data["project_id"],
            rule_id=data["rule_id"],
            rule_set_name=data.get("rule_set_name"),
            added_at=added_at,
        )


@dataclass
class ProjectVersion:
    """
    Project version entity representing version tracking for projects.
    """

    # Required fields
    project_id: int
    version_number: int

    # Optional fields
    id: Optional[int] = None
    changes_description: Optional[str] = None
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization validation and setup."""
        # Set default timestamp
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

    def set_changes_description(self, description: str) -> None:
        """Set changes description."""
        self.changes_description = description

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "version_number": self.version_number,
            "changes_description": self.changes_description,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectVersion":
        """Create ProjectVersion from dictionary."""
        created_at = None
        if data.get("created_at"):
            if isinstance(data["created_at"], str):
                created_at = datetime.fromisoformat(
                    data["created_at"].replace("Z", "+00:00")
                )
            elif isinstance(data["created_at"], datetime):
                created_at = data["created_at"]

        return cls(
            id=data.get("id"),
            project_id=data["project_id"],
            version_number=data["version_number"],
            changes_description=data.get("changes_description"),
            created_by=data.get("created_by"),
            created_at=created_at,
        )
