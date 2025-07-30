#!/usr/bin/env python3
"""
Base test utilities and fixtures for the migration tool tests.
"""

import pytest
import tempfile
import shutil
import yaml
from pathlib import Path
from migracraft import SchemaMigrationTool


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace for testing"""
    tmp_dir = tempfile.mkdtemp()
    tmp_path = Path(tmp_dir)
    
    workspace = {
        'root': tmp_path,
        'schemas': tmp_path / "schemas",
        'migrations': tmp_path / "migrations",
        'entities': tmp_path / "entities"
    }
    
    # Create directories
    workspace['schemas'].mkdir()
    workspace['migrations'].mkdir(exist_ok=True)
    workspace['entities'].mkdir(exist_ok=True)
    
    yield workspace
    
    # Cleanup
    shutil.rmtree(tmp_dir)


@pytest.fixture
def migration_tool(temp_workspace):
    """Create a migration tool instance with temporary workspace"""
    return SchemaMigrationTool(
        str(temp_workspace['schemas']),
        str(temp_workspace['migrations'])
    )


@pytest.fixture
def sample_user_schema():
    """Sample user schema for testing"""
    return {
        'tables': {
            'users': {
                'columns': {
                    'id': {'type': 'SERIAL', 'primary_key': True},
                    'username': {'type': 'VARCHAR(50)', 'not_null': True, 'unique': True},
                    'email': {'type': 'VARCHAR(255)', 'not_null': True, 'unique': True},
                    'password_hash': {'type': 'VARCHAR(255)', 'not_null': True},
                    'first_name': {'type': 'VARCHAR(100)'},
                    'last_name': {'type': 'VARCHAR(100)'},
                    'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
                    'updated_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'},
                    'is_active': {'type': 'BOOLEAN', 'default': 'true'}
                }
            }
        }
    }


@pytest.fixture
def sample_complex_schema():
    """Complex schema with multiple tables and relationships"""
    return {
        'tables': {
            'categories': {
                'columns': {
                    'id': {'type': 'SERIAL', 'primary_key': True},
                    'name': {'type': 'VARCHAR(100)', 'not_null': True, 'unique': True},
                    'description': {'type': 'TEXT'},
                    'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'}
                }
            },
            'products': {
                'columns': {
                    'id': {'type': 'SERIAL', 'primary_key': True},
                    'name': {'type': 'VARCHAR(200)', 'not_null': True},
                    'price': {'type': 'DECIMAL(10,2)', 'not_null': True},
                    'category_id': {'type': 'INTEGER', 'not_null': True},
                    'stock_quantity': {'type': 'INTEGER', 'default': '0'},
                    'is_available': {'type': 'BOOLEAN', 'default': 'true'},
                    'created_at': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'}
                },
                'foreign_keys': [
                    {
                        'name': 'products_category_fk',
                        'columns': ['category_id'],
                        'references_table': 'categories',
                        'references_columns': ['id'],
                        'on_delete': 'CASCADE'
                    }
                ]
            },
            'orders': {
                'columns': {
                    'id': {'type': 'SERIAL', 'primary_key': True},
                    'user_id': {'type': 'INTEGER', 'not_null': True},
                    'total_amount': {'type': 'DECIMAL(12,2)', 'not_null': True},
                    'status': {'type': 'VARCHAR(20)', 'default': "'pending'"},
                    'order_date': {'type': 'TIMESTAMP', 'default': 'CURRENT_TIMESTAMP'}
                }
            }
        },
        'functions': {
            'update_updated_at': {
                'returns': 'TRIGGER',
                'language': 'plpgsql',
                'body': '''
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                '''
            }
        }
    }


def write_schema_file(schemas_dir: Path, filename: str, schema: dict):
    """Utility function to write a schema file"""
    with open(schemas_dir / filename, 'w') as f:
        yaml.dump(schema, f, default_flow_style=False)


def read_migration_file(migration_path: Path) -> str:
    """Utility function to read a migration file"""
    with open(migration_path, 'r') as f:
        return f.read()


def get_latest_migration(migrations_dir: Path) -> Path:
    """Get the latest migration file"""
    migrations = list(migrations_dir.glob("*.sql"))
    if not migrations:
        raise FileNotFoundError("No migration files found")
    return max(migrations, key=lambda p: p.stat().st_mtime)
