#!/usr/bin/env python3

import os
import tempfile
import shutil
from pathlib import Path
from migration_tool import SchemaMigrationTool

def test_differential_migration():
    """Test differential migration functionality"""
    # Create temporary directories
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Create initial schema
        initial_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True}
                    }
                }
            }
        }
        
        # Write initial schema file
        import yaml
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        # Create migration tool
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        
        # Create first migration (should be full since no previous state)
        print("Creating first migration...")
        tool.create_migration("initial")
        
        # Check migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 1
        
        # Read migration content
        with open(migrations[0], 'r') as f:
            first_migration = f.read()
        
        print(f"First migration content:\n{first_migration}")
        
        # Now modify schema
        modified_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True},
                        'email': {'type': 'VARCHAR(255)', 'unique': True}  # Added column
                    }
                },
                'posts': {  # Added table
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)', 'not_null': True},
                        'user_id': {'type': 'INTEGER', 'not_null': True}
                    }
                }
            }
        }
        
        # Write modified schema
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        print("\nCreating differential migration...")
        tool.create_migration("add_email_and_posts")
        
        # Check second migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 2
        
        # Find the newest migration
        newest_migration = max(migrations, key=lambda p: p.stat().st_mtime)
        
        with open(newest_migration, 'r') as f:
            second_migration = f.read()
        
        print(f"Second migration content:\n{second_migration}")
        
        # Verify the differential migration contains expected changes
        assert "ADD COLUMN email" in second_migration
        assert "CREATE TABLE IF NOT EXISTS posts" in second_migration
        
        print("\nTest passed! Differential migration working correctly.")

if __name__ == "__main__":
    test_differential_migration()