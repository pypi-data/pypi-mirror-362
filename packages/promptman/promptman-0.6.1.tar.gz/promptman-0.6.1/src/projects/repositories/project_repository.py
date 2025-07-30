"""
Project repositories for data access layer.

This module implements repository classes for project-related database operations
following the Repository pattern for clean separation of concerns.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ...core.base.database_manager import BaseDatabaseManager
from ...core.base.repository_base import TenantAwareRepository
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


class ProjectRepository(TenantAwareRepository[Project]):
    """Repository for project entity operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project repository."""
        super().__init__(db_manager, "projects")

    def _get_id_field(self) -> str:
        """Get the primary key field name."""
        return "id"

    def _row_to_entity(self, row: Dict[str, Any]) -> Project:
        """Convert database row to Project entity."""
        return Project.from_dict(row)

    def _entity_to_dict(self, entity: Project) -> Dict[str, Any]:
        """Convert Project entity to dictionary."""
        return entity.to_dict(include_metadata=False)

    def _dict_to_entity(self, entity_dict: Dict[str, Any]) -> Project:
        """Convert dictionary to Project entity."""
        return Project.from_dict(entity_dict)

    def find_by_name(self, name: str) -> Optional[Project]:
        """Find project by name within current tenant."""
        return self.find_one_by_field("name", name)

    def find_by_user(self, user_id: str) -> List[Project]:
        """Find all projects owned by a specific user."""
        return self.find_by_field("user_id", user_id)

    def find_accessible_projects(self, user_id: str) -> List[Project]:
        """
        Find all projects accessible to a user (owned, shared, or public).

        This includes:
        - Projects owned by the user
        - Projects where user is a member
        - Projects shared with tenant
        - Public projects
        """
        try:
            self._ensure_tenant_context()

            # Build complex query for accessible projects
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT DISTINCT p.* 
                    FROM projects p
                    LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = %s
                    WHERE p.tenant_id = %s 
                    AND (p.user_id = %s OR pm.user_id = %s OR p.shared_with_tenant = TRUE OR p.visibility = 'public')
                    ORDER BY 
                        CASE WHEN p.user_id = %s AND p.visibility = 'private' THEN 0 ELSE 1 END,
                        p.updated_at DESC
                """
                params = (user_id, self.current_tenant_id, user_id, user_id, user_id)
            else:
                query = """
                    SELECT DISTINCT p.* 
                    FROM projects p
                    LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = ?
                    WHERE p.tenant_id = ? 
                    AND (p.user_id = ? OR pm.user_id = ? OR p.shared_with_tenant = 1 OR p.visibility = 'public')
                    ORDER BY 
                        CASE WHEN p.user_id = ? AND p.visibility = 'private' THEN 0 ELSE 1 END,
                        p.updated_at DESC
                """
                params = (user_id, self.current_tenant_id, user_id, user_id, user_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding accessible projects for user {user_id}: {str(e)}"
            )
            raise

    def find_by_type(self, project_type: ProjectType) -> List[Project]:
        """Find projects by type."""
        return self.find_by_field("project_type", project_type.value)

    def find_public_projects(self) -> List[Project]:
        """Find all public projects in current tenant."""
        return self.find_by_field("visibility", ProjectVisibility.PUBLIC.value)

    def find_shared_projects(self) -> List[Project]:
        """Find all projects shared with current tenant."""
        return self.find_by_field("shared_with_tenant", True)


