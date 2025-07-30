#!/usr/bin/env python3

import os
import tempfile
import yaml
from pathlib import Path
from migration_tool import SchemaMigrationTool

def test_foreign_key_validation():
    """Test foreign key validation"""
    print("Testing foreign key validation...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        schemas_dir.mkdir()
        
        # Test valid foreign key schema
        valid_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True}
                    }
                },
                'posts': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)', 'not_null': True},
                        'user_id': {'type': 'INTEGER', 'not_null': True}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['user_id'],
                            'references_table': 'users',
                            'references_columns': ['id'],
                            'name': 'fk_posts_user',
                            'on_delete': 'CASCADE',
                            'on_update': 'RESTRICT'
                        }
                    ]
                }
            }
        }
        
        with open(schemas_dir / "valid_fk.yaml", 'w') as f:
            yaml.dump(valid_schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(tmp_path / "migrations"))
        success = tool.validate_schemas_only()
        assert success, "Valid foreign key schema should pass validation"
        print("✓ Valid foreign key schema passed validation")
        
        # Test invalid foreign key schemas
        invalid_schemas = [
            # Missing required field
            {
                'name': 'missing_references_table',
                'schema': {
                    'tables': {
                        'posts': {
                            'columns': {
                                'id': {'type': 'SERIAL', 'primary_key': True},
                                'user_id': {'type': 'INTEGER'}
                            },
                            'foreign_keys': [
                                {
                                    'columns': ['user_id'],
                                    'references_columns': ['id']
                                    # Missing references_table
                                }
                            ]
                        }
                    }
                }
            },
            # Invalid action
            {
                'name': 'invalid_action',
                'schema': {
                    'tables': {
                        'posts': {
                            'columns': {
                                'id': {'type': 'SERIAL', 'primary_key': True},
                                'user_id': {'type': 'INTEGER'}
                            },
                            'foreign_keys': [
                                {
                                    'columns': ['user_id'],
                                    'references_table': 'users',
                                    'references_columns': ['id'],
                                    'on_delete': 'INVALID_ACTION'
                                }
                            ]
                        }
                    }
                }
            },
            # Column count mismatch
            {
                'name': 'column_count_mismatch',
                'schema': {
                    'tables': {
                        'posts': {
                            'columns': {
                                'id': {'type': 'SERIAL', 'primary_key': True},
                                'user_id': {'type': 'INTEGER'}
                            },
                            'foreign_keys': [
                                {
                                    'columns': ['user_id'],
                                    'references_table': 'users',
                                    'references_columns': ['id', 'name']  # Mismatch
                                }
                            ]
                        }
                    }
                }
            }
        ]
        
        for test_case in invalid_schemas:
            print(f"  Testing invalid case: {test_case['name']}")
            
            # Clear previous files
            for f in schemas_dir.glob("*.yaml"):
                f.unlink()
            
            with open(schemas_dir / "invalid_fk.yaml", 'w') as f:
                yaml.dump(test_case['schema'], f)
            
            success = tool.validate_schemas_only()
            assert not success, f"Invalid schema '{test_case['name']}' should fail validation"
            print(f"  ✓ {test_case['name']} correctly failed validation")

