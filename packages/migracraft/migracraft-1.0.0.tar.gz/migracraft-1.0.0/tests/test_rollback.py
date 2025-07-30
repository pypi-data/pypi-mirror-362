#!/usr/bin/env python3

import os
import tempfile
import yaml
from pathlib import Path
from migration_tool import SchemaMigrationTool

def test_rollback_functionality():
    """Test rollback migration functionality"""
    print("Testing rollback functionality...")
    
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
            },
            'functions': {
                'get_user_count': {
                    'returns': 'INTEGER',
                    'body': 'SELECT COUNT(*) FROM users;',
                    'language': 'sql'
                }
            }
        }
        
        # Write initial schema file
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        # Create migration tool
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        
        # Create first migration
        print("Creating first migration...")
        tool.create_migration("initial")
        
        # Check migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 1
        print(f"✓ First migration created: {migrations[0].name}")
        
        # Now modify schema significantly
        modified_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True},
                        'email': {'type': 'VARCHAR(255)', 'unique': True},  # Added column
                        'age': {'type': 'INTEGER'}  # Added column
                    },
                    'indexes': [
                        {'columns': ['email'], 'unique': True}  # Added index
                    ]
                },
                'posts': {  # Added table
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)', 'not_null': True},
                        'user_id': {'type': 'INTEGER', 'not_null': True}
                    }
                }
            },
            'functions': {
                'get_user_count': {
                    'returns': 'INTEGER',
                    'body': 'SELECT COUNT(*) FROM users WHERE age > 18;',  # Modified function
                    'language': 'sql'
                },
                'get_post_count': {  # Added function
                    'returns': 'INTEGER',
                    'body': 'SELECT COUNT(*) FROM posts;',
                    'language': 'sql'
                }
            }
        }
        
        # Write modified schema
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        print("Creating differential migration...")
        tool.create_migration("add_features")
        
        # Check second migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 2
        print(f"✓ Differential migration created")
        
        # Find the newest migration
        newest_migration = max(migrations, key=lambda p: p.stat().st_mtime)
        
        with open(newest_migration, 'r') as f:
            migration_content = f.read()
        
        print(f"Migration content preview:\n{migration_content[:200]}...")
        
        # Verify the differential migration contains expected changes
        assert "ADD COLUMN email" in migration_content
        assert "ADD COLUMN age" in migration_content
        assert "CREATE TABLE IF NOT EXISTS posts" in migration_content
        assert "CREATE OR REPLACE FUNCTION get_post_count" in migration_content
        
        print("✓ Differential migration contains expected changes")
        
        # Now test rollback creation
        print("\nTesting rollback creation...")
        tool.create_rollback_migration("undo_features")
        
        # Check rollback migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 3
        
        # Find the rollback migration
        rollback_migration = None
        for migration in migrations:
            if "rollback" in migration.name.lower():
                rollback_migration = migration
                break
        
        assert rollback_migration is not None
        print(f"✓ Rollback migration created: {rollback_migration.name}")
        
        # Read rollback migration content
        with open(rollback_migration, 'r') as f:
            rollback_content = f.read()
        
        print(f"Rollback content preview:\n{rollback_content[:300]}...")
        
        # Verify rollback migration contains expected rollback operations
        assert "-- ROLLBACK MIGRATION" in rollback_content
        assert "DROP COLUMN IF EXISTS email" in rollback_content
        assert "DROP COLUMN IF EXISTS age" in rollback_content
        assert "DROP TABLE IF EXISTS posts" in rollback_content
        assert "DROP FUNCTION IF EXISTS get_post_count" in rollback_content
        
        print("✓ Rollback migration contains expected rollback operations")
        
        print("\n✅ Rollback functionality test passed!")

def test_rollback_table_modifications():
    """Test rollback for table modifications"""
    print("\nTesting rollback for table modifications...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Create initial schema
        initial_schema = {
            'tables': {
                'products': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True},
                        'price': {'type': 'DECIMAL(10,2)'}
                    }
                }
            }
        }
        
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("initial")
        
        # Modify table - change column type and remove column
        modified_schema = {
            'tables': {
                'products': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'TEXT', 'not_null': True},  # Changed type
                        # price column removed
                        'category': {'type': 'VARCHAR(50)'}  # Added column
                    }
                }
            }
        }
        
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        tool.create_migration("modify_products")
        
        # Create rollback
        tool.create_rollback_migration("revert_products")
        
        # Check rollback migration
        migrations = list(migrations_dir.glob("*rollback*.sql"))
        assert len(migrations) == 1
        
        with open(migrations[0], 'r') as f:
            rollback_content = f.read()
        
        # Verify rollback restores the original state
        assert "DROP COLUMN IF EXISTS category" in rollback_content
        assert "ADD COLUMN price DECIMAL(10,2)" in rollback_content
        assert "ALTER COLUMN name TYPE VARCHAR(100)" in rollback_content
        
        print("✓ Table modification rollback test passed!")

def test_rollback_without_previous_migration():
    """Test rollback when there's no previous migration"""
    print("\nTesting rollback without previous migration...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        
        # Try to create rollback without any previous migration
        print("Attempting rollback without previous migration...")
        tool.create_rollback_migration()
        
        # Should not create any migration files
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 0
        
        print("✓ Correctly handled case with no previous migration")

def test_rollback_function_changes():
    """Test rollback for function changes"""
    print("\nTesting rollback for function changes...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Create initial schema with function
        initial_schema = {
            'functions': {
                'calculate_total': {
                    'parameters': {'amount': 'DECIMAL', 'tax_rate': 'DECIMAL'},
                    'returns': 'DECIMAL',
                    'body': 'RETURN amount * (1 + tax_rate);',
                    'language': 'sql'
                }
            }
        }
        
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("initial")
        
        # Modify function and add new one
        modified_schema = {
            'functions': {
                'calculate_total': {
                    'parameters': {'amount': 'DECIMAL', 'tax_rate': 'DECIMAL'},
                    'returns': 'DECIMAL',
                    'body': 'RETURN amount * (1 + tax_rate) + 0.50;',  # Modified
                    'language': 'plpgsql'  # Changed language
                },
                'get_discount': {  # Added function
                    'parameters': {'amount': 'DECIMAL'},
                    'returns': 'DECIMAL',
                    'body': 'RETURN amount * 0.1;',
                    'language': 'sql'
                }
            }
        }
        
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        tool.create_migration("modify_functions")
        
        # Create rollback
        tool.create_rollback_migration("revert_functions")
        
        # Check rollback migration
        migrations = list(migrations_dir.glob("*rollback*.sql"))
        assert len(migrations) == 1
        
        with open(migrations[0], 'r') as f:
            rollback_content = f.read()
        
        # Verify rollback restores original function and removes new one
        assert "RETURN amount * (1 + tax_rate);" in rollback_content
        assert "DROP FUNCTION IF EXISTS get_discount" in rollback_content
        
        print("✓ Function changes rollback test passed!")

def run_all_rollback_tests():
    """Run all rollback tests"""
    print("Running rollback functionality tests...\n")
    
    test_rollback_functionality()
    test_rollback_table_modifications()
    test_rollback_without_previous_migration()
    test_rollback_function_changes()
    
    print("\n✅ All rollback tests passed!")

if __name__ == "__main__":
    run_all_rollback_tests()