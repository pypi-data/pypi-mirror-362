"""
SQL generation module for PostgreSQL migrations.
"""

from typing import Dict, Any, List


class SQLGenerator:
    """Generates PostgreSQL SQL from schema definitions"""
    
    def generate_table_sql(self, table_name: str, table_def: Dict) -> str:
        """Generate CREATE TABLE SQL from YAML definition"""
        sql_lines = [f"CREATE TABLE IF NOT EXISTS {table_name} ("]
        
        columns = []
        for col_name, col_def in table_def.get('columns', {}).items():
            col_type = col_def.get('type', 'VARCHAR')
            constraints = []
            
            if col_def.get('primary_key'):
                constraints.append('PRIMARY KEY')
            if col_def.get('not_null'):
                constraints.append('NOT NULL')
            if col_def.get('unique'):
                constraints.append('UNIQUE')
            if col_def.get('default'):
                constraints.append(f"DEFAULT {col_def['default']}")
                
            constraint_str = ' '.join(constraints)
            columns.append(f"  {col_name} {col_type} {constraint_str}".strip())
        
        sql_lines.append(',\n'.join(columns))
        sql_lines.append(");")
        
        # Add indexes
        indexes = table_def.get('indexes', [])
        for index in indexes:
            index_name = index.get('name', f"idx_{table_name}_{index['columns'][0]}")
            columns_str = ', '.join(index['columns'])
            unique = 'UNIQUE ' if index.get('unique') else ''
            sql_lines.append(f"CREATE {unique}INDEX IF NOT EXISTS {index_name} ON {table_name} ({columns_str});")
        
        # Add foreign keys
        foreign_keys = table_def.get('foreign_keys', [])
        for fk in foreign_keys:
            fk_sql = self.generate_foreign_key_sql(table_name, fk)
            if fk_sql:
                sql_lines.append(fk_sql)
        
        return '\n'.join(sql_lines)
    
    def generate_foreign_key_sql(self, table_name: str, fk_def: Dict) -> str:
        """Generate foreign key constraint SQL"""
        # Get foreign key name
        fk_name = fk_def.get('name', f"fk_{table_name}_{fk_def['columns'][0]}")
        
        # Build column lists
        local_columns = ', '.join(fk_def['columns'])
        ref_columns = ', '.join(fk_def['references_columns'])
        ref_table = fk_def['references_table']
        
        # Build the constraint SQL
        sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {fk_name} "
        sql += f"FOREIGN KEY ({local_columns}) REFERENCES {ref_table} ({ref_columns})"
        
        # Add ON DELETE action
        if 'on_delete' in fk_def:
            sql += f" ON DELETE {fk_def['on_delete']}"
        
        # Add ON UPDATE action
        if 'on_update' in fk_def:
            sql += f" ON UPDATE {fk_def['on_update']}"
        
        sql += ";"
        
        return sql
    
    def generate_drop_foreign_key_sql(self, table_name: str, fk_def: Dict) -> str:
        """Generate DROP CONSTRAINT SQL for foreign key"""
        fk_name = fk_def.get('name', f"fk_{table_name}_{fk_def['columns'][0]}")
        return f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {fk_name};"
    
    def generate_drop_table_sql(self, table_name: str) -> str:
        """Generate DROP TABLE SQL"""
        return f"DROP TABLE IF EXISTS {table_name};"
    
    def generate_function_sql(self, func_name: str, func_def: Dict) -> str:
        """Generate CREATE FUNCTION SQL from YAML definition"""
        params = func_def.get('parameters', {})
        returns = func_def.get('returns', 'void')
        body = func_def.get('body', '')
        language = func_def.get('language', 'sql')
        
        param_list = []
        for param_name, param_type in params.items():
            param_list.append(f"{param_name} {param_type}")
        
        params_str = ', '.join(param_list)
        
        sql = f"""CREATE OR REPLACE FUNCTION {func_name}({params_str})
RETURNS {returns}
AS $$
{body}
$$ LANGUAGE {language};"""
        
        return sql
    
    def generate_drop_function_sql(self, func_name: str, func_def: Dict) -> str:
        """Generate DROP FUNCTION SQL"""
        params = func_def.get('parameters', {})
        param_list = []
        for param_name, param_type in params.items():
            param_list.append(f"{param_name} {param_type}")
        params_str = ', '.join(param_list)
        return f"DROP FUNCTION IF EXISTS {func_name}({params_str});"
    
    def generate_table_modification_sql(self, table_name: str, current_def: Dict, previous_def: Dict) -> str:
        """Generate ALTER TABLE SQL for modified table"""
        sql_lines = []
        
        current_columns = current_def.get('columns', {})
        previous_columns = previous_def.get('columns', {})
        
        # Added columns
        for col_name, col_def in current_columns.items():
            if col_name not in previous_columns:
                col_type = col_def.get('type', 'VARCHAR')
                constraints = []
                
                if col_def.get('not_null'):
                    constraints.append('NOT NULL')
                if col_def.get('unique'):
                    constraints.append('UNIQUE')
                if col_def.get('default'):
                    constraints.append(f"DEFAULT {col_def['default']}")
                
                constraint_str = ' '.join(constraints)
                sql_lines.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {constraint_str};".strip())
        
        # Modified columns (simplified - only detect type changes)
        for col_name, col_def in current_columns.items():
            if col_name in previous_columns:
                current_type = col_def.get('type', 'VARCHAR')
                previous_type = previous_columns[col_name].get('type', 'VARCHAR')
                if current_type != previous_type:
                    sql_lines.append(f"ALTER TABLE {table_name} ALTER COLUMN {col_name} TYPE {current_type};")
        
        # Removed columns
        for col_name in previous_columns:
            if col_name not in current_columns:
                sql_lines.append(f"ALTER TABLE {table_name} DROP COLUMN {col_name};")
        
        # Handle indexes
        sql_lines.extend(self._generate_index_changes(table_name, current_def, previous_def))
        
        # Handle foreign key changes
        sql_lines.extend(self._generate_foreign_key_changes(table_name, current_def, previous_def))
        
        return '\n'.join(sql_lines)
    
    def _generate_index_changes(self, table_name: str, current_def: Dict, previous_def: Dict) -> List[str]:
        """Generate SQL for index changes"""
        sql_lines = []
        current_indexes = current_def.get('indexes', [])
        previous_indexes = previous_def.get('indexes', [])
        
        # Simple index comparison by name
        current_index_names = {idx.get('name', f"idx_{table_name}_{idx['columns'][0]}"): idx for idx in current_indexes}
        previous_index_names = {idx.get('name', f"idx_{table_name}_{idx['columns'][0]}"): idx for idx in previous_indexes}
        
        # Added indexes
        for idx_name, idx_def in current_index_names.items():
            if idx_name not in previous_index_names:
                columns_str = ', '.join(idx_def['columns'])
                unique = 'UNIQUE ' if idx_def.get('unique') else ''
                sql_lines.append(f"CREATE {unique}INDEX IF NOT EXISTS {idx_name} ON {table_name} ({columns_str});")
        
        # Removed indexes
        for idx_name in previous_index_names:
            if idx_name not in current_index_names:
                sql_lines.append(f"DROP INDEX IF EXISTS {idx_name};")
        
        return sql_lines
    
    def _generate_foreign_key_changes(self, table_name: str, current_def: Dict, previous_def: Dict) -> List[str]:
        """Generate SQL for foreign key changes"""
        sql_lines = []
        current_fks = current_def.get('foreign_keys', [])
        previous_fks = previous_def.get('foreign_keys', [])
        
        # Simple foreign key comparison by name
        current_fk_names = {fk.get('name', f"fk_{table_name}_{fk['columns'][0]}"): fk for fk in current_fks}
        previous_fk_names = {fk.get('name', f"fk_{table_name}_{fk['columns'][0]}"): fk for fk in previous_fks}
        
        # Removed foreign keys (drop first to avoid conflicts)
        for fk_name, fk_def in previous_fk_names.items():
            if fk_name not in current_fk_names:
                sql_lines.append(self.generate_drop_foreign_key_sql(table_name, fk_def))
        
        # Modified foreign keys (drop and recreate)
        for fk_name, fk_def in current_fk_names.items():
            if fk_name in previous_fk_names and fk_def != previous_fk_names[fk_name]:
                sql_lines.append(self.generate_drop_foreign_key_sql(table_name, previous_fk_names[fk_name]))
                sql_lines.append(self.generate_foreign_key_sql(table_name, fk_def))
        
        # Added foreign keys
        for fk_name, fk_def in current_fk_names.items():
            if fk_name not in previous_fk_names:
                sql_lines.append(self.generate_foreign_key_sql(table_name, fk_def))
        
        return sql_lines
    
    def generate_table_rollback_sql(self, table_name: str, current_def: Dict, previous_def: Dict) -> str:
        """Generate SQL to rollback table modifications"""
        sql_lines = []
        
        current_columns = current_def.get('columns', {})
        previous_columns = previous_def.get('columns', {})
        
        # Rollback added columns (drop them)
        for col_name in current_columns:
            if col_name not in previous_columns:
                sql_lines.append(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {col_name};")
        
        # Rollback removed columns (add them back)
        for col_name, col_def in previous_columns.items():
            if col_name not in current_columns:
                col_type = col_def.get('type', 'VARCHAR')
                constraints = []
                
                if col_def.get('not_null'):
                    constraints.append('NOT NULL')
                if col_def.get('unique'):
                    constraints.append('UNIQUE')
                if col_def.get('default'):
                    constraints.append(f"DEFAULT {col_def['default']}")
                
                constraint_str = ' '.join(constraints)
                sql_lines.append(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type} {constraint_str};".strip())
        
        # Rollback modified columns (revert type changes)
        for col_name, col_def in previous_columns.items():
            if col_name in current_columns:
                previous_type = col_def.get('type', 'VARCHAR')
                current_type = current_columns[col_name].get('type', 'VARCHAR')
                if current_type != previous_type:
                    sql_lines.append(f"ALTER TABLE {table_name} ALTER COLUMN {col_name} TYPE {previous_type};")
        
        # Handle index rollbacks
        sql_lines.extend(self._generate_index_rollbacks(table_name, current_def, previous_def))
        
        # Handle foreign key rollbacks
        sql_lines.extend(self._generate_foreign_key_rollbacks(table_name, current_def, previous_def))
        
        return '\n'.join(sql_lines)
    
    def _generate_index_rollbacks(self, table_name: str, current_def: Dict, previous_def: Dict) -> List[str]:
        """Generate SQL for index rollbacks"""
        sql_lines = []
        current_indexes = current_def.get('indexes', [])
        previous_indexes = previous_def.get('indexes', [])
        
        current_index_names = {idx.get('name', f"idx_{table_name}_{idx['columns'][0]}"): idx for idx in current_indexes}
        previous_index_names = {idx.get('name', f"idx_{table_name}_{idx['columns'][0]}"): idx for idx in previous_indexes}
        
        # Rollback added indexes (drop them)
        for idx_name in current_index_names:
            if idx_name not in previous_index_names:
                sql_lines.append(f"DROP INDEX IF EXISTS {idx_name};")
        
        # Rollback removed indexes (recreate them)
        for idx_name, idx_def in previous_index_names.items():
            if idx_name not in current_index_names:
                columns_str = ', '.join(idx_def['columns'])
                unique = 'UNIQUE ' if idx_def.get('unique') else ''
                sql_lines.append(f"CREATE {unique}INDEX IF NOT EXISTS {idx_name} ON {table_name} ({columns_str});")
        
        return sql_lines
    
    def _generate_foreign_key_rollbacks(self, table_name: str, current_def: Dict, previous_def: Dict) -> List[str]:
        """Generate SQL for foreign key rollbacks"""
        sql_lines = []
        current_fks = current_def.get('foreign_keys', [])
        previous_fks = previous_def.get('foreign_keys', [])
        
        current_fk_names = {fk.get('name', f"fk_{table_name}_{fk['columns'][0]}"): fk for fk in current_fks}
        previous_fk_names = {fk.get('name', f"fk_{table_name}_{fk['columns'][0]}"): fk for fk in previous_fks}
        
        # Rollback added foreign keys (drop them)
        for fk_name, fk_def in current_fk_names.items():
            if fk_name not in previous_fk_names:
                sql_lines.append(self.generate_drop_foreign_key_sql(table_name, fk_def))
        
        # Rollback modified foreign keys (restore previous version)
        for fk_name, fk_def in previous_fk_names.items():
            if fk_name in current_fk_names and fk_def != current_fk_names[fk_name]:
                sql_lines.append(self.generate_drop_foreign_key_sql(table_name, current_fk_names[fk_name]))
                sql_lines.append(self.generate_foreign_key_sql(table_name, fk_def))
        
        # Rollback removed foreign keys (recreate them)
        for fk_name, fk_def in previous_fk_names.items():
            if fk_name not in current_fk_names:
                sql_lines.append(self.generate_foreign_key_sql(table_name, fk_def))
        
        return sql_lines
