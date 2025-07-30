#!/usr/bin/env python3

import os
import tempfile
import yaml
from pathlib import Path
from migration_tool import SchemaMigrationTool, SchemaValidationError

def test_valid_schema():
    """Test with a valid schema"""
    print("Testing valid schema...")
    
    valid_schema = {
        'tables': {
            'users': {
                'columns': {
                    'id': {'type': 'SERIAL', 'primary_key': True},
                    'name': {'type': 'VARCHAR(100)', 'not_null': True},
                    'email': {'type': 'VARCHAR(255)', 'unique': True},
                    'created_at': {'type': 'TIMESTAMP', 'default': 'NOW()'}
                },
                'indexes': [
                    {'columns': ['email'], 'unique': True},
                    {'columns': ['name'], 'name': 'idx_users_name'}
                ]
            }
        },
        'functions': {
            'get_user_count': {
                'returns': 'INTEGER',
                'body': 'SELECT COUNT(*) FROM users;',
                'language': 'sql'
            },
            'update_user_email': {
                'parameters': {
                    'user_id': 'INTEGER',
                    'new_email': 'VARCHAR(255)'
                },
                'returns': 'BOOLEAN',
                'body': '''
                    UPDATE users SET email = new_email WHERE id = user_id;
                    RETURN FOUND;
                ''',
                'language': 'plpgsql'
            }
        }
    }
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        schemas_dir.mkdir()
        
        # Write valid schema
        with open(schemas_dir / "test_schema.yaml", 'w') as f:
            yaml.dump(valid_schema, f)
        
        # Test validation
        tool = SchemaMigrationTool(str(schemas_dir), str(tmp_path / "migrations"))
        success = tool.validate_schemas_only()
        
        assert success, "Valid schema should pass validation"
        print("✓ Valid schema test passed")

def test_invalid_schemas():
    """Test with various invalid schemas"""
    print("\nTesting invalid schemas...")
    
    invalid_schemas = [
        # Missing required column type
        {
            'name': 'missing_column_type',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {
                            'id': {'primary_key': True},  # Missing type
                            'name': {'type': 'VARCHAR(100)'}
                        }
                    }
                }
            }
        },
        # Invalid column type
        {
            'name': 'invalid_column_type',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {
                            'id': {'type': 'INVALID_TYPE', 'primary_key': True}
                        }
                    }
                }
            }
        },
        # Multiple primary keys
        {
            'name': 'multiple_primary_keys',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {
                            'id': {'type': 'SERIAL', 'primary_key': True},
                            'email': {'type': 'VARCHAR(255)', 'primary_key': True}
                        }
                    }
                }
            }
        },
        # Invalid table name
        {
            'name': 'invalid_table_name',
            'schema': {
                'tables': {
                    '123invalid': {  # Invalid identifier
                        'columns': {
                            'id': {'type': 'SERIAL', 'primary_key': True}
                        }
                    }
                }
            }
        },
        # Empty table
        {
            'name': 'empty_table',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {}  # Empty columns
                    }
                }
            }
        },
        # Invalid constraint type
        {
            'name': 'invalid_constraint_type',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {
                            'id': {'type': 'SERIAL', 'primary_key': 'yes'}  # Should be boolean
                        }
                    }
                }
            }
        },
        # Invalid index definition
        {
            'name': 'invalid_index',
            'schema': {
                'tables': {
                    'users': {
                        'columns': {
                            'id': {'type': 'SERIAL', 'primary_key': True}
                        },
                        'indexes': [
                            {'columns': []}  # Empty columns list
                        ]
                    }
                }
            }
        },
        # Function without body
        {
            'name': 'function_without_body',
            'schema': {
                'functions': {
                    'test_func': {
                        'returns': 'INTEGER'
                        # Missing body
                    }
                }
            }
        },
        # Invalid function language
        {
            'name': 'invalid_function_language',
            'schema': {
                'functions': {
                    'test_func': {
                        'body': 'SELECT 1;',
                        'language': 'invalid_lang'
                    }
                }
            }
        },
        # Invalid function parameter name
        {
            'name': 'invalid_function_parameter',
            'schema': {
                'functions': {
                    'test_func': {
                        'parameters': {
                            '123invalid': 'INTEGER'  # Invalid parameter name
                        },
                        'body': 'SELECT 1;'
                    }
                }
            }
        }
    ]
    
    for test_case in invalid_schemas:
        print(f"  Testing: {test_case['name']}")
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            schemas_dir = tmp_path / "schemas"
            schemas_dir.mkdir()
            
            # Write invalid schema
            with open(schemas_dir / "test_schema.yaml", 'w') as f:
                yaml.dump(test_case['schema'], f)
            
            # Test validation should fail
            tool = SchemaMigrationTool(str(schemas_dir), str(tmp_path / "migrations"))
            success = tool.validate_schemas_only()
            
            assert not success, f"Invalid schema '{test_case['name']}' should fail validation"
            print(f"  ✓ {test_case['name']} correctly failed validation")

def test_yaml_syntax_error():
    """Test with invalid YAML syntax"""
    print("\nTesting YAML syntax error...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        schemas_dir.mkdir()
        
        # Write invalid YAML
        with open(schemas_dir / "invalid.yaml", 'w') as f:
            f.write("invalid: yaml: content: [\n")  # Malformed YAML
        
        # Test validation should fail
        tool = SchemaMigrationTool(str(schemas_dir), str(tmp_path / "migrations"))
        success = tool.validate_schemas_only()
        
        assert not success, "Invalid YAML should fail validation"
        print("✓ YAML syntax error test passed")

def test_mixed_valid_invalid():
    """Test with mix of valid and invalid schemas"""
    print("\nTesting mixed valid/invalid schemas...")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        schemas_dir = tmp_path / "schemas"
        schemas_dir.mkdir()
        
        # Write valid schema
        valid_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True}
                    }
                }
            }
        }
        with open(schemas_dir / "valid.yaml", 'w') as f:
            yaml.dump(valid_schema, f)
        
        # Write invalid schema
        invalid_schema = {
            'tables': {
                'posts': {
                    'columns': {
                        'id': {'primary_key': True}  # Missing type
                    }
                }
            }
        }
        with open(schemas_dir / "invalid.yaml", 'w') as f:
            yaml.dump(invalid_schema, f)
        
        # Test validation should fail (one invalid schema fails the whole validation)
        tool = SchemaMigrationTool(str(schemas_dir), str(tmp_path / "migrations"))
        success = tool.validate_schemas_only()
        
        assert not success, "Mixed valid/invalid schemas should fail validation"
        print("✓ Mixed schemas test passed")

def run_all_tests():
    """Run all validation tests"""
    print("Running schema validation tests...\n")
    
    test_valid_schema()
    test_invalid_schemas()
    test_yaml_syntax_error()
    test_mixed_valid_invalid()
    
    print("\n✅ All validation tests passed!")

if __name__ == "__main__":
    run_all_tests()