class ProjectMemberRepository(TenantAwareRepository[ProjectMember]):
    """Repository for project member entity operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project member repository."""
        super().__init__(db_manager, "project_members")

    def _get_id_field(self) -> str:
        """Get the primary key field name."""
        return "id"

    def _row_to_entity(self, row: Dict[str, Any]) -> ProjectMember:
        """Convert database row to ProjectMember entity."""
        return ProjectMember.from_dict(row)

    def _entity_to_dict(self, entity: ProjectMember) -> Dict[str, Any]:
        """Convert ProjectMember entity to dictionary."""
        return entity.to_dict()

    def _dict_to_entity(self, entity_dict: Dict[str, Any]) -> ProjectMember:
        """Convert dictionary to ProjectMember entity."""
        return ProjectMember.from_dict(entity_dict)

    def find_by_project(self, project_id: int) -> List[ProjectMember]:
        """Find all members of a project."""
        try:
            # Don't use tenant filtering for this table as it doesn't have tenant_id
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.project_id = %s AND p.tenant_id = %s
                    ORDER BY 
                        CASE pm.role 
                            WHEN 'owner' THEN 0 
                            WHEN 'member' THEN 1 
                            WHEN 'viewer' THEN 2 
                        END,
                        pm.added_at
                """
                params = (project_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.project_id = ? AND p.tenant_id = ?
                    ORDER BY 
                        CASE pm.role 
                            WHEN 'owner' THEN 0 
                            WHEN 'member' THEN 1 
                            WHEN 'viewer' THEN 2 
                        END,
                        pm.added_at
                """
                params = (project_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding members for project {project_id}: {str(e)}"
            )
            raise

    def find_by_user(self, user_id: str) -> List[ProjectMember]:
        """Find all project memberships for a user."""
        try:
            # Find memberships for projects in current tenant
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.user_id = %s AND p.tenant_id = %s
                    ORDER BY pm.added_at DESC
                """
                params = (user_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.user_id = ? AND p.tenant_id = ?
                    ORDER BY pm.added_at DESC
                """
                params = (user_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error finding memberships for user {user_id}: {str(e)}")
            raise

    def find_member(self, project_id: int, user_id: str) -> Optional[ProjectMember]:
        """Find specific project member."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.project_id = %s AND pm.user_id = %s AND p.tenant_id = %s
                """
                params = (project_id, user_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pm.* FROM project_members pm
                    JOIN projects p ON pm.project_id = p.id
                    WHERE pm.project_id = ? AND pm.user_id = ? AND p.tenant_id = ?
                """
                params = (project_id, user_id, self.current_tenant_id)

            row = self.db_manager.execute_query(query, params, fetch_one=True)
            return self._row_to_entity(row) if row else None

        except Exception as e:
            self.logger.error(
                f"Error finding member {user_id} in project {project_id}: {str(e)}"
            )
            raise

    def get_user_role(
        self, project_id: int, user_id: str
    ) -> Optional[ProjectMemberRole]:
        """Get user's role in a project."""
        member = self.find_member(project_id, user_id)
        return member.role if member else None

    def is_member(self, project_id: int, user_id: str) -> bool:
        """Check if user is a member of project."""
        return self.find_member(project_id, user_id) is not None

    def remove_member(self, project_id: int, user_id: str) -> bool:
        """Remove a member from project."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    DELETE FROM project_members 
                    WHERE project_id = %s AND user_id = %s
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = %s)
                """
                params = (project_id, user_id, self.current_tenant_id)
            else:
                query = """
                    DELETE FROM project_members 
                    WHERE project_id = ? AND user_id = ?
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = ?)
                """
                params = (project_id, user_id, self.current_tenant_id)

            affected_rows = self.db_manager.execute_query(query, params)
            return bool(affected_rows) and affected_rows > 0

        except Exception as e:
            self.logger.error(
                f"Error removing member {user_id} from project {project_id}: {str(e)}"
            )
            raise

    def save(self, entity: ProjectMember) -> ProjectMember:
        """Save project member entity (custom implementation without tenant_id)."""
        try:
            entity_dict = self._entity_to_dict(entity)

            # Check if this is an insert or update
            entity_id = entity_dict.get("id")

            if entity_id and self._member_exists(entity_id):
                # Update existing entity
                return self._update_member(entity_dict)
            else:
                # Insert new entity
                return self._insert_member(entity_dict)

        except Exception as e:
            self.logger.error(f"Error saving project member: {str(e)}")
            raise

    def _member_exists(self, member_id: int) -> bool:
        """Check if member exists."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = "SELECT 1 FROM project_members WHERE id = %s"
            else:
                query = "SELECT 1 FROM project_members WHERE id = ?"

            result = self.db_manager.execute_query(query, (member_id,), fetch_one=True)
            return result is not None

        except Exception:
            return False

    def _insert_member(self, entity_dict: Dict[str, Any]) -> ProjectMember:
        """Insert new project member."""
        # Add timestamp if not present
        if "added_at" not in entity_dict or entity_dict["added_at"] is None:
            entity_dict["added_at"] = datetime.now(timezone.utc)

        # Build INSERT query
        fields = [k for k, v in entity_dict.items() if v is not None and k != "id"]
        placeholders = ["?" for _ in fields]
        values = [entity_dict[field] for field in fields]

        if self.db_manager.config.db_type.value == "postgres":
            placeholders = ["%s" for _ in fields]
            query = f"""
                INSERT INTO project_members ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """

            row = self.db_manager.execute_query(query, tuple(values), fetch_one=True)
            return self._row_to_entity(row)
        else:
            query = f"""
                INSERT INTO project_members ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """

            with self.db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(values))
                conn.commit()

                # Get the last inserted row ID
                cursor.execute("SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]

                # Fetch the complete record
                cursor.execute("SELECT * FROM project_members WHERE id = ?", (last_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    row_dict = dict(zip(columns, row))
                    return self._row_to_entity(row_dict)
                else:
                    raise Exception(
                        f"Failed to retrieve inserted project member with ID {last_id}"
                    )

    def _update_member(self, entity_dict: Dict[str, Any]) -> ProjectMember:
        """Update existing project member."""
        member_id = entity_dict["id"]

        # Build UPDATE query
        update_fields = [
            k for k in entity_dict.keys() if k != "id" and entity_dict[k] is not None
        ]
        set_clauses = [f"{field} = ?" for field in update_fields]
        values = [entity_dict[field] for field in update_fields]
        values.append(member_id)

        query = f"""
            UPDATE project_members
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """

        if self.db_manager.config.db_type.value == "postgres":
            query = query.replace("?", "%s")

        affected_rows = self.db_manager.execute_query(query, tuple(values))

        if affected_rows == 0:
            raise Exception(f"No project member found with id = {member_id}")

        # Return updated entity
        if self.db_manager.config.db_type.value == "postgres":
            fetch_query = "SELECT * FROM project_members WHERE id = %s"
        else:
            fetch_query = "SELECT * FROM project_members WHERE id = ?"

        row = self.db_manager.execute_query(fetch_query, (member_id,), fetch_one=True)
        if not row:
            raise Exception(f"Failed to retrieve updated project member")

        return self._row_to_entity(row)


class ProjectPromptRepository(TenantAwareRepository[ProjectPrompt]):
    """Repository for project prompt entity operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project prompt repository."""
        super().__init__(db_manager, "project_prompts")

    def _get_id_field(self) -> str:
        """Get the primary key field name."""
        return "id"

    def _row_to_entity(self, row: Dict[str, Any]) -> ProjectPrompt:
        """Convert database row to ProjectPrompt entity."""
        return ProjectPrompt.from_dict(row)

    def _entity_to_dict(self, entity: ProjectPrompt) -> Dict[str, Any]:
        """Convert ProjectPrompt entity to dictionary."""
        return entity.to_dict()

    def _dict_to_entity(self, entity_dict: Dict[str, Any]) -> ProjectPrompt:
        """Convert dictionary to ProjectPrompt entity."""
        return ProjectPrompt.from_dict(entity_dict)

    def find_by_project(self, project_id: int) -> List[ProjectPrompt]:
        """Find all prompts in a project."""
        try:
            # Join with projects table to ensure tenant filtering
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.project_id = %s AND p.tenant_id = %s
                    ORDER BY pp.sequence_order, pp.added_at
                """
                params = (project_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.project_id = ? AND p.tenant_id = ?
                    ORDER BY pp.sequence_order, pp.added_at
                """
                params = (project_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding prompts for project {project_id}: {str(e)}"
            )
            raise

    def find_by_prompt(self, prompt_id: int) -> List[ProjectPrompt]:
        """Find all projects containing a specific prompt."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.prompt_id = %s AND p.tenant_id = %s
                    ORDER BY p.title
                """
                params = (prompt_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.prompt_id = ? AND p.tenant_id = ?
                    ORDER BY p.title
                """
                params = (prompt_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding projects for prompt {prompt_id}: {str(e)}"
            )
            raise

    def find_association(
        self, project_id: int, prompt_id: int
    ) -> Optional[ProjectPrompt]:
        """Find specific project-prompt association."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.project_id = %s AND pp.prompt_id = %s AND p.tenant_id = %s
                """
                params = (project_id, prompt_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pp.* FROM project_prompts pp
                    JOIN projects p ON pp.project_id = p.id
                    WHERE pp.project_id = ? AND pp.prompt_id = ? AND p.tenant_id = ?
                """
                params = (project_id, prompt_id, self.current_tenant_id)

            row = self.db_manager.execute_query(query, params, fetch_one=True)
            return self._row_to_entity(row) if row else None

        except Exception as e:
            self.logger.error(
                f"Error finding association project {project_id} - prompt {prompt_id}: {str(e)}"
            )
            raise

    def remove_association(self, project_id: int, prompt_id: int) -> bool:
        """Remove project-prompt association."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    DELETE FROM project_prompts 
                    WHERE project_id = %s AND prompt_id = %s
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = %s)
                """
                params = (project_id, prompt_id, self.current_tenant_id)
            else:
                query = """
                    DELETE FROM project_prompts 
                    WHERE project_id = ? AND prompt_id = ?
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = ?)
                """
                params = (project_id, prompt_id, self.current_tenant_id)

            affected_rows = self.db_manager.execute_query(query, params)
            return bool(affected_rows) and affected_rows > 0

        except Exception as e:
            self.logger.error(
                f"Error removing association project {project_id} - prompt {prompt_id}: {str(e)}"
            )
            raise

    def save(self, entity: ProjectPrompt) -> ProjectPrompt:
        """Save project prompt entity (custom implementation without tenant_id)."""
        try:
            entity_dict = self._entity_to_dict(entity)

            # Check if this is an insert or update
            entity_id = entity_dict.get("id")

            if entity_id and self._association_exists(entity_id):
                # Update existing entity
                return self._update_association(entity_dict)
            else:
                # Insert new entity
                return self._insert_association(entity_dict)

        except Exception as e:
            self.logger.error(f"Error saving project prompt: {str(e)}")
            raise

    def _association_exists(self, association_id: int) -> bool:
        """Check if association exists."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = "SELECT 1 FROM project_prompts WHERE id = %s"
            else:
                query = "SELECT 1 FROM project_prompts WHERE id = ?"

            result = self.db_manager.execute_query(
                query, (association_id,), fetch_one=True
            )
            return result is not None

        except Exception:
            return False

    def _insert_association(self, entity_dict: Dict[str, Any]) -> ProjectPrompt:
        """Insert new project prompt association."""
        # Add timestamp if not present
        if "added_at" not in entity_dict or entity_dict["added_at"] is None:
            entity_dict["added_at"] = datetime.now(timezone.utc)

        # Build INSERT query
        fields = [k for k, v in entity_dict.items() if v is not None and k != "id"]
        placeholders = ["?" for _ in fields]
        values = [entity_dict[field] for field in fields]

        if self.db_manager.config.db_type.value == "postgres":
            placeholders = ["%s" for _ in fields]
            query = f"""
                INSERT INTO project_prompts ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """

            row = self.db_manager.execute_query(query, tuple(values), fetch_one=True)
            return self._row_to_entity(row)
        else:
            query = f"""
                INSERT INTO project_prompts ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """

            with self.db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(values))
                conn.commit()

                # Get the last inserted row ID
                cursor.execute("SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]

                # Fetch the complete record
                cursor.execute("SELECT * FROM project_prompts WHERE id = ?", (last_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    row_dict = dict(zip(columns, row))
                    return self._row_to_entity(row_dict)
                else:
                    raise Exception(
                        f"Failed to retrieve inserted project prompt with ID {last_id}"
                    )

    def _update_association(self, entity_dict: Dict[str, Any]) -> ProjectPrompt:
        """Update existing project prompt association."""
        association_id = entity_dict["id"]

        # Build UPDATE query
        update_fields = [
            k for k in entity_dict.keys() if k != "id" and entity_dict[k] is not None
        ]
        set_clauses = [f"{field} = ?" for field in update_fields]
        values = [entity_dict[field] for field in update_fields]
        values.append(association_id)

        query = f"""
            UPDATE project_prompts
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """

        if self.db_manager.config.db_type.value == "postgres":
            query = query.replace("?", "%s")

        affected_rows = self.db_manager.execute_query(query, tuple(values))

        if affected_rows == 0:
            raise Exception(f"No project prompt found with id = {association_id}")

        # Return updated entity
        if self.db_manager.config.db_type.value == "postgres":
            fetch_query = "SELECT * FROM project_prompts WHERE id = %s"
        else:
            fetch_query = "SELECT * FROM project_prompts WHERE id = ?"

        row = self.db_manager.execute_query(
            fetch_query, (association_id,), fetch_one=True
        )
        if not row:
            raise Exception(f"Failed to retrieve updated project prompt")

        return self._row_to_entity(row)


class ProjectRuleRepository(TenantAwareRepository[ProjectRule]):
    """Repository for project rule entity operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project rule repository."""
        super().__init__(db_manager, "project_rules")

    def _get_id_field(self) -> str:
        """Get the primary key field name."""
        return "id"

    def _row_to_entity(self, row: Dict[str, Any]) -> ProjectRule:
        """Convert database row to ProjectRule entity."""
        return ProjectRule.from_dict(row)

    def _entity_to_dict(self, entity: ProjectRule) -> Dict[str, Any]:
        """Convert ProjectRule entity to dictionary."""
        return entity.to_dict()

    def _dict_to_entity(self, entity_dict: Dict[str, Any]) -> ProjectRule:
        """Convert dictionary to ProjectRule entity."""
        return ProjectRule.from_dict(entity_dict)

    def find_by_project(self, project_id: int) -> List[ProjectRule]:
        """Find all rules in a project."""
        try:
            # Join with projects table to ensure tenant filtering
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = %s AND p.tenant_id = %s
                    ORDER BY pr.rule_set_name, pr.added_at
                """
                params = (project_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = ? AND p.tenant_id = ?
                    ORDER BY pr.rule_set_name, pr.added_at
                """
                params = (project_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error finding rules for project {project_id}: {str(e)}")
            raise

    def find_by_rule(self, rule_id: int) -> List[ProjectRule]:
        """Find all projects containing a specific rule."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.rule_id = %s AND p.tenant_id = %s
                    ORDER BY p.title
                """
                params = (rule_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.rule_id = ? AND p.tenant_id = ?
                    ORDER BY p.title
                """
                params = (rule_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(f"Error finding projects for rule {rule_id}: {str(e)}")
            raise

    def find_by_rule_set(
        self, project_id: int, rule_set_name: str
    ) -> List[ProjectRule]:
        """Find all rules in a specific rule set within a project."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = %s AND pr.rule_set_name = %s AND p.tenant_id = %s
                    ORDER BY pr.added_at
                """
                params = (project_id, rule_set_name, self.current_tenant_id)
            else:
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = ? AND pr.rule_set_name = ? AND p.tenant_id = ?
                    ORDER BY pr.added_at
                """
                params = (project_id, rule_set_name, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding rule set {rule_set_name} for project {project_id}: {str(e)}"
            )
            raise

    def find_association(self, project_id: int, rule_id: int) -> Optional[ProjectRule]:
        """Find specific project-rule association."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = %s AND pr.rule_id = %s AND p.tenant_id = %s
                """
                params = (project_id, rule_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pr.* FROM project_rules pr
                    JOIN projects p ON pr.project_id = p.id
                    WHERE pr.project_id = ? AND pr.rule_id = ? AND p.tenant_id = ?
                """
                params = (project_id, rule_id, self.current_tenant_id)

            row = self.db_manager.execute_query(query, params, fetch_one=True)
            return self._row_to_entity(row) if row else None

        except Exception as e:
            self.logger.error(
                f"Error finding association project {project_id} - rule {rule_id}: {str(e)}"
            )
            raise

    def remove_association(self, project_id: int, rule_id: int) -> bool:
        """Remove project-rule association."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    DELETE FROM project_rules 
                    WHERE project_id = %s AND rule_id = %s
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = %s)
                """
                params = (project_id, rule_id, self.current_tenant_id)
            else:
                query = """
                    DELETE FROM project_rules 
                    WHERE project_id = ? AND rule_id = ?
                    AND project_id IN (SELECT id FROM projects WHERE tenant_id = ?)
                """
                params = (project_id, rule_id, self.current_tenant_id)

            affected_rows = self.db_manager.execute_query(query, params)
            return bool(affected_rows) and affected_rows > 0

        except Exception as e:
            self.logger.error(
                f"Error removing association project {project_id} - rule {rule_id}: {str(e)}"
            )
            raise

    def save(self, entity: ProjectRule) -> ProjectRule:
        """Save project rule entity (custom implementation without tenant_id)."""
        try:
            entity_dict = self._entity_to_dict(entity)

            # Check if this is an insert or update
            entity_id = entity_dict.get("id")

            if entity_id and self._association_exists(entity_id):
                # Update existing entity
                return self._update_association(entity_dict)
            else:
                # Insert new entity
                return self._insert_association(entity_dict)

        except Exception as e:
            self.logger.error(f"Error saving project rule: {str(e)}")
            raise

    def _association_exists(self, association_id: int) -> bool:
        """Check if association exists."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = "SELECT 1 FROM project_rules WHERE id = %s"
            else:
                query = "SELECT 1 FROM project_rules WHERE id = ?"

            result = self.db_manager.execute_query(
                query, (association_id,), fetch_one=True
            )
            return result is not None

        except Exception:
            return False

    def _insert_association(self, entity_dict: Dict[str, Any]) -> ProjectRule:
        """Insert new project rule association."""
        # Add timestamp if not present
        if "added_at" not in entity_dict or entity_dict["added_at"] is None:
            entity_dict["added_at"] = datetime.now(timezone.utc)

        # Build INSERT query
        fields = [k for k, v in entity_dict.items() if v is not None and k != "id"]
        placeholders = ["?" for _ in fields]
        values = [entity_dict[field] for field in fields]

        if self.db_manager.config.db_type.value == "postgres":
            placeholders = ["%s" for _ in fields]
            query = f"""
                INSERT INTO project_rules ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """

            row = self.db_manager.execute_query(query, tuple(values), fetch_one=True)
            return self._row_to_entity(row)
        else:
            query = f"""
                INSERT INTO project_rules ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """

            with self.db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(values))
                conn.commit()

                # Get the last inserted row ID
                cursor.execute("SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]

                # Fetch the complete record
                cursor.execute("SELECT * FROM project_rules WHERE id = ?", (last_id,))
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    row_dict = dict(zip(columns, row))
                    return self._row_to_entity(row_dict)
                else:
                    raise Exception(
                        f"Failed to retrieve inserted project rule with ID {last_id}"
                    )

    def _update_association(self, entity_dict: Dict[str, Any]) -> ProjectRule:
        """Update existing project rule association."""
        association_id = entity_dict["id"]

        # Build UPDATE query
        update_fields = [
            k for k in entity_dict.keys() if k != "id" and entity_dict[k] is not None
        ]
        set_clauses = [f"{field} = ?" for field in update_fields]
        values = [entity_dict[field] for field in update_fields]
        values.append(association_id)

        query = f"""
            UPDATE project_rules
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """

        if self.db_manager.config.db_type.value == "postgres":
            query = query.replace("?", "%s")

        affected_rows = self.db_manager.execute_query(query, tuple(values))

        if affected_rows == 0:
            raise Exception(f"No project rule found with id = {association_id}")

        # Return updated entity
        if self.db_manager.config.db_type.value == "postgres":
            fetch_query = "SELECT * FROM project_rules WHERE id = %s"
        else:
            fetch_query = "SELECT * FROM project_rules WHERE id = ?"

        row = self.db_manager.execute_query(
            fetch_query, (association_id,), fetch_one=True
        )
        if not row:
            raise Exception(f"Failed to retrieve updated project rule")

        return self._row_to_entity(row)


class ProjectVersionRepository(TenantAwareRepository[ProjectVersion]):
    """Repository for project version entity operations."""

    def __init__(self, db_manager: BaseDatabaseManager):
        """Initialize project version repository."""
        super().__init__(db_manager, "project_versions")

    def _get_id_field(self) -> str:
        """Get the primary key field name."""
        return "id"

    def _row_to_entity(self, row: Dict[str, Any]) -> ProjectVersion:
        """Convert database row to ProjectVersion entity."""
        return ProjectVersion.from_dict(row)

    def _entity_to_dict(self, entity: ProjectVersion) -> Dict[str, Any]:
        """Convert ProjectVersion entity to dictionary."""
        return entity.to_dict()

    def _dict_to_entity(self, entity_dict: Dict[str, Any]) -> ProjectVersion:
        """Convert dictionary to ProjectVersion entity."""
        return ProjectVersion.from_dict(entity_dict)

    def find_by_project(self, project_id: int) -> List[ProjectVersion]:
        """Find all versions for a project."""
        try:
            # Join with projects table to ensure tenant filtering
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pv.* FROM project_versions pv
                    JOIN projects p ON pv.project_id = p.id
                    WHERE pv.project_id = %s AND p.tenant_id = %s
                    ORDER BY pv.version_number DESC
                """
                params = (project_id, self.current_tenant_id)
            else:
                query = """
                    SELECT pv.* FROM project_versions pv
                    JOIN projects p ON pv.project_id = p.id
                    WHERE pv.project_id = ? AND p.tenant_id = ?
                    ORDER BY pv.version_number DESC
                """
                params = (project_id, self.current_tenant_id)

            rows = self.db_manager.execute_query(query, params, fetch_all=True)
            return [self._row_to_entity(row) for row in rows]

        except Exception as e:
            self.logger.error(
                f"Error finding versions for project {project_id}: {str(e)}"
            )
            raise

    def find_by_version_number(
        self, project_id: int, version_number: int
    ) -> Optional[ProjectVersion]:
        """Find specific version of a project."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = """
                    SELECT pv.* FROM project_versions pv
                    JOIN projects p ON pv.project_id = p.id
                    WHERE pv.project_id = %s AND pv.version_number = %s AND p.tenant_id = %s
                """
                params = (project_id, version_number, self.current_tenant_id)
            else:
                query = """
                    SELECT pv.* FROM project_versions pv
                    JOIN projects p ON pv.project_id = p.id
                    WHERE pv.project_id = ? AND pv.version_number = ? AND p.tenant_id = ?
                """
                params = (project_id, version_number, self.current_tenant_id)

            row = self.db_manager.execute_query(query, params, fetch_one=True)
            return self._row_to_entity(row) if row else None

        except Exception as e:
            self.logger.error(
                f"Error finding version {version_number} for project {project_id}: {str(e)}"
            )
            raise

    def get_latest_version(self, project_id: int) -> Optional[ProjectVersion]:
        """Get the latest version for a project."""
        versions = self.find_by_project(project_id)
        return versions[0] if versions else None

    def get_next_version_number(self, project_id: int) -> int:
        """Get the next version number for a project."""
        latest = self.get_latest_version(project_id)
        return latest.version_number + 1 if latest else 1

    def save(self, entity: ProjectVersion) -> ProjectVersion:
        """Save project version entity (custom implementation without tenant_id)."""
        try:
            entity_dict = self._entity_to_dict(entity)

            # Check if this is an insert or update
            entity_id = entity_dict.get("id")

            if entity_id and self._version_exists(entity_id):
                # Update existing entity
                return self._update_version(entity_dict)
            else:
                # Insert new entity
                return self._insert_version(entity_dict)

        except Exception as e:
            self.logger.error(f"Error saving project version: {str(e)}")
            raise

    def _version_exists(self, version_id: int) -> bool:
        """Check if version exists."""
        try:
            if self.db_manager.config.db_type.value == "postgres":
                query = "SELECT 1 FROM project_versions WHERE id = %s"
            else:
                query = "SELECT 1 FROM project_versions WHERE id = ?"

            result = self.db_manager.execute_query(query, (version_id,), fetch_one=True)
            return result is not None

        except Exception:
            return False

    def _insert_version(self, entity_dict: Dict[str, Any]) -> ProjectVersion:
        """Insert new project version."""
        # Add timestamp if not present
        if "created_at" not in entity_dict or entity_dict["created_at"] is None:
            entity_dict["created_at"] = datetime.now(timezone.utc)

        # Build INSERT query
        fields = [k for k, v in entity_dict.items() if v is not None and k != "id"]
        placeholders = ["?" for _ in fields]
        values = [entity_dict[field] for field in fields]

        if self.db_manager.config.db_type.value == "postgres":
            placeholders = ["%s" for _ in fields]
            query = f"""
                INSERT INTO project_versions ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """

            row = self.db_manager.execute_query(query, tuple(values), fetch_one=True)
            return self._row_to_entity(row)
        else:
            query = f"""
                INSERT INTO project_versions ({', '.join(fields)})
                VALUES ({', '.join(placeholders)})
            """

            with self.db_manager.get_connection_context() as conn:
                cursor = conn.cursor()
                cursor.execute(query, tuple(values))
                conn.commit()

                # Get the last inserted row ID
                cursor.execute("SELECT last_insert_rowid()")
                last_id = cursor.fetchone()[0]

                # Fetch the complete record
                cursor.execute(
                    "SELECT * FROM project_versions WHERE id = ?", (last_id,)
                )
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    row_dict = dict(zip(columns, row))
                    return self._row_to_entity(row_dict)
                else:
                    raise Exception(
                        f"Failed to retrieve inserted project version with ID {last_id}"
                    )

    def _update_version(self, entity_dict: Dict[str, Any]) -> ProjectVersion:
        """Update existing project version."""
        version_id = entity_dict["id"]

        # Build UPDATE query
        update_fields = [
            k for k in entity_dict.keys() if k != "id" and entity_dict[k] is not None
        ]
        set_clauses = [f"{field} = ?" for field in update_fields]
        values = [entity_dict[field] for field in update_fields]
        values.append(version_id)

        query = f"""
            UPDATE project_versions
            SET {', '.join(set_clauses)}
            WHERE id = ?
        """

        if self.db_manager.config.db_type.value == "postgres":
            query = query.replace("?", "%s")

        affected_rows = self.db_manager.execute_query(query, tuple(values))

        if affected_rows == 0:
            raise Exception(f"No project version found with id = {version_id}")

        # Return updated entity
        if self.db_manager.config.db_type.value == "postgres":
            fetch_query = "SELECT * FROM project_versions WHERE id = %s"
        else:
            fetch_query = "SELECT * FROM project_versions WHERE id = ?"

        row = self.db_manager.execute_query(fetch_query, (version_id,), fetch_one=True)
        if not row:
            raise Exception(f"Failed to retrieve updated project version")

        return self._row_to_entity(row)
