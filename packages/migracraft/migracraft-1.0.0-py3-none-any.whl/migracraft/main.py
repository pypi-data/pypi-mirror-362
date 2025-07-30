"""
Main schema migration tool class.
"""

import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from .exceptions import SchemaValidationError
from .validator import SchemaValidator
from .migration_manager import MigrationManager
from .entity_generator import EntityGenerator


class SchemaMigrationTool:
    """Main tool for generating PostgreSQL migrations from YAML schemas"""
    
    def __init__(self, schemas_dir: str = "schemas", migrations_dir: str = "migrations"):
        self.schemas_dir = Path(schemas_dir)
        self.migrations_dir = Path(migrations_dir)
        self.validator = SchemaValidator()
        self.migration_manager = MigrationManager(migrations_dir)
        self.entity_generator = EntityGenerator()
        
    def load_schemas(self) -> Dict[str, Any]:
        """Load and validate all YAML schema files"""
        schemas = {}
        validation_errors = []
        
        for yaml_file in self.schemas_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r') as f:
                    schema_name = yaml_file.stem
                    schema_data = yaml.safe_load(f)
                    
                    # Validate schema
                    if self.validator.validate_schema(schema_name, schema_data):
                        schemas[schema_name] = schema_data
                    else:
                        errors = self.validator.get_errors()
                        validation_errors.extend([f"File '{yaml_file}': {error}" for error in errors])
                        
            except yaml.YAMLError as e:
                validation_errors.append(f"YAML syntax error in '{yaml_file}': {e}")
            except Exception as e:
                validation_errors.append(f"Error loading '{yaml_file}': {e}")
        
        if validation_errors:
            error_msg = "Schema validation failed:\n" + "\n".join(validation_errors)
            raise SchemaValidationError(error_msg)
                
        return schemas
    
    def create_migration(self, name: Optional[str] = None, differential: bool = True):
        """Create a new migration file"""
        # Load schemas
        try:
            schemas = self.load_schemas()
        except SchemaValidationError as e:
            print(f"Error: {e}")
            return
        
        if not schemas:
            print("No schema files found in", self.schemas_dir)
            return
        
        # Generate migration SQL
        if differential:
            previous_schemas = self.migration_manager.load_previous_schema_state()
            changes = self.migration_manager.compare_schemas(schemas, previous_schemas)
            
            # Check if there are any changes
            has_changes = any(
                changes['tables'][change_type] or changes['functions'][change_type]
                for change_type in ['added', 'modified', 'removed']
            )
            
            if not has_changes:
                print("No changes detected in schemas. No migration needed.")
                return
            
            migration_sql = self.migration_manager.generate_differential_migration_sql(changes)
            migration_type = "differential"
        else:
            migration_sql = self.migration_manager.generate_migration_sql(schemas)
            migration_type = "full"
        
        # Create migration file
        migration_number = self.migration_manager.get_latest_migration_number() + 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if name:
            filename = f"{migration_number:03d}_{name}_{timestamp}.sql"
        else:
            filename = f"{migration_number:03d}_{migration_type}_migration_{timestamp}.sql"
        
        migration_path = self.migrations_dir / filename
        
        with open(migration_path, 'w') as f:
            f.write(migration_sql)
        
        # Save current schema state for next comparison
        self.migration_manager.save_schema_state(schemas)
        
        # Save rollback information for differential migrations
        if differential:
            self.migration_manager.save_rollback_info(migration_path.name, changes, previous_schemas)
        
        print(f"Created {migration_type} migration: {migration_path}")
        print(f"Migration contains {len(migration_sql.splitlines())} lines")
        
        if differential and migration_sql.strip():
            print("Changes detected:")
            changes_summary = []
            for change_type in ['added', 'modified', 'removed']:
                table_count = len(changes['tables'][change_type])
                func_count = len(changes['functions'][change_type])
                if table_count > 0:
                    changes_summary.append(f"  Tables {change_type}: {table_count}")
                if func_count > 0:
                    changes_summary.append(f"  Functions {change_type}: {func_count}")
            
            if changes_summary:
                print('\n'.join(changes_summary))
    
    def validate_schemas_only(self):
        """Validate schemas without creating migrations"""
        try:
            schemas = self.load_schemas()
            print(f"✓ All schemas valid! Found {len(schemas)} schema(s).")
            return True
        except SchemaValidationError as e:
            print(f"✗ Schema validation failed:\n{e}")
            return False
    
    def create_rollback_migration(self, name: Optional[str] = None):
        """Create a rollback migration file to undo the last migration"""
        # Load rollback information
        rollback_info = self.migration_manager.load_rollback_info()
        
        if not rollback_info:
            print("No rollback information found. Cannot create rollback migration.")
            print("Rollback information is only available for migrations created with this tool version.")
            return
        
        # Get the migration file being rolled back
        last_migration_file = rollback_info.get('migration_file')
        changes = rollback_info.get('changes')
        
        if not changes:
            print("No changes information found in rollback data.")
            return
        
        # Check if there are any changes to rollback
        has_changes = any(
            changes['tables'][change_type] or changes['functions'][change_type]
            for change_type in ['added', 'modified', 'removed']
        )
        
        if not has_changes:
            print("No changes to rollback from the last migration.")
            return
        
        # Generate rollback SQL
        rollback_sql = self.migration_manager.generate_rollback_sql(changes)
        
        if not rollback_sql.strip():
            print("No rollback operations needed.")
            return
        
        # Create rollback migration file
        migration_number = self.migration_manager.get_latest_migration_number() + 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if name:
            filename = f"{migration_number:03d}_rollback_{name}_{timestamp}.sql"
        else:
            filename = f"{migration_number:03d}_rollback_{timestamp}.sql"
        
        migration_path = self.migrations_dir / filename
        
        # Add header comment with rollback information
        header = f"""-- ROLLBACK MIGRATION
-- This migration rolls back changes from: {last_migration_file}
-- Generated on: {datetime.now().isoformat()}
-- 
-- WARNING: This rollback migration is based on the recorded changes.
-- Please review the SQL carefully before applying it to your database.

"""
        
        with open(migration_path, 'w') as f:
            f.write(header + rollback_sql)
        
        print(f"Created rollback migration: {migration_path}")
        print(f"This will undo changes from: {last_migration_file}")
        
        # Show summary of what will be rolled back
        print("Operations to be rolled back:")
        for change_type in ['added', 'modified', 'removed']:
            table_count = len(changes['tables'][change_type])
            func_count = len(changes['functions'][change_type])
            if table_count > 0:
                action = {'added': 'drop', 'modified': 'revert', 'removed': 'recreate'}[change_type]
                print(f"  Tables to {action}: {table_count}")
            if func_count > 0:
                action = {'added': 'drop', 'modified': 'revert', 'removed': 'recreate'}[change_type]
                print(f"  Functions to {action}: {func_count}")
        
        print(f"\nMigration contains {len(rollback_sql.splitlines())} lines")
        print("⚠️  IMPORTANT: Review the rollback migration carefully before applying!")
    
    def generate_entities(self, language: str, output_dir: str = "entities"):
        """Generate entity classes for all schemas in the specified language"""
        try:
            # Load and validate schemas
            schemas = self.load_schemas()
        except SchemaValidationError as e:
            print(f"Error: {e}")
            return False
        
        if not schemas:
            print("No schema files found in", self.schemas_dir)
            return False
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate entities for all schemas
        try:
            self.entity_generator.generate_entities(
                schemas=schemas,
                language=language,
                output_dir=str(output_path)
            )
            print(f"✓ Successfully generated {language} entities for {len(schemas)} schema(s) in: {output_path}")
            
            # List generated files
            generated_files = list(output_path.glob(f"*.{self._get_file_extension(language)}"))
            if generated_files:
                print(f"Generated files:")
                for file_path in generated_files:
                    print(f"  - {file_path}")
            
            return True
        except Exception as e:
            print(f"✗ Error generating entities: {e}")
            return False
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for the given language"""
        extensions = {
            'typescript': 'ts',
            'python': 'py',
            'dart': 'dart',
            'java': 'java',
            'cpp': 'hpp',
            'csharp': 'cs',
            'go': 'go'
        }
        return extensions.get(language, 'txt')
