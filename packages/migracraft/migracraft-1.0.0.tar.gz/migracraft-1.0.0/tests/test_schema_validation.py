#!/usr/bin/env python3
"""
Tests for schema validation functionality.
"""

import pytest
from tests.conftest import write_schema_file


class TestSchemaValidation:
    """Test suite for schema validation functionality"""
    
    def test_valid_schema_passes(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that valid schemas pass validation"""
        # Write valid schema file
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        
        # Validate schemas
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_invalid_column_type_fails(self, migration_tool, temp_workspace):
        """Test that invalid column types fail validation"""
        invalid_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'INVALID_TYPE', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True}
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "invalid.yaml", invalid_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_missing_required_fields_fails(self, migration_tool, temp_workspace):
        """Test that missing required fields fail validation"""
        invalid_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'primary_key': True},  # Missing 'type'
                        'name': {'type': 'VARCHAR(100)'}
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "missing_type.yaml", invalid_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_invalid_yaml_syntax_fails(self, migration_tool, temp_workspace):
        """Test that invalid YAML syntax fails validation"""
        # Write invalid YAML
        invalid_yaml_path = temp_workspace['schemas'] / "invalid.yaml"
        with open(invalid_yaml_path, 'w') as f:
            f.write("""
            tables:
              users:
                columns:
                  id: {type: 'SERIAL', primary_key: True
                  name: 'VARCHAR(100)'  # Missing closing brace
            """)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_empty_schema_passes(self, migration_tool, temp_workspace):
        """Test that empty schemas pass validation (they're ignored)"""
        empty_schema = {}
        
        write_schema_file(temp_workspace['schemas'], "empty.yaml", empty_schema)
        
        # Validation should pass (empty schemas are ignored)
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_schema_without_tables_passes(self, migration_tool, temp_workspace):
        """Test that schemas with only functions pass validation"""
        no_tables_schema = {
            'functions': {
                'test_function': {
                    'returns': 'INTEGER',
                    'language': 'plpgsql',
                    'body': 'BEGIN RETURN 1; END;'
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "no_tables.yaml", no_tables_schema)
        
        # Validation should pass (functions-only schemas are valid)
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_table_without_columns_fails(self, migration_tool, temp_workspace):
        """Test that tables without columns fail validation"""
        no_columns_schema = {
            'tables': {
                'users': {}  # No columns
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "no_columns.yaml", no_columns_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_invalid_foreign_key_reference_fails(self, migration_tool, temp_workspace):
        """Test that invalid foreign key references fail validation"""
        invalid_fk_schema = {
            'tables': {
                'posts': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'user_id': {'type': 'INTEGER', 'not_null': True}
                    },
                    'foreign_keys': {
                        'posts_user_fk': {
                            'column': 'user_id',
                            'references': 'nonexistent_table(id)',  # Table doesn't exist
                            'on_delete': 'CASCADE'
                        }
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "invalid_fk.yaml", invalid_fk_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_multiple_primary_keys_fails(self, migration_tool, temp_workspace):
        """Test that multiple primary keys fail validation"""
        multiple_pk_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'email': {'type': 'VARCHAR(255)', 'primary_key': True},  # Second primary key
                        'name': {'type': 'VARCHAR(100)', 'not_null': True}
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "multiple_pk.yaml", multiple_pk_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_valid_function_definition_passes(self, migration_tool, temp_workspace):
        """Test that valid function definitions pass validation"""
        function_schema = {
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
                    'language': 'plpgsql',
                    'body': '''
                    BEGIN
                        RETURN (SELECT COUNT(*) FROM users);
                    END;
                    '''
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "with_function.yaml", function_schema)
        
        # Validation should pass
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_invalid_function_definition_passes(self, migration_tool, temp_workspace):
        """Test that function definitions without 'returns' still pass (basic validation)"""
        function_schema_without_returns = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'name': {'type': 'VARCHAR(100)', 'not_null': True}
                    }
                }
            },
            'functions': {
                'simple_function': {
                    'language': 'plpgsql',  # Missing 'returns' but still valid in basic validation
                    'body': 'BEGIN RETURN 1; END;'
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "function_no_returns.yaml", function_schema_without_returns)
        
        # Basic validation should pass (detailed function validation would catch this)
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_constraints_not_supported_fails(self, migration_tool, temp_workspace):
        """Test that unsupported 'constraints' key fails validation"""
        constraints_schema = {
            'tables': {
                'users': {
                    'columns': {
                        'id': {'type': 'SERIAL', 'primary_key': True},
                        'email': {'type': 'VARCHAR(255)', 'not_null': True, 'unique': True},
                        'age': {'type': 'INTEGER'},
                        'status': {'type': 'VARCHAR(20)', 'default': "'active'"}
                    },
                    'constraints': {  # This key is not supported by the current validator
                        'users_age_check': {
                            'type': 'CHECK',
                            'condition': 'age >= 0 AND age <= 150'
                        }
                    }
                }
            }
        }
        
        write_schema_file(temp_workspace['schemas'], "constraints.yaml", constraints_schema)
        
        # Validation should fail because 'constraints' is unknown
        success = migration_tool.validate_schemas_only()
        assert not success
    
    def test_multiple_schemas_validation(self, migration_tool, temp_workspace, sample_user_schema, sample_complex_schema):
        """Test validation of multiple schema files"""
        # Write multiple valid schemas
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        write_schema_file(temp_workspace['schemas'], "catalog.yaml", sample_complex_schema)
        
        # Validation should pass
        success = migration_tool.validate_schemas_only()
        assert success
    
    def test_mixed_valid_invalid_schemas_fails(self, migration_tool, temp_workspace, sample_user_schema):
        """Test that validation fails if any schema is invalid"""
        # Write one valid schema
        write_schema_file(temp_workspace['schemas'], "users.yaml", sample_user_schema)
        
        # Write one invalid schema
        invalid_schema = {
            'tables': {
                'invalid': {
                    'columns': {
                        'id': {'type': 'INVALID_TYPE'}
                    }
                }
            }
        }
        write_schema_file(temp_workspace['schemas'], "invalid.yaml", invalid_schema)
        
        # Validation should fail
        success = migration_tool.validate_schemas_only()
        assert not success
