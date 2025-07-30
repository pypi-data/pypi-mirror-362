"""
Migration management module for handling migration files and state.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from .sql_generator import SQLGenerator


class MigrationManager:
    """Manages migration files and state tracking"""
    
    def __init__(self, migrations_dir: str = "migrations"):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        self.state_file = self.migrations_dir / ".schema_state.json"
        self.rollback_file = self.migrations_dir / ".rollback_info.json"
        self.sql_generator = SQLGenerator()
    
    def save_schema_state(self, schemas: Dict[str, Any]) -> None:
        """Save current schema state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(schemas, f, indent=2)
    
    def load_previous_schema_state(self) -> Optional[Dict[str, Any]]:
        """Load previous schema state from file"""
        if not self.state_file.exists():
            return None
        
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def save_rollback_info(self, migration_file: str, changes: Dict[str, Any], previous_schemas: Optional[Dict[str, Any]]) -> None:
        """Save rollback information for the migration"""
        rollback_info = {
            'migration_file': migration_file,
            'changes': changes,
            'previous_schemas': previous_schemas,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.rollback_file, 'w') as f:
            json.dump(rollback_info, f, indent=2)
    
    def load_rollback_info(self) -> Optional[Dict[str, Any]]:
        """Load rollback information for the last migration"""
        if not self.rollback_file.exists():
            return None
        
        try:
            with open(self.rollback_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return None
    
    def get_latest_migration_number(self) -> int:
        """Get the latest migration number"""
        migrations = list(self.migrations_dir.glob("*.sql"))
        if not migrations:
            return 0
            
        numbers = []
        for migration in migrations:
            try:
                number = int(migration.stem.split('_')[0])
                numbers.append(number)
            except (ValueError, IndexError):
                continue
                
        return max(numbers) if numbers else 0
    
    def get_latest_migration_file(self) -> Optional[Path]:
        """Get the latest migration file"""
        migrations = list(self.migrations_dir.glob("*.sql"))
        if not migrations:
            return None
        
        # Sort by migration number (extracted from filename)
        def get_migration_number(path: Path) -> int:
            try:
                return int(path.stem.split('_')[0])
            except (ValueError, IndexError):
                return 0
        
        return max(migrations, key=get_migration_number)
    
    def parse_migration_file(self, migration_path: Path) -> Dict[str, Any]:
        """Parse a migration file to extract basic information"""
        with open(migration_path, 'r') as f:
            content = f.read()
        
        # Simple parsing to identify operations
        operations = {
            'tables_created': [],
            'tables_dropped': [],
            'tables_modified': [],
            'functions_created': [],
            'functions_dropped': [],
            'functions_modified': []
        }
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('-- Create table:'):
                table_name = line.split(':', 1)[1].strip()
                operations['tables_created'].append(table_name)
            elif line.startswith('-- Drop table:'):
                table_name = line.split(':', 1)[1].strip()
                operations['tables_dropped'].append(table_name)
            elif line.startswith('-- Modify table:'):
                table_name = line.split(':', 1)[1].strip()
                operations['tables_modified'].append(table_name)
            elif line.startswith('-- Create function:'):
                func_name = line.split(':', 1)[1].strip()
                operations['functions_created'].append(func_name)
            elif line.startswith('-- Drop function:'):
                func_name = line.split(':', 1)[1].strip()
                operations['functions_dropped'].append(func_name)
            elif line.startswith('-- Modify function:'):
                func_name = line.split(':', 1)[1].strip()
                operations['functions_modified'].append(func_name)
        
        return operations
    
    def compare_schemas(self, current: Dict[str, Any], previous: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare current and previous schemas to detect changes"""
        if previous is None:
            return {
                'tables': {'added': current.get('tables', {}), 'modified': {}, 'removed': {}},
                'functions': {'added': current.get('functions', {}), 'modified': {}, 'removed': {}}
            }
        
        changes = {
            'tables': {'added': {}, 'modified': {}, 'removed': {}},
            'functions': {'added': {}, 'modified': {}, 'removed': {}}
        }
        
        # Compare all schemas
        for schema_name, current_schema in current.items():
            previous_schema = previous.get(schema_name, {})
            
            # Compare tables
            current_tables = current_schema.get('tables', {})
            previous_tables = previous_schema.get('tables', {})
            
            for table_name, table_def in current_tables.items():
                if table_name not in previous_tables:
                    changes['tables']['added'][table_name] = table_def
                elif table_def != previous_tables[table_name]:
                    changes['tables']['modified'][table_name] = {
                        'current': table_def,
                        'previous': previous_tables[table_name]
                    }
            
            for table_name in previous_tables:
                if table_name not in current_tables:
                    changes['tables']['removed'][table_name] = previous_tables[table_name]
            
            # Compare functions
            current_functions = current_schema.get('functions', {})
            previous_functions = previous_schema.get('functions', {})
            
            for func_name, func_def in current_functions.items():
                if func_name not in previous_functions:
                    changes['functions']['added'][func_name] = func_def
                elif func_def != previous_functions[func_name]:
                    changes['functions']['modified'][func_name] = {
                        'current': func_def,
                        'previous': previous_functions[func_name]
                    }
            
            for func_name in previous_functions:
                if func_name not in current_functions:
                    changes['functions']['removed'][func_name] = previous_functions[func_name]
        
        return changes
    
    def generate_differential_migration_sql(self, changes: Dict[str, Any]) -> str:
        """Generate SQL for only the detected changes"""
        sql_parts = []
        
        # Handle table changes
        table_changes = changes.get('tables', {})
        
        # Removed tables first
        for table_name, table_def in table_changes.get('removed', {}).items():
            sql_parts.append(f"-- Drop table: {table_name}")
            sql_parts.append(self.sql_generator.generate_drop_table_sql(table_name))
            sql_parts.append("")
        
        # Added tables
        for table_name, table_def in table_changes.get('added', {}).items():
            sql_parts.append(f"-- Create table: {table_name}")
            sql_parts.append(self.sql_generator.generate_table_sql(table_name, table_def))
            sql_parts.append("")
        
        # Modified tables
        for table_name, table_changes in table_changes.get('modified', {}).items():
            sql_parts.append(f"-- Modify table: {table_name}")
            modification_sql = self.sql_generator.generate_table_modification_sql(
                table_name, 
                table_changes['current'], 
                table_changes['previous']
            )
            if modification_sql:
                sql_parts.append(modification_sql)
                sql_parts.append("")
        
        # Handle function changes
        function_changes = changes.get('functions', {})
        
        # Removed functions
        for func_name, func_def in function_changes.get('removed', {}).items():
            sql_parts.append(f"-- Drop function: {func_name}")
            sql_parts.append(self.sql_generator.generate_drop_function_sql(func_name, func_def))
            sql_parts.append("")
        
        # Added and modified functions (both use CREATE OR REPLACE)
        for func_name, func_def in function_changes.get('added', {}).items():
            sql_parts.append(f"-- Create function: {func_name}")
            sql_parts.append(self.sql_generator.generate_function_sql(func_name, func_def))
            sql_parts.append("")
        
        for func_name, func_changes in function_changes.get('modified', {}).items():
            sql_parts.append(f"-- Modify function: {func_name}")
            sql_parts.append(self.sql_generator.generate_function_sql(func_name, func_changes['current']))
            sql_parts.append("")
        
        return '\n'.join(sql_parts)
    
    def generate_rollback_sql(self, changes: Dict[str, Any]) -> str:
        """Generate SQL to rollback the changes made in the last migration"""
        sql_parts = []
        
        # Handle table rollbacks (reverse order)
        table_changes = changes.get('tables', {})
        
        # Rollback modified tables (revert to previous state)
        for table_name, table_changes_detail in table_changes.get('modified', {}).items():
            sql_parts.append(f"-- Rollback table modifications: {table_name}")
            rollback_sql = self.sql_generator.generate_table_rollback_sql(
                table_name, 
                table_changes_detail['current'], 
                table_changes_detail['previous']
            )
            if rollback_sql:
                sql_parts.append(rollback_sql)
                sql_parts.append("")
        
        # Rollback added tables (drop them)
        for table_name, table_def in table_changes.get('added', {}).items():
            sql_parts.append(f"-- Rollback added table: {table_name}")
            sql_parts.append(self.sql_generator.generate_drop_table_sql(table_name))
            sql_parts.append("")
        
        # Rollback removed tables (recreate them)
        for table_name, table_def in table_changes.get('removed', {}).items():
            sql_parts.append(f"-- Rollback removed table: {table_name}")
            sql_parts.append(self.sql_generator.generate_table_sql(table_name, table_def))
            sql_parts.append("")
        
        # Handle function rollbacks
        function_changes = changes.get('functions', {})
        
        # Rollback modified functions (restore previous version)
        for func_name, func_changes_detail in function_changes.get('modified', {}).items():
            sql_parts.append(f"-- Rollback modified function: {func_name}")
            sql_parts.append(self.sql_generator.generate_function_sql(func_name, func_changes_detail['previous']))
            sql_parts.append("")
        
        # Rollback added functions (drop them)
        for func_name, func_def in function_changes.get('added', {}).items():
            sql_parts.append(f"-- Rollback added function: {func_name}")
            sql_parts.append(self.sql_generator.generate_drop_function_sql(func_name, func_def))
            sql_parts.append("")
        
        # Rollback removed functions (recreate them)
        for func_name, func_def in function_changes.get('removed', {}).items():
            sql_parts.append(f"-- Rollback removed function: {func_name}")
            sql_parts.append(self.sql_generator.generate_function_sql(func_name, func_def))
            sql_parts.append("")
        
        return '\n'.join(sql_parts)
    
    def generate_migration_sql(self, schemas: Dict[str, Any]) -> str:
        """Generate complete migration SQL from schemas"""
        sql_parts = []
        
        for schema_name, schema_def in schemas.items():
            sql_parts.append(f"-- Schema: {schema_name}")
            sql_parts.append("")
            
            # Generate tables
            if 'tables' in schema_def:
                for table_name, table_def in schema_def['tables'].items():
                    sql_parts.append(self.sql_generator.generate_table_sql(table_name, table_def))
                    sql_parts.append("")
            
            # Generate functions
            if 'functions' in schema_def:
                for func_name, func_def in schema_def['functions'].items():
                    sql_parts.append(self.sql_generator.generate_function_sql(func_name, func_def))
                    sql_parts.append("")
        
        return '\n'.join(sql_parts)
