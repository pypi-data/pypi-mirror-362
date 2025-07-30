"""
Project service layer for business logic implementation.

This module implements the business logic for project management operations,
providing a clean interface between the web layer and data layer.
"""

from typing import Any, Dict, List, Optional

from ...core.base.database_manager import BaseDatabaseManager
from ...core.base.service_base import ServiceResult, TenantAwareService
from ...core.exceptions.base import ValidationException
from ..models.project import (
    Project,
    ProjectMember,
    ProjectMemberRole,
    ProjectPrompt,
    ProjectRule,
    ProjectType,
    ProjectVersion,
    ProjectVisibility,
)
from ..repositories.project_repository import (
    ProjectMemberRepository,
    ProjectPromptRepository,
    ProjectRepository,
    ProjectRuleRepository,
    ProjectVersionRepository,
)


class ProjectService(TenantAwareService):
    """Service class for project management operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project service with database manager."""
        super().__init__("ProjectService")
        self.db_manager = db_manager

        # Initialize repositories
        self.project_repo = ProjectRepository(db_manager)
        self.member_repo = ProjectMemberRepository(db_manager)
        self.prompt_repo = ProjectPromptRepository(db_manager)
        self.rule_repo = ProjectRuleRepository(db_manager)
        self.version_repo = ProjectVersionRepository(db_manager)

    def set_context(self, tenant_id: str, user_id: str) -> None:
        """Set tenant and user context for all repositories."""
        super().set_context(tenant_id, user_id)

        # Set context for all repositories
        self.project_repo.set_tenant_context(tenant_id)
        self.member_repo.set_tenant_context(tenant_id)
        self.prompt_repo.set_tenant_context(tenant_id)
        self.rule_repo.set_tenant_context(tenant_id)
        self.version_repo.set_tenant_context(tenant_id)

    # Project CRUD Operations

    def create_project(self, project_data: Dict[str, Any]) -> ServiceResult[Project]:
        """
        Create a new project.

        Args:
            project_data: Project creation data

        Returns:
            ServiceResult containing the created project or error
        """
        try:
            self.ensure_tenant_context()

            # Validate required fields
            self.validate_required_fields(project_data, ["name", "title"])

            # Validate field types
            self.validate_field_types(
                project_data,
                {
                    "name": str,
                    "title": str,
                    "description": str,
                    "project_type": str,
                    "visibility": str,
                    "shared_with_tenant": bool,
                },
            )

            # Sanitize input
            sanitized_data = self.sanitize_input(project_data)

            # Validate project name is unique
            existing_project = self.project_repo.find_by_name(sanitized_data["name"])
            if existing_project:
                return ServiceResult.error_result(
                    f"Project with name '{sanitized_data['name']}' already exists",
                    error_code="PROJECT_NAME_EXISTS",
                )

            # Validate project type and visibility
            project_type = sanitized_data.get("project_type", "general")
            if project_type not in [pt.value for pt in ProjectType]:
                return ServiceResult.error_result(
                    f"Invalid project type: {project_type}",
                    error_code="INVALID_PROJECT_TYPE",
                )

            visibility = sanitized_data.get("visibility", "private")
            if visibility not in [pv.value for pv in ProjectVisibility]:
                return ServiceResult.error_result(
                    f"Invalid visibility: {visibility}", error_code="INVALID_VISIBILITY"
                )

            # Create project entity
            project = Project(
                tenant_id=self.current_tenant_id,
                user_id=self.current_user_id,
                name=sanitized_data["name"],
                title=sanitized_data["title"],
                description=sanitized_data.get("description", ""),
                project_type=ProjectType(project_type),
                visibility=ProjectVisibility(visibility),
                shared_with_tenant=sanitized_data.get("shared_with_tenant", False),
            )

            # Save project
            saved_project = self.project_repo.save(project)

            # Add creator as owner
            owner_member = ProjectMember(
                project_id=saved_project.id,
                user_id=self.current_user_id,
                role=ProjectMemberRole.OWNER,
            )
            self.member_repo.save(owner_member)

            self.log_operation(
                "create_project",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={
                    "project_id": saved_project.id,
                    "project_name": saved_project.name,
                },
            )

            return ServiceResult.success_result(saved_project)

        except ValidationException as e:
            return self.handle_error("create project", e)
        except Exception as e:
            return self.handle_error("create project", e)

    def get_project(self, project_id: int) -> ServiceResult[Project]:
        """
        Get a project by ID with access control.

        Args:
            project_id: Project ID

        Returns:
            ServiceResult containing the project or error
        """
        try:
            self.ensure_tenant_context()

            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            # Check access permissions
            if not self._can_access_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Access denied to project", error_code="PROJECT_ACCESS_DENIED"
                )

            return ServiceResult.success_result(project)

        except Exception as e:
            return self.handle_error("get project", e)

    def update_project(
        self, project_id: int, update_data: Dict[str, Any]
    ) -> ServiceResult[Project]:
        """
        Update an existing project.

        Args:
            project_id: Project ID
            update_data: Fields to update

        Returns:
            ServiceResult containing the updated project or error
        """
        try:
            self.ensure_tenant_context()

            # Get existing project
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to edit project",
                    error_code="PROJECT_EDIT_DENIED",
                )

            # Validate and sanitize update data
            sanitized_data = self.sanitize_input(update_data)

            # Update allowed fields
            if "title" in sanitized_data:
                project.title = sanitized_data["title"]
            if "description" in sanitized_data:
                project.description = sanitized_data["description"]
            if "project_type" in sanitized_data:
                try:
                    project.project_type = ProjectType(sanitized_data["project_type"])
                except ValueError:
                    return ServiceResult.error_result(
                        f"Invalid project type: {sanitized_data['project_type']}",
                        error_code="INVALID_PROJECT_TYPE",
                    )
            if "visibility" in sanitized_data:
                try:
                    project.visibility = ProjectVisibility(sanitized_data["visibility"])
                except ValueError:
                    return ServiceResult.error_result(
                        f"Invalid visibility: {sanitized_data['visibility']}",
                        error_code="INVALID_VISIBILITY",
                    )
            if "shared_with_tenant" in sanitized_data:
                project.shared_with_tenant = bool(sanitized_data["shared_with_tenant"])

            # Save updated project
            updated_project = self.project_repo.save(project)

            self.log_operation(
                "update_project",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={
                    "project_id": project_id,
                    "updated_fields": list(sanitized_data.keys()),
                },
            )

            return ServiceResult.success_result(updated_project)

        except Exception as e:
            return self.handle_error("update project", e)

    def delete_project(self, project_id: int) -> ServiceResult[bool]:
        """
        Delete a project (only by owner).

        Args:
            project_id: Project ID

        Returns:
            ServiceResult indicating success or error
        """
        try:
            self.ensure_tenant_context()

            # Get existing project
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            # Check ownership
            if project.user_id != self.current_user_id:
                return ServiceResult.error_result(
                    "Only project owner can delete project",
                    error_code="PROJECT_DELETE_DENIED",
                )

            # Delete project (cascade will handle related records)
            success = self.project_repo.delete(project_id)

            if success:
                self.log_operation(
                    "delete_project",
                    user_id=self.current_user_id,
                    tenant_id=self.current_tenant_id,
                    details={"project_id": project_id, "project_name": project.name},
                )

            return ServiceResult.success_result(success)

        except Exception as e:
            return self.handle_error("delete project", e)

    def get_user_projects(
        self, include_shared: bool = True
    ) -> ServiceResult[List[Project]]:
        """
        Get all projects accessible to the current user.

        Args:
            include_shared: Whether to include shared projects

        Returns:
            ServiceResult containing list of projects
        """
        try:
            self.ensure_tenant_context()

            if include_shared:
                projects = self.project_repo.find_accessible_projects(
                    self.current_user_id
                )
            else:
                projects = self.project_repo.find_by_user(self.current_user_id)

            return ServiceResult.success_result(projects)

        except Exception as e:
            return self.handle_error("get user projects", e)

    # Project Member Management

    def add_project_member(
        self, project_id: int, user_id: str, role: str = "member"
    ) -> ServiceResult[ProjectMember]:
        """
        Add a member to a project.

        Args:
            project_id: Project ID
            user_id: User ID to add
            role: Member role

        Returns:
            ServiceResult containing the added member or error
        """
        try:
            self.ensure_tenant_context()

            # Check if user is project owner
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            if project.user_id != self.current_user_id:
                return ServiceResult.error_result(
                    "Only project owner can add members",
                    error_code="PROJECT_MEMBER_ADD_DENIED",
                )

            # Validate role
            try:
                member_role = ProjectMemberRole(role)
            except ValueError:
                return ServiceResult.error_result(
                    f"Invalid role: {role}", error_code="INVALID_MEMBER_ROLE"
                )

            # Check if user is already a member
            existing_member = self.member_repo.find_member(project_id, user_id)
            if existing_member:
                return ServiceResult.error_result(
                    "User is already a member of this project",
                    error_code="USER_ALREADY_MEMBER",
                )

            # Create new member
            member = ProjectMember(
                project_id=project_id,
                user_id=user_id,
                role=member_role,
            )

            saved_member = self.member_repo.save(member)

            self.log_operation(
                "add_project_member",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={
                    "project_id": project_id,
                    "added_user_id": user_id,
                    "role": role,
                },
            )

            return ServiceResult.success_result(saved_member)

        except Exception as e:
            return self.handle_error("add project member", e)

    def remove_project_member(
        self, project_id: int, user_id: str
    ) -> ServiceResult[bool]:
        """
        Remove a member from a project.

        Args:
            project_id: Project ID
            user_id: User ID to remove

        Returns:
            ServiceResult indicating success or error
        """
        try:
            self.ensure_tenant_context()

            # Check if user is project owner
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            if project.user_id != self.current_user_id:
                return ServiceResult.error_result(
                    "Only project owner can remove members",
                    error_code="PROJECT_MEMBER_REMOVE_DENIED",
                )

            # Can't remove the owner
            if user_id == self.current_user_id:
                return ServiceResult.error_result(
                    "Project owner cannot be removed", error_code="CANNOT_REMOVE_OWNER"
                )

            # Remove member
            success = self.member_repo.remove_member(project_id, user_id)

            if success:
                self.log_operation(
                    "remove_project_member",
                    user_id=self.current_user_id,
                    tenant_id=self.current_tenant_id,
                    details={"project_id": project_id, "removed_user_id": user_id},
                )

            return ServiceResult.success_result(success)

        except Exception as e:
            return self.handle_error("remove project member", e)

    def get_project_members(
        self, project_id: int
    ) -> ServiceResult[List[ProjectMember]]:
        """
        Get all members of a project.

        Args:
            project_id: Project ID

        Returns:
            ServiceResult containing list of members
        """
        try:
            self.ensure_tenant_context()

            # Check access to project
            if not self._can_access_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Access denied to project", error_code="PROJECT_ACCESS_DENIED"
                )

            members = self.member_repo.find_by_project(project_id)
            return ServiceResult.success_result(members)

        except Exception as e:
            return self.handle_error("get project members", e)

    # Project Prompt Management

    def add_prompt_to_project(
        self, project_id: int, prompt_id: int, sequence_order: int = 0
    ) -> ServiceResult[ProjectPrompt]:
        """
        Add a prompt to a project.

        Args:
            project_id: Project ID
            prompt_id: Prompt ID
            sequence_order: Order for sequenced projects

        Returns:
            ServiceResult containing the association or error
        """
        try:
            self.ensure_tenant_context()

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to modify project",
                    error_code="PROJECT_EDIT_DENIED",
                )

            # TODO: Validate prompt exists and check visibility constraints
            # This would require a prompt repository/service integration

            # Check if prompt is already in project
            existing_association = self.prompt_repo.find_association(
                project_id, prompt_id
            )
            if existing_association:
                return ServiceResult.error_result(
                    "Prompt is already in this project",
                    error_code="PROMPT_ALREADY_IN_PROJECT",
                )

            # Create association
            project_prompt = ProjectPrompt(
                project_id=project_id,
                prompt_id=prompt_id,
                sequence_order=sequence_order,
            )

            saved_association = self.prompt_repo.save(project_prompt)

            self.log_operation(
                "add_prompt_to_project",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={
                    "project_id": project_id,
                    "prompt_id": prompt_id,
                    "sequence_order": sequence_order,
                },
            )

            return ServiceResult.success_result(saved_association)

        except Exception as e:
            return self.handle_error("add prompt to project", e)

    def remove_prompt_from_project(
        self, project_id: int, prompt_id: int
    ) -> ServiceResult[bool]:
        """
        Remove a prompt from a project.

        Args:
            project_id: Project ID
            prompt_id: Prompt ID

        Returns:
            ServiceResult indicating success or error
        """
        try:
            self.ensure_tenant_context()

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to modify project",
                    error_code="PROJECT_EDIT_DENIED",
                )

            # Remove association
            success = self.prompt_repo.remove_association(project_id, prompt_id)

            if success:
                self.log_operation(
                    "remove_prompt_from_project",
                    user_id=self.current_user_id,
                    tenant_id=self.current_tenant_id,
                    details={"project_id": project_id, "prompt_id": prompt_id},
                )

            return ServiceResult.success_result(success)

        except Exception as e:
            return self.handle_error("remove prompt from project", e)

    def get_project_prompts(
        self, project_id: int
    ) -> ServiceResult[List[ProjectPrompt]]:
        """
        Get all prompts in a project.

        Args:
            project_id: Project ID

        Returns:
            ServiceResult containing list of project prompts
        """
        try:
            self.ensure_tenant_context()

            # Check access to project
            if not self._can_access_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Access denied to project", error_code="PROJECT_ACCESS_DENIED"
                )

            prompts = self.prompt_repo.find_by_project(project_id)
            return ServiceResult.success_result(prompts)

        except Exception as e:
            return self.handle_error("get project prompts", e)

    # Project Rule Management

    def add_rule_to_project(
        self, project_id: int, rule_id: int, rule_set_name: Optional[str] = None
    ) -> ServiceResult[ProjectRule]:
        """
        Add a rule to a project.

        Args:
            project_id: Project ID
            rule_id: Rule ID
            rule_set_name: Optional rule set name for grouping

        Returns:
            ServiceResult containing the association or error
        """
        try:
            self.ensure_tenant_context()

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to modify project",
                    error_code="PROJECT_EDIT_DENIED",
                )

            # TODO: Validate rule exists
            # This would require a rule repository/service integration

            # Check if rule is already in project
            existing_association = self.rule_repo.find_association(project_id, rule_id)
            if existing_association:
                return ServiceResult.error_result(
                    "Rule is already in this project",
                    error_code="RULE_ALREADY_IN_PROJECT",
                )

            # Create association
            project_rule = ProjectRule(
                project_id=project_id,
                rule_id=rule_id,
                rule_set_name=rule_set_name,
            )

            saved_association = self.rule_repo.save(project_rule)

            self.log_operation(
                "add_rule_to_project",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={
                    "project_id": project_id,
                    "rule_id": rule_id,
                    "rule_set_name": rule_set_name,
                },
            )

            return ServiceResult.success_result(saved_association)

        except Exception as e:
            return self.handle_error("add rule to project", e)

    def remove_rule_from_project(
        self, project_id: int, rule_id: int
    ) -> ServiceResult[bool]:
        """
        Remove a rule from a project.

        Args:
            project_id: Project ID
            rule_id: Rule ID

        Returns:
            ServiceResult indicating success or error
        """
        try:
            self.ensure_tenant_context()

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to modify project",
                    error_code="PROJECT_EDIT_DENIED",
                )

            # Remove association
            success = self.rule_repo.remove_association(project_id, rule_id)

            if success:
                self.log_operation(
                    "remove_rule_from_project",
                    user_id=self.current_user_id,
                    tenant_id=self.current_tenant_id,
                    details={"project_id": project_id, "rule_id": rule_id},
                )

            return ServiceResult.success_result(success)

        except Exception as e:
            return self.handle_error("remove rule from project", e)

    def get_project_rules(self, project_id: int) -> ServiceResult[List[ProjectRule]]:
        """
        Get all rules in a project.

        Args:
            project_id: Project ID

        Returns:
            ServiceResult containing list of project rules
        """
        try:
            self.ensure_tenant_context()

            # Check access to project
            if not self._can_access_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Access denied to project", error_code="PROJECT_ACCESS_DENIED"
                )

            rules = self.rule_repo.find_by_project(project_id)
            return ServiceResult.success_result(rules)

        except Exception as e:
            return self.handle_error("get project rules", e)

    # Project Versioning

    def create_project_version(
        self, project_id: int, changes_description: str = ""
    ) -> ServiceResult[ProjectVersion]:
        """
        Create a new version of a project.

        Args:
            project_id: Project ID
            changes_description: Description of changes

        Returns:
            ServiceResult containing the new version or error
        """
        try:
            self.ensure_tenant_context()

            # Check edit permissions
            if not self._can_edit_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Permission denied to version project",
                    error_code="PROJECT_VERSION_DENIED",
                )

            # Get project to increment version
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return ServiceResult.error_result(
                    "Project not found", error_code="PROJECT_NOT_FOUND"
                )

            # Get next version number
            next_version = self.version_repo.get_next_version_number(project_id)

            # Update project version
            project.increment_version()
            self.project_repo.save(project)

            # Create version record
            version = ProjectVersion(
                project_id=project_id,
                version_number=next_version,
                changes_description=changes_description,
                created_by=self.current_user_id,
            )

            saved_version = self.version_repo.save(version)

            self.log_operation(
                "create_project_version",
                user_id=self.current_user_id,
                tenant_id=self.current_tenant_id,
                details={"project_id": project_id, "version_number": next_version},
            )

            return ServiceResult.success_result(saved_version)

        except Exception as e:
            return self.handle_error("create project version", e)

    def get_project_versions(
        self, project_id: int
    ) -> ServiceResult[List[ProjectVersion]]:
        """
        Get all versions of a project.

        Args:
            project_id: Project ID

        Returns:
            ServiceResult containing list of versions
        """
        try:
            self.ensure_tenant_context()

            # Check access to project
            if not self._can_access_project(project_id, self.current_user_id):
                return ServiceResult.error_result(
                    "Access denied to project", error_code="PROJECT_ACCESS_DENIED"
                )

            versions = self.version_repo.find_by_project(project_id)
            return ServiceResult.success_result(versions)

        except Exception as e:
            return self.handle_error("get project versions", e)

    # Permission Helper Methods

    def _can_access_project(self, project_id: int, user_id: str) -> bool:
        """Check if user can access a project."""
        try:
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return False

            # Owner can always access
            if project.user_id == user_id:
                return True

            # Public projects are accessible to all
            if project.visibility == ProjectVisibility.PUBLIC:
                return True

            # Projects shared with tenant are accessible to all tenant users
            if project.shared_with_tenant:
                return True

            # Check if user is a member
            return self.member_repo.is_member(project_id, user_id)

        except Exception:
            return False

    def _can_edit_project(self, project_id: int, user_id: str) -> bool:
        """Check if user can edit a project."""
        try:
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return False

            # Owner can always edit
            if project.user_id == user_id:
                return True

            # Check if user is a member with edit permissions
            user_role = self.member_repo.get_user_role(project_id, user_id)
            return user_role in [ProjectMemberRole.OWNER, ProjectMemberRole.MEMBER]

        except Exception:
            return False

    def get_user_role_in_project(
        self, project_id: int, user_id: str
    ) -> Optional[ProjectMemberRole]:
        """Get user's role in a project."""
        try:
            project = self.project_repo.find_by_id(project_id)
            if not project:
                return None

            # Owner has owner role
            if project.user_id == user_id:
                return ProjectMemberRole.OWNER

            # Check membership role
            return self.member_repo.get_user_role(project_id, user_id)

        except Exception:
            return None