def test_foreign_key_creation():
    """Test foreign key creation in migrations"""
    print("\nTesting foreign key creation...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Create schema with foreign keys
        schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'email': {'type': 'VARCHAR(255)', 'unique': True}
                    }
                },
                'posts': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)', 'not_null': True},
                        'author_id': {'type': 'INTEGER', 'not_null': True}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['author_id'],
                            'references_table': 'users',
                            'references_columns': ['id'],
                            'name': 'fk_posts_author',
                            'on_delete': 'CASCADE'
                        }
                    ]
                },
                'comments': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'content': {'type': 'TEXT'},
                        'post_id': {'type': 'INTEGER'},
                        'user_id': {'type': 'INTEGER'}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['post_id'],
                            'references_table': 'posts',
                            'references_columns': ['id'],
                            'on_delete': 'CASCADE'
                        },
                        {
                            'columns': ['user_id'],
                            'references_table': 'users',
                            'references_columns': ['id'],
                            'on_delete': 'SET NULL'
                        }
                    ]
                }
            }
        }
        
        with open(schemas_dir / "blog_schema.yaml", 'w') as f:
            yaml.dump(schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("create_blog_schema")
        
        # Check migration was created
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 1
        
        with open(migrations[0], 'r') as f:
            migration_content = f.read()
        
        # Verify foreign key constraints are in the migration
        assert "ADD CONSTRAINT fk_posts_author" in migration_content
        assert "FOREIGN KEY (author_id) REFERENCES users (id)" in migration_content
        assert "ON DELETE CASCADE" in migration_content
        assert "FOREIGN KEY (post_id) REFERENCES posts (id)" in migration_content
        assert "FOREIGN KEY (user_id) REFERENCES users (id)" in migration_content
        assert "ON DELETE SET NULL" in migration_content
        
        print("✓ Foreign key creation test passed")

def test_foreign_key_modifications():
    """Test foreign key modifications in differential migrations"""
    print("\nTesting foreign key modifications...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Initial schema
        initial_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)'}
                    }
                },
                'posts': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)'},
                        'user_id': {'type': 'INTEGER'}
                    }
                }
            }
        }
        
        with open(schemas_dir / "blog_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("initial")
        
        # Modified schema - add foreign keys
        modified_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)'}
                    }
                },
                'posts': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'title': {'type': 'VARCHAR(200)'},
                        'user_id': {'type': 'INTEGER'}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['user_id'],
                            'references_table': 'users',
                            'references_columns': ['id'],
                            'on_delete': 'CASCADE'
                        }
                    ]
                }
            }
        }
        
        with open(schemas_dir / "blog_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        tool.create_migration("add_foreign_keys")
        
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 2
        
        # Find the newest migration
        newest_migration = max(migrations, key=lambda p: p.stat().st_mtime)
        
        with open(newest_migration, 'r') as f:
            migration_content = f.read()
        
        # Verify foreign key addition
        assert "ADD CONSTRAINT" in migration_content
        assert "FOREIGN KEY (user_id) REFERENCES users (id)" in migration_content
        
        print("✓ Foreign key modification test passed")

def test_foreign_key_rollback():
    """Test foreign key rollback functionality"""
    print("\nTesting foreign key rollback...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Initial schema without foreign keys
        initial_schema = {
            'tables': {
                'orders': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'customer_id': {'type': 'INTEGER'}
                    }
                }
            }
        }
        
        with open(schemas_dir / "orders_schema.yaml", 'w') as f:
            yaml.dump(initial_schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("initial")
        
        # Add foreign key
        modified_schema = {
            'tables': {
                'customers': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)'}
                    }
                },
                'orders': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'customer_id': {'type': 'INTEGER'}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['customer_id'],
                            'references_table': 'customers',
                            'references_columns': ['id'],
                            'name': 'fk_orders_customer',
                            'on_delete': 'RESTRICT'
                        }
                    ]
                }
            }
        }
        
        with open(schemas_dir / "orders_schema.yaml", 'w') as f:
            yaml.dump(modified_schema, f)
        
        # Create differential migration
        tool.create_migration("add_customers_and_fk")
        
        # Create rollback
        tool.create_rollback_migration("rollback_customers")
        
        # Check rollback migration
        migrations = list(migrations_dir.glob("*rollback*.sql"))
        assert len(migrations) == 1
        
        with open(migrations[0], 'r') as f:
            rollback_content = f.read()
        
        # Verify rollback drops foreign key and table
        assert "DROP CONSTRAINT IF EXISTS fk_orders_customer" in rollback_content
        assert "DROP TABLE IF EXISTS customers" in rollback_content
        
        print("✓ Foreign key rollback test passed")

def test_composite_foreign_keys():
    """Test composite foreign keys"""
    print("\nTesting composite foreign keys...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        migrations_dir = tmp_path / "migrations"
        
        schemas_dir.mkdir()
        
        # Schema with composite foreign key
        schema = {
            'tables': {
                'categories': {
                    'columns': {
                        'tenant_id': {'type': 'INTEGER', 'not_null': True},
                        'category_id': {'type': 'INTEGER', 'not_null': True},
                        'name': {'type': 'VARCHAR(100)'}
                    }
                },
                'products': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(200)'},
                        'tenant_id': {'type': 'INTEGER'},
                        'category_id': {'type': 'INTEGER'}
                    },
                    'foreign_keys': [
                        {
                            'columns': ['tenant_id', 'category_id'],
                            'references_table': 'categories',
                            'references_columns': ['tenant_id', 'category_id'],
                            'name': 'fk_products_category',
                            'on_delete': 'CASCADE'
                        }
                    ]
                }
            }
        }
        
        with open(schemas_dir / "composite_fk.yaml", 'w') as f:
            yaml.dump(schema, f)
        
        tool = SchemaMigrationTool(str(schemas_dir), str(migrations_dir))
        tool.create_migration("composite_fk")
        
        migrations = list(migrations_dir.glob("*.sql"))
        assert len(migrations) == 1
        
        with open(migrations[0], 'r') as f:
            migration_content = f.read()
        
        # Verify composite foreign key
        assert "FOREIGN KEY (tenant_id, category_id) REFERENCES categories (tenant_id, category_id)" in migration_content
        
        print("✓ Composite foreign key test passed")

def run_all_foreign_key_tests():
    """Run all foreign key tests"""
    print("Running foreign key functionality tests...\n")
    
    test_foreign_key_validation()
    test_foreign_key_creation()
    test_foreign_key_modifications()
    test_foreign_key_rollback()
    test_composite_foreign_keys()
    
    print("\n✅ All foreign key tests passed!")

if __name__ == "__main__":
    run_all_foreign_key_tests()