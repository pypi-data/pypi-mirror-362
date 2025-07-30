#!/usr/bin/env python3
"""
Tests for rollback migration functionality.
"""

import pytest
from pathlib import Path
from tests.conftest import write_schema_file, read_migration_file, get_latest_migration


class TestRollbackMigration:
    """Test suite for rollback migration functionality"""
    
    def test_rollback_after_add_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after adding a column"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Add a column
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['phone'] = {
            'type': 'VARCHAR(20)',
            'unique': True
        }
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("add_phone")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("remove_phone")
        
        # Check rollback migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 3  # initial + add_phone + rollback
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain DROP COLUMN
        assert "ALTER TABLE users DROP COLUMN phone" in rollback_content
        assert "ROLLBACK MIGRATION" in rollback_content
    
    def test_rollback_after_add_table(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after adding a table"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Add a table
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['posts'] = {
            'columns': {
                'id': {'type': 'SERIAL', 'primary_key': True},
                'title': {'type': 'VARCHAR(200)', 'not_null': True},
                'user_id': {'type': 'INTEGER', 'not_null': True}
            },
            'foreign_keys': {
                'posts_user_fk': {
                    'column': 'user_id',
                    'references': 'users(id)',
                    'on_delete': 'CASCADE'
                }
            }
        }
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("add_posts")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("remove_posts")
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain DROP TABLE
        assert "DROP TABLE IF EXISTS posts" in rollback_content
    
    def test_rollback_after_remove_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after removing a column"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Remove a column
        modified_schema = sample_user_schema.copy()
        del modified_schema['tables']['users']['columns']['last_name']
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("remove_last_name")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("restore_last_name")
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain ADD COLUMN to restore the removed column
        assert "ALTER TABLE users ADD COLUMN last_name VARCHAR(100)" in rollback_content
    
    def test_rollback_after_modify_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after modifying a column"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Modify a column
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['username']['type'] = 'VARCHAR(100)'  # Changed from VARCHAR(50)
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("expand_username")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("revert_username")
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain ALTER COLUMN to revert the change
        assert "ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(50)" in rollback_content
    
    def test_rollback_after_add_function(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after adding a function"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Add a function
        modified_schema = sample_user_schema.copy()
        modified_schema['functions'] = {
            'get_user_count': {
                'returns': 'INTEGER',
                'language': 'plpgsql',
                'body': '''
                BEGIN
                    RETURN (SELECT COUNT(*) FROM users);
                END;
                '''
            }
        }
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("add_function")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("remove_function")
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain DROP FUNCTION
        assert "DROP FUNCTION IF EXISTS get_user_count" in rollback_content
    
    def test_rollback_complex_changes(self, migration_tool, temp_workspace, sample_user_schema):
        """Test rollback after multiple complex changes"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Make multiple changes
        modified_schema = sample_user_schema.copy()
        
        # Add column
        modified_schema['tables']['users']['columns']['phone'] = {
            'type': 'VARCHAR(20)',
            'unique': True
        }
        
        # Remove column
        del modified_schema['tables']['users']['columns']['last_name']
        
        # Modify column
        modified_schema['tables']['users']['columns']['username']['type'] = 'VARCHAR(100)'
        
        # Add new table
        modified_schema['tables']['user_sessions'] = {
            'columns': {
                'id': {'type': 'SERIAL', 'primary_key': True},
                'user_id': {'type': 'INTEGER', 'not_null': True},
                'session_token': {'type': 'VARCHAR(255)', 'not_null': True, 'unique': True},
                'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'}
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("complex_changes")
        
        # Create rollback migration
        migration_tool.create_rollback_migration("rollback_complex")
        
        # Get the latest migration (rollback)
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Should contain all reverse operations
        assert "ALTER TABLE users DROP COLUMN phone" in rollback_content
        assert "ALTER TABLE users ADD COLUMN last_name VARCHAR(100)" in rollback_content
        assert "ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(50)" in rollback_content
        assert "DROP TABLE IF EXISTS user_sessions" in rollback_content
    
    def test_no_rollback_info_fails(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that rollback fails when no rollback info exists"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Delete rollback info file if it exists
        rollback_info_file = temp_workspace['migrations'] / ".rollback_info.json"
        if rollback_info_file.exists():
            rollback_info_file.unlink()
        
        # Try to create rollback migration
        migration_tool.create_rollback_migration("should_fail")
        
        # Should still have only the initial migration
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 1
    
    def test_rollback_after_no_changes_fails(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that rollback fails when there were no changes in last migration"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Try to create another migration with no changes
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("no_changes")  # This should not create a migration
        
        # Try to create rollback
        migration_tool.create_rollback_migration("rollback_nothing")
        
        # Should still have only the initial migration
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 1
    
    def test_rollback_migration_filename_format(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that rollback migration files have correct naming format"""
        # Create initial migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Make a change
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['phone'] = {'type': 'VARCHAR(20)'}
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("add_phone")
        
        # Create rollback migration with custom name
        migration_tool.create_rollback_migration("custom_rollback")
        
        # Check migration files
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        rollback_files = [m for m in migrations if "rollback" in m.name.lower()]
        
        assert len(rollback_files) == 1
        rollback_file = rollback_files[0]
        
        # Check filename format: should contain rollback and custom name
        assert "rollback" in rollback_file.name.lower()
        assert "custom_rollback" in rollback_file.name
        
        # Check migration number is incremented
        assert rollback_file.name.startswith("003_")  # Should be third migration
    
    def test_rollback_migration_header_content(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that rollback migration has proper header information"""
        # Create initial migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Make a change
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['phone'] = {'type': 'VARCHAR(20)'}
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        migration_tool.create_migration("add_phone")
        
        # Create rollback migration
        migration_tool.create_rollback_migration()
        
        # Get rollback migration
        rollback_migration = get_latest_migration(temp_workspace['migrations'])
        rollback_content = read_migration_file(rollback_migration)
        
        # Check header content
        assert "-- ROLLBACK MIGRATION" in rollback_content
        assert "-- This migration rolls back changes from:" in rollback_content
        assert "-- Generated on:" in rollback_content
        assert "-- WARNING:" in rollback_content
