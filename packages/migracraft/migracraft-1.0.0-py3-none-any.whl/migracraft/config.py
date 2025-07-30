"""
Configuration constants for the migration tool.
"""

# Valid PostgreSQL data types
VALID_TYPES = {
    'SERIAL', 'BIGSERIAL', 'SMALLSERIAL',
    'INTEGER', 'BIGINT', 'SMALLINT', 'INT', 'INT2', 'INT4', 'INT8',
    'DECIMAL', 'NUMERIC', 'REAL', 'DOUBLE PRECISION', 'FLOAT4', 'FLOAT8',
    'MONEY',
    'CHARACTER VARYING', 'VARCHAR', 'CHARACTER', 'CHAR', 'TEXT',
    'BYTEA',
    'TIMESTAMP', 'TIMESTAMPTZ', 'DATE', 'TIME', 'TIMETZ', 'INTERVAL',
    'BOOLEAN', 'BOOL',
    'POINT', 'LINE', 'LSEG', 'BOX', 'PATH', 'POLYGON', 'CIRCLE',
    'CIDR', 'INET', 'MACADDR', 'MACADDR8',
    'BIT', 'BIT VARYING', 'VARBIT',
    'TSVECTOR', 'TSQUERY',
    'UUID', 'XML', 'JSON', 'JSONB',
    'ARRAY'
}

# Valid function languages
VALID_LANGUAGES = {'sql', 'plpgsql', 'c', 'python', 'perl', 'tcl'}

# Valid foreign key actions
VALID_FK_ACTIONS = {'CASCADE', 'SET NULL', 'SET DEFAULT', 'RESTRICT', 'NO ACTION'}

# Valid schema top-level keys
VALID_SCHEMA_KEYS = {'tables', 'functions'}

# Valid table keys
VALID_TABLE_KEYS = {'columns', 'indexes', 'foreign_keys'}

# Valid column constraints
VALID_COLUMN_CONSTRAINTS = {'primary_key', 'not_null', 'unique', 'default'}

# Valid index keys
VALID_INDEX_KEYS = {'columns', 'name', 'unique'}

# Valid foreign key keys
VALID_FK_KEYS = {'columns', 'references_table', 'references_columns', 'name', 'on_delete', 'on_update'}

# Valid function keys
VALID_FUNCTION_KEYS = {'parameters', 'returns', 'body', 'language'}
