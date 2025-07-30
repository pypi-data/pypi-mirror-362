"""
Schema validation module for YAML schema definitions.
"""

import re
from typing import Dict, Any, List

from .config import (
    VALID_TYPES, VALID_LANGUAGES, VALID_FK_ACTIONS,
    VALID_SCHEMA_KEYS, VALID_TABLE_KEYS, VALID_COLUMN_CONSTRAINTS,
    VALID_INDEX_KEYS, VALID_FK_KEYS, VALID_FUNCTION_KEYS
)


class SchemaValidator:
    """Validates YAML schema definitions"""
    
    def __init__(self):
        self.errors: List[str] = []
    
    def validate_schema(self, schema_name: str, schema_def: Dict[str, Any]) -> bool:
        """Validate a complete schema definition"""
        self.errors = []
        
        if not isinstance(schema_def, dict):
            self.errors.append(f"Schema '{schema_name}' must be a dictionary")
            return False
        
        # Validate tables
        if 'tables' in schema_def:
            self._validate_tables(schema_def['tables'], schema_name)
        
        # Validate functions
        if 'functions' in schema_def:
            self._validate_functions(schema_def['functions'], schema_name)
        
        # Check for unknown top-level keys
        for key in schema_def.keys():
            if key not in VALID_SCHEMA_KEYS:
                self.errors.append(f"Unknown top-level key '{key}' in schema '{schema_name}'")
        
        return len(self.errors) == 0
    
    def _validate_tables(self, tables: Dict[str, Any], schema_name: str) -> None:
        """Validate table definitions"""
        if not isinstance(tables, dict):
            self.errors.append(f"'tables' in schema '{schema_name}' must be a dictionary")
            return
        
        for table_name, table_def in tables.items():
            self._validate_table(table_name, table_def, schema_name)
    
    def _validate_table(self, table_name: str, table_def: Dict[str, Any], schema_name: str) -> None:
        """Validate a single table definition"""
        if not isinstance(table_def, dict):
            self.errors.append(f"Table '{table_name}' in schema '{schema_name}' must be a dictionary")
            return
        
        # Validate table name
        if not self._is_valid_identifier(table_name):
            self.errors.append(f"Invalid table name '{table_name}' in schema '{schema_name}'")
        
        # Validate columns (required)
        if 'columns' not in table_def:
            self.errors.append(f"Table '{table_name}' in schema '{schema_name}' must have 'columns'")
        else:
            self._validate_columns(table_def['columns'], table_name, schema_name)
        
        # Validate indexes (optional)
        if 'indexes' in table_def:
            self._validate_indexes(table_def['indexes'], table_name, schema_name)
        
        # Validate foreign keys (optional)
        if 'foreign_keys' in table_def:
            self._validate_foreign_keys(table_def['foreign_keys'], table_name, schema_name)
        
        # Check for unknown keys
        for key in table_def.keys():
            if key not in VALID_TABLE_KEYS:
                self.errors.append(f"Unknown key '{key}' in table '{table_name}' in schema '{schema_name}'")
    
    def _validate_columns(self, columns: Dict[str, Any], table_name: str, schema_name: str) -> None:
        """Validate column definitions"""
        if not isinstance(columns, dict):
            self.errors.append(f"'columns' in table '{table_name}' in schema '{schema_name}' must be a dictionary")
            return
        
        if not columns:
            self.errors.append(f"Table '{table_name}' in schema '{schema_name}' must have at least one column")
            return
        
        primary_key_count = 0
        for column_name, column_def in columns.items():
            primary_key_count += self._validate_column(column_name, column_def, table_name, schema_name)
        
        # Check for multiple primary keys
        if primary_key_count > 1:
            self.errors.append(f"Table '{table_name}' in schema '{schema_name}' cannot have multiple primary keys")
    
    def _validate_column(self, column_name: str, column_def: Dict[str, Any], table_name: str, schema_name: str) -> int:
        """Validate a single column definition. Returns 1 if primary key, 0 otherwise"""
        if not isinstance(column_def, dict):
            self.errors.append(f"Column '{column_name}' in table '{table_name}' in schema '{schema_name}' must be a dictionary")
            return 0
        
        # Validate column name
        if not self._is_valid_identifier(column_name):
            self.errors.append(f"Invalid column name '{column_name}' in table '{table_name}' in schema '{schema_name}'")
        
        # Validate type (required)
        if 'type' not in column_def:
            self.errors.append(f"Column '{column_name}' in table '{table_name}' in schema '{schema_name}' must have 'type'")
        else:
            self._validate_column_type(column_def['type'], column_name, table_name, schema_name)
        
        # Validate constraints
        is_primary_key = 0
        
        for constraint, value in column_def.items():
            if constraint == 'type':
                continue
            elif constraint not in VALID_COLUMN_CONSTRAINTS:
                self.errors.append(f"Unknown constraint '{constraint}' in column '{column_name}' in table '{table_name}' in schema '{schema_name}'")
            elif constraint == 'primary_key' and value:
                is_primary_key = 1
            elif constraint in {'primary_key', 'not_null', 'unique'} and not isinstance(value, bool):
                self.errors.append(f"Constraint '{constraint}' in column '{column_name}' in table '{table_name}' in schema '{schema_name}' must be boolean")
        
        return is_primary_key
    
    def _validate_column_type(self, column_type: str, column_name: str, table_name: str, schema_name: str) -> None:
        """Validate column data type"""
        if not isinstance(column_type, str):
            self.errors.append(f"Type for column '{column_name}' in table '{table_name}' in schema '{schema_name}' must be a string")
            return
        
        # Extract base type (handle VARCHAR(100), DECIMAL(10,2), etc.)
        base_type = re.split(r'[(\[\s]', column_type.upper())[0]
        
        if base_type not in VALID_TYPES:
            # Check if it's a valid type with size specification
            if not any(column_type.upper().startswith(valid_type) for valid_type in VALID_TYPES):
                self.errors.append(f"Invalid type '{column_type}' for column '{column_name}' in table '{table_name}' in schema '{schema_name}'")
    
    def _validate_indexes(self, indexes: List[Dict[str, Any]], table_name: str, schema_name: str) -> None:
        """Validate index definitions"""
        if not isinstance(indexes, list):
            self.errors.append(f"'indexes' in table '{table_name}' in schema '{schema_name}' must be a list")
            return
        
        for i, index_def in enumerate(indexes):
            self._validate_index(index_def, i, table_name, schema_name)
    
    def _validate_index(self, index_def: Dict[str, Any], index_num: int, table_name: str, schema_name: str) -> None:
        """Validate a single index definition"""
        if not isinstance(index_def, dict):
            self.errors.append(f"Index {index_num} in table '{table_name}' in schema '{schema_name}' must be a dictionary")
            return
        
        # Validate columns (required)
        if 'columns' not in index_def:
            self.errors.append(f"Index {index_num} in table '{table_name}' in schema '{schema_name}' must have 'columns'")
        else:
            columns = index_def['columns']
            if not isinstance(columns, list) or not columns:
                self.errors.append(f"'columns' in index {index_num} in table '{table_name}' in schema '{schema_name}' must be a non-empty list")
            else:
                for column in columns:
                    if not isinstance(column, str) or not self._is_valid_identifier(column):
                        self.errors.append(f"Invalid column name '{column}' in index {index_num} in table '{table_name}' in schema '{schema_name}'")
        
        # Validate optional fields
        if 'name' in index_def:
            if not isinstance(index_def['name'], str) or not self._is_valid_identifier(index_def['name']):
                self.errors.append(f"Invalid index name '{index_def['name']}' in table '{table_name}' in schema '{schema_name}'")
        
        if 'unique' in index_def and not isinstance(index_def['unique'], bool):
            self.errors.append(f"'unique' in index {index_num} in table '{table_name}' in schema '{schema_name}' must be boolean")
        
        # Check for unknown keys
        for key in index_def.keys():
            if key not in VALID_INDEX_KEYS:
                self.errors.append(f"Unknown key '{key}' in index {index_num} in table '{table_name}' in schema '{schema_name}'")
    
    def _validate_foreign_keys(self, foreign_keys: List[Dict[str, Any]], table_name: str, schema_name: str) -> None:
        """Validate foreign key definitions"""
        if not isinstance(foreign_keys, list):
            self.errors.append(f"'foreign_keys' in table '{table_name}' in schema '{schema_name}' must be a list")
            return
        
        for i, fk_def in enumerate(foreign_keys):
            self._validate_foreign_key(fk_def, i, table_name, schema_name)
    
    def _validate_foreign_key(self, fk_def: Dict[str, Any], fk_num: int, table_name: str, schema_name: str) -> None:
        """Validate a single foreign key definition"""
        if not isinstance(fk_def, dict):
            self.errors.append(f"Foreign key {fk_num} in table '{table_name}' in schema '{schema_name}' must be a dictionary")
            return
        
        # Validate required fields
        required_fields = {'columns', 'references_table', 'references_columns'}
        for field in required_fields:
            if field not in fk_def:
                self.errors.append(f"Foreign key {fk_num} in table '{table_name}' in schema '{schema_name}' must have '{field}'")
        
        # Validate columns (local columns)
        if 'columns' in fk_def:
            columns = fk_def['columns']
            if not isinstance(columns, list) or not columns:
                self.errors.append(f"'columns' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}' must be a non-empty list")
            else:
                for column in columns:
                    if not isinstance(column, str) or not self._is_valid_identifier(column):
                        self.errors.append(f"Invalid column name '{column}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
        
        # Validate references_table
        if 'references_table' in fk_def:
            if not isinstance(fk_def['references_table'], str) or not self._is_valid_identifier(fk_def['references_table']):
                self.errors.append(f"Invalid references_table '{fk_def['references_table']}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
        
        # Validate references_columns
        if 'references_columns' in fk_def:
            ref_columns = fk_def['references_columns']
            if not isinstance(ref_columns, list) or not ref_columns:
                self.errors.append(f"'references_columns' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}' must be a non-empty list")
            else:
                for column in ref_columns:
                    if not isinstance(column, str) or not self._is_valid_identifier(column):
                        self.errors.append(f"Invalid referenced column name '{column}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
        
        # Validate column count match
        if 'columns' in fk_def and 'references_columns' in fk_def:
            if len(fk_def['columns']) != len(fk_def['references_columns']):
                self.errors.append(f"Foreign key {fk_num} in table '{table_name}' in schema '{schema_name}' must have same number of columns and references_columns")
        
        # Validate optional fields
        if 'name' in fk_def:
            if not isinstance(fk_def['name'], str) or not self._is_valid_identifier(fk_def['name']):
                self.errors.append(f"Invalid foreign key name '{fk_def['name']}' in table '{table_name}' in schema '{schema_name}'")
        
        if 'on_delete' in fk_def:
            if fk_def['on_delete'] not in VALID_FK_ACTIONS:
                self.errors.append(f"Invalid on_delete action '{fk_def['on_delete']}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
        
        if 'on_update' in fk_def:
            if fk_def['on_update'] not in VALID_FK_ACTIONS:
                self.errors.append(f"Invalid on_update action '{fk_def['on_update']}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
        
        # Check for unknown keys
        for key in fk_def.keys():
            if key not in VALID_FK_KEYS:
                self.errors.append(f"Unknown key '{key}' in foreign key {fk_num} in table '{table_name}' in schema '{schema_name}'")
    
    def _validate_functions(self, functions: Dict[str, Any], schema_name: str) -> None:
        """Validate function definitions"""
        if not isinstance(functions, dict):
            self.errors.append(f"'functions' in schema '{schema_name}' must be a dictionary")
            return
        
        for func_name, func_def in functions.items():
            self._validate_function(func_name, func_def, schema_name)
    
    def _validate_function(self, func_name: str, func_def: Dict[str, Any], schema_name: str) -> None:
        """Validate a single function definition"""
        if not isinstance(func_def, dict):
            self.errors.append(f"Function '{func_name}' in schema '{schema_name}' must be a dictionary")
            return
        
        # Validate function name
        if not self._is_valid_identifier(func_name):
            self.errors.append(f"Invalid function name '{func_name}' in schema '{schema_name}'")
        
        # Validate required fields
        if 'body' not in func_def:
            self.errors.append(f"Function '{func_name}' in schema '{schema_name}' must have 'body'")
        elif not isinstance(func_def['body'], str):
            self.errors.append(f"'body' in function '{func_name}' in schema '{schema_name}' must be a string")
        
        # Validate optional fields
        if 'parameters' in func_def:
            if not isinstance(func_def['parameters'], dict):
                self.errors.append(f"'parameters' in function '{func_name}' in schema '{schema_name}' must be a dictionary")
            else:
                for param_name, param_type in func_def['parameters'].items():
                    if not self._is_valid_identifier(param_name):
                        self.errors.append(f"Invalid parameter name '{param_name}' in function '{func_name}' in schema '{schema_name}'")
                    if not isinstance(param_type, str):
                        self.errors.append(f"Parameter type for '{param_name}' in function '{func_name}' in schema '{schema_name}' must be a string")
        
        if 'returns' in func_def:
            if not isinstance(func_def['returns'], str):
                self.errors.append(f"'returns' in function '{func_name}' in schema '{schema_name}' must be a string")
        
        if 'language' in func_def:
            if not isinstance(func_def['language'], str):
                self.errors.append(f"'language' in function '{func_name}' in schema '{schema_name}' must be a string")
            elif func_def['language'].lower() not in VALID_LANGUAGES:
                self.errors.append(f"Invalid language '{func_def['language']}' in function '{func_name}' in schema '{schema_name}'")
        
        # Check for unknown keys
        for key in func_def.keys():
            if key not in VALID_FUNCTION_KEYS:
                self.errors.append(f"Unknown key '{key}' in function '{func_name}' in schema '{schema_name}'")
    
    def _is_valid_identifier(self, identifier: str) -> bool:
        """Check if identifier is valid for PostgreSQL"""
        if not isinstance(identifier, str):
            return False
        
        # PostgreSQL identifier rules: start with letter or underscore, then letters, digits, underscores
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier) is not None
    
    def get_errors(self) -> List[str]:
        """Get list of validation errors"""
        return self.errors.copy()
