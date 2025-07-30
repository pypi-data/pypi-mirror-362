"""
Non-Commercial License

Copyright (c) 2025 MakerCorn

Multi-tenant prompt data manager with database abstraction for SQLite and PostgreSQL.

This software is licensed for non-commercial use only. See LICENSE file for details.
"""

import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_PATH = os.getenv("DB_PATH", "prompts.db")
POSTGRES_DSN = os.getenv("POSTGRES_DSN")


class PromptDataManager:
    def __init__(
        self,
        db_path: Optional[str] = None,
        tenant_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ):
        self.db_type = DB_TYPE
        self.tenant_id = tenant_id
        self.user_id = user_id
        if self.db_type == "postgres":
            if not POSTGRES_AVAILABLE:
                raise ImportError(
                    "psycopg2 is required for Postgres support. Please install it."
                )
            self.dsn = POSTGRES_DSN
            if not self.dsn:
                raise ValueError(
                    "POSTGRES_DSN environment variable must be set for Postgres."
                )
            self.db_path: Optional[str] = None
        else:
            self.db_path = db_path or DB_PATH
        self.init_database()

    def get_conn(self):
        if self.db_type == "postgres":
            return psycopg2.connect(self.dsn, cursor_factory=RealDictCursor)
        else:
            if self.db_path is None:
                raise ValueError("Database path not set for SQLite connection")
            return sqlite3.connect(self.db_path)

    def init_database(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        if self.db_type == "postgres":
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prompts (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'Uncategorized',
                    tags TEXT,
                    is_enhancement_prompt BOOLEAN DEFAULT FALSE,
                    visibility TEXT DEFAULT 'private',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public'))
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    key TEXT NOT NULL,
                    value TEXT,
                    UNIQUE(tenant_id, user_id, key)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS templates (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    name TEXT NOT NULL,
                    description TEXT,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'Custom',
                    tags TEXT DEFAULT '',
                    variables TEXT,
                    is_builtin BOOLEAN DEFAULT FALSE,
                    visibility TEXT DEFAULT 'private',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public'))
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rules (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'General',
                    tags TEXT DEFAULT '',
                    description TEXT,
                    is_builtin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_models (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    name TEXT NOT NULL,
                    display_name TEXT,
                    provider TEXT NOT NULL,
                    model_id TEXT NOT NULL,
                    description TEXT,
                    api_key TEXT,
                    api_endpoint TEXT,
                    api_version TEXT,
                    deployment_name TEXT,
                    max_tokens INTEGER,
                    temperature DECIMAL(3,2) DEFAULT 0.7,
                    top_p DECIMAL(3,2) DEFAULT 1.0,
                    frequency_penalty DECIMAL(3,2) DEFAULT 0.0,
                    presence_penalty DECIMAL(3,2) DEFAULT 0.0,
                    cost_per_1k_input_tokens DECIMAL(10,6) DEFAULT 0.0,
                    cost_per_1k_output_tokens DECIMAL(10,6) DEFAULT 0.0,
                    max_context_length INTEGER,
                    supports_streaming BOOLEAN DEFAULT FALSE,
                    supports_function_calling BOOLEAN DEFAULT FALSE,
                    supports_vision BOOLEAN DEFAULT FALSE,
                    supports_json_mode BOOLEAN DEFAULT FALSE,
                    is_enabled BOOLEAN DEFAULT TRUE,
                    is_available BOOLEAN DEFAULT FALSE,
                    last_health_check TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_operation_configs (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    operation_type TEXT NOT NULL,
                    primary_model TEXT,
                    fallback_models TEXT,
                    is_enabled BOOLEAN DEFAULT TRUE,
                    custom_parameters TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, operation_type)
                )
            """
            )

            # Add columns to existing tables if they don't exist
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='prompts' AND column_name='tenant_id'
                    ) THEN
                        ALTER TABLE prompts ADD COLUMN tenant_id UUID;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='prompts' AND column_name='user_id'
                    ) THEN
                        ALTER TABLE prompts ADD COLUMN user_id UUID;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='prompts' AND column_name='visibility'
                    ) THEN
                        ALTER TABLE prompts ADD COLUMN visibility TEXT DEFAULT 'private';
                        ALTER TABLE prompts ADD CONSTRAINT prompts_visibility_check
                            CHECK (visibility IN ('private', 'public'));
                    END IF;
                END $$;
            """
            )
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='config' AND column_name='tenant_id'
                    ) THEN
                        ALTER TABLE config ADD COLUMN tenant_id UUID;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='config' AND column_name='user_id'
                    ) THEN
                        ALTER TABLE config ADD COLUMN user_id UUID;
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='config' AND column_name='id'
                    ) THEN
                        ALTER TABLE config ADD COLUMN id SERIAL PRIMARY KEY;
                    END IF;
                END $$;
            """
            )
            cursor.execute(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='templates' AND column_name='tags'
                    ) THEN
                        ALTER TABLE templates ADD COLUMN tags TEXT DEFAULT '';
                    END IF;
                    IF NOT EXISTS (
                        SELECT 1 FROM information_schema.columns
                        WHERE table_name='templates' AND column_name='visibility'
                    ) THEN
                        ALTER TABLE templates ADD COLUMN visibility TEXT DEFAULT 'private';
                        ALTER TABLE templates ADD CONSTRAINT templates_visibility_check
                            CHECK (visibility IN ('private', 'public'));
                    END IF;
                END $$;
            """
            )
        else:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'Uncategorized',
                    tags TEXT,
                    is_enhancement_prompt BOOLEAN DEFAULT 0,
                    visibility TEXT DEFAULT 'private',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public'))
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS config (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    key TEXT NOT NULL,
                    value TEXT,
                    UNIQUE(tenant_id, user_id, key)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS templates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    name TEXT NOT NULL,
                    description TEXT,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'Custom',
                    tags TEXT DEFAULT '',
                    variables TEXT,
                    is_builtin BOOLEAN DEFAULT 0,
                    visibility TEXT DEFAULT 'private',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public'))
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    category TEXT DEFAULT 'General',
                    tags TEXT DEFAULT '',
                    description TEXT,
                    is_builtin BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_models (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    name TEXT NOT NULL,
                    display_name TEXT,
                    provider TEXT NOT NULL,
                    model_id TEXT NOT NULL,
                    description TEXT,
                    api_key TEXT,
                    api_endpoint TEXT,
                    api_version TEXT,
                    deployment_name TEXT,
                    max_tokens INTEGER,
                    temperature REAL DEFAULT 0.7,
                    top_p REAL DEFAULT 1.0,
                    frequency_penalty REAL DEFAULT 0.0,
                    presence_penalty REAL DEFAULT 0.0,
                    cost_per_1k_input_tokens REAL DEFAULT 0.0,
                    cost_per_1k_output_tokens REAL DEFAULT 0.0,
                    max_context_length INTEGER,
                    supports_streaming BOOLEAN DEFAULT 0,
                    supports_function_calling BOOLEAN DEFAULT 0,
                    supports_vision BOOLEAN DEFAULT 0,
                    supports_json_mode BOOLEAN DEFAULT 0,
                    is_enabled BOOLEAN DEFAULT 1,
                    is_available BOOLEAN DEFAULT 0,
                    last_health_check TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ai_operation_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    operation_type TEXT NOT NULL,
                    primary_model TEXT,
                    fallback_models TEXT,
                    is_enabled BOOLEAN DEFAULT 1,
                    custom_parameters TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, operation_type)
                )
            """
            )
            cursor.execute("PRAGMA table_info(prompts)")
            columns = [column[1] for column in cursor.fetchall()]
            if "is_enhancement_prompt" not in columns:
                cursor.execute(
                    "ALTER TABLE prompts ADD COLUMN is_enhancement_prompt "
                    "BOOLEAN DEFAULT 0"
                )
            if "tenant_id" not in columns:
                cursor.execute("ALTER TABLE prompts ADD COLUMN tenant_id TEXT")
            if "user_id" not in columns:
                cursor.execute("ALTER TABLE prompts ADD COLUMN user_id TEXT")
            if "name" not in columns:
                cursor.execute("ALTER TABLE prompts ADD COLUMN name TEXT")
                cursor.execute("UPDATE prompts SET name = title WHERE name IS NULL")
            if "visibility" not in columns:
                cursor.execute(
                    "ALTER TABLE prompts ADD COLUMN visibility TEXT DEFAULT 'private'"
                )

            # Update templates table structure
            cursor.execute("PRAGMA table_info(templates)")
            template_columns = [column[1] for column in cursor.fetchall()]
            if "tags" not in template_columns:
                cursor.execute("ALTER TABLE templates ADD COLUMN tags TEXT DEFAULT ''")
            if "visibility" not in template_columns:
                cursor.execute(
                    "ALTER TABLE templates ADD COLUMN visibility TEXT DEFAULT 'private'"
                )

            # Update config table structure
            cursor.execute("PRAGMA table_info(config)")
            config_columns = [column[1] for column in cursor.fetchall()]
            if "tenant_id" not in config_columns:
                cursor.execute("ALTER TABLE config ADD COLUMN tenant_id TEXT")
            if "user_id" not in config_columns:
                cursor.execute("ALTER TABLE config ADD COLUMN user_id TEXT")
            if "id" not in config_columns:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS config_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tenant_id TEXT,
                        user_id TEXT,
                        key TEXT NOT NULL,
                        value TEXT,
                        UNIQUE(tenant_id, user_id, key)
                    )
                """
                )
                cursor.execute(
                    "INSERT INTO config_new (key, value) SELECT key, value FROM config"
                )
                cursor.execute("DROP TABLE config")
                cursor.execute("ALTER TABLE config_new RENAME TO config")

        # Create project-related tables
        if self.db_type == "postgres":
            # Projects table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id SERIAL PRIMARY KEY,
                    tenant_id UUID,
                    user_id UUID,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    project_type TEXT DEFAULT 'general',
                    visibility TEXT DEFAULT 'private',
                    shared_with_tenant BOOLEAN DEFAULT FALSE,
                    version INTEGER DEFAULT 1,
                    tags TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public')),
                    CHECK (project_type IN ('general', 'sequenced', 'llm_comparison', 'developer'))
                )
                """
            )

            # Add tags column to existing projects table if it doesn't exist
            try:
                cursor.execute("ALTER TABLE projects ADD COLUMN tags TEXT")
            except Exception:
                # Column already exists or other error, ignore
                pass

            # Project members table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_members (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    user_id UUID NOT NULL,
                    role TEXT DEFAULT 'member',
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(project_id, user_id),
                    CHECK (role IN ('owner', 'member', 'viewer'))
                )
                """
            )

            # Project prompts table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_prompts (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    prompt_id INTEGER REFERENCES prompts(id) ON DELETE CASCADE,
                    sequence_order INTEGER DEFAULT 0,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(project_id, prompt_id)
                )
                """
            )

            # Project rules table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_rules (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    rule_id INTEGER REFERENCES rules(id) ON DELETE CASCADE,
                    rule_set_name TEXT,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(project_id, rule_id)
                )
                """
            )

            # Project versions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_versions (
                    id SERIAL PRIMARY KEY,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    version_number INTEGER NOT NULL,
                    changes_description TEXT,
                    snapshot_data TEXT,
                    created_by UUID,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        else:
            # SQLite version
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tenant_id TEXT,
                    user_id TEXT,
                    name TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    project_type TEXT DEFAULT 'general',
                    visibility TEXT DEFAULT 'private',
                    shared_with_tenant INTEGER DEFAULT 0,
                    version INTEGER DEFAULT 1,
                    tags TEXT,
                    created_at TEXT DEFAULT (datetime('now')),
                    updated_at TEXT DEFAULT (datetime('now')),
                    UNIQUE(tenant_id, name),
                    CHECK (visibility IN ('private', 'public')),
                    CHECK (project_type IN ('general', 'sequenced', 'llm_comparison', 'developer'))
                )
                """
            )

            # Add tags column to existing projects table if it doesn't exist
            try:
                cursor.execute("ALTER TABLE projects ADD COLUMN tags TEXT")
            except Exception:
                # Column already exists or other error, ignore
                pass

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    user_id TEXT NOT NULL,
                    role TEXT DEFAULT 'member',
                    added_at TEXT DEFAULT (datetime('now')),
                    UNIQUE(project_id, user_id),
                    CHECK (role IN ('owner', 'member', 'viewer'))
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_prompts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    prompt_id INTEGER REFERENCES prompts(id) ON DELETE CASCADE,
                    sequence_order INTEGER DEFAULT 0,
                    added_at TEXT DEFAULT (datetime('now')),
                    UNIQUE(project_id, prompt_id)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    rule_id INTEGER REFERENCES rules(id) ON DELETE CASCADE,
                    rule_set_name TEXT,
                    added_at TEXT DEFAULT (datetime('now')),
                    UNIQUE(project_id, rule_id)
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS project_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
                    version_number INTEGER NOT NULL,
                    changes_description TEXT,
                    snapshot_data TEXT,
                    created_by TEXT,
                    created_at TEXT DEFAULT (datetime('now'))
                )
                """
            )

        conn.commit()
        conn.close()

    def add_prompt(
        self,
        name: str,
        title: str,
        content: str,
        category: str,
        tags: str,
        is_enhancement_prompt: bool = False,
        visibility: str = "private",
    ) -> str:
        if not name.strip():
            return "Error: Name is required!"
        if not title.strip() or not content.strip():
            return "Error: Title and content are required!"
        if not self.tenant_id:
            return "Error: No tenant context available!"
        if visibility not in ["private", "public"]:
            return "Error: Visibility must be 'private' or 'public'!"

        name = name.strip()
        category = category.strip() or "Uncategorized"
        conn = self.get_conn()
        cursor = conn.cursor()

        # Check for existing prompt within tenant
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM prompts WHERE name = %s AND tenant_id = %s",
                (name, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM prompts WHERE name = ? AND tenant_id = ?",
                (name, self.tenant_id),
            )

        if cursor.fetchone():
            conn.close()
            return (
                f"Error: A prompt with name '{name}' already exists in your workspace!"
            )

        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO prompts (tenant_id, user_id, name, title, content,
                category, tags, is_enhancement_prompt, visibility, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    self.tenant_id,
                    self.user_id,
                    name,
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip(),
                    is_enhancement_prompt,
                    visibility,
                    datetime.now(),
                    datetime.now(),
                ),
            )
        else:
            cursor.execute(
                """
                INSERT INTO prompts (tenant_id, user_id, name, title, content,
                category, tags, is_enhancement_prompt, visibility, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    self.tenant_id,
                    self.user_id,
                    name,
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip(),
                    is_enhancement_prompt,
                    visibility,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )

        conn.commit()
        conn.close()
        prompt_type = "Enhancement prompt" if is_enhancement_prompt else "Prompt"
        return f"{prompt_type} '{name}' added successfully!"

    def update_prompt(
        self,
        original_name: str,
        new_name: str,
        title: str,
        content: str,
        category: str,
        tags: str,
        is_enhancement_prompt: bool = False,
        visibility: str = "private",
    ) -> str:
        if not original_name.strip() or not new_name.strip():
            return "Error: Original name and new name are required!"
        if not title.strip() or not content.strip():
            return "Error: Title and content are required!"
        if not self.tenant_id:
            return "Error: No tenant context available!"
        if visibility not in ["private", "public"]:
            return "Error: Visibility must be 'private' or 'public'!"

        original_name = original_name.strip()
        new_name = new_name.strip()
        category = category.strip() or "Uncategorized"
        conn = self.get_conn()
        cursor = conn.cursor()

        # Check if original prompt exists in tenant
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM prompts WHERE name = %s AND tenant_id = %s",
                (original_name, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM prompts WHERE name = ? AND tenant_id = ?",
                (original_name, self.tenant_id),
            )

        if not cursor.fetchone():
            conn.close()
            return f"Error: Prompt '{original_name}' not found in your workspace!"

        # Check if new name conflicts within tenant
        if original_name != new_name:
            if self.db_type == "postgres":
                cursor.execute(
                    "SELECT id FROM prompts WHERE name = %s AND tenant_id = %s",
                    (new_name, self.tenant_id),
                )
            else:
                cursor.execute(
                    "SELECT id FROM prompts WHERE name = ? AND tenant_id = ?",
                    (new_name, self.tenant_id),
                )

            if cursor.fetchone():
                conn.close()
                return (
                    f"Error: A prompt with name '{new_name}' already exists "
                    "in your workspace!"
                )

        if self.db_type == "postgres":
            cursor.execute(
                """
                UPDATE prompts
                SET name=%s, title=%s, content=%s, category=%s, tags=%s,
                is_enhancement_prompt=%s, visibility=%s, updated_at=%s
                WHERE name=%s AND tenant_id=%s
            """,
                (
                    new_name,
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip(),
                    is_enhancement_prompt,
                    visibility,
                    datetime.now(),
                    original_name,
                    self.tenant_id,
                ),
            )
        else:
            cursor.execute(
                """
                UPDATE prompts
                SET name=?, title=?, content=?, category=?, tags=?,
                is_enhancement_prompt=?, visibility=?, updated_at=?
                WHERE name=? AND tenant_id=?
            """,
                (
                    new_name,
                    title.strip(),
                    content.strip(),
                    category,
                    tags.strip(),
                    is_enhancement_prompt,
                    visibility,
                    datetime.now().isoformat(),
                    original_name,
                    self.tenant_id,
                ),
            )

        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return "Prompt updated successfully!"
        else:
            conn.close()
            return "Error: Prompt not found in your workspace!"

    def delete_prompt(self, name: str) -> str:
        if not name.strip():
            return "Error: Name is required!"
        if not self.tenant_id:
            return "Error: No tenant context available!"

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "DELETE FROM prompts WHERE name = %s AND tenant_id = %s",
                (name.strip(), self.tenant_id),
            )
        else:
            cursor.execute(
                "DELETE FROM prompts WHERE name = ? AND tenant_id = ?",
                (name.strip(), self.tenant_id),
            )

        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return f"Prompt '{name}' deleted successfully!"
        else:
            conn.close()
            return f"Error: Prompt '{name}' not found in your workspace!"

    def get_all_prompts(self, include_enhancement_prompts: bool = True) -> List[Dict]:
        """
        Get all prompts with visibility filtering.
        In multi-tenant mode: user's own prompts + public prompts from tenant
        In single-user mode: all prompts (visibility ignored)
        """
        if not self.tenant_id:
            return []

        # Check if single-user mode by environment variable
        import os

        is_single_user = os.getenv("MULTITENANT_MODE", "true").lower() == "false"

        if is_single_user or not self.user_id:
            # Single-user mode or no user context - show all prompts
            return self._get_all_prompts_no_visibility(include_enhancement_prompts)
        else:
            # Multi-tenant mode - use visibility filtering
            return self.get_all_prompts_with_visibility(
                include_enhancement_prompts, include_public_from_tenant=True
            )

    def _get_all_prompts_no_visibility(
        self, include_enhancement_prompts: bool = True
    ) -> List[Dict]:
        """Internal method for single-user mode - shows all prompts regardless of visibility"""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = %s ORDER BY category, name
                """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = %s
                    AND is_enhancement_prompt = FALSE ORDER BY category, name
                """,
                    (self.tenant_id,),
                )
        else:
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = ? ORDER BY category, name
                """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = ?
                    AND is_enhancement_prompt = 0 ORDER BY category, name
                """,
                    (self.tenant_id,),
                )

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
            )
        conn.close()
        return prompts

    def get_enhancement_prompts(self) -> List[Dict]:
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                tags, is_enhancement_prompt, visibility, created_at, updated_at
                FROM prompts WHERE tenant_id = %s AND is_enhancement_prompt = TRUE
                ORDER BY name
            """,
                (self.tenant_id,),
            )
        else:
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                tags, is_enhancement_prompt, visibility, created_at, updated_at
                FROM prompts WHERE tenant_id = ? AND is_enhancement_prompt = 1
                ORDER BY name
            """,
                (self.tenant_id,),
            )

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": bool(row[8]),
                    "created_at": row[9],
                    "updated_at": row[10],
                }
            )
        conn.close()
        return prompts

    def get_categories(self) -> List[str]:
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "SELECT DISTINCT category FROM prompts WHERE tenant_id = %s "
                "ORDER BY category",
                (self.tenant_id,),
            )
        else:
            cursor.execute(
                "SELECT DISTINCT category FROM prompts WHERE tenant_id = ? "
                "ORDER BY category",
                (self.tenant_id,),
            )

        categories = [row[0] for row in cursor.fetchall()]
        conn.close()

        # If no categories exist yet (empty database), provide default categories
        if not categories:
            categories = ["Business", "Technical", "Creative", "Analytical", "General"]

        return sorted(categories)

    def search_prompts(
        self, search_term: str, include_enhancement_prompts: bool = True
    ) -> List[Dict]:
        if not search_term.strip():
            return self.get_all_prompts(include_enhancement_prompts)
        if not self.tenant_id:
            return []

        # Check if single-user mode by environment variable
        import os

        is_single_user = os.getenv("MULTITENANT_MODE", "true").lower() == "false"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Build visibility conditions
        if is_single_user or not self.user_id:
            # Single-user mode or no user context - no visibility filtering
            visibility_condition = ""
            visibility_params = []
        else:
            # Multi-tenant mode - include user's own prompts + public prompts
            if self.db_type == "postgres":
                visibility_condition = " AND (user_id = %s OR visibility = 'public')"
            else:
                visibility_condition = " AND (user_id = ? OR visibility = 'public')"
            visibility_params = [self.user_id]

        if self.db_type == "postgres":
            like = f"%{search_term}%"
            base_params = [self.tenant_id, like, like, like, like]

            if include_enhancement_prompts:
                query = f"""
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts
                    WHERE tenant_id = %s
                    AND (name ILIKE %s OR title ILIKE %s OR content ILIKE %s
                    OR tags ILIKE %s){visibility_condition}
                    ORDER BY category, name
                """
                cursor.execute(query, base_params + visibility_params)
            else:
                query = f"""
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts
                    WHERE tenant_id = %s
                    AND (name ILIKE %s OR title ILIKE %s OR content ILIKE %s
                    OR tags ILIKE %s) AND is_enhancement_prompt = FALSE{visibility_condition}
                    ORDER BY category, name
                """
                cursor.execute(query, base_params + visibility_params)
        else:
            base_params = [
                self.tenant_id,
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
                f"%{search_term}%",
            ]

            if include_enhancement_prompts:
                query = f"""
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts
                    WHERE tenant_id = ?
                    AND (name LIKE ? OR title LIKE ? OR content LIKE ?
                    OR tags LIKE ?){visibility_condition}
                    ORDER BY category, name
                """
                cursor.execute(query, base_params + visibility_params)
            else:
                query = f"""
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts
                    WHERE tenant_id = ?
                    AND (name LIKE ? OR title LIKE ? OR content LIKE ?
                    OR tags LIKE ?) AND is_enhancement_prompt = 0{visibility_condition}
                    ORDER BY category, name
                """
                cursor.execute(query, base_params + visibility_params)

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
            )
        conn.close()
        return prompts

    def get_prompts_by_category(
        self, category: Optional[str] = None, include_enhancement_prompts: bool = True
    ) -> List[Dict]:
        if not category or category == "All":
            return self.get_all_prompts(include_enhancement_prompts)
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = %s AND category = %s
                    ORDER BY name
                """,
                    (self.tenant_id, category),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = %s AND category = %s
                    AND is_enhancement_prompt = FALSE
                    ORDER BY name
                """,
                    (self.tenant_id, category),
                )
        else:
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = ? AND category = ?
                    ORDER BY name
                """,
                    (self.tenant_id, category),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts WHERE tenant_id = ? AND category = ?
                    AND is_enhancement_prompt = 0
                    ORDER BY name
                """,
                    (self.tenant_id, category),
                )

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
            )
        conn.close()
        return prompts

    def get_prompt_by_name(self, name: str) -> Optional[Dict]:
        if not name.strip() or not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, is_enhancement_prompt, visibility, created_at, updated_at
                FROM prompts WHERE name = %s AND tenant_id = %s
            """,
                (name.strip(), self.tenant_id),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "id": row["id"],
                    "tenant_id": row["tenant_id"],
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": row["category"],
                    "tags": row["tags"],
                    "is_enhancement_prompt": (
                        bool(row["is_enhancement_prompt"])
                        if row["is_enhancement_prompt"] is not None
                        else False
                    ),
                    "visibility": (
                        row["visibility"]
                        if row["visibility"] is not None
                        else "private"
                    ),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
        else:
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, is_enhancement_prompt, visibility, created_at, updated_at
                FROM prompts WHERE name = ? AND tenant_id = ?
            """,
                (name.strip(), self.tenant_id),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
        return None

    # Rules Management Methods

    def add_rule(
        self,
        name: str,
        title: str,
        content: str,
        category: str = "General",
        tags: str = "",
        description: str = "",
        is_builtin: bool = False,
    ) -> str:
        """Add a new rule to the database."""
        if not name.strip() or not title.strip() or not content.strip():
            return "Name, title, and content are required."

        if not self.tenant_id or not self.user_id:
            return "Tenant ID and User ID are required."

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO rules (tenant_id, user_id, name, title, content, category, tags, description, is_builtin)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        self.tenant_id,
                        self.user_id,
                        name.strip(),
                        title.strip(),
                        content.strip(),
                        category.strip() or "General",
                        tags.strip(),
                        description.strip(),
                        is_builtin,
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO rules (tenant_id, user_id, name, title, content, category, tags, description, is_builtin)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        self.tenant_id,
                        self.user_id,
                        name.strip(),
                        title.strip(),
                        content.strip(),
                        category.strip() or "General",
                        tags.strip(),
                        description.strip(),
                        is_builtin,
                    ),
                )
            conn.commit()
            conn.close()
            return "Rule added successfully."
        except Exception as e:
            conn.rollback()
            conn.close()
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e):
                return f"Error: A rule with the name '{name}' already exists."
            return f"Error adding rule: {str(e)}"

    def update_rule(
        self,
        original_name: str,
        name: str,
        title: str,
        content: str,
        category: str = "General",
        tags: str = "",
        description: str = "",
    ) -> str:
        """Update an existing rule."""
        if not name.strip() or not title.strip() or not content.strip():
            return "Name, title, and content are required."

        if not self.tenant_id:
            return "Tenant ID is required."

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    UPDATE rules
                    SET name = %s, title = %s, content = %s, category = %s, tags = %s, description = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE name = %s AND tenant_id = %s
                """,
                    (
                        name.strip(),
                        title.strip(),
                        content.strip(),
                        category.strip() or "General",
                        tags.strip(),
                        description.strip(),
                        original_name.strip(),
                        self.tenant_id,
                    ),
                )
            else:
                cursor.execute(
                    """
                    UPDATE rules
                    SET name = ?, title = ?, content = ?, category = ?, tags = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE name = ? AND tenant_id = ?
                """,
                    (
                        name.strip(),
                        title.strip(),
                        content.strip(),
                        category.strip() or "General",
                        tags.strip(),
                        description.strip(),
                        original_name.strip(),
                        self.tenant_id,
                    ),
                )

            if cursor.rowcount == 0:
                conn.close()
                return f"Error: Rule '{original_name}' not found."

            conn.commit()
            conn.close()
            return "Rule updated successfully."
        except Exception as e:
            conn.rollback()
            conn.close()
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e):
                return f"Error: A rule with the name '{name}' already exists."
            return f"Error updating rule: {str(e)}"

    def delete_rule(self, name: str) -> str:
        """Delete a rule from the database."""
        if not name.strip() or not self.tenant_id:
            return "Rule name and tenant ID are required."

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    "DELETE FROM rules WHERE name = %s AND tenant_id = %s",
                    (name.strip(), self.tenant_id),
                )
            else:
                cursor.execute(
                    "DELETE FROM rules WHERE name = ? AND tenant_id = ?",
                    (name.strip(), self.tenant_id),
                )

            if cursor.rowcount == 0:
                conn.close()
                return f"Error: Rule '{name}' not found."

            conn.commit()
            conn.close()
            return "Rule deleted successfully."
        except Exception as e:
            conn.rollback()
            conn.close()
            return f"Error deleting rule: {str(e)}"

    def get_all_rules(self) -> List[Dict]:
        """Retrieve all rules for the current tenant."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE tenant_id = %s
                ORDER BY created_at DESC
            """,
                (self.tenant_id,),
            )
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": row["id"],
                    "tenant_id": row["tenant_id"],
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": row["category"],
                    "tags": row["tags"],
                    "description": row["description"],
                    "is_builtin": (
                        bool(row["is_builtin"])
                        if row["is_builtin"] is not None
                        else False
                    ),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                for row in rows
            ]
        else:
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE tenant_id = ?
                ORDER BY created_at DESC
            """,
                (self.tenant_id,),
            )
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "description": row[8],
                    "is_builtin": bool(row[9]) if row[9] is not None else False,
                    "created_at": row[10],
                    "updated_at": row[11],
                }
                for row in rows
            ]

    def search_rules(
        self,
        search_term: str,
        category_filter: str = "all",
        tags_filter: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Search rules by name, title, content, or tags."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        # Build search conditions
        conditions = []
        params = []

        # Add tenant filter
        if self.db_type == "postgres":
            conditions.append("tenant_id = %s")
            placeholder = "%s"
        else:
            conditions.append("tenant_id = ?")
            placeholder = "?"
        params.append(self.tenant_id)

        # Add search term filter
        if search_term.strip():
            search_condition = (
                f"(name ILIKE {placeholder} OR title ILIKE {placeholder} OR content ILIKE {placeholder} OR tags ILIKE {placeholder})"
                if self.db_type == "postgres"
                else f"(name LIKE {placeholder} OR title LIKE {placeholder} OR content LIKE {placeholder} OR tags LIKE {placeholder})"
            )
            conditions.append(search_condition)
            search_pattern = f"%{search_term.strip()}%"
            params.extend([search_pattern] * 4)

        # Add category filter
        if category_filter and category_filter.lower() != "all":
            conditions.append(f"category = {placeholder}")
            params.append(category_filter)

        # Add tags filter
        if tags_filter:
            for tag in tags_filter:
                conditions.append(
                    f"tags ILIKE {placeholder}"
                    if self.db_type == "postgres"
                    else f"tags LIKE {placeholder}"
                )
                params.append(f"%{tag.strip()}%")

        where_clause = " AND ".join(conditions) if conditions else "1=1"

        query = f"""
            SELECT id, tenant_id, user_id, name, title, content, category,
                   tags, description, is_builtin, created_at, updated_at
            FROM rules WHERE {where_clause}
            ORDER BY created_at DESC
        """

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        if self.db_type == "postgres":
            return [
                {
                    "id": row["id"],
                    "tenant_id": row["tenant_id"],
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": row["category"],
                    "tags": row["tags"],
                    "description": row["description"],
                    "is_builtin": (
                        bool(row["is_builtin"])
                        if row["is_builtin"] is not None
                        else False
                    ),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                for row in rows
            ]
        else:
            return [
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "description": row[8],
                    "is_builtin": bool(row[9]) if row[9] is not None else False,
                    "created_at": row[10],
                    "updated_at": row[11],
                }
                for row in rows
            ]

    def get_rules_by_category(self, category: str) -> List[Dict]:
        """Get all rules in a specific category."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE tenant_id = %s AND category = %s
                ORDER BY created_at DESC
            """,
                (self.tenant_id, category),
            )
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": row["id"],
                    "tenant_id": row["tenant_id"],
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": row["category"],
                    "tags": row["tags"],
                    "description": row["description"],
                    "is_builtin": (
                        bool(row["is_builtin"])
                        if row["is_builtin"] is not None
                        else False
                    ),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
                for row in rows
            ]
        else:
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE tenant_id = ? AND category = ?
                ORDER BY created_at DESC
            """,
                (self.tenant_id, category),
            )
            rows = cursor.fetchall()
            conn.close()
            return [
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "description": row[8],
                    "is_builtin": bool(row[9]) if row[9] is not None else False,
                    "created_at": row[10],
                    "updated_at": row[11],
                }
                for row in rows
            ]

    def get_rule_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific rule by name."""
        if not name.strip() or not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE name = %s AND tenant_id = %s
            """,
                (name.strip(), self.tenant_id),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "id": row["id"],
                    "tenant_id": row["tenant_id"],
                    "user_id": row["user_id"],
                    "name": row["name"],
                    "title": row["title"],
                    "content": row["content"],
                    "category": row["category"],
                    "tags": row["tags"],
                    "description": row["description"],
                    "is_builtin": (
                        bool(row["is_builtin"])
                        if row["is_builtin"] is not None
                        else False
                    ),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"],
                }
        else:
            cursor.execute(
                """
                SELECT id, tenant_id, user_id, name, title, content, category,
                       tags, description, is_builtin, created_at, updated_at
                FROM rules WHERE name = ? AND tenant_id = ?
            """,
                (name.strip(), self.tenant_id),
            )
            row = cursor.fetchone()
            conn.close()
            if row:
                return {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "description": row[8],
                    "is_builtin": bool(row[9]) if row[9] is not None else False,
                    "created_at": row[10],
                    "updated_at": row[11],
                }
        return None

    # Tag Management Methods

    def get_all_tags(self, entity_type: str = "all") -> List[str]:
        """Get all unique tags across prompts, templates, and/or rules."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()
        all_tags = set()

        try:
            # Get tags from prompts
            if entity_type in ["all", "prompts"]:
                if self.db_type == "postgres":
                    cursor.execute(
                        "SELECT tags FROM prompts WHERE tenant_id = %s AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )
                else:
                    cursor.execute(
                        "SELECT tags FROM prompts WHERE tenant_id = ? AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )

                for row in cursor.fetchall():
                    if row[0]:
                        tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                        all_tags.update(tags)

            # Get tags from templates
            if entity_type in ["all", "templates"]:
                if self.db_type == "postgres":
                    cursor.execute(
                        "SELECT tags FROM templates WHERE tenant_id = %s AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )
                else:
                    cursor.execute(
                        "SELECT tags FROM templates WHERE tenant_id = ? AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )

                for row in cursor.fetchall():
                    if row[0]:
                        tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                        all_tags.update(tags)

            # Get tags from rules
            if entity_type in ["all", "rules"]:
                if self.db_type == "postgres":
                    cursor.execute(
                        "SELECT tags FROM rules WHERE tenant_id = %s AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )
                else:
                    cursor.execute(
                        "SELECT tags FROM rules WHERE tenant_id = ? AND tags IS NOT NULL",
                        (self.tenant_id,),
                    )

                for row in cursor.fetchall():
                    if row[0]:
                        tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                        all_tags.update(tags)

            conn.close()
            return sorted(list(all_tags))

        except Exception:
            conn.close()
            return []

    def search_by_tags(
        self,
        tags: List[str],
        entity_type: str = "prompts",
        match_all: bool = False,
        include_enhancement_prompts: bool = True,
    ) -> List[Dict]:
        """Search entities by tags with AND/OR logic."""
        if not tags or not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        # Prepare tag conditions
        tag_conditions = []
        params = [self.tenant_id]

        for tag in tags:
            if self.db_type == "postgres":
                tag_conditions.append("tags ILIKE %s")
                params.append(f"%{tag}%")
            else:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")

        # Join conditions with AND or OR
        condition_join = " AND " if match_all else " OR "
        tag_where = f"({condition_join.join(tag_conditions)})"

        try:
            if entity_type == "prompts":
                enhancement_filter = (
                    ""
                    if include_enhancement_prompts
                    else " AND is_enhancement_prompt = FALSE"
                )

                if self.db_type == "postgres":
                    query = f"""
                        SELECT id, tenant_id, user_id, name, title, content, category,
                               tags, is_enhancement_prompt, created_at, updated_at
                        FROM prompts
                        WHERE tenant_id = %s AND {tag_where}{enhancement_filter}
                        ORDER BY category, name
                    """
                else:
                    query = f"""
                        SELECT id, tenant_id, user_id, name, title, content, category,
                               tags, is_enhancement_prompt, created_at, updated_at
                        FROM prompts
                        WHERE tenant_id = ? AND {tag_where}{enhancement_filter}
                        ORDER BY category, name
                    """

                cursor.execute(query, params)
                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "id": row[0],
                            "tenant_id": row[1],
                            "user_id": row[2],
                            "name": row[3],
                            "title": row[4],
                            "content": row[5],
                            "category": row[6],
                            "tags": row[7],
                            "is_enhancement_prompt": (
                                bool(row[8]) if row[8] is not None else False
                            ),
                            "created_at": row[9],
                            "updated_at": row[10],
                        }
                    )

            elif entity_type == "templates":
                if self.db_type == "postgres":
                    query = f"""
                        SELECT id, tenant_id, user_id, name, description, content,
                               category, tags, variables, is_builtin, created_at, updated_at
                        FROM templates
                        WHERE tenant_id = %s AND {tag_where}
                        ORDER BY category, name
                    """
                else:
                    query = f"""
                        SELECT id, tenant_id, user_id, name, description, content,
                               category, tags, variables, is_builtin, created_at, updated_at
                        FROM templates
                        WHERE tenant_id = ? AND {tag_where}
                        ORDER BY category, name
                    """

                cursor.execute(query, params)
                results = []
                for row in cursor.fetchall():
                    results.append(
                        {
                            "id": row[0],
                            "tenant_id": row[1],
                            "user_id": row[2],
                            "name": row[3],
                            "description": row[4],
                            "content": row[5],
                            "category": row[6],
                            "tags": row[7],
                            "variables": row[8],
                            "is_builtin": bool(row[9]) if row[9] is not None else False,
                            "created_at": row[10],
                            "updated_at": row[11],
                        }
                    )
            else:
                results = []

            conn.close()
            return results

        except Exception:
            conn.close()
            return []

    def get_tag_statistics(self) -> Dict[str, Dict]:
        """Get statistics about tag usage across prompts, templates, and rules."""
        if not self.tenant_id:
            return {}

        conn = self.get_conn()
        cursor = conn.cursor()
        tag_stats = {}

        try:
            # Count tags in prompts
            if self.db_type == "postgres":
                cursor.execute(
                    "SELECT tags FROM prompts WHERE tenant_id = %s AND tags IS NOT NULL",
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    "SELECT tags FROM prompts WHERE tenant_id = ? AND tags IS NOT NULL",
                    (self.tenant_id,),
                )

            for row in cursor.fetchall():
                if row[0]:
                    tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                    for tag in tags:
                        if tag not in tag_stats:
                            tag_stats[tag] = {
                                "prompts": 0,
                                "templates": 0,
                                "rules": 0,
                                "total": 0,
                            }
                        tag_stats[tag]["prompts"] += 1
                        tag_stats[tag]["total"] += 1

            # Count tags in templates
            if self.db_type == "postgres":
                cursor.execute(
                    "SELECT tags FROM templates WHERE tenant_id = %s AND tags IS NOT NULL",
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    "SELECT tags FROM templates WHERE tenant_id = ? AND tags IS NOT NULL",
                    (self.tenant_id,),
                )

            for row in cursor.fetchall():
                if row[0]:
                    tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                    for tag in tags:
                        if tag not in tag_stats:
                            tag_stats[tag] = {
                                "prompts": 0,
                                "templates": 0,
                                "rules": 0,
                                "total": 0,
                            }
                        tag_stats[tag]["templates"] += 1
                        tag_stats[tag]["total"] += 1

            # Count tags in rules
            if self.db_type == "postgres":
                cursor.execute(
                    "SELECT tags FROM rules WHERE tenant_id = %s AND tags IS NOT NULL",
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    "SELECT tags FROM rules WHERE tenant_id = ? AND tags IS NOT NULL",
                    (self.tenant_id,),
                )

            for row in cursor.fetchall():
                if row[0]:
                    tags = [tag.strip() for tag in row[0].split(",") if tag.strip()]
                    for tag in tags:
                        if tag not in tag_stats:
                            tag_stats[tag] = {
                                "prompts": 0,
                                "templates": 0,
                                "rules": 0,
                                "total": 0,
                            }
                        tag_stats[tag]["rules"] += 1
                        tag_stats[tag]["total"] += 1

            conn.close()
            return tag_stats

        except Exception:
            conn.close()
            return {}

    def get_popular_tags(self, entity_type: str = "all", limit: int = 10) -> List[Dict]:
        """Get most popular tags with usage counts."""
        tag_stats = self.get_tag_statistics()

        # Filter by entity type if specified
        if entity_type == "prompts":
            filtered_stats = {
                tag: stats for tag, stats in tag_stats.items() if stats["prompts"] > 0
            }
            sort_key = "prompts"
        elif entity_type == "templates":
            filtered_stats = {
                tag: stats for tag, stats in tag_stats.items() if stats["templates"] > 0
            }
            sort_key = "templates"
        else:
            filtered_stats = tag_stats
            sort_key = "total"

        # Sort by usage count and limit results
        popular_tags = [
            {"tag": tag, "count": stats[sort_key], "details": stats}
            for tag, stats in filtered_stats.items()
        ]
        popular_tags.sort(key=lambda x: x["count"], reverse=True)

        return popular_tags[:limit]

    def suggest_tags(self, partial_tag: str, limit: int = 5) -> List[str]:
        """Suggest tags based on partial input."""
        if not partial_tag.strip():
            return []

        all_tags = self.get_all_tags()
        partial_lower = partial_tag.lower()

        # Find exact matches first, then prefix matches, then substring matches
        exact_matches = [tag for tag in all_tags if tag.lower() == partial_lower]
        prefix_matches = [
            tag
            for tag in all_tags
            if tag.lower().startswith(partial_lower) and tag.lower() != partial_lower
        ]
        substring_matches = [
            tag
            for tag in all_tags
            if partial_lower in tag.lower()
            and not tag.lower().startswith(partial_lower)
        ]

        # Combine and limit results
        suggestions = exact_matches + prefix_matches + substring_matches
        return suggestions[:limit]

    def save_config(self, key: str, value: str) -> bool:
        """Save configuration for tenant/user"""
        if not self.tenant_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO config (tenant_id, user_id, key, value)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (tenant_id, user_id, key)
                    DO UPDATE SET value = EXCLUDED.value
                """,
                    (self.tenant_id, self.user_id, key, value),
                )
            else:
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO config (tenant_id, user_id, key, value)
                    VALUES (?, ?, ?, ?)
                """,
                    (self.tenant_id, self.user_id, key, value),
                )

            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False

    def get_config(self, key: str) -> Optional[str]:
        """Get configuration for tenant/user"""
        if not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT value FROM config
                    WHERE tenant_id = %s AND user_id = %s AND key = %s
                    """,
                    (self.tenant_id, self.user_id, key),
                )
            else:
                cursor.execute(
                    """
                    SELECT value FROM config
                    WHERE tenant_id = ? AND user_id = ? AND key = ?
                    """,
                    (self.tenant_id, self.user_id, key),
                )

            result = cursor.fetchone()
            conn.close()

            if result:
                value = result[0] if not self.db_type == "postgres" else result["value"]
                return str(value) if value is not None else None
            return None
        except Exception:
            conn.close()
            return None

    # Template management methods
    def get_all_templates(self) -> List[Dict]:
        """Get all templates for the current tenant"""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE tenant_id = %s
                    ORDER BY created_at DESC
                    """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE tenant_id = ?
                    ORDER BY created_at DESC
                    """,
                    (self.tenant_id,),
                )

            rows = cursor.fetchall()
            conn.close()

            templates = []
            for row in rows:
                if self.db_type == "postgres":
                    template = dict(row)
                else:
                    template = {
                        "id": row[0],
                        "tenant_id": row[1],
                        "user_id": row[2],
                        "name": row[3],
                        "description": row[4],
                        "content": row[5],
                        "category": row[6],
                        "tags": row[7],
                        "variables": row[8],
                        "is_builtin": bool(row[9]) if row[9] is not None else False,
                        "created_at": row[10],
                        "updated_at": row[11],
                    }
                templates.append(template)

            return templates
        except Exception:
            conn.close()
            return []

    def get_template_by_id(self, template_id: int) -> Optional[Dict]:
        """Get a specific template by ID"""
        if not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE id = %s AND tenant_id = %s
                    """,
                    (template_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE id = ? AND tenant_id = ?
                    """,
                    (template_id, self.tenant_id),
                )

            row = cursor.fetchone()
            conn.close()

            if row:
                if self.db_type == "postgres":
                    return dict(row)
                else:
                    return {
                        "id": row[0],
                        "tenant_id": row[1],
                        "user_id": row[2],
                        "name": row[3],
                        "description": row[4],
                        "content": row[5],
                        "category": row[6],
                        "tags": row[7],
                        "variables": row[8],
                        "is_builtin": bool(row[9]) if row[9] is not None else False,
                        "created_at": row[10],
                        "updated_at": row[11],
                    }
            return None
        except Exception:
            conn.close()
            return None

    def get_template_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific template by name"""
        if not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE name = %s AND tenant_id = %s
                    """,
                    (name, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, description, content,
                           category, tags, variables, is_builtin, created_at, updated_at
                    FROM templates
                    WHERE name = ? AND tenant_id = ?
                    """,
                    (name, self.tenant_id),
                )

            row = cursor.fetchone()
            conn.close()

            if row:
                if self.db_type == "postgres":
                    return dict(row)
                else:
                    return {
                        "id": row[0],
                        "tenant_id": row[1],
                        "user_id": row[2],
                        "name": row[3],
                        "description": row[4],
                        "content": row[5],
                        "category": row[6],
                        "tags": row[7],
                        "variables": row[8],
                        "is_builtin": bool(row[9]) if row[9] is not None else False,
                        "created_at": row[10],
                        "updated_at": row[11],
                    }
            return None
        except Exception:
            conn.close()
            return None

    def create_template(
        self,
        name: str,
        description: str,
        content: str,
        category: str = "Custom",
        variables: str = "",
        tags: str = "",
    ) -> str:
        """Create a new template"""
        if not self.tenant_id or not self.user_id:
            return "Error: Missing tenant or user information"

        if not name or not content:
            return "Error: Template name and content are required"

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            current_time = datetime.now().isoformat()

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO templates (tenant_id, user_id, name, description,
                                          content, category, tags, variables, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        self.tenant_id,
                        self.user_id,
                        name,
                        description,
                        content,
                        category,
                        tags,
                        variables,
                        current_time,
                        current_time,
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO templates (tenant_id, user_id, name, description,
                                          content, category, tags, variables, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.tenant_id,
                        self.user_id,
                        name,
                        description,
                        content,
                        category,
                        tags,
                        variables,
                        current_time,
                        current_time,
                    ),
                )

            conn.commit()
            conn.close()
            return "Template created successfully"

        except Exception as e:
            conn.close()
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e):
                return "Error: A template with this name already exists"
            return f"Error: Failed to create template - {str(e)}"

    def update_template(
        self,
        template_id: int,
        name: str,
        description: str,
        content: str,
        category: str = "Custom",
        variables: str = "",
        tags: str = "",
    ) -> str:
        """Update an existing template"""
        if not self.tenant_id or not self.user_id:
            return "Error: Missing tenant or user information"

        if not name or not content:
            return "Error: Template name and content are required"

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            current_time = datetime.now().isoformat()

            if self.db_type == "postgres":
                cursor.execute(
                    """
                    UPDATE templates
                    SET name = %s, description = %s, content = %s,
                        category = %s, tags = %s, variables = %s, updated_at = %s
                    WHERE id = %s AND tenant_id = %s AND user_id = %s
                    """,
                    (
                        name,
                        description,
                        content,
                        category,
                        tags,
                        variables,
                        current_time,
                        template_id,
                        self.tenant_id,
                        self.user_id,
                    ),
                )
            else:
                cursor.execute(
                    """
                    UPDATE templates
                    SET name = ?, description = ?, content = ?,
                        category = ?, tags = ?, variables = ?, updated_at = ?
                    WHERE id = ? AND tenant_id = ? AND user_id = ?
                    """,
                    (
                        name,
                        description,
                        content,
                        category,
                        tags,
                        variables,
                        current_time,
                        template_id,
                        self.tenant_id,
                        self.user_id,
                    ),
                )

            if cursor.rowcount == 0:
                conn.close()
                return (
                    "Error: Template not found or you don't have permission to edit it"
                )

            conn.commit()
            conn.close()
            return "Template updated successfully"

        except Exception as e:
            conn.close()
            if "UNIQUE constraint failed" in str(e) or "duplicate key" in str(e):
                return "Error: A template with this name already exists"
            return f"Error: Failed to update template - {str(e)}"

    def delete_template(self, template_id: int) -> bool:
        """Delete a template"""
        if not self.tenant_id or not self.user_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    DELETE FROM templates
                    WHERE id = %s AND tenant_id = %s AND user_id = %s
                    AND is_builtin = FALSE
                    """,
                    (template_id, self.tenant_id, self.user_id),
                )
            else:
                cursor.execute(
                    """
                    DELETE FROM templates
                    WHERE id = ? AND tenant_id = ? AND user_id = ?
                    AND is_builtin = 0
                    """,
                    (template_id, self.tenant_id, self.user_id),
                )

            success = bool(cursor.rowcount > 0)
            conn.commit()
            conn.close()
            return success

        except Exception:
            conn.close()
            return False

    def get_template_categories(self) -> List[str]:
        """Get all unique template categories for the current tenant"""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT DISTINCT category FROM templates
                    WHERE tenant_id = %s ORDER BY category
                    """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT DISTINCT category FROM templates
                    WHERE tenant_id = ? ORDER BY category
                    """,
                    (self.tenant_id,),
                )

            rows = cursor.fetchall()
            conn.close()

            categories = []
            for row in rows:
                category = row[0] if not self.db_type == "postgres" else row["category"]
                if category:
                    categories.append(category)

            # Add default categories if not present
            default_categories = [
                "Business",
                "Technical",
                "Creative",
                "Analytical",
                "Custom",
                "General",
            ]
            for cat in default_categories:
                if cat not in categories:
                    categories.append(cat)

            return sorted(categories)
        except Exception:
            conn.close()
            return [
                "Business",
                "Technical",
                "Creative",
                "Analytical",
                "Custom",
                "General",
            ]

    # AI Model Management Methods

    def add_ai_model(self, model_data: Dict) -> bool:
        """Add a new AI model configuration"""
        if not self.tenant_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO ai_models (
                        tenant_id, user_id, name, display_name, provider, model_id, description,
                        api_key, api_endpoint, api_version, deployment_name, max_tokens,
                        temperature, top_p, frequency_penalty, presence_penalty,
                        cost_per_1k_input_tokens, cost_per_1k_output_tokens, max_context_length,
                        supports_streaming, supports_function_calling,
                        supports_vision, supports_json_mode,
                        is_enabled, is_available
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s
                    )
                    """,
                    (
                        self.tenant_id,
                        self.user_id,
                        model_data.get("name"),
                        model_data.get("display_name"),
                        model_data.get("provider"),
                        model_data.get("model_id"),
                        model_data.get("description"),
                        model_data.get("api_key"),
                        model_data.get("api_endpoint"),
                        model_data.get("api_version"),
                        model_data.get("deployment_name"),
                        model_data.get("max_tokens"),
                        model_data.get("temperature", 0.7),
                        model_data.get("top_p", 1.0),
                        model_data.get("frequency_penalty", 0.0),
                        model_data.get("presence_penalty", 0.0),
                        model_data.get("cost_per_1k_input_tokens", 0.0),
                        model_data.get("cost_per_1k_output_tokens", 0.0),
                        model_data.get("max_context_length"),
                        model_data.get("supports_streaming", False),
                        model_data.get("supports_function_calling", False),
                        model_data.get("supports_vision", False),
                        model_data.get("supports_json_mode", False),
                        model_data.get("is_enabled", True),
                        model_data.get("is_available", False),
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO ai_models (
                        tenant_id, user_id, name, display_name, provider, model_id, description,
                        api_key, api_endpoint, api_version, deployment_name, max_tokens,
                        temperature, top_p, frequency_penalty, presence_penalty,
                        cost_per_1k_input_tokens, cost_per_1k_output_tokens, max_context_length,
                        supports_streaming, supports_function_calling,
                        supports_vision, supports_json_mode,
                        is_enabled, is_available
                    ) VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                    """,
                    (
                        self.tenant_id,
                        self.user_id,
                        model_data.get("name"),
                        model_data.get("display_name"),
                        model_data.get("provider"),
                        model_data.get("model_id"),
                        model_data.get("description"),
                        model_data.get("api_key"),
                        model_data.get("api_endpoint"),
                        model_data.get("api_version"),
                        model_data.get("deployment_name"),
                        model_data.get("max_tokens"),
                        model_data.get("temperature", 0.7),
                        model_data.get("top_p", 1.0),
                        model_data.get("frequency_penalty", 0.0),
                        model_data.get("presence_penalty", 0.0),
                        model_data.get("cost_per_1k_input_tokens", 0.0),
                        model_data.get("cost_per_1k_output_tokens", 0.0),
                        model_data.get("max_context_length"),
                        int(model_data.get("supports_streaming", False)),
                        int(model_data.get("supports_function_calling", False)),
                        int(model_data.get("supports_vision", False)),
                        int(model_data.get("supports_json_mode", False)),
                        int(model_data.get("is_enabled", True)),
                        int(model_data.get("is_available", False)),
                    ),
                )

            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False

    def get_ai_models(self) -> List[Dict]:
        """Get all AI models for the current tenant"""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, display_name, provider,
                           model_id, description, api_key, api_endpoint, api_version,
                           deployment_name, max_tokens, temperature, top_p,
                           frequency_penalty, presence_penalty,
                           cost_per_1k_input_tokens, cost_per_1k_output_tokens,
                           max_context_length, supports_streaming,
                           supports_function_calling, supports_vision,
                           supports_json_mode, is_enabled, is_available,
                           last_health_check, created_at, updated_at
                    FROM ai_models WHERE tenant_id = %s ORDER BY name
                    """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, display_name, provider,
                           model_id, description, api_key, api_endpoint, api_version,
                           deployment_name, max_tokens, temperature, top_p,
                           frequency_penalty, presence_penalty,
                           cost_per_1k_input_tokens, cost_per_1k_output_tokens,
                           max_context_length, supports_streaming,
                           supports_function_calling, supports_vision,
                           supports_json_mode, is_enabled, is_available,
                           last_health_check, created_at, updated_at
                    FROM ai_models WHERE tenant_id = ? ORDER BY name
                    """,
                    (self.tenant_id,),
                )

            models = []
            for row in cursor.fetchall():
                if self.db_type == "postgres":
                    model = dict(row)
                else:
                    model = {
                        "id": row[0],
                        "tenant_id": row[1],
                        "user_id": row[2],
                        "name": row[3],
                        "display_name": row[4],
                        "provider": row[5],
                        "model_id": row[6],
                        "description": row[7],
                        "api_key": row[8],
                        "api_endpoint": row[9],
                        "api_version": row[10],
                        "deployment_name": row[11],
                        "max_tokens": row[12],
                        "temperature": row[13],
                        "top_p": row[14],
                        "frequency_penalty": row[15],
                        "presence_penalty": row[16],
                        "cost_per_1k_input_tokens": row[17],
                        "cost_per_1k_output_tokens": row[18],
                        "max_context_length": row[19],
                        "supports_streaming": bool(row[20]),
                        "supports_function_calling": bool(row[21]),
                        "supports_vision": bool(row[22]),
                        "supports_json_mode": bool(row[23]),
                        "is_enabled": bool(row[24]),
                        "is_available": bool(row[25]),
                        "last_health_check": row[26],
                        "created_at": row[27],
                        "updated_at": row[28],
                    }
                models.append(model)

            conn.close()
            return models
        except Exception:
            conn.close()
            return []

    def update_ai_model(self, model_name: str, updates: Dict) -> bool:
        """Update an AI model configuration"""
        if not self.tenant_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Build dynamic update query
            set_clauses = []
            values = []

            for key, value in updates.items():
                if key in [
                    "display_name",
                    "description",
                    "api_key",
                    "api_endpoint",
                    "api_version",
                    "deployment_name",
                    "max_tokens",
                    "temperature",
                    "top_p",
                    "frequency_penalty",
                    "presence_penalty",
                    "cost_per_1k_input_tokens",
                    "cost_per_1k_output_tokens",
                    "max_context_length",
                    "supports_streaming",
                    "supports_function_calling",
                    "supports_vision",
                    "supports_json_mode",
                    "is_enabled",
                    "is_available",
                    "last_health_check",
                ]:
                    set_clauses.append(
                        f"{key} = {'%s' if self.db_type == 'postgres' else '?'}"
                    )
                    if key.startswith("supports_") or key in [
                        "is_enabled",
                        "is_available",
                    ]:
                        values.append(
                            value if self.db_type == "postgres" else int(value)
                        )
                    else:
                        values.append(value)

            if not set_clauses:
                # No valid fields to update, but this is not an error
                conn.close()
                return True

            # Add updated_at
            set_clauses.append(
                "updated_at = "
                + (
                    "CURRENT_TIMESTAMP"
                    if self.db_type == "postgres"
                    else "CURRENT_TIMESTAMP"
                )
            )

            # Add WHERE clause values
            values.extend([self.tenant_id, model_name])

            # set_clauses and WHERE params are controlled, not user input  # nosec B608
            query = f"""
                UPDATE ai_models
                SET {', '.join(set_clauses)}
                WHERE tenant_id = {'%s' if self.db_type == 'postgres' else '?'}
                AND name = {'%s' if self.db_type == 'postgres' else '?'}
            """

            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return bool(cursor.rowcount > 0)
        except Exception:
            conn.close()
            return False

    def delete_ai_model(self, model_name: str) -> bool:
        """Delete an AI model configuration"""
        if not self.tenant_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    "DELETE FROM ai_models WHERE tenant_id = %s AND name = %s",
                    (self.tenant_id, model_name),
                )
            else:
                cursor.execute(
                    "DELETE FROM ai_models WHERE tenant_id = ? AND name = ?",
                    (self.tenant_id, model_name),
                )

            conn.commit()
            conn.close()
            return bool(cursor.rowcount > 0)
        except Exception:
            conn.close()
            return False

    def get_ai_operation_configs(self) -> List[Dict]:
        """Get all AI operation configurations for the current tenant"""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, operation_type, primary_model,
                           fallback_models, is_enabled, custom_parameters,
                           created_at, updated_at
                    FROM ai_operation_configs WHERE tenant_id = %s
                    ORDER BY operation_type
                    """,
                    (self.tenant_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, operation_type, primary_model,
                           fallback_models, is_enabled, custom_parameters,
                           created_at, updated_at
                    FROM ai_operation_configs WHERE tenant_id = ?
                    ORDER BY operation_type
                    """,
                    (self.tenant_id,),
                )

            configs = []
            for row in cursor.fetchall():
                if self.db_type == "postgres":
                    config = dict(row)
                else:
                    config = {
                        "id": row[0],
                        "tenant_id": row[1],
                        "user_id": row[2],
                        "operation_type": row[3],
                        "primary_model": row[4],
                        "fallback_models": row[5],
                        "is_enabled": bool(row[6]),
                        "custom_parameters": row[7],
                        "created_at": row[8],
                        "updated_at": row[9],
                    }
                configs.append(config)

            conn.close()
            return configs
        except Exception:
            conn.close()
            return []

    def update_ai_operation_config(
        self, operation_type: str, config_data: Dict
    ) -> bool:
        """Update or create an AI operation configuration"""
        if not self.tenant_id:
            return False

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Check if config exists
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id FROM ai_operation_configs
                    WHERE tenant_id = %s AND operation_type = %s
                    """,
                    (self.tenant_id, operation_type),
                )
            else:
                cursor.execute(
                    """
                    SELECT id FROM ai_operation_configs
                    WHERE tenant_id = ? AND operation_type = ?
                    """,
                    (self.tenant_id, operation_type),
                )

            exists = cursor.fetchone() is not None

            if exists:
                # Update existing config
                if self.db_type == "postgres":
                    cursor.execute(
                        """
                        UPDATE ai_operation_configs
                        SET primary_model = %s, fallback_models = %s, is_enabled = %s,
                            custom_parameters = %s, updated_at = CURRENT_TIMESTAMP
                        WHERE tenant_id = %s AND operation_type = %s
                        """,
                        (
                            config_data.get("primary_model"),
                            config_data.get("fallback_models"),
                            config_data.get("is_enabled", True),
                            config_data.get("custom_parameters"),
                            self.tenant_id,
                            operation_type,
                        ),
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE ai_operation_configs
                        SET primary_model = ?, fallback_models = ?, is_enabled = ?,
                            custom_parameters = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE tenant_id = ? AND operation_type = ?
                        """,
                        (
                            config_data.get("primary_model"),
                            config_data.get("fallback_models"),
                            int(config_data.get("is_enabled", True)),
                            config_data.get("custom_parameters"),
                            self.tenant_id,
                            operation_type,
                        ),
                    )
            else:
                # Create new config
                if self.db_type == "postgres":
                    cursor.execute(
                        """
                        INSERT INTO ai_operation_configs (
                            tenant_id, user_id, operation_type, primary_model, fallback_models,
                            is_enabled, custom_parameters
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            self.tenant_id,
                            self.user_id,
                            operation_type,
                            config_data.get("primary_model"),
                            config_data.get("fallback_models"),
                            config_data.get("is_enabled", True),
                            config_data.get("custom_parameters"),
                        ),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO ai_operation_configs (
                            tenant_id, user_id, operation_type, primary_model, fallback_models,
                            is_enabled, custom_parameters
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            self.tenant_id,
                            self.user_id,
                            operation_type,
                            config_data.get("primary_model"),
                            config_data.get("fallback_models"),
                            int(config_data.get("is_enabled", True)),
                            config_data.get("custom_parameters"),
                        ),
                    )

            conn.commit()
            conn.close()
            return True
        except Exception:
            conn.close()
            return False

    def get_all_prompts_with_visibility(
        self,
        include_enhancement_prompts: bool = True,
        include_public_from_tenant: bool = True,
    ) -> List[Dict]:
        """
        Get prompts with visibility filtering.
        - Always includes user's own prompts (private + public)
        - Optionally includes public prompts from other users in the same tenant
        """
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        # Base query conditions
        conditions = [
            "tenant_id = %s" if self.db_type == "postgres" else "tenant_id = ?"
        ]
        params = [self.tenant_id]

        # Visibility filtering
        if include_public_from_tenant:
            # Include user's own prompts AND public prompts from others
            visibility_condition = (
                "(user_id = %s OR visibility = 'public')"
                if self.db_type == "postgres"
                else "(user_id = ? OR visibility = 'public')"
            )
            conditions.append(visibility_condition)
            params.append(self.user_id)
        else:
            # Only user's own prompts
            user_condition = (
                "user_id = %s" if self.db_type == "postgres" else "user_id = ?"
            )
            conditions.append(user_condition)
            params.append(self.user_id)

        # Enhancement prompt filtering
        if not include_enhancement_prompts:
            enhancement_condition = (
                "is_enhancement_prompt = FALSE"
                if self.db_type == "postgres"
                else "is_enhancement_prompt = 0"
            )
            conditions.append(enhancement_condition)

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT id, tenant_id, user_id, name, title, content, category,
            tags, is_enhancement_prompt, visibility, created_at, updated_at
            FROM prompts WHERE {where_clause} ORDER BY category, name
        """

        cursor.execute(query, tuple(params))

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
            )
        conn.close()
        return prompts

    def get_public_prompts_in_tenant(
        self, include_enhancement_prompts: bool = True
    ) -> List[Dict]:
        """Get all public prompts within the tenant (excluding user's own prompts)"""
        if not self.tenant_id or not self.user_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts 
                    WHERE tenant_id = %s AND visibility = 'public' AND user_id != %s
                    ORDER BY category, name
                """,
                    (self.tenant_id, self.user_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts 
                    WHERE tenant_id = %s AND visibility = 'public' AND user_id != %s
                    AND is_enhancement_prompt = FALSE
                    ORDER BY category, name
                """,
                    (self.tenant_id, self.user_id),
                )
        else:
            if include_enhancement_prompts:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts 
                    WHERE tenant_id = ? AND visibility = 'public' AND user_id != ?
                    ORDER BY category, name
                """,
                    (self.tenant_id, self.user_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, tenant_id, user_id, name, title, content, category,
                    tags, is_enhancement_prompt, visibility, created_at, updated_at
                    FROM prompts 
                    WHERE tenant_id = ? AND visibility = 'public' AND user_id != ?
                    AND is_enhancement_prompt = 0
                    ORDER BY category, name
                """,
                    (self.tenant_id, self.user_id),
                )

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                }
            )
        conn.close()
        return prompts

    # Project Management Methods
    def add_project(
        self,
        name: str,
        title: str,
        description: str = "",
        project_type: str = "general",
        visibility: str = "private",
        shared_with_tenant: bool = False,
    ) -> str:
        """Add a new project to the database."""
        if not name.strip():
            return "Error: Name is required!"
        if not title.strip():
            return "Error: Title is required!"
        if not self.tenant_id:
            return "Error: No tenant context available!"
        if visibility not in ["private", "public"]:
            return "Error: Visibility must be 'private' or 'public'!"
        if project_type not in ["general", "sequenced", "llm_comparison", "developer"]:
            return "Error: Invalid project type!"

        name = name.strip()
        title = title.strip()
        description = description.strip()

        conn = self.get_conn()
        cursor = conn.cursor()

        # Check for existing project within tenant
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM projects WHERE name = %s AND tenant_id = %s",
                (name, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM projects WHERE name = ? AND tenant_id = ?",
                (name, self.tenant_id),
            )

        if cursor.fetchone():
            conn.close()
            return (
                f"Error: A project with name '{name}' already exists in your workspace!"
            )

        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO projects (tenant_id, user_id, name, title, description,
                project_type, visibility, shared_with_tenant, version, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
                (
                    self.tenant_id,
                    self.user_id,
                    name,
                    title,
                    description,
                    project_type,
                    visibility,
                    shared_with_tenant,
                    1,
                    datetime.now(),
                    datetime.now(),
                ),
            )
            project_id = cursor.fetchone()[0]
        else:
            cursor.execute(
                """
                INSERT INTO projects (tenant_id, user_id, name, title, description,
                project_type, visibility, shared_with_tenant, version, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    self.tenant_id,
                    self.user_id,
                    name,
                    title,
                    description,
                    project_type,
                    visibility,
                    int(shared_with_tenant),
                    1,
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                ),
            )
            project_id = cursor.lastrowid

        # Add the creator as the owner
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (%s, %s, %s, %s)
            """,
                (project_id, self.user_id, "owner", datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (?, ?, ?, ?)
            """,
                (project_id, self.user_id, "owner", datetime.now().isoformat()),
            )

        conn.commit()
        conn.close()
        return f"Project '{title}' created successfully!"

    def get_projects(self, include_shared: bool = True) -> List[Dict]:
        """Get all projects accessible to the current user."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if include_shared:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT DISTINCT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                           p.project_type, p.visibility, p.shared_with_tenant, p.version,
                           p.tags, p.created_at, p.updated_at, pm.role
                    FROM projects p
                    LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = %s
                    WHERE p.tenant_id = %s 
                    AND (p.user_id = %s OR pm.user_id = %s OR p.shared_with_tenant = TRUE OR p.visibility = 'public')
                    ORDER BY 
                        CASE WHEN p.user_id = %s AND p.visibility = 'private' THEN 0 ELSE 1 END,
                        p.updated_at DESC
                """,
                    (
                        self.user_id,
                        self.tenant_id,
                        self.user_id,
                        self.user_id,
                        self.user_id,
                    ),
                )
            else:
                cursor.execute(
                    """
                    SELECT DISTINCT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                           p.project_type, p.visibility, p.shared_with_tenant, p.version,
                           p.tags, p.created_at, p.updated_at, pm.role
                    FROM projects p
                    LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = ?
                    WHERE p.tenant_id = ? 
                    AND (p.user_id = ? OR pm.user_id = ? OR p.shared_with_tenant = 1 OR p.visibility = 'public')
                    ORDER BY 
                        CASE WHEN p.user_id = ? AND p.visibility = 'private' THEN 0 ELSE 1 END,
                        p.updated_at DESC
                """,
                    (
                        self.user_id,
                        self.tenant_id,
                        self.user_id,
                        self.user_id,
                        self.user_id,
                    ),
                )
        else:
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                           p.project_type, p.visibility, p.shared_with_tenant, p.version,
                           p.tags, p.created_at, p.updated_at, 'owner' as role
                    FROM projects p
                    WHERE p.tenant_id = %s AND p.user_id = %s
                    ORDER BY p.updated_at DESC
                """,
                    (self.tenant_id, self.user_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                           p.project_type, p.visibility, p.shared_with_tenant, p.version,
                           p.tags, p.created_at, p.updated_at, 'owner' as role
                    FROM projects p
                    WHERE p.tenant_id = ? AND p.user_id = ?
                    ORDER BY p.updated_at DESC
                """,
                    (self.tenant_id, self.user_id),
                )

        projects = []
        for row in cursor.fetchall():
            project_dict = {
                "id": row[0],
                "tenant_id": row[1],
                "user_id": row[2],
                "name": row[3],
                "title": row[4],
                "description": row[5],
                "project_type": row[6],
                "visibility": row[7],
                "shared_with_tenant": bool(row[8]) if row[8] is not None else False,
                "version": row[9],
                "tags": row[10] if row[10] else "",
                "created_at": row[11],
                "updated_at": row[12],
                "user_role": row[13] if row[13] else None,
            }

            # Add token cost information
            token_info = self.calculate_project_token_cost(row[0])
            project_dict.update(
                {
                    "token_count": token_info.get("total_tokens", 0),
                    "token_cost": token_info.get("total_cost", 0.0),
                }
            )

            projects.append(project_dict)
        conn.close()
        return projects

    def search_projects(
        self,
        search_term: str = "",
        project_type: str = "",
        tags: str = "",
        visibility: str = "",
        include_shared: bool = True,
        limit: int = None,
        offset: int = 0,
    ) -> List[Dict]:
        """Search projects with advanced filtering and pagination."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        # Build base query with permissions
        base_query = """
            SELECT DISTINCT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                   p.project_type, p.visibility, p.shared_with_tenant, p.version,
                   p.tags, p.created_at, p.updated_at, pm.role
            FROM projects p
            LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = {}
            WHERE p.tenant_id = {}
        """.format(
            "%s" if self.db_type == "postgres" else "?",
            "%s" if self.db_type == "postgres" else "?",
        )

        params = [self.user_id, self.tenant_id]
        conditions = []

        # Permission filter
        if include_shared:
            permission_filter = "(p.user_id = {} OR pm.user_id = {} OR p.shared_with_tenant = TRUE OR p.visibility = 'public')".format(
                "%s" if self.db_type == "postgres" else "?",
                "%s" if self.db_type == "postgres" else "?",
            )
            params.extend([self.user_id, self.user_id])
        else:
            permission_filter = "p.user_id = {}".format(
                "%s" if self.db_type == "postgres" else "?"
            )
            params.append(self.user_id)

        conditions.append(permission_filter)

        # Search term filter
        if search_term.strip():
            search_condition = "(p.name LIKE {} OR p.title LIKE {} OR p.description LIKE {} OR p.tags LIKE {})".format(
                "%s" if self.db_type == "postgres" else "?",
                "%s" if self.db_type == "postgres" else "?",
                "%s" if self.db_type == "postgres" else "?",
                "%s" if self.db_type == "postgres" else "?",
            )
            conditions.append(search_condition)
            search_pattern = f"%{search_term.strip()}%"
            params.extend(
                [search_pattern, search_pattern, search_pattern, search_pattern]
            )

        # Project type filter
        if project_type.strip():
            conditions.append(
                "p.project_type = {}".format(
                    "%s" if self.db_type == "postgres" else "?"
                )
            )
            params.append(project_type.strip())

        # Tags filter
        if tags.strip():
            tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
            if tag_list:
                tag_conditions = []
                for tag in tag_list:
                    tag_conditions.append(
                        "p.tags LIKE {}".format(
                            "%s" if self.db_type == "postgres" else "?"
                        )
                    )
                    params.append(f"%{tag}%")
                conditions.append(f"({' OR '.join(tag_conditions)})")

        # Visibility filter
        if visibility.strip():
            conditions.append(
                "p.visibility = {}".format("%s" if self.db_type == "postgres" else "?")
            )
            params.append(visibility.strip())

        # Combine all conditions
        if conditions:
            base_query += " AND " + " AND ".join(conditions)

        # Add ordering
        base_query += " ORDER BY p.updated_at DESC"

        # Add pagination
        if limit:
            if self.db_type == "postgres":
                base_query += f" LIMIT %s OFFSET %s"
                params.extend([limit, offset])
            else:
                base_query += f" LIMIT ? OFFSET ?"
                params.extend([limit, offset])

        cursor.execute(base_query, params)
        rows = cursor.fetchall()

        projects = []
        for row in rows:
            project_dict = {
                "id": row[0],
                "tenant_id": row[1],
                "user_id": row[2],
                "name": row[3],
                "title": row[4],
                "description": row[5],
                "project_type": row[6],
                "visibility": row[7],
                "shared_with_tenant": bool(row[8]) if row[8] is not None else False,
                "version": row[9],
                "tags": row[10] if row[10] else "",
                "created_at": row[11],
                "updated_at": row[12],
                "user_role": row[13] if row[13] else None,
            }

            # Add token cost information (cached for performance)
            try:
                token_info = self.calculate_project_token_cost(row[0])
                project_dict.update(
                    {
                        "token_count": token_info.get("total_tokens", 0),
                        "token_cost": token_info.get("total_cost", 0.0),
                    }
                )
            except Exception:
                # Fallback if token calculation fails
                project_dict.update({"token_count": 0, "token_cost": 0.0})

            projects.append(project_dict)

        conn.close()
        return projects

    def get_project_by_id(self, project_id: int) -> Optional[Dict]:
        """Get a specific project by ID with permission check."""
        if not self.tenant_id:
            return None

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT DISTINCT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                       p.project_type, p.visibility, p.shared_with_tenant, p.version,
                       p.tags, p.created_at, p.updated_at, pm.role
                FROM projects p
                LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = %s
                WHERE p.id = %s AND p.tenant_id = %s 
                AND (p.user_id = %s OR pm.user_id = %s OR p.shared_with_tenant = TRUE OR p.visibility = 'public')
            """,
                (self.user_id, project_id, self.tenant_id, self.user_id, self.user_id),
            )
        else:
            cursor.execute(
                """
                SELECT DISTINCT p.id, p.tenant_id, p.user_id, p.name, p.title, p.description,
                       p.project_type, p.visibility, p.shared_with_tenant, p.version,
                       p.tags, p.created_at, p.updated_at, pm.role
                FROM projects p
                LEFT JOIN project_members pm ON p.id = pm.project_id AND pm.user_id = ?
                WHERE p.id = ? AND p.tenant_id = ? 
                AND (p.user_id = ? OR pm.user_id = ? OR p.shared_with_tenant = 1 OR p.visibility = 'public')
            """,
                (self.user_id, project_id, self.tenant_id, self.user_id, self.user_id),
            )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        return {
            "id": row[0],
            "tenant_id": row[1],
            "user_id": row[2],
            "name": row[3],
            "title": row[4],
            "description": row[5],
            "project_type": row[6],
            "visibility": row[7],
            "shared_with_tenant": bool(row[8]) if row[8] is not None else False,
            "version": row[9],
            "tags": row[10] if row[10] else "",
            "created_at": row[11],
            "updated_at": row[12],
            "user_role": row[13] if row[13] else None,
        }

    # Project Management Methods - Additional methods for PromptDataManager

    def update_project(
        self,
        project_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        project_type: Optional[str] = None,
        visibility: Optional[str] = None,
        shared_with_tenant: Optional[bool] = None,
    ) -> str:
        """Update an existing project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check if user has permission to edit this project
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to edit this project!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Build update query dynamically
        update_fields = []
        update_values = []

        if title is not None:
            update_fields.append("title")
            update_values.append(title.strip())
        if description is not None:
            update_fields.append("description")
            update_values.append(description.strip())
        if project_type is not None:
            if project_type not in [
                "general",
                "sequenced",
                "llm_comparison",
                "developer",
            ]:
                conn.close()
                return "Error: Invalid project type!"
            update_fields.append("project_type")
            update_values.append(project_type)
        if visibility is not None:
            if visibility not in ["private", "public"]:
                conn.close()
                return "Error: Visibility must be 'private' or 'public'!"
            update_fields.append("visibility")
            update_values.append(visibility)
        if shared_with_tenant is not None:
            update_fields.append("shared_with_tenant")
            update_values.append(shared_with_tenant)

        if not update_fields:
            conn.close()
            return "Error: No fields to update!"

        update_fields.append("updated_at")
        update_values.append(
            datetime.now() if self.db_type == "postgres" else datetime.now().isoformat()
        )
        update_values.append(project_id)

        if self.db_type == "postgres":
            placeholders = ", ".join([f"{field} = %s" for field in update_fields])
            cursor.execute(
                f"UPDATE projects SET {placeholders} WHERE id = %s",
                update_values,
            )
        else:
            placeholders = ", ".join([f"{field} = ?" for field in update_fields])
            cursor.execute(
                f"UPDATE projects SET {placeholders} WHERE id = ?",
                update_values,
            )

        conn.commit()
        conn.close()
        return "Project updated successfully!"

    def delete_project(self, project_id: int) -> str:
        """Delete a project (only by owner)."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check if user owns this project
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id:
            return "Error: Only the project owner can delete this project!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Delete project (cascade will handle related tables)
        if self.db_type == "postgres":
            cursor.execute("DELETE FROM projects WHERE id = %s", (project_id,))
        else:
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))

        conn.commit()
        conn.close()
        return f"Project '{project['title']}' deleted successfully!"

    def add_prompt_to_project(
        self, project_id: int, prompt_id: int, sequence_order: int = 0
    ) -> str:
        """Add a prompt to a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to modify this project!"

        # Check prompt exists and access
        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id, name, title, tenant_id, visibility FROM prompts WHERE id = %s AND tenant_id = %s",
                (prompt_id, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id, name, title, tenant_id, visibility FROM prompts WHERE id = ? AND tenant_id = ?",
                (prompt_id, self.tenant_id),
            )

        prompt_row = cursor.fetchone()
        conn.close()

        if not prompt_row:
            return "Error: Prompt not found or access denied!"

        prompt = {
            "id": prompt_row[0],
            "name": prompt_row[1],
            "title": prompt_row[2],
            "tenant_id": prompt_row[3],
            "visibility": prompt_row[4],
        }

        # Check visibility constraints: only public prompts can be added to public projects
        if project["visibility"] == "public" and prompt["visibility"] != "public":
            return "Error: Only public prompts can be added to public projects!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Check if prompt is already in project
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM project_prompts WHERE project_id = %s AND prompt_id = %s",
                (project_id, prompt_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM project_prompts WHERE project_id = ? AND prompt_id = ?",
                (project_id, prompt_id),
            )

        if cursor.fetchone():
            conn.close()
            return "Error: Prompt is already in this project!"

        # Add prompt to project
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_prompts (project_id, prompt_id, sequence_order, added_at)
                VALUES (%s, %s, %s, %s)
            """,
                (project_id, prompt_id, sequence_order, datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_prompts (project_id, prompt_id, sequence_order, added_at)
                VALUES (?, ?, ?, ?)
            """,
                (project_id, prompt_id, sequence_order, datetime.now().isoformat()),
            )

        conn.commit()
        conn.close()
        return f"Prompt '{prompt['title']}' added to project successfully!"

    def remove_prompt_from_project(self, project_id: int, prompt_id: int) -> str:
        """Remove a prompt from a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to modify this project!"

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "DELETE FROM project_prompts WHERE project_id = %s AND prompt_id = %s",
                (project_id, prompt_id),
            )
        else:
            cursor.execute(
                "DELETE FROM project_prompts WHERE project_id = ? AND prompt_id = ?",
                (project_id, prompt_id),
            )

        if cursor.rowcount == 0:
            conn.close()
            return "Error: Prompt not found in this project!"

        conn.commit()
        conn.close()
        return "Prompt removed from project successfully!"

    def get_project_prompts(self, project_id: int) -> List[Dict]:
        """Get all prompts in a project."""
        if not self.tenant_id:
            return []

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT p.id, p.tenant_id, p.user_id, p.name, p.title, p.content, p.category,
                       p.tags, p.is_enhancement_prompt, p.visibility, p.created_at, p.updated_at,
                       pp.sequence_order, pp.added_at
                FROM prompts p
                JOIN project_prompts pp ON p.id = pp.prompt_id
                WHERE pp.project_id = %s
                ORDER BY pp.sequence_order, pp.added_at
            """,
                (project_id,),
            )
        else:
            cursor.execute(
                """
                SELECT p.id, p.tenant_id, p.user_id, p.name, p.title, p.content, p.category,
                       p.tags, p.is_enhancement_prompt, p.visibility, p.created_at, p.updated_at,
                       pp.sequence_order, pp.added_at
                FROM prompts p
                JOIN project_prompts pp ON p.id = pp.prompt_id
                WHERE pp.project_id = ?
                ORDER BY pp.sequence_order, pp.added_at
            """,
                (project_id,),
            )

        prompts = []
        for row in cursor.fetchall():
            prompts.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "is_enhancement_prompt": (
                        bool(row[8]) if row[8] is not None else False
                    ),
                    "visibility": row[9] if row[9] is not None else "private",
                    "created_at": row[10],
                    "updated_at": row[11],
                    "sequence_order": row[12],
                    "added_to_project_at": row[13],
                }
            )
        conn.close()
        return prompts

    def add_rule_to_project(
        self, project_id: int, rule_id: int, rule_set_name: Optional[str] = None
    ) -> str:
        """Add a rule to a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to modify this project!"

        # Check rule exists
        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id, name, title, tenant_id FROM rules WHERE id = %s AND tenant_id = %s",
                (rule_id, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id, name, title, tenant_id FROM rules WHERE id = ? AND tenant_id = ?",
                (rule_id, self.tenant_id),
            )

        rule_row = cursor.fetchone()
        if not rule_row:
            conn.close()
            return "Error: Rule not found!"

        rule = {
            "id": rule_row[0],
            "name": rule_row[1],
            "title": rule_row[2],
            "tenant_id": rule_row[3],
        }

        # Check if rule is already in project
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM project_rules WHERE project_id = %s AND rule_id = %s",
                (project_id, rule_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM project_rules WHERE project_id = ? AND rule_id = ?",
                (project_id, rule_id),
            )

        if cursor.fetchone():
            conn.close()
            return "Error: Rule is already in this project!"

        # Add rule to project
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_rules (project_id, rule_id, rule_set_name, added_at)
                VALUES (%s, %s, %s, %s)
            """,
                (project_id, rule_id, rule_set_name, datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_rules (project_id, rule_id, rule_set_name, added_at)
                VALUES (?, ?, ?, ?)
            """,
                (project_id, rule_id, rule_set_name, datetime.now().isoformat()),
            )

        conn.commit()
        conn.close()
        return f"Rule '{rule['title']}' added to project successfully!"

    def remove_rule_from_project(self, project_id: int, rule_id: int) -> str:
        """Remove a rule from a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to modify this project!"

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "DELETE FROM project_rules WHERE project_id = %s AND rule_id = %s",
                (project_id, rule_id),
            )
        else:
            cursor.execute(
                "DELETE FROM project_rules WHERE project_id = ? AND rule_id = ?",
                (project_id, rule_id),
            )

        if cursor.rowcount == 0:
            conn.close()
            return "Error: Rule not found in this project!"

        conn.commit()
        conn.close()
        return "Rule removed from project successfully!"

    def get_project_rules(self, project_id: int) -> List[Dict]:
        """Get all rules in a project."""
        if not self.tenant_id:
            return []

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT r.id, r.tenant_id, r.user_id, r.name, r.title, r.content, r.category,
                       r.tags, r.description, r.is_builtin, r.created_at, r.updated_at,
                       pr.rule_set_name, pr.added_at
                FROM rules r
                JOIN project_rules pr ON r.id = pr.rule_id
                WHERE pr.project_id = %s
                ORDER BY pr.rule_set_name, pr.added_at
            """,
                (project_id,),
            )
        else:
            cursor.execute(
                """
                SELECT r.id, r.tenant_id, r.user_id, r.name, r.title, r.content, r.category,
                       r.tags, r.description, r.is_builtin, r.created_at, r.updated_at,
                       pr.rule_set_name, pr.added_at
                FROM rules r
                JOIN project_rules pr ON r.id = pr.rule_id
                WHERE pr.project_id = ?
                ORDER BY pr.rule_set_name, pr.added_at
            """,
                (project_id,),
            )

        rules = []
        for row in cursor.fetchall():
            rules.append(
                {
                    "id": row[0],
                    "tenant_id": row[1],
                    "user_id": row[2],
                    "name": row[3],
                    "title": row[4],
                    "content": row[5],
                    "category": row[6],
                    "tags": row[7],
                    "description": row[8],
                    "is_builtin": bool(row[9]) if row[9] is not None else False,
                    "created_at": row[10],
                    "updated_at": row[11],
                    "rule_set_name": row[12],
                    "added_to_project_at": row[13],
                }
            )
        conn.close()
        return rules

    def add_project_member(
        self, project_id: int, user_id: str, role: str = "member"
    ) -> str:
        """Add a member to a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access (only owner can add members)
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id:
            return "Error: Only the project owner can add members!"

        if role not in ["owner", "member", "viewer"]:
            return "Error: Invalid role! Must be 'owner', 'member', or 'viewer'!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Check if user is already a member
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = %s AND user_id = %s",
                (project_id, user_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = ? AND user_id = ?",
                (project_id, user_id),
            )

        if cursor.fetchone():
            conn.close()
            return "Error: User is already a member of this project!"

        # Add member
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (%s, %s, %s, %s)
            """,
                (project_id, user_id, role, datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (?, ?, ?, ?)
            """,
                (project_id, user_id, role, datetime.now().isoformat()),
            )

        conn.commit()
        conn.close()
        return f"User added to project as {role} successfully!"

    def remove_project_member(self, project_id: int, user_id: str) -> str:
        """Remove a member from a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access (only owner can remove members)
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id:
            return "Error: Only the project owner can remove members!"

        # Can't remove the owner
        if user_id == self.user_id:
            return "Error: Project owner cannot be removed!"

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "DELETE FROM project_members WHERE project_id = %s AND user_id = %s",
                (project_id, user_id),
            )
        else:
            cursor.execute(
                "DELETE FROM project_members WHERE project_id = ? AND user_id = ?",
                (project_id, user_id),
            )

        if cursor.rowcount == 0:
            conn.close()
            return "Error: User not found in this project!"

        conn.commit()
        conn.close()
        return "User removed from project successfully!"

    def get_project_members(self, project_id: int) -> List[Dict]:
        """Get all members of a project."""
        if not self.tenant_id:
            return []

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT pm.id, pm.project_id, pm.user_id, pm.role, pm.added_at
                FROM project_members pm
                WHERE pm.project_id = %s
                ORDER BY 
                    CASE pm.role 
                        WHEN 'owner' THEN 0 
                        WHEN 'member' THEN 1 
                        WHEN 'viewer' THEN 2 
                    END,
                    pm.added_at
            """,
                (project_id,),
            )
        else:
            cursor.execute(
                """
                SELECT pm.id, pm.project_id, pm.user_id, pm.role, pm.added_at
                FROM project_members pm
                WHERE pm.project_id = ?
                ORDER BY 
                    CASE pm.role 
                        WHEN 'owner' THEN 0 
                        WHEN 'member' THEN 1 
                        WHEN 'viewer' THEN 2 
                    END,
                    pm.added_at
            """,
                (project_id,),
            )

        members = []
        for row in cursor.fetchall():
            members.append(
                {
                    "id": row[0],
                    "project_id": row[1],
                    "user_id": row[2],
                    "role": row[3],
                    "added_at": row[4],
                }
            )
        conn.close()
        return members

    def change_project_member_role(
        self, project_id: int, user_id: str, new_role: str
    ) -> str:
        """Change the role of a project member."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access (only owner can change roles)
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id:
            return "Error: Only the project owner can change member roles!"

        if new_role not in ["owner", "member", "viewer"]:
            return "Error: Invalid role! Must be 'owner', 'member', or 'viewer'!"

        # Cannot change owner role
        if user_id == project["user_id"]:
            return "Error: Cannot change the role of the project owner!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Check if user is a member
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = %s AND user_id = %s",
                (project_id, user_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = ? AND user_id = ?",
                (project_id, user_id),
            )

        if not cursor.fetchone():
            conn.close()
            return "Error: User is not a member of this project!"

        # Update role
        if self.db_type == "postgres":
            cursor.execute(
                "UPDATE project_members SET role = %s WHERE project_id = %s AND user_id = %s",
                (new_role, project_id, user_id),
            )
        else:
            cursor.execute(
                "UPDATE project_members SET role = ? WHERE project_id = ? AND user_id = ?",
                (new_role, project_id, user_id),
            )

        conn.commit()
        conn.close()
        return f"User role changed to {new_role} successfully!"

    def invite_project_member(
        self, project_id: int, email: str, role: str = "member", message: str = ""
    ) -> str:
        """Invite a user to join a project by email."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access (only owner can invite members)
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id:
            return "Error: Only the project owner can invite members!"

        if role not in ["member", "viewer"]:
            return "Error: Invalid role! Can only invite as 'member' or 'viewer'!"

        # For now, we'll simulate the invitation process by checking if user exists
        # In a full implementation, this would send an email invitation
        conn = self.get_conn()
        cursor = conn.cursor()

        # Check if user exists in the tenant
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM users WHERE email = %s AND tenant_id = %s",
                (email, self.tenant_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM users WHERE email = ? AND tenant_id = ?",
                (email, self.tenant_id),
            )

        user_record = cursor.fetchone()
        if not user_record:
            conn.close()
            return "Error: User not found in this organization!"

        user_id = user_record[0]

        # Check if user is already a member
        if self.db_type == "postgres":
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = %s AND user_id = %s",
                (project_id, user_id),
            )
        else:
            cursor.execute(
                "SELECT id FROM project_members WHERE project_id = ? AND user_id = ?",
                (project_id, user_id),
            )

        if cursor.fetchone():
            conn.close()
            return "Error: User is already a member of this project!"

        # Add user directly (in a full implementation, this would create an invitation record)
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (%s, %s, %s, %s)
            """,
                (project_id, user_id, role, datetime.now()),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_members (project_id, user_id, role, added_at)
                VALUES (?, ?, ?, ?)
            """,
                (project_id, user_id, role, datetime.now().isoformat()),
            )

        conn.commit()
        conn.close()
        return f"User {email} invited to project as {role} successfully!"

    def get_user_project_permissions(self, project_id: int) -> Dict:
        """Get the current user's permissions for a specific project."""
        if not self.tenant_id:
            return {
                "can_view": False,
                "can_edit": False,
                "can_manage": False,
                "role": None,
            }

        project = self.get_project_by_id(project_id)
        if not project:
            return {
                "can_view": False,
                "can_edit": False,
                "can_manage": False,
                "role": None,
            }

        # Project owner has all permissions
        if project["user_id"] == self.user_id:
            return {
                "can_view": True,
                "can_edit": True,
                "can_manage": True,
                "role": "owner",
            }

        # Check member role
        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                "SELECT role FROM project_members WHERE project_id = %s AND user_id = %s",
                (project_id, self.user_id),
            )
        else:
            cursor.execute(
                "SELECT role FROM project_members WHERE project_id = ? AND user_id = ?",
                (project_id, self.user_id),
            )

        member_record = cursor.fetchone()
        conn.close()

        if member_record:
            role = member_record[0]
            if role == "member":
                return {
                    "can_view": True,
                    "can_edit": True,
                    "can_manage": False,
                    "role": "member",
                }
            elif role == "viewer":
                return {
                    "can_view": True,
                    "can_edit": False,
                    "can_manage": False,
                    "role": "viewer",
                }

        # Check if project is public and user has tenant access
        if project.get("visibility") == "public" or project.get("shared_with_tenant"):
            return {
                "can_view": True,
                "can_edit": False,
                "can_manage": False,
                "role": "public",
            }

        return {"can_view": False, "can_edit": False, "can_manage": False, "role": None}

    def transfer_project_ownership(
        self, project_id: int, new_owner_user_id: str
    ) -> Dict:
        """
        Transfer project ownership to another member of the project.

        Args:
            project_id: The project ID
            new_owner_user_id: The user ID of the new owner (must be a project member)

        Returns:
            Dictionary with success status and optional message/error
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        # Check that current user is the project owner
        project = self.get_project_by_id(project_id)
        if not project:
            return {"success": False, "error": "Project not found"}

        if project["user_id"] != self.user_id:
            return {
                "success": False,
                "error": "Only the project owner can transfer ownership",
            }

        # Verify new owner is a member of the project
        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Check if new owner is a project member
            cursor.execute(
                """
                SELECT role FROM project_members 
                WHERE project_id = ? AND user_id = ?
            """,
                (project_id, new_owner_user_id),
            )

            member_record = cursor.fetchone()
            if not member_record:
                return {
                    "success": False,
                    "error": "New owner must be a member of the project",
                }

            # Start transaction for ownership transfer
            # 1. Update project owner
            cursor.execute(
                """
                UPDATE projects 
                SET user_id = ?, updated_at = ?
                WHERE id = ? AND tenant_id = ?
            """,
                (
                    new_owner_user_id,
                    datetime.now().isoformat(),
                    project_id,
                    self.tenant_id,
                ),
            )

            # 2. Update new owner role to "owner" in members table
            cursor.execute(
                """
                UPDATE project_members 
                SET role = 'owner' 
                WHERE project_id = ? AND user_id = ?
            """,
                (project_id, new_owner_user_id),
            )

            # 3. Update old owner role to "member" (they're already in the table as owner)
            cursor.execute(
                """
                UPDATE project_members 
                SET role = 'member' 
                WHERE project_id = ? AND user_id = ?
            """,
                (project_id, self.user_id),
            )

            conn.commit()
            return {
                "success": True,
                "message": "Project ownership transferred successfully",
                "old_owner": self.user_id,
                "new_owner": new_owner_user_id,
            }

        except Exception as e:
            conn.rollback()
            return {
                "success": False,
                "error": f"Failed to transfer ownership: {str(e)}",
            }
        finally:
            conn.close()

    def calculate_project_token_cost(self, project_id: int) -> Dict:
        """
        Calculate total token cost for all prompts and rules in a project.

        Args:
            project_id: The project ID

        Returns:
            Dictionary with token counts and cost information
        """
        if not self.tenant_id:
            return {
                "success": False,
                "error": "Tenant ID is required",
                "total_tokens": 0,
                "total_cost": 0.0,
            }

        # Check permissions - user must be able to view the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_view"):
            return {
                "success": False,
                "error": "Permission denied",
                "total_tokens": 0,
                "total_cost": 0.0,
            }

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get all prompts in the project and calculate their tokens
            cursor.execute(
                """
                SELECT p.content FROM prompts p
                JOIN project_prompts pp ON p.id = pp.prompt_id
                WHERE pp.project_id = ? AND p.tenant_id = ?
            """,
                (project_id, self.tenant_id),
            )

            prompt_contents = cursor.fetchall()

            # Get all rules in the project and calculate their tokens
            cursor.execute(
                """
                SELECT r.content FROM rules r
                JOIN project_rules pr ON r.id = pr.rule_id
                WHERE pr.project_id = ? AND r.tenant_id = ?
            """,
                (project_id, self.tenant_id),
            )

            rule_contents = cursor.fetchall()

            # Calculate tokens using a simple estimation (4 characters ≈ 1 token)
            total_tokens = 0
            prompt_tokens = 0
            rule_tokens = 0

            for content_tuple in prompt_contents:
                content = content_tuple[0] if content_tuple[0] else ""
                prompt_tokens += len(content) // 4

            for content_tuple in rule_contents:
                content = content_tuple[0] if content_tuple[0] else ""
                rule_tokens += len(content) // 4

            total_tokens = prompt_tokens + rule_tokens

            # Estimate cost (using GPT-4 pricing as baseline: ~$0.03 per 1K tokens)
            cost_per_1k_tokens = 0.03
            total_cost = (total_tokens / 1000) * cost_per_1k_tokens

            return {
                "success": True,
                "total_tokens": total_tokens,
                "prompt_tokens": prompt_tokens,
                "rule_tokens": rule_tokens,
                "total_cost": round(total_cost, 4),
                "cost_per_1k_tokens": cost_per_1k_tokens,
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to calculate tokens: {str(e)}",
                "total_tokens": 0,
                "total_cost": 0.0,
            }
        finally:
            conn.close()

    def get_project_aggregate_tags(self, project_id: int) -> List[str]:
        """
        Get aggregate tags from all prompts and rules in a project.

        Args:
            project_id: The project ID

        Returns:
            List of unique tags from project contents
        """
        if not self.tenant_id:
            return []

        # Check permissions - user must be able to view the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_view"):
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            all_tags = set()

            # Get tags from all prompts in the project
            cursor.execute(
                """
                SELECT p.tags FROM prompts p
                JOIN project_prompts pp ON p.id = pp.prompt_id
                WHERE pp.project_id = ? AND p.tenant_id = ? AND p.tags IS NOT NULL
            """,
                (project_id, self.tenant_id),
            )

            for tags_tuple in cursor.fetchall():
                tags_str = tags_tuple[0]
                if tags_str:
                    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
                    all_tags.update(tags)

            # Get tags from all rules in the project
            cursor.execute(
                """
                SELECT r.tags FROM rules r
                JOIN project_rules pr ON r.id = pr.rule_id
                WHERE pr.project_id = ? AND r.tenant_id = ? AND r.tags IS NOT NULL
            """,
                (project_id, self.tenant_id),
            )

            for tags_tuple in cursor.fetchall():
                tags_str = tags_tuple[0]
                if tags_str:
                    tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
                    all_tags.update(tags)

            return sorted(list(all_tags))

        except Exception as e:
            return []
        finally:
            conn.close()

    def update_project_tags(self, project_id: int, tags: str) -> Dict:
        """
        Update project-specific tags.

        Args:
            project_id: The project ID
            tags: Comma-separated tags string

        Returns:
            Dictionary with success status and optional message/error
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        # Check permissions - user must be able to edit the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_edit"):
            return {
                "success": False,
                "error": "Permission denied: Cannot edit this project",
            }

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE projects 
                SET tags = ?, updated_at = ?
                WHERE id = ? AND tenant_id = ?
            """,
                (tags, datetime.now().isoformat(), project_id, self.tenant_id),
            )

            if cursor.rowcount == 0:
                return {"success": False, "error": "Project not found"}

            conn.commit()
            return {"success": True, "message": "Project tags updated successfully"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Failed to update tags: {str(e)}"}
        finally:
            conn.close()

    def assign_rule_to_project(self, project_id: int, rule_id: int) -> Dict:
        """
        Assign a rule to a project.

        Args:
            project_id: The project ID
            rule_id: The rule ID to assign

        Returns:
            Dictionary with success status and optional message/error
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        # Check permissions - user must be able to edit the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_edit"):
            return {
                "success": False,
                "error": "Permission denied: Cannot edit this project",
            }

        # Verify rule exists and user has access
        rule = self.get_rule(rule_id)
        if not rule:
            return {"success": False, "error": "Rule not found"}

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Check if assignment already exists
            cursor.execute(
                """
                SELECT id FROM project_rules 
                WHERE project_id = ? AND rule_id = ? AND tenant_id = ?
            """,
                (project_id, rule_id, self.tenant_id),
            )

            if cursor.fetchone():
                return {
                    "success": False,
                    "error": "Rule is already assigned to this project",
                }

            # Create the assignment
            cursor.execute(
                """
                INSERT INTO project_rules (project_id, rule_id, tenant_id, user_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    project_id,
                    rule_id,
                    self.tenant_id,
                    self.user_id,
                    datetime.now().isoformat(),
                ),
            )

            conn.commit()
            return {"success": True, "message": "Rule assigned to project successfully"}

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Failed to assign rule: {str(e)}"}
        finally:
            conn.close()

    def unassign_rule_from_project(self, project_id: int, rule_id: int) -> Dict:
        """
        Remove a rule assignment from a project.

        Args:
            project_id: The project ID
            rule_id: The rule ID to unassign

        Returns:
            Dictionary with success status and optional message/error
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        # Check permissions - user must be able to edit the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_edit"):
            return {
                "success": False,
                "error": "Permission denied: Cannot edit this project",
            }

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM project_rules 
                WHERE project_id = ? AND rule_id = ? AND tenant_id = ?
            """,
                (project_id, rule_id, self.tenant_id),
            )

            if cursor.rowcount == 0:
                return {"success": False, "error": "Rule assignment not found"}

            conn.commit()
            return {
                "success": True,
                "message": "Rule unassigned from project successfully",
            }

        except Exception as e:
            conn.rollback()
            return {"success": False, "error": f"Failed to unassign rule: {str(e)}"}
        finally:
            conn.close()

    def get_project_rules(self, project_id: int, limit: int = 50) -> List[Dict]:
        """
        Get all rules assigned to a project.

        Args:
            project_id: The project ID
            limit: Maximum number of rules to return

        Returns:
            List of rule dictionaries
        """
        if not self.tenant_id:
            return []

        # Check permissions - user must be able to view the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_view"):
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT r.id, r.name, r.title, r.content, r.category, r.tags, 
                       r.description, r.is_builtin, r.created_at, r.updated_at,
                       pr.created_at as assigned_at
                FROM rules r
                JOIN project_rules pr ON r.id = pr.rule_id
                WHERE pr.project_id = ? AND r.tenant_id = ?
                ORDER BY pr.created_at DESC
                LIMIT ?
            """,
                (project_id, self.tenant_id, limit),
            )

            rules = []
            for row in cursor.fetchall():
                rule = {
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "content": row[3],
                    "category": row[4],
                    "tags": row[5].split(",") if row[5] else [],
                    "description": row[6],
                    "is_builtin": bool(row[7]),
                    "created_at": row[8],
                    "updated_at": row[9],
                    "assigned_at": row[10],
                }
                rules.append(rule)

            return rules

        except Exception as e:
            return []
        finally:
            conn.close()

    def get_available_rules_for_project(
        self, project_id: int, search: str = "", category: str = ""
    ) -> List[Dict]:
        """
        Get rules that can be assigned to a project (not already assigned).

        Args:
            project_id: The project ID
            search: Optional search term
            category: Optional category filter

        Returns:
            List of available rule dictionaries
        """
        if not self.tenant_id:
            return []

        # Check permissions - user must be able to edit the project
        permissions = self.get_user_project_permissions(project_id)
        if not permissions.get("can_edit"):
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Build query conditions
            conditions = ["r.tenant_id = ?"]
            params = [self.tenant_id]

            # Exclude already assigned rules
            conditions.append(
                """
                r.id NOT IN (
                    SELECT rule_id FROM project_rules 
                    WHERE project_id = ? AND tenant_id = ?
                )
            """
            )
            params.extend([project_id, self.tenant_id])

            # Add search filter
            if search:
                conditions.append(
                    "(r.name LIKE ? OR r.title LIKE ? OR r.content LIKE ?)"
                )
                search_term = f"%{search}%"
                params.extend([search_term, search_term, search_term])

            # Add category filter
            if category and category != "All":
                conditions.append("r.category = ?")
                params.append(category)

            where_clause = " AND ".join(conditions)

            cursor.execute(
                f"""
                SELECT id, name, title, content, category, tags, description, 
                       is_builtin, created_at, updated_at
                FROM rules r
                WHERE {where_clause}
                ORDER BY r.created_at DESC
                LIMIT 100
            """,
                params,
            )

            rules = []
            for row in cursor.fetchall():
                rule = {
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "content": row[3],
                    "category": row[4],
                    "tags": row[5].split(",") if row[5] else [],
                    "description": row[6],
                    "is_builtin": bool(row[7]),
                    "created_at": row[8],
                    "updated_at": row[9],
                }
                rules.append(rule)

            return rules

        except Exception as e:
            return []
        finally:
            conn.close()

    def create_project_version(
        self, project_id: int, changes_description: str = ""
    ) -> str:
        """Create a new version of a project."""
        if not self.tenant_id:
            return "Error: No tenant context available!"

        # Check project access (only owner/member can version)
        project = self.get_project_by_id(project_id)
        if not project:
            return "Error: Project not found or access denied!"

        if project["user_id"] != self.user_id and project.get("user_role") not in [
            "owner",
            "member",
        ]:
            return "Error: You don't have permission to version this project!"

        conn = self.get_conn()
        cursor = conn.cursor()

        # Get current version and increment
        current_version = project["version"]
        new_version = current_version + 1

        # Update project version
        if self.db_type == "postgres":
            cursor.execute(
                "UPDATE projects SET version = %s, updated_at = %s WHERE id = %s",
                (new_version, datetime.now(), project_id),
            )
        else:
            cursor.execute(
                "UPDATE projects SET version = ?, updated_at = ? WHERE id = ?",
                (new_version, datetime.now().isoformat(), project_id),
            )

        # Create version record
        if self.db_type == "postgres":
            cursor.execute(
                """
                INSERT INTO project_versions (project_id, version_number, changes_description, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s)
            """,
                (
                    project_id,
                    new_version,
                    changes_description,
                    self.user_id,
                    datetime.now(),
                ),
            )
        else:
            cursor.execute(
                """
                INSERT INTO project_versions (project_id, version_number, changes_description, created_by, created_at)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    project_id,
                    new_version,
                    changes_description,
                    self.user_id,
                    datetime.now().isoformat(),
                ),
            )

        conn.commit()
        conn.close()
        return f"Project version {new_version} created successfully!"

    def get_project_versions(self, project_id: int) -> List[Dict]:
        """Get all versions of a project."""
        if not self.tenant_id:
            return []

        # Check project access
        project = self.get_project_by_id(project_id)
        if not project:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        if self.db_type == "postgres":
            cursor.execute(
                """
                SELECT pv.id, pv.project_id, pv.version_number, pv.changes_description, 
                       pv.created_by, pv.created_at
                FROM project_versions pv
                WHERE pv.project_id = %s
                ORDER BY pv.version_number DESC
            """,
                (project_id,),
            )
        else:
            cursor.execute(
                """
                SELECT pv.id, pv.project_id, pv.version_number, pv.changes_description, 
                       pv.created_by, pv.created_at
                FROM project_versions pv
                WHERE pv.project_id = ?
                ORDER BY pv.version_number DESC
            """,
                (project_id,),
            )

        versions = []
        for row in cursor.fetchall():
            versions.append(
                {
                    "id": row[0],
                    "project_id": row[1],
                    "version_number": row[2],
                    "changes_description": row[3],
                    "created_by": row[4],
                    "created_at": row[5],
                }
            )
        conn.close()
        return versions

    # Project Type-Specific Methods

    def execute_sequenced_project(
        self, project_id: int, execution_params: Optional[Dict] = None
    ) -> Dict:
        """
        Execute prompts in a sequenced project in order.

        Args:
            project_id: The project ID
            execution_params: Optional execution parameters

        Returns:
            Dictionary with execution results and status
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project or project["project_type"] != "sequenced":
                return {
                    "success": False,
                    "error": "Project not found or not a sequenced project",
                }

            # Get project prompts in sequence order
            cursor.execute(
                """
                SELECT pp.prompt_id, pp.sequence_order, p.name, p.title, p.content
                FROM project_prompts pp
                JOIN prompts p ON pp.prompt_id = p.id
                WHERE pp.project_id = ? AND p.tenant_id = ?
                ORDER BY pp.sequence_order ASC, pp.added_at ASC
            """,
                (project_id, self.tenant_id),
            )

            prompts = cursor.fetchall()
            if not prompts:
                return {
                    "success": False,
                    "error": "No prompts found in sequenced project",
                }

            # Execute prompts in sequence
            results = []
            execution_context = execution_params or {}

            for prompt_row in prompts:
                prompt_result = {
                    "prompt_id": prompt_row[0],
                    "sequence_order": prompt_row[1],
                    "name": prompt_row[2],
                    "title": prompt_row[3],
                    "content": prompt_row[4],
                    "executed_at": datetime.now().isoformat(),
                    "status": "ready",
                    "output": None,
                    "context": execution_context.copy(),
                }

                # For now, mark as ready for execution
                # In a full implementation, this would integrate with AI services
                results.append(prompt_result)

            # Log execution
            cursor.execute(
                """
                INSERT INTO project_versions (project_id, version_number, changes_description, created_by, created_at)
                VALUES (?, (SELECT COALESCE(MAX(version_number), 0) + 1 FROM project_versions WHERE project_id = ?), 
                        ?, ?, ?)
            """,
                (
                    project_id,
                    project_id,
                    f"Sequenced execution with {len(results)} prompts",
                    self.user_id,
                    datetime.now().isoformat(),
                ),
            )

            conn.commit()

            return {
                "success": True,
                "project_id": project_id,
                "project_name": project["name"],
                "execution_type": "sequenced",
                "total_prompts": len(results),
                "results": results,
                "executed_at": datetime.now().isoformat(),
            }

        except Exception as e:
            conn.rollback()
            return {
                "success": False,
                "error": f"Failed to execute sequenced project: {str(e)}",
            }
        finally:
            conn.close()

    def setup_llm_comparison_project(
        self, project_id: int, comparison_config: Dict
    ) -> str:
        """
        Set up LLM comparison configuration for a project.

        Args:
            project_id: The project ID
            comparison_config: Configuration for LLM comparison including models, prompts, criteria

        Returns:
            Success or error message
        """
        if not self.tenant_id:
            return "Error: Tenant ID is required"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Verify project exists and is LLM comparison type
            project = self.get_project_by_id(project_id)
            if not project or project["project_type"] != "llm_comparison":
                return "Error: Project not found or not an LLM comparison project"

            # Store comparison configuration in project metadata
            import json

            config_json = json.dumps(comparison_config)

            # Update project with comparison configuration
            cursor.execute(
                """
                UPDATE projects 
                SET description = CASE 
                    WHEN description IS NULL OR description = '' 
                    THEN 'LLM Comparison Configuration: ' || ?
                    ELSE description || ' | LLM Config: ' || ?
                END,
                updated_at = ?
                WHERE id = ? AND tenant_id = ?
            """,
                (
                    config_json,
                    config_json,
                    datetime.now().isoformat(),
                    project_id,
                    self.tenant_id,
                ),
            )

            if cursor.rowcount == 0:
                return "Error: Project not found or access denied"

            conn.commit()
            return (
                f"LLM comparison configuration saved for project '{project['title']}'"
            )

        except Exception as e:
            conn.rollback()
            return f"Error: Failed to setup LLM comparison: {str(e)}"
        finally:
            conn.close()

    def run_llm_comparison(self, project_id: int, test_inputs: List[str]) -> Dict:
        """
        Run LLM comparison analysis for a project.

        Args:
            project_id: The project ID
            test_inputs: List of test inputs to compare across models

        Returns:
            Dictionary with comparison results
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project or project["project_type"] != "llm_comparison":
                return {
                    "success": False,
                    "error": "Project not found or not an LLM comparison project",
                }

            # Get project prompts for comparison
            cursor.execute(
                """
                SELECT p.id, p.name, p.title, p.content
                FROM project_prompts pp
                JOIN prompts p ON pp.prompt_id = p.id
                WHERE pp.project_id = ? AND p.tenant_id = ?
                ORDER BY pp.added_at ASC
            """,
                (project_id, self.tenant_id),
            )

            prompts = cursor.fetchall()
            if not prompts:
                return {"success": False, "error": "No prompts found for comparison"}

            # Prepare comparison results structure
            comparison_results = {
                "project_id": project_id,
                "project_name": project["name"],
                "comparison_type": "llm_comparison",
                "test_inputs": test_inputs,
                "prompts_tested": len(prompts),
                "comparisons": [],
                "summary": {},
                "executed_at": datetime.now().isoformat(),
            }

            # For each test input, compare across all prompts
            for input_idx, test_input in enumerate(test_inputs):
                input_comparison = {
                    "input_id": input_idx + 1,
                    "test_input": test_input,
                    "prompt_results": [],
                }

                for prompt_row in prompts:
                    prompt_result = {
                        "prompt_id": prompt_row[0],
                        "prompt_name": prompt_row[1],
                        "prompt_title": prompt_row[2],
                        "prompt_content": prompt_row[3],
                        "status": "ready_for_testing",
                        "output": None,
                        "metrics": {
                            "response_length": 0,
                            "processing_time": 0,
                            "quality_score": 0,
                        },
                    }

                    # In a full implementation, this would execute the prompt with different LLMs
                    # For now, we prepare the structure for comparison
                    input_comparison["prompt_results"].append(prompt_result)

                comparison_results["comparisons"].append(input_comparison)

            # Generate summary statistics
            comparison_results["summary"] = {
                "total_comparisons": len(test_inputs) * len(prompts),
                "prompts_analyzed": len(prompts),
                "inputs_tested": len(test_inputs),
                "status": "ready_for_execution",
            }

            # Log comparison setup
            cursor.execute(
                """
                INSERT INTO project_versions (project_id, version_number, changes_description, created_by, created_at)
                VALUES (?, (SELECT COALESCE(MAX(version_number), 0) + 1 FROM project_versions WHERE project_id = ?), 
                        ?, ?, ?)
            """,
                (
                    project_id,
                    project_id,
                    f"LLM comparison setup: {len(prompts)} prompts, {len(test_inputs)} test inputs",
                    self.user_id,
                    datetime.now().isoformat(),
                ),
            )

            conn.commit()

            return {"success": True, **comparison_results}

        except Exception as e:
            conn.rollback()
            return {
                "success": False,
                "error": f"Failed to run LLM comparison: {str(e)}",
            }
        finally:
            conn.close()

    def setup_developer_workflow(self, project_id: int, workflow_config: Dict) -> str:
        """
        Set up developer workflow configuration for a project.

        Args:
            project_id: The project ID
            workflow_config: Developer workflow configuration

        Returns:
            Success or error message
        """
        if not self.tenant_id:
            return "Error: Tenant ID is required"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Verify project exists and is developer type
            project = self.get_project_by_id(project_id)
            if not project or project["project_type"] != "developer":
                return "Error: Project not found or not a developer project"

            # Set up developer-specific categories and organize prompts
            developer_categories = [
                "Code Review",
                "Bug Fixing",
                "Documentation",
                "Testing",
                "Refactoring",
                "Architecture",
                "Debugging",
                "Performance",
            ]

            # Store workflow configuration
            import json

            config_json = json.dumps(
                {
                    **workflow_config,
                    "categories": developer_categories,
                    "setup_at": datetime.now().isoformat(),
                }
            )

            # Update project with developer workflow configuration
            cursor.execute(
                """
                UPDATE projects 
                SET description = CASE 
                    WHEN description IS NULL OR description = '' 
                    THEN 'Developer Workflow: ' || ?
                    ELSE description || ' | Workflow: ' || ?
                END,
                updated_at = ?
                WHERE id = ? AND tenant_id = ?
            """,
                (
                    config_json,
                    config_json,
                    datetime.now().isoformat(),
                    project_id,
                    self.tenant_id,
                ),
            )

            if cursor.rowcount == 0:
                return "Error: Project not found or access denied"

            conn.commit()
            return f"Developer workflow configured for project '{project['title']}' with {len(developer_categories)} categories"

        except Exception as e:
            conn.rollback()
            return f"Error: Failed to setup developer workflow: {str(e)}"
        finally:
            conn.close()

    def get_developer_tools(
        self, project_id: int, category: Optional[str] = None
    ) -> Dict:
        """
        Get developer tools and prompts organized by category.

        Args:
            project_id: The project ID
            category: Optional category filter

        Returns:
            Dictionary with organized developer tools
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project or project["project_type"] != "developer":
                return {
                    "success": False,
                    "error": "Project not found or not a developer project",
                }

            # Get project prompts and rules
            query = """
                SELECT p.id, p.name, p.title, p.content, p.category, p.tags,
                       'prompt' as type, pp.added_at
                FROM project_prompts pp
                JOIN prompts p ON pp.prompt_id = p.id
                WHERE pp.project_id = ? AND p.tenant_id = ?
            """
            params = [project_id, self.tenant_id]

            if category:
                query += " AND p.category = ?"
                params.append(category)

            query += """
                UNION ALL
                SELECT r.id, r.name, r.title, r.content, r.category, r.tags,
                       'rule' as type, pr.added_at
                FROM project_rules pr
                JOIN rules r ON pr.rule_id = r.id
                WHERE pr.project_id = ? AND r.tenant_id = ?
            """
            params.extend([project_id, self.tenant_id])

            if category:
                query += " AND r.category = ?"
                params.append(category)

            query += " ORDER BY type, category, added_at DESC"

            cursor.execute(query, params)
            tools = cursor.fetchall()

            # Organize tools by category
            organized_tools = {
                "project_id": project_id,
                "project_name": project["name"],
                "workflow_type": "developer",
                "categories": {},
                "total_tools": len(tools),
                "filtered_category": category,
                "retrieved_at": datetime.now().isoformat(),
            }

            for tool in tools:
                tool_category = tool[4] or "General"
                if tool_category not in organized_tools["categories"]:
                    organized_tools["categories"][tool_category] = {
                        "prompts": [],
                        "rules": [],
                        "count": 0,
                    }

                tool_data = {
                    "id": tool[0],
                    "name": tool[1],
                    "title": tool[2],
                    "content": tool[3][:200] + "..." if len(tool[3]) > 200 else tool[3],
                    "tags": tool[5],
                    "added_at": tool[7],
                }

                tool_type = tool[6]
                organized_tools["categories"][tool_category][f"{tool_type}s"].append(
                    tool_data
                )
                organized_tools["categories"][tool_category]["count"] += 1

            return {"success": True, **organized_tools}

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get developer tools: {str(e)}",
            }
        finally:
            conn.close()

    def get_project_execution_history(self, project_id: int, limit: int = 10) -> Dict:
        """
        Get execution history for any project type.

        Args:
            project_id: The project ID
            limit: Maximum number of history entries to return

        Returns:
            Dictionary with execution history
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project:
                return {"success": False, "error": "Project not found"}

            # Get execution history from project versions
            cursor.execute(
                """
                SELECT pv.id, pv.version_number, pv.changes_description, 
                       pv.created_by, pv.created_at, p.title as project_title,
                       p.project_type
                FROM project_versions pv
                JOIN projects p ON pv.project_id = p.id
                WHERE pv.project_id = ? AND p.tenant_id = ?
                ORDER BY pv.created_at DESC
                LIMIT ?
            """,
                (project_id, self.tenant_id, limit),
            )

            history_entries = []
            for row in cursor.fetchall():
                entry = {
                    "id": row[0],
                    "version_number": row[1],
                    "description": row[2],
                    "executed_by": row[3],
                    "executed_at": row[4],
                    "project_title": row[5],
                    "project_type": row[6],
                }
                history_entries.append(entry)

            return {
                "success": True,
                "project_id": project_id,
                "project_name": project["name"],
                "project_type": project["project_type"],
                "total_entries": len(history_entries),
                "history": history_entries,
                "retrieved_at": datetime.now().isoformat(),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get execution history: {str(e)}",
            }
        finally:
            conn.close()

    # Project Dashboard Data Methods

    def get_project_dashboard_data(self, project_id: int) -> dict:
        """
        Get comprehensive dashboard data for a project.

        Args:
            project_id: The project ID

        Returns:
            Dictionary with dashboard data including stats, recent items, and members
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        try:
            # Get basic project info
            project = self.get_project_by_id(project_id)
            if not project:
                return {"success": False, "error": "Project not found"}

            # Get user permissions for this project
            permissions = self.get_user_project_permissions(project_id)

            # Get project statistics
            project_stats = self.get_project_stats(project_id)

            # Get recent prompts (last 5)
            recent_prompts = self.get_project_prompts(project_id, limit=5)

            # Get recent rules (last 5)
            recent_rules = self.get_project_rules(project_id, limit=5)

            # Get project members
            members = self.get_project_members(project_id)

            # Get recent activity/versions
            recent_versions = self.get_project_versions(project_id)[:3]

            return {
                "success": True,
                "project": project,
                "project_stats": project_stats,
                "recent_prompts": recent_prompts,
                "recent_rules": recent_rules,
                "members": members,
                "recent_versions": recent_versions,
                # Get user permissions for the project
                "can_edit": permissions.get("can_edit", False),
                "can_manage": permissions.get("can_manage", False),
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get dashboard data: {str(e)}",
            }

    def get_project_stats(self, project_id: int) -> dict:
        """Get project statistics including counts and metrics."""
        if not self.tenant_id:
            return {}

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            stats = {
                "prompt_count": 0,
                "rule_count": 0,
                "member_count": 1,
                "version": 1,
            }

            # Get prompt count
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = %s AND p.tenant_id = %s
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = ? AND p.tenant_id = ?
                """,
                    (project_id, self.tenant_id),
                )

            stats["prompt_count"] = cursor.fetchone()[0]

            # Get rule count
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = %s AND r.tenant_id = %s
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = ? AND r.tenant_id = ?
                """,
                    (project_id, self.tenant_id),
                )

            stats["rule_count"] = cursor.fetchone()[0]

            # Get member count
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_members
                    WHERE project_id = %s
                """,
                    (project_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM project_members
                    WHERE project_id = ?
                """,
                    (project_id,),
                )

            stats["member_count"] = cursor.fetchone()[0] or 1

            # Get latest version
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(version_number), 1) FROM project_versions
                    WHERE project_id = %s
                """,
                    (project_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(version_number), 1) FROM project_versions
                    WHERE project_id = ?
                """,
                    (project_id,),
                )

            stats["version"] = cursor.fetchone()[0]

            return stats

        except Exception as e:
            print(f"Error getting project stats: {e}")
            return {"prompt_count": 0, "rule_count": 0, "member_count": 1, "version": 1}
        finally:
            conn.close()

    def get_project_prompts(self, project_id: int, limit: int = None) -> list:
        """Get prompts associated with a project."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get project prompts with details
            limit_clause = f"LIMIT {limit}" if limit else ""

            if self.db_type == "postgres":
                cursor.execute(
                    f"""
                    SELECT p.id, p.name, p.title, p.content, p.category, p.tags, 
                           p.created_at, p.updated_at, pp.sequence_order, pp.added_at as added_to_project_at
                    FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = %s AND p.tenant_id = %s
                    ORDER BY pp.sequence_order, pp.added_at DESC
                    {limit_clause}
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    f"""
                    SELECT p.id, p.name, p.title, p.content, p.category, p.tags, 
                           p.created_at, p.updated_at, pp.sequence_order, pp.added_at as added_to_project_at
                    FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = ? AND p.tenant_id = ?
                    ORDER BY pp.sequence_order, pp.added_at DESC
                    {limit_clause}
                """,
                    (project_id, self.tenant_id),
                )

            prompts = []
            for row in cursor.fetchall():
                prompt = {
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "content": row[3],
                    "category": row[4],
                    "tags": row[5],
                    "created_at": row[6],
                    "updated_at": row[7],
                    "sequence_order": row[8],
                    "added_to_project_at": row[9],
                }
                prompts.append(prompt)

            return prompts

        except Exception as e:
            print(f"Error getting project prompts: {e}")
            return []
        finally:
            conn.close()

    def get_project_rules(self, project_id: int, limit: int = None) -> list:
        """Get rules associated with a project."""
        if not self.tenant_id:
            return []

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get project rules with details
            limit_clause = f"LIMIT {limit}" if limit else ""

            if self.db_type == "postgres":
                cursor.execute(
                    f"""
                    SELECT r.id, r.name, r.title, r.content, r.category, r.tags, 
                           r.created_at, r.updated_at, pr.rule_set_name, pr.added_at as added_to_project_at
                    FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = %s AND r.tenant_id = %s
                    ORDER BY pr.added_at DESC
                    {limit_clause}
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    f"""
                    SELECT r.id, r.name, r.title, r.content, r.category, r.tags, 
                           r.created_at, r.updated_at, pr.rule_set_name, pr.added_at as added_to_project_at
                    FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = ? AND r.tenant_id = ?
                    ORDER BY pr.added_at DESC
                    {limit_clause}
                """,
                    (project_id, self.tenant_id),
                )

            rules = []
            for row in cursor.fetchall():
                rule = {
                    "id": row[0],
                    "name": row[1],
                    "title": row[2],
                    "content": row[3],
                    "category": row[4],
                    "tags": row[5],
                    "created_at": row[6],
                    "updated_at": row[7],
                    "rule_set_name": row[8],
                    "added_to_project_at": row[9],
                }
                rules.append(rule)

            return rules

        except Exception as e:
            print(f"Error getting project rules: {e}")
            return []
        finally:
            conn.close()

    def get_project_members(self, project_id: int) -> list:
        """Get members of a project."""
        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get project members with details
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT pm.user_id, pm.role, pm.added_at
                    FROM project_members pm
                    WHERE pm.project_id = %s
                    ORDER BY pm.added_at
                """,
                    (project_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT pm.user_id, pm.role, pm.added_at
                    FROM project_members pm
                    WHERE pm.project_id = ?
                    ORDER BY pm.added_at
                """,
                    (project_id,),
                )

            members = []
            for row in cursor.fetchall():
                member = {
                    "user_id": row[0],
                    "user_name": row[0],  # TODO: Get actual user name from users table
                    "role": row[1],
                    "added_at": row[2],
                }
                members.append(member)

            return members

        except Exception as e:
            print(f"Error getting project members: {e}")
            return []
        finally:
            conn.close()

    # Advanced Project Versioning and Change Tracking Methods

    def create_project_snapshot(
        self,
        project_id: int,
        snapshot_description: str = "",
        include_content: bool = True,
    ) -> str:
        """
        Create a complete snapshot of a project including all prompts, rules, and settings.

        Args:
            project_id: The project ID
            snapshot_description: Description of the snapshot
            include_content: Whether to include full content or just metadata

        Returns:
            Success or error message
        """
        if not self.tenant_id:
            return "Error: Tenant ID is required"

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project:
                return "Error: Project not found"

            # Create new version number
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(version_number), 0) + 1 as next_version
                    FROM project_versions 
                    WHERE project_id = %s
                """,
                    (project_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(version_number), 0) + 1 as next_version
                    FROM project_versions 
                    WHERE project_id = ?
                """,
                    (project_id,),
                )
            next_version = cursor.fetchone()[0]

            # Collect project snapshot data
            snapshot_data = {
                "project": project,
                "prompts": [],
                "rules": [],
                "members": [],
                "metadata": {
                    "snapshot_version": next_version,
                    "created_at": datetime.now().isoformat(),
                    "created_by": self.user_id,
                    "include_content": include_content,
                },
            }

            # Get project prompts
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT pp.prompt_id, pp.sequence_order, p.name, p.title, p.content, 
                           p.category, p.tags, p.visibility, pp.added_at
                    FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = %s AND p.tenant_id = %s
                    ORDER BY pp.sequence_order, pp.added_at
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT pp.prompt_id, pp.sequence_order, p.name, p.title, p.content, 
                           p.category, p.tags, p.visibility, pp.added_at
                    FROM project_prompts pp
                    JOIN prompts p ON pp.prompt_id = p.id
                    WHERE pp.project_id = ? AND p.tenant_id = ?
                    ORDER BY pp.sequence_order, pp.added_at
                """,
                    (project_id, self.tenant_id),
                )

            for row in cursor.fetchall():
                prompt_data = {
                    "prompt_id": row[0],
                    "sequence_order": row[1],
                    "name": row[2],
                    "title": row[3],
                    "content": (
                        row[4] if include_content else f"[{len(row[4])} characters]"
                    ),
                    "category": row[5],
                    "tags": row[6],
                    "visibility": row[7],
                    "added_at": row[8],
                }
                snapshot_data["prompts"].append(prompt_data)

            # Get project rules
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT pr.rule_id, pr.rule_set_name, r.name, r.title, r.content,
                           r.category, r.tags, pr.added_at
                    FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = %s AND r.tenant_id = %s
                    ORDER BY pr.added_at
                """,
                    (project_id, self.tenant_id),
                )
            else:
                cursor.execute(
                    """
                    SELECT pr.rule_id, pr.rule_set_name, r.name, r.title, r.content,
                           r.category, r.tags, pr.added_at
                    FROM project_rules pr
                    JOIN rules r ON pr.rule_id = r.id
                    WHERE pr.project_id = ? AND r.tenant_id = ?
                    ORDER BY pr.added_at
                """,
                    (project_id, self.tenant_id),
                )

            for row in cursor.fetchall():
                rule_data = {
                    "rule_id": row[0],
                    "rule_set_name": row[1],
                    "name": row[2],
                    "title": row[3],
                    "content": (
                        row[4] if include_content else f"[{len(row[4])} characters]"
                    ),
                    "category": row[5],
                    "tags": row[6],
                    "added_at": row[7],
                }
                snapshot_data["rules"].append(rule_data)

            # Get project members
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT user_id, role, added_at
                    FROM project_members
                    WHERE project_id = %s
                    ORDER BY added_at
                """,
                    (project_id,),
                )
            else:
                cursor.execute(
                    """
                    SELECT user_id, role, added_at
                    FROM project_members
                    WHERE project_id = ?
                    ORDER BY added_at
                """,
                    (project_id,),
                )

            for row in cursor.fetchall():
                member_data = {"user_id": row[0], "role": row[1], "added_at": row[2]}
                snapshot_data["members"].append(member_data)

            # Store snapshot as JSON in project_versions
            import json

            snapshot_json = json.dumps(snapshot_data, indent=2)

            # Create version entry
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    INSERT INTO project_versions (project_id, version_number, changes_description, 
                                                snapshot_data, created_by, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (
                        project_id,
                        next_version,
                        snapshot_description
                        or f"Snapshot v{next_version}: {len(snapshot_data['prompts'])} prompts, {len(snapshot_data['rules'])} rules",
                        snapshot_json,
                        self.user_id,
                        datetime.now().isoformat(),
                    ),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO project_versions (project_id, version_number, changes_description, 
                                                snapshot_data, created_by, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        project_id,
                        next_version,
                        snapshot_description
                        or f"Snapshot v{next_version}: {len(snapshot_data['prompts'])} prompts, {len(snapshot_data['rules'])} rules",
                        snapshot_json,
                        self.user_id,
                        datetime.now().isoformat(),
                    ),
                )

            conn.commit()

            return f"Project snapshot v{next_version} created successfully! Captured {len(snapshot_data['prompts'])} prompts and {len(snapshot_data['rules'])} rules."

        except Exception as e:
            conn.rollback()
            return f"Error: Failed to create project snapshot: {str(e)}"
        finally:
            conn.close()

    def compare_project_versions(
        self, project_id: int, version1: int, version2: int
    ) -> Dict:
        """
        Compare two versions of a project and show differences.

        Args:
            project_id: The project ID
            version1: First version number to compare
            version2: Second version number to compare

        Returns:
            Dictionary with comparison results
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get both versions
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT version_number, snapshot_data, changes_description, created_at
                    FROM project_versions
                    WHERE project_id = %s AND version_number IN (%s, %s)
                    ORDER BY version_number
                """,
                    (project_id, version1, version2),
                )
            else:
                cursor.execute(
                    """
                    SELECT version_number, snapshot_data, changes_description, created_at
                    FROM project_versions
                    WHERE project_id = ? AND version_number IN (?, ?)
                    ORDER BY version_number
                """,
                    (project_id, version1, version2),
                )

            versions = cursor.fetchall()
            if len(versions) != 2:
                return {"success": False, "error": "One or both versions not found"}

            import json

            # Parse snapshot data
            v1_data = json.loads(versions[0][1]) if versions[0][1] else {}
            v2_data = json.loads(versions[1][1]) if versions[1][1] else {}

            # Compare project settings
            project_changes = []
            if v1_data.get("project") and v2_data.get("project"):
                p1, p2 = v1_data["project"], v2_data["project"]
                for key in [
                    "title",
                    "description",
                    "project_type",
                    "visibility",
                    "shared_with_tenant",
                ]:
                    if p1.get(key) != p2.get(key):
                        project_changes.append(
                            {
                                "field": key,
                                "old_value": p1.get(key),
                                "new_value": p2.get(key),
                            }
                        )

            # Compare prompts
            v1_prompts = {p["prompt_id"]: p for p in v1_data.get("prompts", [])}
            v2_prompts = {p["prompt_id"]: p for p in v2_data.get("prompts", [])}

            prompt_changes = {
                "added": [p for pid, p in v2_prompts.items() if pid not in v1_prompts],
                "removed": [
                    p for pid, p in v1_prompts.items() if pid not in v2_prompts
                ],
                "modified": [],
            }

            # Check for modified prompts
            for pid in set(v1_prompts.keys()) & set(v2_prompts.keys()):
                p1, p2 = v1_prompts[pid], v2_prompts[pid]
                changes = []
                for key in ["title", "content", "category", "tags", "sequence_order"]:
                    if p1.get(key) != p2.get(key):
                        changes.append(
                            {
                                "field": key,
                                "old_value": p1.get(key),
                                "new_value": p2.get(key),
                            }
                        )
                if changes:
                    prompt_changes["modified"].append(
                        {"prompt": p2, "changes": changes}
                    )

            # Compare rules
            v1_rules = {r["rule_id"]: r for r in v1_data.get("rules", [])}
            v2_rules = {r["rule_id"]: r for r in v2_data.get("rules", [])}

            rule_changes = {
                "added": [r for rid, r in v2_rules.items() if rid not in v1_rules],
                "removed": [r for rid, r in v1_rules.items() if rid not in v2_rules],
                "modified": [],
            }

            # Check for modified rules
            for rid in set(v1_rules.keys()) & set(v2_rules.keys()):
                r1, r2 = v1_rules[rid], v2_rules[rid]
                changes = []
                for key in ["title", "content", "category", "tags", "rule_set_name"]:
                    if r1.get(key) != r2.get(key):
                        changes.append(
                            {
                                "field": key,
                                "old_value": r1.get(key),
                                "new_value": r2.get(key),
                            }
                        )
                if changes:
                    rule_changes["modified"].append({"rule": r2, "changes": changes})

            # Compare members
            v1_members = {m["user_id"]: m for m in v1_data.get("members", [])}
            v2_members = {m["user_id"]: m for m in v2_data.get("members", [])}

            member_changes = {
                "added": [m for uid, m in v2_members.items() if uid not in v1_members],
                "removed": [
                    m for uid, m in v1_members.items() if uid not in v2_members
                ],
                "role_changes": [],
            }

            # Check for role changes
            for uid in set(v1_members.keys()) & set(v2_members.keys()):
                m1, m2 = v1_members[uid], v2_members[uid]
                if m1.get("role") != m2.get("role"):
                    member_changes["role_changes"].append(
                        {
                            "user_id": uid,
                            "old_role": m1.get("role"),
                            "new_role": m2.get("role"),
                        }
                    )

            return {
                "success": True,
                "project_id": project_id,
                "version1": {
                    "number": versions[0][0],
                    "description": versions[0][2],
                    "created_at": versions[0][3],
                },
                "version2": {
                    "number": versions[1][0],
                    "description": versions[1][2],
                    "created_at": versions[1][3],
                },
                "changes": {
                    "project": project_changes,
                    "prompts": prompt_changes,
                    "rules": rule_changes,
                    "members": member_changes,
                },
                "summary": {
                    "total_changes": len(project_changes)
                    + len(prompt_changes["added"])
                    + len(prompt_changes["removed"])
                    + len(prompt_changes["modified"])
                    + len(rule_changes["added"])
                    + len(rule_changes["removed"])
                    + len(rule_changes["modified"])
                    + len(member_changes["added"])
                    + len(member_changes["removed"])
                    + len(member_changes["role_changes"]),
                    "prompts_added": len(prompt_changes["added"]),
                    "prompts_removed": len(prompt_changes["removed"]),
                    "prompts_modified": len(prompt_changes["modified"]),
                    "rules_added": len(rule_changes["added"]),
                    "rules_removed": len(rule_changes["removed"]),
                    "rules_modified": len(rule_changes["modified"]),
                },
            }

        except Exception as e:
            return {"success": False, "error": f"Failed to compare versions: {str(e)}"}
        finally:
            conn.close()

    def restore_project_version(
        self, project_id: int, version_number: int, restore_mode: str = "full"
    ) -> str:
        """
        Restore a project to a previous version.

        Args:
            project_id: The project ID
            version_number: Version number to restore to
            restore_mode: 'full' (restore everything), 'project_only' (settings only), 'prompts_only', 'rules_only'

        Returns:
            Success or error message
        """
        if not self.tenant_id:
            return "Error: Tenant ID is required"

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get the version to restore
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT snapshot_data, changes_description
                    FROM project_versions
                    WHERE project_id = %s AND version_number = %s
                """,
                    (project_id, version_number),
                )
            else:
                cursor.execute(
                    """
                    SELECT snapshot_data, changes_description
                    FROM project_versions
                    WHERE project_id = ? AND version_number = ?
                """,
                    (project_id, version_number),
                )

            version_row = cursor.fetchone()
            if not version_row or not version_row[0]:
                return "Error: Version not found or no snapshot data available"

            import json

            snapshot_data = json.loads(version_row[0])

            # Create a backup snapshot before restoring
            backup_result = self.create_project_snapshot(
                project_id,
                f"Backup before restoring to v{version_number}",
                include_content=True,
            )

            if not backup_result.startswith("Project snapshot"):
                return f"Error: Failed to create backup: {backup_result}"

            # Restore based on mode
            if restore_mode in ["full", "project_only"]:
                # Restore project settings
                project_data = snapshot_data.get("project", {})
                if project_data:
                    cursor.execute(
                        """
                        UPDATE projects 
                        SET title = ?, description = ?, project_type = ?, 
                            visibility = ?, shared_with_tenant = ?, updated_at = ?
                        WHERE id = ? AND tenant_id = ?
                    """,
                        (
                            project_data.get("title"),
                            project_data.get("description"),
                            project_data.get("project_type"),
                            project_data.get("visibility"),
                            project_data.get("shared_with_tenant"),
                            datetime.now().isoformat(),
                            project_id,
                            self.tenant_id,
                        ),
                    )

            if restore_mode in ["full", "prompts_only"]:
                # Restore prompts - remove all current prompts and add from snapshot
                cursor.execute(
                    "DELETE FROM project_prompts WHERE project_id = ?", (project_id,)
                )

                for prompt_data in snapshot_data.get("prompts", []):
                    # Check if prompt still exists
                    cursor.execute(
                        """
                        SELECT id FROM prompts 
                        WHERE id = ? AND tenant_id = ?
                    """,
                        (prompt_data["prompt_id"], self.tenant_id),
                    )

                    if cursor.fetchone():
                        cursor.execute(
                            """
                            INSERT INTO project_prompts (project_id, prompt_id, sequence_order, added_by, added_at)
                            VALUES (?, ?, ?, ?, ?)
                        """,
                            (
                                project_id,
                                prompt_data["prompt_id"],
                                prompt_data.get("sequence_order", 0),
                                self.user_id,
                                datetime.now().isoformat(),
                            ),
                        )

            if restore_mode in ["full", "rules_only"]:
                # Restore rules - remove all current rules and add from snapshot
                cursor.execute(
                    "DELETE FROM project_rules WHERE project_id = ?", (project_id,)
                )

                for rule_data in snapshot_data.get("rules", []):
                    # Check if rule still exists
                    cursor.execute(
                        """
                        SELECT id FROM rules 
                        WHERE id = ? AND tenant_id = ?
                    """,
                        (rule_data["rule_id"], self.tenant_id),
                    )

                    if cursor.fetchone():
                        cursor.execute(
                            """
                            INSERT INTO project_rules (project_id, rule_id, rule_set_name, added_by, added_at)
                            VALUES (?, ?, ?, ?, ?)
                        """,
                            (
                                project_id,
                                rule_data["rule_id"],
                                rule_data.get("rule_set_name"),
                                self.user_id,
                                datetime.now().isoformat(),
                            ),
                        )

            if restore_mode == "full":
                # Restore members (only if full restore)
                cursor.execute(
                    "DELETE FROM project_members WHERE project_id = ?", (project_id,)
                )

                for member_data in snapshot_data.get("members", []):
                    cursor.execute(
                        """
                        INSERT INTO project_members (project_id, user_id, role, added_by, added_at)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            project_id,
                            member_data["user_id"],
                            member_data.get("role", "member"),
                            self.user_id,
                            datetime.now().isoformat(),
                        ),
                    )

            # Log the restore operation
            cursor.execute(
                """
                INSERT INTO project_versions (project_id, version_number, changes_description, created_by, created_at)
                VALUES (?, (SELECT COALESCE(MAX(version_number), 0) + 1 FROM project_versions WHERE project_id = ?), 
                        ?, ?, ?)
            """,
                (
                    project_id,
                    project_id,
                    f"Restored to version {version_number} ({restore_mode} mode): {version_row[1]}",
                    self.user_id,
                    datetime.now().isoformat(),
                ),
            )

            conn.commit()

            restored_items = []
            if restore_mode in ["full", "project_only"]:
                restored_items.append("project settings")
            if restore_mode in ["full", "prompts_only"]:
                restored_items.append(
                    f"{len(snapshot_data.get('prompts', []))} prompts"
                )
            if restore_mode in ["full", "rules_only"]:
                restored_items.append(f"{len(snapshot_data.get('rules', []))} rules")
            if restore_mode == "full":
                restored_items.append(
                    f"{len(snapshot_data.get('members', []))} members"
                )

            return f"Project restored to version {version_number} successfully! Restored: {', '.join(restored_items)}."

        except Exception as e:
            conn.rollback()
            return f"Error: Failed to restore project version: {str(e)}"
        finally:
            conn.close()

    def get_project_change_log(self, project_id: int, limit: int = 20) -> Dict:
        """
        Get comprehensive change log for a project.

        Args:
            project_id: The project ID
            limit: Maximum number of entries to return

        Returns:
            Dictionary with change log entries
        """
        if not self.tenant_id:
            return {"success": False, "error": "Tenant ID is required"}

        conn = self.get_conn()
        cursor = conn.cursor()

        try:
            # Get project details
            project = self.get_project_by_id(project_id)
            if not project:
                return {"success": False, "error": "Project not found"}

            # Get version history with change analysis
            if self.db_type == "postgres":
                cursor.execute(
                    """
                    SELECT id, version_number, changes_description, snapshot_data,
                           created_by, created_at
                    FROM project_versions
                    WHERE project_id = %s
                    ORDER BY version_number DESC
                    LIMIT %s
                """,
                    (project_id, limit),
                )
            else:
                cursor.execute(
                    """
                    SELECT id, version_number, changes_description, snapshot_data,
                           created_by, created_at
                    FROM project_versions
                    WHERE project_id = ?
                    ORDER BY version_number DESC
                    LIMIT ?
                """,
                    (project_id, limit),
                )

            change_entries = []
            prev_snapshot = None

            for row in cursor.fetchall():
                entry = {
                    "id": row[0],
                    "version_number": row[1],
                    "description": row[2],
                    "created_by": row[4],
                    "created_at": row[3],
                    "changes": [],
                    "stats": {
                        "prompts_changed": 0,
                        "rules_changed": 0,
                        "settings_changed": 0,
                        "members_changed": 0,
                    },
                }

                # Parse snapshot data if available
                if row[3]:  # snapshot_data
                    try:
                        import json

                        current_snapshot = json.loads(row[3])

                        if prev_snapshot:
                            # Analyze changes between versions
                            changes = self._analyze_snapshot_changes(
                                prev_snapshot, current_snapshot
                            )
                            entry["changes"] = changes["changes"]
                            entry["stats"] = changes["stats"]

                        prev_snapshot = current_snapshot

                    except (json.JSONDecodeError, KeyError):
                        # Skip analysis if snapshot data is invalid
                        pass

                change_entries.append(entry)

            return {
                "success": True,
                "project_id": project_id,
                "project_name": project["name"],
                "project_title": project["title"],
                "total_versions": len(change_entries),
                "change_log": change_entries,
                "retrieved_at": datetime.now().isoformat(),
            }

        except Exception as e:
            return {"success": False, "error": f"Failed to get change log: {str(e)}"}
        finally:
            conn.close()

    def _analyze_snapshot_changes(self, old_snapshot: Dict, new_snapshot: Dict) -> Dict:
        """
        Analyze changes between two snapshots.

        Args:
            old_snapshot: Previous snapshot data
            new_snapshot: Current snapshot data

        Returns:
            Dictionary with analyzed changes
        """
        changes = []
        stats = {
            "prompts_changed": 0,
            "rules_changed": 0,
            "settings_changed": 0,
            "members_changed": 0,
        }

        # Analyze project settings changes
        old_project = old_snapshot.get("project", {})
        new_project = new_snapshot.get("project", {})

        for key in [
            "title",
            "description",
            "project_type",
            "visibility",
            "shared_with_tenant",
        ]:
            if old_project.get(key) != new_project.get(key):
                changes.append(
                    {
                        "type": "project_setting",
                        "field": key,
                        "old_value": old_project.get(key),
                        "new_value": new_project.get(key),
                    }
                )
                stats["settings_changed"] += 1

        # Analyze prompts changes
        old_prompts = {p["prompt_id"]: p for p in old_snapshot.get("prompts", [])}
        new_prompts = {p["prompt_id"]: p for p in new_snapshot.get("prompts", [])}

        # Added prompts
        for pid in set(new_prompts.keys()) - set(old_prompts.keys()):
            changes.append({"type": "prompt_added", "prompt": new_prompts[pid]})
            stats["prompts_changed"] += 1

        # Removed prompts
        for pid in set(old_prompts.keys()) - set(new_prompts.keys()):
            changes.append({"type": "prompt_removed", "prompt": old_prompts[pid]})
            stats["prompts_changed"] += 1

        # Modified prompts
        for pid in set(old_prompts.keys()) & set(new_prompts.keys()):
            old_p, new_p = old_prompts[pid], new_prompts[pid]
            prompt_changes = []

            for key in ["title", "content", "category", "sequence_order"]:
                if old_p.get(key) != new_p.get(key):
                    prompt_changes.append(
                        {
                            "field": key,
                            "old_value": old_p.get(key),
                            "new_value": new_p.get(key),
                        }
                    )

            if prompt_changes:
                changes.append(
                    {
                        "type": "prompt_modified",
                        "prompt": new_p,
                        "field_changes": prompt_changes,
                    }
                )
                stats["prompts_changed"] += 1

        # Analyze rules changes (similar logic to prompts)
        old_rules = {r["rule_id"]: r for r in old_snapshot.get("rules", [])}
        new_rules = {r["rule_id"]: r for r in new_snapshot.get("rules", [])}

        for rid in set(new_rules.keys()) - set(old_rules.keys()):
            changes.append({"type": "rule_added", "rule": new_rules[rid]})
            stats["rules_changed"] += 1

        for rid in set(old_rules.keys()) - set(new_rules.keys()):
            changes.append({"type": "rule_removed", "rule": old_rules[rid]})
            stats["rules_changed"] += 1

        # Analyze member changes
        old_members = {m["user_id"]: m for m in old_snapshot.get("members", [])}
        new_members = {m["user_id"]: m for m in new_snapshot.get("members", [])}

        for uid in set(new_members.keys()) - set(old_members.keys()):
            changes.append({"type": "member_added", "member": new_members[uid]})
            stats["members_changed"] += 1

        for uid in set(old_members.keys()) - set(new_members.keys()):
            changes.append({"type": "member_removed", "member": old_members[uid]})
            stats["members_changed"] += 1

        return {"changes": changes, "stats": stats}
