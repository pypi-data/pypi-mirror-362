"""
MigraCraft - Craft perfect PostgreSQL migrations with precision and artistry

A powerful and flexible PostgreSQL schema migration tool that generates SQL migrations 
from YAML schema definitions and creates entity classes for multiple programming languages.
"""

from .exceptions import SchemaValidationError
from .validator import SchemaValidator
from .sql_generator import SQLGenerator
from .migration_manager import MigrationManager
from .entity_generator import EntityGenerator
from .main import SchemaMigrationTool

# Import version info from the version module in the parent directory
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from version import __version__, get_version, get_version_info, print_banner

__author__ = "MigraCraft Team"
__description__ = "Craft perfect PostgreSQL migrations from YAML schema definitions"

__all__ = [
    "SchemaValidationError",
    "SchemaValidator", 
    "SQLGenerator",
    "MigrationManager",
    "EntityGenerator",
    "SchemaMigrationTool"
]
