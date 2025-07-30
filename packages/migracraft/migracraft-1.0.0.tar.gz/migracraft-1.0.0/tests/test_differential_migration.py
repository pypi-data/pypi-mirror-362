#!/usr/bin/env python3
"""
Tests for differential migration functionality.
"""

import pytest
from pathlib import Path
from tests.conftest import write_schema_file, read_migration_file, get_latest_migration


class TestDifferentialMigration:
    """Test suite for differential migration functionality"""
    
    def test_initial_migration_is_full(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that the first migration is always full"""
        # Write schema file
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        
        # Create first migration
        migration_tool.create_migration("initial")
        
        # Check migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 1
        
        # Read migration content
        migration_content = read_migration_file(migrations[0])
        
        # Should contain CREATE TABLE statement
        assert "CREATE TABLE IF NOT EXISTS users" in migration_content
        assert "id SERIAL PRIMARY KEY" in migration_content
        assert "username VARCHAR(50) NOT NULL UNIQUE" in migration_content
    
    def test_differential_migration_add_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test adding a column generates correct differential migration"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Modify schema - add a new column
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['phone'] = {
            'type': 'VARCHAR(20)',
            'unique': True
        }
        
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        
        # Create differential migration
        migration_tool.create_migration("add_phone_column")
        
        # Check second migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 2
        
        # Get the latest migration
        latest_migration = get_latest_migration(temp_workspace['migrations'])
        migration_content = read_migration_file(latest_migration)
        
        # Should contain ALTER TABLE ADD COLUMN
        assert "ALTER TABLE users ADD COLUMN phone VARCHAR(20)" in migration_content
        assert "ALTER TABLE users ADD CONSTRAINT" in migration_content
        assert "UNIQUE (phone)" in migration_content
    
    def test_differential_migration_add_table(self, migration_tool, temp_workspace, sample_user_schema):
        """Test adding a new table generates correct differential migration"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Add a new table to schema
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['user_profiles'] = {
            'columns': {
                'id': {'type': 'SERIAL', 'primary_key': True},
                'user_id': {'type': 'INTEGER', 'not_null': True},
                'bio': {'type': 'TEXT'},
                'avatar_url': {'type': 'VARCHAR(500)'}
            },
            'foreign_keys': {
                'user_profiles_user_fk': {
                    'column': 'user_id',
                    'references': 'users(id)',
                    'on_delete': 'CASCADE'
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        
        # Create differential migration
        migration_tool.create_migration("add_user_profiles")
        
        # Check second migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 2
        
        # Get the latest migration
        latest_migration = get_latest_migration(temp_workspace['migrations'])
        migration_content = read_migration_file(latest_migration)
        
        # Should contain CREATE TABLE for new table
        assert "CREATE TABLE IF NOT EXISTS user_profiles" in migration_content
        assert "user_id INTEGER NOT NULL" in migration_content
        assert "FOREIGN KEY (user_id) REFERENCES users(id)" in migration_content
    
    def test_differential_migration_remove_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test removing a column generates correct differential migration"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Remove a column from schema
        modified_schema = sample_user_schema.copy()
        del modified_schema['tables']['users']['columns']['last_name']
        
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        
        # Create differential migration
        migration_tool.create_migration("remove_last_name")
        
        # Check second migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 2
        
        # Get the latest migration
        latest_migration = get_latest_migration(temp_workspace['migrations'])
        migration_content = read_migration_file(latest_migration)
        
        # Should contain DROP COLUMN
        assert "ALTER TABLE users DROP COLUMN last_name" in migration_content
    
    def test_differential_migration_modify_column(self, migration_tool, temp_workspace, sample_user_schema):
        """Test modifying a column generates correct differential migration"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Modify a column in schema
        modified_schema = sample_user_schema.copy()
        modified_schema['tables']['users']['columns']['username']['type'] = 'VARCHAR(100)'  # Changed from VARCHAR(50)
        
        write_schema_file(temp_workspace['schemas'], "users.yaml", modified_schema)
        
        # Create differential migration
        migration_tool.create_migration("modify_username_length")
        
        # Check second migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 2
        
        # Get the latest migration
        latest_migration = get_latest_migration(temp_workspace['migrations'])
        migration_content = read_migration_file(latest_migration)
        
        # Should contain ALTER COLUMN
        assert "ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(100)" in migration_content
    
    def test_no_changes_no_migration(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that no migration is created when there are no changes"""
        # Create initial schema and migration
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        migration_tool.create_migration("initial")
        
        # Write the same schema again (no changes)
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        
        # Try to create another migration
        migration_tool.create_migration("no_changes")
        
        # Should still have only one migration
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 1
    
    def test_complex_differential_migration(self, migration_tool, temp_workspace, sample_complex_schema):
        """Test complex changes in a single differential migration"""
        # Create initial simple schema
        initial_schema = {
            'tables': {
                'categories': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(50)', 'not_null': True}
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "catalog.yaml", initial_schema)
        migration_tool.create_migration("initial")
        
        # Update to complex schema
        write_schema_file(temp_workspace['schemas'], "catalog.yaml", sample_complex_schema)
        
        # Create differential migration
        migration_tool.create_migration("add_products_and_orders")
        
        # Check migration was created
        migrations = list(temp_workspace['migrations'].glob("*.sql"))
        assert len(migrations) == 2
        
        # Get the latest migration
        latest_migration = get_latest_migration(temp_workspace['migrations'])
        migration_content = read_migration_file(latest_migration)
        
        # Should contain multiple changes
        assert "ALTER TABLE categories ADD COLUMN description TEXT" in migration_content
        assert "CREATE TABLE IF NOT EXISTS products" in migration_content
        assert "CREATE TABLE IF NOT EXISTS orders" in migration_content
        assert "CREATE OR REPLACE FUNCTION update_updated_at" in migration_content
